# Spring Data JPA 도입하기

> 데이터베이스 학습 기록 — 노션 내용 정리 예정

## 개념 정리

### 1. ORM과 JPA의 이해

- **SQL 중심 기술(MyBatis, Spring JDBC)**: 개발자가 SQL을 직접 작성·관리하는 전통적 방식. 쿼리 통제력은 높지만 Java 코드에 SQL이 노출되고, 스키마 변경 시 SQL을 전수 수정해야 하는 유지보수 부담이 있다.
- **패러다임 불일치(Object-Relational Impedance Mismatch)**: 객체지향(참조·상속·다형성 중심)과 관계형 DB(테이블·외래키·정규화 중심)는 데이터를 표현하는 방식이 근본적으로 다르다. 객체의 상속 구조, 참조, 컬렉션 필드는 테이블로 그대로 표현되지 않아 매핑 문제(Mapping Gap)가 발생한다.
- **ORM**은 이 불일치를 해소하기 위해 객체 ↔ 테이블 매핑을 자동 처리하는 기술. 생산성·가독성이 향상되지만, 내부 동작을 모르면 성능 저하나 예기치 못한 쿼리가 발생할 수 있다.
- **JPA(Java Persistence API)**는 자바 진영의 **ORM 표준 명세(인터페이스 규약)**일 뿐이고, 실제 동작은 구현체(대표적으로 **Hibernate**)가 담당한다. 즉 JPA는 "ORM이 어떤 모습이어야 하는지"를 정의한 명세(규약)일 뿐, JPA 자체가 실제로 매핑 작업을 수행하지는 않는다 — Java의 `List` 인터페이스가 규약만 정의하고 실제 동작은 `ArrayList` 같은 구현체가 담당하는 것과 같은 관계다. `jakarta.persistence` 패키지 기반(JPA 3.0 이상, Spring Boot 3.x부터 사용)이며, 객체 중심 개발·벤더 독립성·JPQL(객체 기반 쿼리 언어)을 제공한다.
- **영속성 컨텍스트(Persistence Context)**: 엔티티를 영구 저장하는 환경으로, 엔티티 매니저(EntityManager) 생성 시 함께 만들어지며 Key-Value로 엔티티를 관리한다. 엔티티 매니저는 Thread-Safe하지 않아 Web에서는 보통 Request Scope와 일치시킨다.
  - **엔티티 생명주기**: 비영속(new) → 영속(managed) → 준영속(detached)/삭제(removed), 준영속 → 병합(merge)으로 다시 영속화 가능.
  - **1차 캐시**: `@Id`를 key로 하는 영속성 컨텍스트 내부 캐시. 같은 트랜잭션에서 동일 식별자 조회 시 항상 같은 인스턴스를 반환(동일성 보장)하고, 두 번째 조회부터는 DB를 타지 않는다.
  - **쓰기 지연(Write-Behind)**: INSERT/UPDATE/DELETE SQL을 즉시 보내지 않고 쓰기 지연 저장소에 모았다가, 커밋 또는 `flush()` 시점에 한꺼번에 DB로 전송한다.
  - **변경 감지(Dirty Checking)**: 영속 상태 엔티티는 최초 스냅샷과 현재 상태를 flush 시점에 비교해 변경분만 UPDATE SQL로 자동 생성한다. 비영속·준영속 객체는 변경 감지 대상이 아니다.

### 2. Spring Data JPA 시작하기

- **Spring Data JPA**는 Spring Data 프로젝트의 하위 모듈로, JPA(EntityManager, 쿼리 작성 등)를 추상화해 Repository 인터페이스만으로 데이터 접근 계층을 구현하게 해주는 프레임워크다. `JPA(표준 명세) → Hibernate(구현체) → Spring Data JPA(자동화 레이어)` 관계로 이해하면 된다.
- 주요 기능: `JpaRepository` 상속만으로 CRUD 자동 구현, 메서드 이름 기반 쿼리 생성(`findByPriceLessThan` 등), `@Query`/QueryDSL/Native Query를 통한 커스텀 쿼리, `Pageable`/`Sort`를 통한 페이징·정렬, Spring 트랜잭션·예외 변환과의 통합.
- **설정**: `spring-boot-starter-data-jpa` 의존성 하나로 Spring Data JPA + Hibernate + JPA가 자동 구성되며, DBMS별 JDBC 드라이버만 추가하면 된다. `application.yaml`의 `spring.jpa.hibernate.ddl-auto`로 스키마 자동 생성 전략을 제어한다.

  | 값 | 설명 |
  | --- | --- |
  | `none` | DDL 미실행 |
  | `validate` | 매핑만 검증, DDL 미실행 |
  | `update` | 차이점만 반영(ALTER/CREATE), 기존 데이터 보존 |
  | `create` | 기존 테이블 DROP 후 재생성(데이터 전부 삭제) |
  | `create-drop` | 시작 시 생성, 종료 시 DROP(테스트용) |

  → 실무에서는 `validate` 또는 `none`을 사용하고, `update`/`create`는 실습·테스트 환경에서만 사용하는 것이 일반적이다.

- **Repository 계층 구조**: `Repository`(마커 인터페이스) → `CrudRepository`(기본 CRUD) → `PagingAndSortingRepository`(+페이징/정렬) → `JpaRepository`(+JPA 특화 기능, 벌크·flush 제어 등). 실무에서는 대부분 `JpaRepository`를 직접 상속한다.
- **자동 구현 원리**: Spring Boot 실행 시 `@EnableJpaRepositories`가 활성화되어 사용자 정의 Repository 인터페이스를 스캔하고, `JpaRepositoryFactoryBean → JpaRepositoryFactory`가 `SimpleJpaRepository`를 상속한 **프록시 객체**를 런타임에 생성해 빈으로 등록한다. `QueryLookupStrategy`가 메서드 이름을 분석해 쿼리를 생성하거나 `@Query`를 해석한다.

### 3. Entity 설계 기초

- `@Entity`는 클래스가 DB 테이블과 매핑됨을 선언하는 어노테이션. 기본 생성자 필수, `final`/`inner class` 불가, `@Id`가 반드시 하나 이상 있어야 하며 없으면 앱 실행 자체가 실패한다.
- `@Table(name = "...")`로 매핑될 테이블명을 명시(생략 시 클래스명 사용). 실무에서는 테이블명 규칙(`tbl_` 접두어 등)을 명시하는 경우가 많다.
- **기본 키**: `@Id`로 지정, `@GeneratedValue`로 자동 생성 전략 지정. PostgreSQL에서는 일반적으로 `GenerationType.IDENTITY`(DB auto-increment) 전략을 사용한다.
- **필드 매핑(`@Column`)**: 기본적으로 필드명이 컬럼명으로 매핑되지만, `name`, `nullable`, `length`, `unique`, `columnDefinition`, `insertable`/`updatable` 등을 명시해 가독성·데이터 품질을 높이는 것이 실무 권장이다.
- **Java ↔ SQL 타입 매핑**(PostgreSQL 기준): `String → varchar(255)`, `int/Integer → integer`, `long/Long → bigint`, `LocalDate → date`, `LocalDateTime → timestamp`, `BigDecimal → numeric`. 방언(dialect)에 따라 실제 SQL 타입은 달라질 수 있다.

### 4. Entity 연관관계 매핑

- **방향성**: 단방향(한쪽만 참조)과 양방향(서로 참조, 한쪽에 `mappedBy` 필수)으로 구분된다.
- **다중성**: 1:1, 1:N, N:1, N:M. N:M은 JPA가 중간 테이블을 자동 생성해야 하는 관계다.
- **연관관계의 주인(owner)**: 외래 키를 실제로 관리하는 쪽(`@JoinColumn`을 가진 쪽)이 주인이며, 데이터 변경(생성·수정)은 반드시 주인 쪽에서 이루어져야 DB에 반영된다. 주인이 아닌 쪽(`mappedBy`)에서 값을 설정해도 무시된다.
- **어노테이션별 특징**
  - `@ManyToOne`: 가장 흔한 관계(N:1). 기본 FetchType은 `EAGER`이므로 성능을 위해 명시적으로 `LAZY` 지정 권장.
  - `@OneToMany(mappedBy = "...")`: 보통 연관관계의 주인이 아닌 쪽. 단방향 `@OneToMany`는 중간 테이블이 추가로 생기므로 비추천.
  - `@OneToOne`: 드물게 사용, 상세/부가 정보 분리 시 활용.
  - `@ManyToMany`: 중간 테이블에 추가 컬럼을 둘 수 없고 유지보수가 어려워 실무에서는 거의 쓰지 않고, **중간 엔티티를 직접 만들어 N:1 + 1:N 구조로 해소**하는 방식을 권장한다.
- 실무 팁: 양방향은 `toString()`/JSON 직렬화 시 무한 루프, 순환 의존성 등의 위험이 있어 **데이터 변경 책임이 있는 쪽만 단방향으로 설계**하는 것도 유효한 전략이다. 조회 API에서 엔티티를 그대로 반환하지 않고 **DTO로 변환**해서 무한루프·지연로딩 예외를 피한다.

### 5. Repository 활용

- `JpaRepository<엔티티타입, PK타입>`을 상속하면 `save()`, `findById()`, `findAll()`, `delete()`, `deleteById()`, `existsById()`, `count()` 등 기본 CRUD가 자동 제공된다. `save()`는 PK 유무에 따라 INSERT/UPDATE로 동작하고, `findById()`는 `Optional`을 반환한다.
- **쿼리 메서드(Query Method)**: `findBy[필드][조건]`, `existsBy`, `countBy`, `deleteBy` 등 메서드 이름을 분석해 JPQL을 자동 생성한다. `And`/`Or`, `Between`, `LessThan`/`GreaterThan`, `Like`/`Containing`, `In`, `OrderBy`, `IsNull` 등의 키워드 조합이 가능하며, 연관 엔티티 필드도 `findByCategoryName`처럼 경로 탐색으로 조건을 걸 수 있다.
- 메서드명이 길어지면 `@Query`로 **JPQL**(엔티티 기준, 타입 안정성)을 직접 작성하거나, DB 고유 기능·복잡한 조인이 필요할 때만 `nativeQuery = true`로 **Native Query**를 사용한다. 더 복잡한 동적 쿼리는 QueryDSL 등을 고려한다.

### 6. 페이징과 정렬

- `Pageable`(`page`, `size`, `sort`)로 페이징 요청을 표현한다. `PageRequest.of(page, size, Sort.by(...))` 형태로 생성하면 내부적으로 `LIMIT/OFFSET/ORDER BY` SQL로 변환된다.
- `Sort.by("field").ascending()`으로 정렬 기준을 지정하며 `.and(Sort.by(...))`로 다중 정렬도 가능하다.
- 반환 타입은 `Page<T>`(전체 개수·전체 페이지 수 포함, 일반적인 페이지 네비게이션에 적합)와 `Slice<T>`(다음 페이지 존재 여부만 제공, count 쿼리 생략 가능해 무한 스크롤에 적합) 중 상황에 맞게 선택한다.

### 7. JPA 활용 시 주의 사항

- **N+1 문제**: 연관 엔티티를 가진 목록을 조회한 뒤 각 항목에서 지연 로딩 필드에 접근하면, 최초 조회 쿼리 1번 + 연관 엔티티 조회 쿼리 N번이 추가로 발생하는 성능 문제. 지연 로딩뿐 아니라 즉시 로딩(EAGER)이어도 컬렉션 조회 시 발생할 수 있다.
  - **해결 1) Fetch Join**: JPQL의 `JOIN FETCH`로 연관 엔티티를 한 번의 쿼리로 함께 조회. 단, 컬렉션 Fetch Join + 페이징을 같이 쓰면 메모리에서 페이징이 일어나 위험하고, 둘 이상의 컬렉션을 동시에 Fetch Join할 수 없으며(카테시안 곱), 1:N에서는 중복 데이터가 생겨 `DISTINCT`가 필요할 수 있다.
  - **해결 2) `@EntityGraph(attributePaths = {...})`**: JPQL 없이 선언적으로 연관 엔티티 로딩 전략을 지정. `findAll()`처럼 기존 메서드에도 적용 가능해 코드 중복을 줄일 수 있지만, 과도하게 지정하면 불필요한 데이터까지 로딩된다.
  - 간단한 관계는 EntityGraph, 복잡한 조건·조인은 Fetch Join이 적합하다.
- **로딩 전략**: `~One`(`@ManyToOne`, `@OneToOne`)의 기본값은 EAGER, `~Many`(`@OneToMany`, `@ManyToMany`)의 기본값은 LAZY. 실무에서는 **모든 연관관계를 기본 LAZY로 설정**하고, 필요한 곳에서만 명시적으로 Fetch Join/EntityGraph를 사용하는 것이 권장된다(EAGER는 예측 어려운 쿼리와 N+1을 야기하기 쉬움). 복잡한 화면은 DTO 직접 조회(JPQL의 `new` 생성자 표현식)로 처리하는 것도 방법이다.
- **영속성 전이(Cascade)**: 부모 엔티티의 상태 변화(PERSIST/MERGE/REMOVE/REFRESH/DETACH/ALL)를 연관된 자식에게 전파하는 기능. **소유권과 생명주기가 명확히 동일한 관계(게시글-첨부파일 등)에서만** 사용해야 하며, 하나의 자식을 여러 부모가 참조하는 구조(다중 소유자)에서는 `CascadeType.REMOVE` 등이 참조 무결성을 깨뜨릴 위험이 있다.
- **고아 객체 제거(`orphanRemoval = true`)**: 컬렉션에서 자식을 제거하거나 참조를 끊으면 해당 자식 엔티티를 자동 삭제한다. `@OneToOne`/`@OneToMany`에서만 사용 가능하며, `CascadeType.ALL`과 함께 쓰면 부모가 자식의 생명주기를 완전히 관리하게 된다(다중 소유자 관계에서는 사용 금지).
