# CLAUDE.md

This file guides Claude Code when working in this repository (`my-TIL`).

## Project overview

This repo is a personal TIL (Today I Learned) archive for Java/Spring 백엔드 학습, organized by topic folders (`Java/`, `Spring/`, `Database/`, `Infra/`, `Network/`, etc.). Each top-level folder has an auto-generated `README.md` (see `.github/workflows/update-readme.yml` and `.github/scripts/update_readme.py` — do not edit the TOC markers between `<!-- TOC:START -->` and `<!-- TOC:END -->` by hand) plus 두 개의 서브패키지 `Concepts/`(개념 정리)와 `QnA/`(질문/답변)가 있고, 같은 주제는 두 폴더에 **동일한 파일명**으로 나란히 존재한다 (예: `Spring/Concepts/01-spring-overview.md` ↔ `Spring/QnA/01-spring-overview.md`). 아래 "주제 매핑표"는 로드맵과 `Concepts/` 쪽 대상 파일을 정리한 것이다.

## 일일 학습 정리 워크플로우

사용자가 그날 공부한 **주제 이름만** 말하면 (예: "객체지향 프로그래밍의 이해"), 아래 절차를 따른다.

1. 원본 자료는 노션에서 export한 마크다운 뭉치이며, `C:\Users\육선우\notion-export\`에 압축 해제되어 있다 (git 저장소 밖의 영속 경로 — 이 폴더는 커밋하지 않는다). 구조는 폴더 계층 없이 **평평하게(flat)** 278개의 `.md` 페이지와 이미지 파일들이 한 폴더에 들어있고, 파일명은 `{노션 페이지 제목} {32자리 hex}.md` 형식이다.
2. 사용자가 말한 주제명으로 아래 "주제 매핑표"에서 노션 원본 파일(제목 접두어로 검색, hex suffix는 무시)과 이 저장소의 대상 파일을 찾는다. 매핑표에 없는 세부 주제라면 `C:\Users\육선우\notion-export\`에서 제목이 일치하는 파일을 직접 찾는다.
3. 원본 페이지 안에 다른 페이지로 연결된 마크다운 링크(같은 폴더 내 다른 `.md` 파일, 역시 `{제목} {hex}.md` 형식)가 있으면, 그 하위 페이지들도 함께 읽어서 전체 내용을 파악한다 (하위 페이지가 많은 주제가 많으므로 빠짐없이 따라간다).
4. 읽은 내용을 핵심 위주로 요약해서, 대상 `{Subject}/Concepts/{topic}.md` 파일의 `## 개념 정리` 섹션에 정리해 넣는다. 기존에 있던 플레이스홀더 주석은 실제 내용으로 교체한다. 짝이 되는 `{Subject}/QnA/{topic}.md` 파일은 건드리지 않고 비워둔다 (사용자가 나중에 질문하면 그때 채운다).
5. 노션 export가 갱신되어 새 zip을 받으면: 이중 zip 구조라 바깥 zip을 풀면 안에 `ExportBlock-*-Part-1.zip`이 또 있다. 한글 파일명이 깨지므로 `unzip`(Bash) 대신 PowerShell `Expand-Archive`로 두 단계 모두 풀어서 같은 `C:\Users\육선우\notion-export\` 경로에 덮어쓴다.

## Q&A 정리 워크플로우

사용자가 채팅에서 학습 내용에 대해 질문하면 (예: "OS가 정확히 뭐지?"), 아래 절차를 따른다.

1. 먼저 **사용자가 현재 IntelliJ에서 보고 있는 파일**을 확인한다(`mcp__idea__get_all_open_file_paths`의 `activeFilePath`). 질문 내용과는 무관하게 이 활성 파일이 기준이다. (열린 파일이 `.md`가 아니거나 확인이 안 되면 사용자에게 어느 파일인지 물어본다.)
2. 기록 대상은 활성 파일 자체가 아니라 **`QnA/` 폴더에 있는, 같은 파일명을 가진 짝 파일**이다: 활성 파일이 `{Subject}/Concepts/{topic}.md`면 `{Subject}/QnA/{topic}.md`에 기록하고, 활성 파일이 이미 `{Subject}/QnA/{topic}.md`면 그 파일 자체에 기록한다. 짝 파일이 없으면(구조가 아직 분리 안 된 옛 파일 등) 만들어서 쓴다.
3. 채팅에서 질문에 답변한다.
4. 새 질문은 기본적으로 **직전 `### Qn.` 항목 안에** 이어지는 후속 질문(같은 주제를 파고드는 질문)으로 취급해서, 그 항목 밑에 `**Q. {질문 원문}**` / 답변 쌍으로 추가한다. 사용자가 화제를 바꾸거나 새 주제로 명시적으로 넘어가면 그때 `### Qn+1.`로 새 번호를 만든다 (n은 그 `QnA/` 파일에서 가장 큰 기존 번호 + 1). 플레이스홀더 주석 `<!-- 다시 읽으면서... -->`이 남아있다면 첫 등록 시 지운다. 기존 Q&A 항목은 건드리지 않는다.

   ```
   ### Qn. {그 항목을 관통하는 주제 요약}

   **Q. {질문 원문}**
   {답변}

   **Q. {후속 질문 원문}**
   {답변}
   ```

   사용자가 여러 개의 개별 Q&A 항목을 하나의 번호로 묶어달라고 요청하면, 그 항목들을 위 형식으로 합쳐서 하나의 `### Qn.`으로 재구성한다.

## 주제 매핑표 (로드맵 순서)

| 사용자가 말할 주제명 | 노션 원본 파일(제목) | 정리 대상 파일 |
|---|---|---|
| Java 프로그래밍 시작하기 | `Java 프로그래밍 시작하기` | `Java/Concepts/01-java-programming-start.md` |
| 객체지향 프로그래밍의 이해 | `객체지향 프로그래밍의 이해` | `Java/Concepts/02-oop.md` |
| 컬렉션 프레임워크와 Stream API | `컬렉션 프레임워크와 Stream API` | `Java/Concepts/03-collections-stream.md` |
| 알고리즘과 자료구조 이해하기 | `알고리즘과 자료구조 이해하기` | `Java/Concepts/04-algorithm-datastructure.md` |
| Java 비동기 처리하기 | `Java 비동기 처리하기` | `Java/Concepts/05-java-async.md` |
| Spring 오버뷰 | `Spring 오버뷰` | `Spring/Concepts/01-spring-overview.md` |
| Spring Boot: 코드 레벨 아키텍처 | `Spring Boot 코드 레벨 아키텍처` | `Spring/Concepts/02-spring-boot-architecture.md` |
| Spring Beans의 이해와 사용 | `Spring Beans의 이해와 사용` | `Spring/Concepts/03-spring-beans.md` |
| Spring MVC: 비지니스 로직 | `Spring MVC 비지니스 로직` | `Spring/Concepts/04-spring-mvc.md` |
| 좋은 웹 API 디자인이란? | `좋은 웹 API 디자인이란` | `Spring/Concepts/05-web-api-design.md` |
| SQL 이해하기 | `SQL 이해하기` | `Database/Concepts/01-sql.md` |
| 데이터베이스 설계 | `데이터베이스 설계` | `Database/Concepts/02-db-design.md` |
| Spring Data JPA 도입하기 | `Spring Data JPA 도입하기` | `Database/Concepts/03-spring-data-jpa.md` |
| Spring Transaction 의 이해 | `Spring Transaction 의 이해` | `Database/Concepts/04-spring-transaction.md` |
| Spring 안정성 높이기 | `Spring 안정성 높이기` | `Spring/Concepts/06-spring-reliability.md` |
| Spring Cache | `Spring Cache` | `Spring/Concepts/07-spring-cache.md` |
| Spring Security 기본기 | `Spring Security 기본기` | `Spring/Concepts/08-spring-security-basics.md` |
| Spring Security - 쿠키/세션 기반 인증/인가 | `Spring Security - 쿠키 세션 기반 인증 인가` | `Spring/Concepts/09-spring-security-session-auth.md` |
| 유저 관리 기능 | `유저 관리 기능` | `Spring/Concepts/10-user-management.md` |
| Docker: 빌드, 배포, 컨테이너 실행하기 | `Docker 빌드, 배포, 컨테이너 실행하기` | `Infra/Concepts/01-docker.md` |
| AWS: 계정 생성부터 ECS, S3, RDS 설정 | `AWS 계정 생성부터 ECS, S3, RDS 설정` | `Infra/Concepts/02-aws-setup.md` |
| AWS ECS 로 프로그램 배포하기 | `AWS ECS 로 프로그램 배포하기` | `Infra/Concepts/03-aws-ecs-deploy.md` |
| 백엔드 통신 디자인 패턴 | `백엔드 통신 디자인 패턴` | `Network/Concepts/01-backend-communication-patterns.md` |
| 프로토콜과 HTTPS 이해하기 | `프로토콜과 HTTPS 이해하기` | `Network/Concepts/02-protocol-https.md` |
| 프록시 및 부하 분산기 | `프록시 및 부하 분산기` | `Network/Concepts/03-proxy-load-balancer.md` |
