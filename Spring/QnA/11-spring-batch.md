# Spring Batch — Q&A

### Q1. batch는 개념이고 Spring Batch는 프레임워크인가

> **Q.** batch 라는게 framework 라는거지?
>
> 아니요, 정확히는 구분이 필요합니다. **batch(배치)**는 특정 프레임워크가 아니라 "대량의 데이터를 실시간이 아니라 정해진 시점/주기에 한꺼번에 처리하는 방식"을 가리키는 일반적인 처리 패턴/개념이고, 언어나 프레임워크와 무관하게 존재합니다. **Spring Batch**가 그 배치 처리 패턴을 Spring 생태계 안에서 구현할 수 있게 해주는 구체적인 프레임워크로, Job/Step/청크 처리/재시작/skip·retry 같은 배치 처리에 공통으로 필요한 기능을 프레임워크 레벨에서 표준 제공합니다. 정리하면 "batch"는 개념(패턴), "Spring Batch"는 그 개념을 구현한 프레임워크입니다.

> **Q.** 음 그러니까 spring batch는 프레임워크라는거 잖아? 그럼 앞에 'spring'이 붙어있는게 spring framework의 하위 개념인거야?
>
> 정확히는 "하위 개념"이라기보다 **"Spring이라는 큰 우산(포트폴리오) 아래 있는 별도의 프로젝트"**에 가깝습니다. **Spring Framework**는 IoC/DI 컨테이너, AOP, 트랜잭션 추상화 같은 핵심 기능을 제공하는 진짜 "코어" 프레임워크이고, **Spring Batch, Spring Security, Spring Data, Spring Cloud, Spring Boot** 등은 전부 Spring Framework 위에 얹혀서(그 DI 컨테이너, 트랜잭션 관리 같은 코어 기능을 가져다 쓰면서) 각자의 특화된 문제(배치 처리, 인증/인가, 데이터 접근, 분산 시스템, 자동 설정 등)를 해결하는 개별 프로젝트다. 각각 별도의 이름·버전·의존성(jar)을 가지고 있어서, Spring Batch를 쓴다고 Spring Security가 딸려오거나 하지 않는다. 그래서 "Spring 하위 개념"보다는 "Spring Framework를 기반으로 만들어진, Spring 생태계(family)에 속한 독립적인 프레임워크"라고 이해하는 게 더 정확하다. 이름에 'Spring'이 붙는 이유는 같은 생태계 소속이라는 걸 나타내기 위함이지, Spring Framework 내부의 한 구성요소라는 뜻은 아니다.

> **Q.** 그럼 spring이라는 환경에 속하는 대용량 처리에 특화된 프레임워크라고 이해하면 돼?
>
> 거의 맞지만 "대용량"보다는 **"일괄(batch) 방식으로 처리하는 데"** 특화된 게 핵심이다. Spring이라는 생태계에 속해있고, 대량의 데이터를 실시간이 아니라 정해진 시점에 한꺼번에(chunk 단위로) 읽고 가공하고 쓰는 배치 처리 패턴에 특화되어 있으며, 그 과정에서 필요한 재시작, skip/retry, 실행 이력 관리 같은 기능을 표준으로 제공하는 프레임워크다. "대용량"은 배치 처리에서 흔히 동반되는 특징이긴 하지만, 핵심은 데이터 양 자체보다 "일괄로, 청크 단위로, 재시작 가능하게 처리하는 방식"이라는 점이다. 그래서 "Spring 생태계에 속한, 대량 데이터의 일괄(batch) 처리에 특화된 프레임워크"라고 이해하면 정확하다.

> **Q.** 음 내가 배울때는 대용량 데이터 처리를 좀 더 중요하게 배웠던거 같은데 그럼 니 말은 batch의 동작 특징으로 chunk 단위로 일어나는 일괄 처리가 좀 더 핵심적인 개념이고 대용량 데이터 처리는 부가적인 효과라는거야?
>
> 앞선 설명을 정정한다. "chunk 처리가 핵심, 대용량은 부가효과"라는 위계는 맞지 않고, 실제로는 목적과 수단의 관계다. 대용량 데이터 처리 자체가 Spring Batch의 존재 이유(목적)다 — 수백만 건을 한 번에 메모리에 올려서 처리하면 OOM이 나거나, 처리 도중 실패하면 처음부터 다시 해야 하는 문제가 생기기 때문에, Spring Batch는 이런 대용량 데이터를 안전하고 효율적으로, 실패해도 복구 가능하게 처리하기 위해 만들어졌다. chunk 지향 처리(일괄 처리 방식)는 그 목적을 실현하기 위한 핵심 메커니즘이다 — 전체를 한 번에 메모리에 올리지 않고 일정 단위씩 읽고 커밋함으로써 메모리 사용량을 제한하고, 실패 시 마지막 커밋 지점부터 재시작 가능하게 만든다. 그래서 대용량 처리는 부가적 효과가 아니라, 대용량 데이터를 감당하기 위해 chunk 단위 처리라는 방식을 택한 것이며, 둘은 우열 관계가 아니라 목적-수단 관계로 뗄 수 없이 붙어있다.

> **Q.** 그럼 다시 정리해서 spring batch의 목적은 대용량 데이터 처리이고 이 목적을 이루기 위해서 채택한 방식이 chunk 단위의 일괄 처리다 맞아?
>
> 맞다. Spring Batch는 대용량 데이터를 안전하고 효율적으로, 실패해도 복구 가능하게 처리하기 위해 만들어진 프레임워크(목적)이고, 그 목적을 이루기 위해 채택한 핵심 방식이 chunk 단위의 일괄 처리 — 정해진 개수만큼 읽고 가공한 뒤 한 번에 커밋하는 방식(수단)이다.

> **Q.** job: 배치 처리의 최상위 단위. 하나 이상의 Step으로 구성 — 내가 프로젝트에서 사용할때는 job + step / read - write - process 방식으로 돌아갔던걸로 기억하는데 맞아?
>
> Job + Step 구조는 맞다. 다만 Step 내부의 처리 순서는 "Read → Write → Process"가 아니라 **"Read → Process → Write"**다. `ItemReader`가 데이터를 한 건씩 읽고 → `ItemProcessor`가 그 건을 가공/변환하고 → chunk 크기만큼 모이면 `ItemWriter`가 한 번에 쓴다. Write는 항상 Process 다음이고, 건별이 아니라 청크 단위로 일어난다는 점이 포인트다.

> **Q.** 내가 썼는대로 아직 정확히 구분이 안되는데 job + step 이랑 read - process - write 는 어떤 관계야? 할때 메서드 명을 무슨job, 무슨 write 이렇게 했던건 기억나는데
>
> 서로 다른 레벨의 개념이다. Job/Step은 "배치 작업을 어떻게 조직하느냐"의 구조적 단위이고(Job 안에 Step이 하나 이상), Read/Process/Write는 Job·Step과 나란한 개념이 아니라 **Step 하나를 chunk 지향 방식으로 만들 때 그 Step 내부에서 실제로 실행되는 처리 단계**다. 즉 Read-Process-Write는 Step의 "내용물"이다.
>
> ```
> Job (myJob)
>  └─ Step (myStep)          ← Job의 하위 단위
>       └─ Reader → Processor → Writer   ← Step "내부"에서 일어나는 처리 흐름
> ```
>
> Java Config로 쓰면 `myJob()`, `myStep()`은 구조(조직) 레벨의 빈이고, `myReader()`/`myProcessor()`/`myWriter()`는 그 `myStep()`을 구성하는 재료로 `.reader()`/`.processor()`/`.writer()`에 끼워 넣는 관계다:
>
> ```java
> @Bean
> public Job myJob(Step myStep) {
>     return jobBuilderFactory.get("myJob").start(myStep).build();
> }
>
> @Bean
> public Step myStep(ItemReader<A> reader, ItemProcessor<A, B> processor, ItemWriter<B> writer) {
>     return stepBuilderFactory.get("myStep")
>         .<A, B>chunk(100)
>         .reader(reader)
>         .processor(processor)
>         .writer(writer)
>         .build();
> }
>
> @Bean
> public ItemReader<A> myReader() { ... }
>
> @Bean
> public ItemProcessor<A, B> myProcessor() { ... }
>
> @Bean
> public ItemWriter<B> myWriter() { ... }
> ```
>
> "무슨job, 무슨write" 네이밍 기억이 정확히 이 계층 구조(Job/Step은 조직 단위, Reader/Processor/Writer는 Step 내부 구성 요소)를 가리키고 있는 것이다.

> **Q.** Job(설계도) → JobInstance(파라미터로 구체화된 실행 단위) → JobExecution(실제 시도 기록) → 그 안의 여러 StepExecution(단계별 실행 기록). 단위나 기록의 목적은 뭐야? 로직상에서 활용가능한 객체로써 남기는거야? 아니면 개발자가 확인을 위해?
>
> 둘 다지만, "프레임워크 로직이 실제로 사용하는 객체"가 우선이고 "개발자 확인용"은 부산물에 가깝다. `JobRepository`가 이 메타데이터(JobInstance/JobExecution/StepExecution)를 DB에 저장해두고, Spring Batch 프레임워크 자신이 실행할 때마다 이걸 실제로 참조해서 판단한다 — 같은 파라미터로 이미 성공한 JobInstance가 있으면 중복 실행을 막고, 실패한 Job을 재시작하면 마지막 StepExecution이 어디까지 처리했는지 보고 그 이후부터 이어서 처리한다. 각 JobExecution/StepExecution에는 `ExecutionContext`라는 키-값 저장소가 붙어있어 "지금까지 몇 건 처리했는지", "다음에 읽을 위치가 어디인지" 같은 상태를 실제로 저장했다가 재시작 시 꺼내 쓰므로, 단순 기록이 아니라 재시작 로직이 작동하기 위해 반드시 필요한 상태 저장소다. 부가적으로는 이 메타데이터 테이블(`BATCH_JOB_EXECUTION` 등)을 직접 조회하거나 관리 도구/actuator로 모니터링·디버깅하는 데도 쓰이고, 코드에서 `@BeforeStep`/`@AfterStep` 리스너에 `StepExecution`을 주입받아 처리 건수 같은 정보를 로직에서 직접 활용할 수도 있다. 정리하면 사람이 보려고 남기는 로그성 기록이 아니라, Spring Batch가 재시작·중복 방지 같은 핵심 동작을 하기 위해 실제로 읽고 쓰는 런타임 상태 객체이고, 그걸 개발자도 모니터링용으로 함께 활용할 수 있는 구조다.

> **Q.** 그럼 단위나 기록을 바탕으로 batch의 재시도 등에 활용하기 위해서 라고 이해하는게 맞겠네?
>
> 방향은 맞지만 "재시도(retry)"가 아니라 **"재시작(restart)"**이 정확한 용어다. 재시도(retry)는 청크 처리 중 아이템 하나에서 일시적 오류가 났을 때 그 아이템을 몇 번 다시 시도하는 것(Step 내부, 아이템 레벨)이고, 재시작(restart)은 Job 전체가 실패했을 때 처음부터가 아니라 마지막으로 성공한 지점부터 다시 실행하는 것(Job/Step 레벨)이다. Job/JobInstance/JobExecution/StepExecution 메타데이터는 바로 이 재시작을 가능하게 하기 위한 근거 데이터다. 정리하면 이 단위·기록들은 실패 시 처음부터 다시 하지 않고 이어서 재시작할 수 있게, 또 같은 파라미터로 중복 실행되는 걸 막고 실행 이력을 추적할 수 있게 하기 위한 것이다.

> **Q.** chunk 단위는 임의로 변경할 수 있어?
>
> 그렇다. Step을 만들 때 `.chunk(100)`처럼 숫자(커밋 간격, commit interval)를 직접 지정하며, 상수로 고정할 수도 있고 설정 파일 값을 주입받아 환경별로 다르게 줄 수도 있다. chunk를 크게 잡으면 커밋 횟수가 줄어 성능은 좋아지지만 메모리 사용량이 커지고 실패 시 롤백/재처리 범위도 커지며, 작게 잡으면 메모리는 절약되지만 커밋 오버헤드가 늘어나므로, 데이터 크기·처리 로직 무게·장애 재처리 비용을 감안해 값을 정한다. 고정 개수 대신 커스텀 `CompletionPolicy`를 넘겨 "일정 시간 경과" 같은 동적 기준으로 청크를 끊는 것도 가능하다. 즉 chunk 크기는 상황에 맞게 임의로 설정/조정 가능한 파라미터다.

> **Q.** 그럼 step 마다 다른 청크 단위 설정도 가능하겠네?
>
> 그렇다. chunk 크기는 Step 단위로 설정하는 값이라, 하나의 Job 안에 여러 Step이 있으면 각 Step을 만들 때마다 독립적으로 `.chunk(n)` 값을 다르게 줄 수 있다. 예를 들어 가벼운 단순 적재 Step은 `.chunk(500)`으로 크게, 외부 API 호출 등 무거운 처리를 하는 Step은 `.chunk(50)`으로 작게 잡는 식으로, 각 Step의 처리 특성(로직 무게, 메모리 사용량, 실패 시 재처리 비용)에 맞춰 서로 다른 chunk 크기를 독립적으로 설정하는 게 일반적이다.

> **Q.** 그럼 응용해서 예를 들어 첫시도에서 100 단위로 했다가 실패시 재시도할때 200으로 변경하는등의 가변적인 설정은 가능해?
>
> 가능은 하지만 프레임워크가 기본 제공하는 기능은 아니고 직접 커스터마이징해야 하는 영역이다. 기본적으로 chunk 크기는 Step 정의 시 고정으로 박아두는 값이라 Spring Batch가 "몇 번째 재시도인지"를 보고 자동으로 바꿔주지는 않는다. 직접 구현하면 (1) `@StepScope` + late binding으로 chunk 크기를 JobParameter처럼 외부 주입받게 하는 방법 — 다만 재시작(restart)이 성립하려면 같은 JobInstance로 인식되어야 하고 이는 보통 JobParameters가 동일해야 유지되므로, chunk 크기를 바꾸는 파라미터는 "identifying하지 않는(non-identifying) 파라미터"로 넘겨야 같은 JobInstance로 인식되면서 값만 바뀔 수 있다. (2) 커스텀 `CompletionPolicy`를 만들어 이전 StepExecution의 실패 이력이나 ExecutionContext 정보를 읽어 동적으로 청크 크기를 결정하는 방법. 다만 실무에서 흔히 쓰는 패턴은 아니며, 보통 "재시도를 더 안전하게" 하려는 목적이라면 chunk 크기를 동적으로 바꾸기보다 skip/retry 정책(아이템 레벨)을 튜닝하거나 애초에 안전한 chunk 크기를 고정해두는 방식으로 해결한다.

> **Q.** 그럼 굳이 커스텀하지말고 1번 batch/chunk(100) 실패시 다음 2번 batch/chunk(200)으로 넘기는 건?
>
> 그건 커스텀 없이 표준 기능만으로 가능하다. 앞서 말한 방식은 "같은 Step"을 재시작할 때 값을 바꾸려는 것이라 non-identifying 파라미터 같은 편법이 필요했지만, 이건 애초에 chunk 크기가 다른 별개의 Step 두 개를 만들어두고 1번 Step이 실패하면 2번 Step으로 흐름을 넘기는 방식이라 Spring Batch가 표준으로 지원하는 조건부 흐름 제어(Flow Control)로 그대로 구현된다.
>
> ```java
> @Bean
> public Job myJob(Step step1, Step step2) {
>     return jobBuilderFactory.get("myJob")
>         .start(step1)              // chunk(100)로 정의된 Step
>             .on("FAILED").to(step2)  // step1 실패하면 step2로
>         .from(step1).on("*").end()   // step1 성공하면 그대로 종료
>         .end()
>         .build();
> }
>
> @Bean
> public Step step1(...) {
>     return stepBuilderFactory.get("step1").<A,B>chunk(100)...build();
> }
>
> @Bean
> public Step step2(...) {
>     return stepBuilderFactory.get("step2").<A,B>chunk(200)...build();
> }
> ```
>
> step1의 종료 상태(exit status, 여기선 FAILED)에 따라 다음에 어떤 Step으로 갈지 조건 분기할 수 있고, 각 Step은 각자 원하는 chunk 크기를 독립적으로 고정해서 가지면 된다. 동일 Step 재시작 시 값 변경 같은 편법 없이, 서로 다른 chunk 설정을 가진 별개 Step을 실패 조건으로 연결하기만 하면 되는 훨씬 자연스럽고 표준적인 방법이다.
