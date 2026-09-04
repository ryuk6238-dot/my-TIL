# Spring 안정성 높이기

> Spring 심화 학습 기록 — 노션 내용 정리 예정

## 개념 정리

### 1. 애플리케이션 안정성 개요

- 웹 애플리케이션의 안정성이란 예상치 못한 상황에서도 서비스가 중단되지 않고 사용자에게 일관된 경험을 제공하는 능력이다.
- 운영 환경에서 자주 발생하는 4가지 문제 상황
  - **잘못된 입력값 유입**: 프론트엔드 검증은 개발자 도구로 우회 가능하므로 서버 측 검증이 반드시 필요하다.
  - **예상치 못한 예외 발생**: DB 연결 실패, 파일 I/O 오류, 타입 변환 오류, 동시성 문제 등.
  - **시스템 리소스 부족**: 메모리 누수로 인한 OOM, CPU 과부하, DB 커넥션 풀 고갈.
  - **외부 시스템 연동 실패**: 결제·소셜 로그인·이메일 발송 등 우리가 직접 제어할 수 없는 영역이므로 타임아웃, 재시도, 대체 수단 같은 사전 대비책이 중요하다.
- 이 4가지 문제에 대응하기 위한 **네 가지 핵심 요소**: 예외 처리(시스템 복원력), 로깅(문제 추적), 입력값 검증(데이터 품질), 모니터링(사전 예방). 각 요소는 독립적이지 않고 상호 보완적으로 작동해야 전체 안정성이 높아진다.

### 2. 예외 처리

**예외 처리가 필요한 이유**
- 안정적 서비스 운영(외부 서비스 장애 시에도 graceful degradation), 사용자에게 이해 가능한 피드백 제공, 하나의 기능 실패가 전체로 전파되는 것을 막는 장애 격리, 디버깅을 위한 컨텍스트 정보 수집.

**Spring의 언체크 예외 중심 설계**
- 체크 예외(`SQLException`, `IOException` 등)는 각 계층마다 `throws` 선언이 강제되어 상위 계층이 하위 계층의 기술적 세부사항에 강하게 결합되는 문제가 있었다.
- Spring은 대부분의 예외를 `RuntimeException` 기반으로 설계해서, 호출자가 굳이 처리하지 않아도 되고 필요한 곳에서만 선택적으로 처리할 수 있게 했다.
- **예외 추상화/변환**: JDBC의 `SQLException`처럼 벤더마다 다른 기술적 예외를, Spring이 `DataAccessException` 계층(`DuplicateKeyException`, `DataIntegrityViolationException` 등)으로 통합 변환해준다. 덕분에 DB나 ORM이 바뀌어도 예외 처리 코드는 크게 바뀌지 않는다.

**예외 계층 구조 설계**
- 모든 커스텀 예외의 공통 부모로 `ApplicationException`(errorCode, context, timestamp 포함)을 두고, 도메인별로 `UserException`, `OrderException` 등을 상속받아 구체적인 예외(`DuplicateEmailException`, `InsufficientStockException` 등)를 만든다.
- `ErrorCode` enum으로 HTTP 상태 코드·코드 문자열·기본 메시지를 표준화하면 모니터링·통계와도 연동하기 쉽다.

**통합 예외 처리 구현**
- `@ExceptionHandler`는 컨트롤러 단위 처리라 코드 중복이 생기기 쉽고, `@RestControllerAdvice`로 전역에서 한 번에 처리하는 것이 일관성 확보에 유리하다.
- 표준화된 `ErrorResponse`(code, message, timestamp, details)로 API 오류 응답을 통일한다.
- 예외는 가능한 한 빨리, 충분한 컨텍스트가 있는 곳(주로 도메인 서비스 레벨)에서, 비즈니스 의미가 명확한 시점에 발생시켜야 한다.
- Repository 등 하위 계층에서는 기술적 예외(`DuplicateKeyException` 등)를 잡아 의미있는 비즈니스 예외로 전환(Exception Translation)한다.

### 3. 로깅

**로깅의 필요성**
- 애플리케이션의 눈과 귀 역할을 하며, 시스템 헬스체크·성능 모니터링, 비즈니스 메트릭 수집, 오류 추적/근본 원인 분석, 분산 시스템에서의 요청 추적(MDC 활용), 사용자 행동 분석, 보안 감사(인증/권한 이벤트, 민감 데이터 변경 이력) 등 폭넓게 활용된다.

**Logback 구조**
- Spring Boot는 기본 로깅 프레임워크로 Logback을 사용하며, 핵심 구성 요소는 **Logger**(메시지 생성), **Appender**(출력), **Layout/Encoder**(형식)다.
- `logback-spring.xml`을 쓰면 `<springProfile>`을 통해 Spring 프로파일과 연동해 환경별로 다른 설정을 적용할 수 있다.
- 로그 레벨은 `TRACE < DEBUG < INFO < WARN < ERROR` 순으로 중요도가 높아지며, 패키지별로 레벨을 다르게 지정할 수 있다(`application` 로그는 상세하게, `org.springframework`/`org.hibernate` 등 외부 라이브러리는 WARN 이상만).
- **MDC(Mapped Diagnostic Context)**로 요청별 traceId 등을 로그에 자동 포함시켜 요청 단위 추적이 가능하다. 스레드마다 값이 저장되므로 `finally`에서 반드시 `MDC.clear()`로 정리해야 메모리 누수를 막을 수 있다.
- 로그 파일은 시간/크기 기반 롤링 정책, 목적별 파일 분리(business/security/error), 비동기 Appender(`AsyncAppender`)로 성능 최적화를 적용한다.
- 환경별 전략: 개발(DEBUG, 짧은 보관), 스테이징(INFO~DEBUG 혼합, 중간 보관), 운영(INFO, 구조화된 패턴 + 비동기, 긴 보관)으로 차별화한다.

**효과적인 로깅 구현**
- 로그 레벨 선택 기준: `ERROR`(즉각 대응 필요한 시스템 오류), `WARN`(예상 가능한 비즈니스 예외·잠재적 문제), `INFO`(중요 비즈니스 이벤트), `DEBUG`(개발용 상세 정보, 운영에서는 보통 비활성화), `TRACE`(매우 상세한 실행 흐름).
- 좋은 로그 메시지는 모호한 `"오류 발생"` 대신 주문ID·사용자·처리시간 같은 구조화된 컨텍스트를 함께 남긴다.
- 비밀번호, 카드번호, IP 등 **민감 정보는 절대 그대로 로깅하지 않고 마스킹**해야 한다.
- 재시도/복구 로직에서는 시도 횟수, 다음 재시도 시점 등 과정을 상세히 기록해야 문제 추적이 쉬워진다.
- 로그 분석 관점에서는 사용자 여정 추적(검색→장바구니→결제 단계별 로깅), 성능 병목 식별(구간별 처리 시간 세분화), 실시간 비즈니스 메트릭 모니터링이 핵심 활용 포인트다. 검색은 시간 범위 + 키워드 조합, 사용자/세션 ID 기반 검색이 효과적이며, 오류율·응답시간 임계치 기반의 예방적 알림 체계를 구축할 수 있다.

### 4. Bean Validation

**필요성**
- 프론트엔드 검증은 우회 가능하므로 서버 측 검증이 보안·안정성의 첫 번째 방어선이다. SQL 인젝션, XSS 등 대부분의 공격은 검증되지 않은 입력을 통해 이루어진다.
- 선언적 어노테이션 방식으로 검증 규칙을 한 곳에 정의해 재사용하면, 여러 API에서 검증 기준이 제각각이 되는 문제를 막을 수 있다.

**기본 검증 어노테이션**
- 문자열: `@NotNull`(null만 금지) < `@NotEmpty`(null+빈 문자열 금지) < `@NotBlank`(null+빈 문자열+공백 문자열 모두 금지, 가장 엄격), `@Size`, `@Email`.
- 숫자: `@Positive`, `@PositiveOrZero`, `@Negative`, `@NegativeOrZero`, `@Min`/`@Max`, `@DecimalMin`/`@DecimalMax`, `@Digits`.
- 날짜/시간: `@Past`, `@PastOrPresent`, `@Future`, `@FutureOrPresent`.
- 기타: `@Pattern`(정규식), `@AssertTrue`/`@AssertFalse`(메서드 기반 복합 검증), `@Valid`(중첩 객체/컬렉션 요소 재귀 검증).

**계층별 검증 전략**
- **Controller**: 외부 요청의 1차 방어선. HTTP 요청 형식·타입, 파일 업로드 크기/확장자, 페이징 파라미터 범위 등 형식적 검증을 담당한다.
- **Service**: 이메일 중복처럼 DB 조회가 필요한 검증, 권한/상태 기반 검증, 외부 시스템 연동 검증, 트랜잭션 범위 내 일관성 검증 등 비즈니스 규칙을 담당한다.

**검증 그룹(Validation Group)**
- 동일한 DTO를 생성/수정 등 여러 상황에서 재사용하면서 각기 다른 검증 규칙을 적용하고 싶을 때, 마커 인터페이스(`OnCreate`, `OnUpdate` 등)를 만들고 어노테이션의 `groups` 속성과 컨트롤러의 `@Validated(Group.class)`를 조합해서 상황별로 검증을 분기한다. 그룹이 너무 많아지면 관리가 어려워지므로 공통 필드는 `Default` 그룹으로 두고 그룹 수를 최소화하는 것이 좋다.

**커스텀 Validator**
- 기본 어노테이션으로 표현할 수 없는 복잡한 규칙(휴대폰 번호 형식, 사업자등록번호 체크섬, 비밀번호 강도 등)은 `@Constraint`를 가진 커스텀 어노테이션 + `ConstraintValidator` 구현체로 만든다.
- `initialize()`에서 정규식 컴파일 등 비용이 큰 초기화를 한 번만 수행하고, `isValid()`에서 실제 검증 로직을 수행한다(`null`은 보통 `@NotNull`에 위임하고 `true` 반환).
- `ConstraintValidatorContext.buildConstraintViolationWithTemplate()`으로 상황에 맞는 동적 오류 메시지를 만들 수 있다.
- 외부 API 호출이 필요한 검증은 타임아웃/장애 시 폴백 전략을 함께 고려해야 하고, 캐시를 쓸 때는 LRU 등으로 메모리 누수를 방지해야 한다.
- `@Valid`를 필드에 붙이면 중첩 객체(`Address` 등)까지 재귀적으로 검증되고, `List<@Valid UserDto>`처럼 타입 파라미터에 붙이면 컬렉션의 각 요소도 개별 검증된다.

### 5. Spring Actuator

- Actuator는 운영 중인 애플리케이션의 상태·메트릭·정보를 노출하는 엔드포인트 모음이며, `spring-boot-starter-actuator` 의존성만 추가하면 사용할 수 있다.
- 기본적으로 대부분의 엔드포인트가 비활성화되어 있어 `management.endpoints.web.exposure.include`에 필요한 것만 명시해야 한다(운영 환경에서는 `*`로 전부 열지 않는다).

**주요 엔드포인트**
- `/actuator/health`: 애플리케이션 및 구성 요소(DB, 디스크, ping 등)의 상태를 `UP`/`DOWN`으로 보여준다. `show-details: always`로 설정하면 각 컴포넌트별 상세 정보까지 확인 가능하고, 로드밸런서/쿠버네티스가 이 응답으로 인스턴스 생존 여부를 판단한다. DB 연결이 끊기면 `db` 컴포넌트가 `DOWN`이 되고 전체 `status`도 `DOWN`으로 바뀐다.
- `/actuator/info`: `info.*`로 설정한 앱 이름/버전/빌드 정보 등을 노출한다. DB 연결 정보나 내부 IP 같은 민감 정보는 절대 포함하지 않아야 하며, 필요하면 Spring Security로 인증된 사용자에게만 노출하도록 제한한다.
- `/actuator/metrics`: JVM 메모리, GC, CPU, `http.server.requests`(요청 수·응답시간) 등을 제공하며, `?tag=key:value` 형태로 특정 URI·메서드·상태코드별 세부 지표를 필터링할 수 있다.

**커스텀 HealthIndicator**
- `HealthIndicator` 인터페이스를 구현해 카카오페이 같은 중요 외부 시스템의 생존 여부를 `/actuator/health` 응답에 추가할 수 있다(`Health.up()`/`Health.down()` + `.withDetail()`).

**모니터링 연동**
- 메트릭 수집은 내부적으로 Micrometer 라이브러리를 사용하며, `micrometer-registry-prometheus` 의존성과 `/actuator/prometheus` 엔드포인트를 통해 Prometheus·Datadog 같은 외부 모니터링 도구와 연동할 수 있다.
