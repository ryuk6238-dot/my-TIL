# my-TIL

Java / Spring 백엔드 기술면접 대비 학습 기록.



## 📌 사용법

1. 최상단에 공부할 주제 폴더(패키지)를 추가합니다. 예: `Algorithm/`
2. push하면 GitHub Actions가 그 패키지 안에 문서 작업용 `README.md`를 만들고,
   아래 목차에 패키지를 자동으로 추가합니다.
3. 주제를 더 쪼개고 싶으면 패키지 안에 새 `.md` 파일이나 하위 패키지를 만들면 됩니다.
   역시 목차에 자동 반영됩니다.

## 🗂 목차

아래 목차는 `.github/workflows/update-readme.yml`이 자동으로 갱신합니다. 직접 수정하지 마세요.

<!-- TOC:START -->

- [CLAUDE.md](./CLAUDE.md)
- 📁 **[Data_Structure](./Data_Structure/README.md)**
- 📁 **[Database](./Database/README.md)**
  - 📁 **[Concepts](./Database/Concepts/README.md)**
    - [SQL 이해하기](./Database/Concepts/01-sql.md)
    - [데이터베이스 설계](./Database/Concepts/02-db-design.md)
    - [Spring Data JPA 도입하기](./Database/Concepts/03-spring-data-jpa.md)
    - [Spring Transaction 의 이해](./Database/Concepts/04-spring-transaction.md)
  - 📁 **[QnA](./Database/QnA/README.md)**
    - [SQL 이해하기 — Q&A](./Database/QnA/01-sql.md)
    - [데이터베이스 설계 — Q&A](./Database/QnA/02-db-design.md)
    - [Spring Data JPA 도입하기 — Q&A](./Database/QnA/03-spring-data-jpa.md)
    - [Spring Transaction 의 이해 — Q&A](./Database/QnA/04-spring-transaction.md)
- 📁 **[Infra](./Infra/README.md)**
  - 📁 **[Concepts](./Infra/Concepts/README.md)**
    - [Docker: 빌드, 배포, 컨테이너 실행하기](./Infra/Concepts/01-docker.md)
    - [AWS: 계정 생성부터 ECS, S3, RDS 설정](./Infra/Concepts/02-aws-setup.md)
    - [AWS ECS 로 프로그램 배포하기](./Infra/Concepts/03-aws-ecs-deploy.md)
  - 📁 **[QnA](./Infra/QnA/README.md)**
    - [Docker: 빌드, 배포, 컨테이너 실행하기 — Q&A](./Infra/QnA/01-docker.md)
    - [AWS: 계정 생성부터 ECS, S3, RDS 설정 — Q&A](./Infra/QnA/02-aws-setup.md)
    - [AWS ECS 로 프로그램 배포하기 — Q&A](./Infra/QnA/03-aws-ecs-deploy.md)
- 📁 **[Java](./Java/README.md)**
  - 📁 **[Concepts](./Java/Concepts/README.md)**
    - [Java 프로그래밍 시작하기](./Java/Concepts/01-java-programming-start.md)
    - [객체지향 프로그래밍의 이해](./Java/Concepts/02-oop.md)
    - [컬렉션 프레임워크와 Stream API](./Java/Concepts/03-collections-stream.md)
    - [알고리즘과 자료구조 이해하기](./Java/Concepts/04-algorithm-datastructure.md)
    - [Java 비동기 처리하기](./Java/Concepts/05-java-async.md)
  - 📁 **[QnA](./Java/QnA/README.md)**
    - [Java 프로그래밍 시작하기 — Q&A](./Java/QnA/01-java-programming-start.md)
    - [객체지향 프로그래밍의 이해 — Q&A](./Java/QnA/02-oop.md)
    - [컬렉션 프레임워크와 Stream API — Q&A](./Java/QnA/03-collections-stream.md)
    - [알고리즘과 자료구조 이해하기 — Q&A](./Java/QnA/04-algorithm-datastructure.md)
    - [Java 비동기 처리하기 — Q&A](./Java/QnA/05-java-async.md)
- 📁 **[JPA](./JPA/README.md)**
- 📁 **[Network](./Network/README.md)**
  - 📁 **[Concepts](./Network/Concepts/README.md)**
    - [백엔드 통신 디자인 패턴](./Network/Concepts/01-backend-communication-patterns.md)
    - [프로토콜과 HTTPS 이해하기](./Network/Concepts/02-protocol-https.md)
    - [프록시 및 부하 분산기](./Network/Concepts/03-proxy-load-balancer.md)
  - 📁 **[QnA](./Network/QnA/README.md)**
    - [백엔드 통신 디자인 패턴 — Q&A](./Network/QnA/01-backend-communication-patterns.md)
    - [프로토콜과 HTTPS 이해하기 — Q&A](./Network/QnA/02-protocol-https.md)
    - [프록시 및 부하 분산기 — Q&A](./Network/QnA/03-proxy-load-balancer.md)
- 📁 **[Operating_System](./Operating_System/README.md)**
- 📁 **[Project](./Project/README.md)**
- 📁 **[Spring](./Spring/README.md)**
  - 📁 **[Concepts](./Spring/Concepts/README.md)**
    - [Spring 오버뷰](./Spring/Concepts/01-spring-overview.md)
    - [Spring Boot: 코드 레벨 아키텍처](./Spring/Concepts/02-spring-boot-architecture.md)
    - [Spring Beans의 이해와 사용](./Spring/Concepts/03-spring-beans.md)
    - [Spring MVC: 비지니스 로직](./Spring/Concepts/04-spring-mvc.md)
    - [좋은 웹 API 디자인이란?](./Spring/Concepts/05-web-api-design.md)
    - [Spring 안정성 높이기](./Spring/Concepts/06-spring-reliability.md)
    - [Spring Cache](./Spring/Concepts/07-spring-cache.md)
    - [Spring Security 기본기](./Spring/Concepts/08-spring-security-basics.md)
    - [Spring Security - 쿠키/세션 기반 인증/인가](./Spring/Concepts/09-spring-security-session-auth.md)
    - [유저 관리 기능](./Spring/Concepts/10-user-management.md)
  - 📁 **[QnA](./Spring/QnA/README.md)**
    - [Spring 오버뷰 — Q&A](./Spring/QnA/01-spring-overview.md)
    - [Spring Boot: 코드 레벨 아키텍처 — Q&A](./Spring/QnA/02-spring-boot-architecture.md)
    - [Spring Beans의 이해와 사용 — Q&A](./Spring/QnA/03-spring-beans.md)
    - [Spring MVC: 비지니스 로직 — Q&A](./Spring/QnA/04-spring-mvc.md)
    - [좋은 웹 API 디자인이란? — Q&A](./Spring/QnA/05-web-api-design.md)
    - [Spring 안정성 높이기 — Q&A](./Spring/QnA/06-spring-reliability.md)
    - [Spring Cache — Q&A](./Spring/QnA/07-spring-cache.md)
    - [Spring Security 기본기 — Q&A](./Spring/QnA/08-spring-security-basics.md)
    - [Spring Security - 쿠키/세션 기반 인증/인가 — Q&A](./Spring/QnA/09-spring-security-session-auth.md)
    - [유저 관리 기능 — Q&A](./Spring/QnA/10-user-management.md)

> 총 70개의 문서

<!-- TOC:END -->
