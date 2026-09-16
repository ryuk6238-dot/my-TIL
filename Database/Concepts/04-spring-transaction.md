# Spring Transaction 의 이해

> 데이터베이스 학습 기록 — 노션 내용 정리 예정

## 개념 정리

### 1. 트랜잭션 기본 개념

- **트랜잭션(Transaction)**은 하나의 논리적 작업 단위로, 그 안의 작업이 모두 성공하거나 모두 실패해야 한다. 여러 테이블에 걸친 작업(주문+결제 등) 중 일부만 성공하면 데이터 정합성이 깨지므로, 다중 테이블 조작·중간 오류 가능성·동시성 처리가 필요한 상황에서 반드시 사용한다.
- **ACID**: Atomicity(원자성, 전부 성공 또는 전부 취소) · Consistency(일관성, 규칙/제약조건 준수) · Isolation(고립성, 다른 트랜잭션의 중간 결과를 볼 수 없음) · Durability(지속성, 커밋되면 영구 반영).
- 트랜잭션은 `활성(Active)` → `부분 완료(Partially Committed)` → `커밋(Committed)` 또는 `실패(Failed)` → `롤백(Aborted)` 흐름으로 상태가 변화한다. 커밋 이후에는 되돌릴 수 없고, 트랜잭션은 짧게 유지할수록 DB 락과 성능 저하를 줄일 수 있다.

### 2. Spring의 트랜잭션 처리 방식

- **선언적 트랜잭션(`@Transactional`)**: 메서드/클래스에 어노테이션만 붙이면 Spring이 AOP 프록시로 트랜잭션 경계를 감싸 커밋/롤백을 자동 처리한다. 실무에서 대부분 이 방식을 사용한다.
- **프로그래밍 방식(`TransactionTemplate`)**: 코드로 트랜잭션 경계를 직접 제어하며, 조건부 커밋/롤백처럼 유연한 처리가 필요할 때 사용한다. 내부적으로 `PlatformTransactionManager`를 사용한다.
- `@Transactional`이 선언된 빈은 실제 객체 대신 **프록시 객체**가 주입되고, 이 프록시가 메서드 호출을 가로채 트랜잭션 시작 → 실제 메서드 실행 → 커밋/롤백을 제어한다(Spring Boot 3.x는 기본적으로 CGLIB 프록시 사용). **같은 클래스 내부에서의 메서드 호출은 프록시를 우회하므로 `@Transactional`이 적용되지 않는다** — 이는 실무에서 자주 발생하는 실수이며, 해결책은 트랜잭션 메서드를 다른 빈으로 분리하는 것이다.
- **`PlatformTransactionManager`**는 트랜잭션의 시작(`getTransaction`)·커밋(`commit`)·롤백(`rollback`)을 담당하는 핵심 인터페이스이며, JPA 환경에서는 `JpaTransactionManager`가 기본으로 사용된다(내부적으로 `EntityManager`와 영속성 컨텍스트 생명주기를 자동 연동).

### 3. 트랜잭션 전파(Propagation)와 격리 수준(Isolation)

- **전파**는 이미 트랜잭션이 진행 중일 때 다른 `@Transactional` 메서드를 호출하면 어떻게 동작할지 정의한다.
  - `REQUIRED`(기본값): 기존 트랜잭션이 있으면 참여, 없으면 새로 생성.
  - `REQUIRES_NEW`: 항상 새 트랜잭션을 생성하고 기존 트랜잭션은 잠시 중단 — 독립적으로 커밋/롤백되어야 하는 로직(예: 실패해도 주문 자체는 유지해야 하는 포인트 적립)에 사용.
  - 이 외에 `SUPPORTS`, `NOT_SUPPORTED`, `MANDATORY`, `NEVER`, `NESTED`가 있다.
  - 주의: `REQUIRES_NEW`도 프록시를 통한 외부 호출일 때만 새 트랜잭션이 생성된다. 내부 메서드 호출로는 분리되지 않는다.
- **격리 수준**은 동시에 여러 트랜잭션이 같은 데이터를 다룰 때 발생하는 동시성 문제를 제어하는 기준이다.
  - Dirty Read(커밋 안 된 데이터를 읽음), Non-repeatable Read(같은 쿼리를 두 번 실행했는데 결과가 다름), Phantom Read(조건에 맞는 행 수가 중간에 바뀜) 세 가지가 대표적인 문제.
  - `READ UNCOMMITTED`(Dirty Read 허용) < `READ COMMITTED`(대부분 DB 기본값, PostgreSQL 포함) < `REPEATABLE READ`(Non-repeatable Read까지 방지, Phantom Read는 허용) < `SERIALIZABLE`(모두 방지하지만 성능 저하 큼) 순으로 엄격해진다.
  - Spring에서는 `@Transactional(isolation = Isolation.XXX)`로 설정하며, 실무에서는 대부분 `READ COMMITTED`로 충분하고 `SERIALIZABLE`은 금융/정산처럼 무결성이 절대적인 경우에만 제한적으로 사용한다.

### 4. 트랜잭션 예외 처리와 롤백

- Spring의 기본 롤백 정책: **언체크 예외(`RuntimeException`, `Error`)는 롤백**되고, **체크 예외(`Exception`)는 기본적으로 롤백되지 않고 커밋**된다.
- `@Transactional(rollbackFor = ...)`: 기본적으로 롤백되지 않는 체크 예외도 롤백시키고 싶을 때 사용.
- `@Transactional(noRollbackFor = ...)`: 기본적으로 롤백 대상인 런타임 예외를 롤백시키지 않고 싶을 때 사용.
- 실무에서 자주 하는 실수: **try-catch로 예외를 잡고 아무 처리도 하지 않으면** 예외가 전파되지 않아 트랜잭션이 정상 종료되며 **커밋**된다. 이 경우 예외를 다시 던지거나 `TransactionAspectSupport.currentTransactionStatus().setRollbackOnly()`를 명시적으로 호출해 롤백을 강제해야 한다.

### 5. 실무 적용 가이드

- 트랜잭션은 **서비스 계층에서 시작·종료**해야 한다. 컨트롤러(단순 요청 흐름 제어)나 리포지토리(Spring Data JPA가 내부 처리)에서는 직접 다루지 않는 것이 원칙.
- 조회 전용 메서드는 `@Transactional(readOnly = true)`로 선언한다 — Hibernate가 dirty checking을 수행하지 않아 메모리 사용과 불필요한 flush를 줄여준다.
- 트랜잭션 범위는 최대한 짧게 유지한다: 계산·검증·변환은 트랜잭션 시작 전에 끝내고, DB 저장 직전~직후만 트랜잭션으로 묶는 것이 이상적이다. 파일 업로드, 이메일 전송, 외부 API 호출처럼 지연이 발생하는 작업은 트랜잭션 밖에서 처리하거나 이벤트/비동기로 위임한다.
- 흔한 실수 정리: (1) 내부 메서드 호출은 프록시를 우회해 `@Transactional`이 적용되지 않음, (2) `REQUIRES_NEW`도 프록시를 통한 외부 빈 호출이어야 동작함, (3) 트랜잭션이 너무 길면 DB 락 점유와 커넥션 풀 고갈로 이어짐, (4) 예외를 삼키거나 체크 예외를 방치하면 롤백이 누락됨. 전파/롤백이 예상대로 동작하지 않을 땐 "프록시를 거쳐 호출했는가?"부터 점검한다.
