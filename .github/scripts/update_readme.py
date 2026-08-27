#!/usr/bin/env python3
"""패키지(폴더) 구조를 읽어 최상단 README.md의 목차를 갱신한다.

하는 일
1. 최상단부터 모든 패키지(폴더)를 재귀 탐색한다.
2. 문서 작업용 파일이 없는 패키지에는 README.md를 템플릿으로 만들어 준다.
3. 패키지/문서 트리를 만들어 README.md의 TOC 마커 사이 내용만 교체한다.

문서 제목은 md 파일의 첫 `# 헤딩`을 쓰고, 없으면 파일명을 쓴다.
"""

from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[2]
README = ROOT / "README.md"

START = "<!-- TOC:START -->"
END = "<!-- TOC:END -->"

# 목차에서 제외할 폴더 이름 (`.`으로 시작하는 폴더는 자동 제외)
EXCLUDE_DIRS = {"node_modules", "assets", "images", "img", "scripts", "venv", "__pycache__"}

PACKAGE_DOC = "README.md"

TEMPLATE = """# {name}

> {name} 학습 기록

## 📝 Notes

<!-- 이 파일에 자유롭게 정리하세요.
     문서를 여러 개로 나누고 싶다면 이 폴더에 새 .md 파일을 추가하면
     최상단 README.md 목차에 자동으로 반영됩니다. -->
"""


def doc_title(md_path: Path) -> str:
    """md 파일의 첫 번째 h1 헤딩을 제목으로 사용한다."""
    try:
        with md_path.open(encoding="utf-8") as f:
            for line in f:
                stripped = line.strip()
                if stripped.startswith("# "):
                    return stripped[2:].strip()
    except (OSError, UnicodeDecodeError):
        pass
    return md_path.stem.replace("_", " ")


def link(path: Path) -> str:
    return "./" + quote(path.relative_to(ROOT).as_posix())


def by_name(paths):
    return sorted(paths, key=lambda p: p.name.lower())


def ensure_package_doc(package: Path) -> Path:
    """패키지 안에 문서 작업용 md 파일이 없으면 템플릿으로 만들어 준다."""
    doc = package / PACKAGE_DOC
    if not doc.exists():
        doc.write_text(TEMPLATE.format(name=package.name), encoding="utf-8")
        print(f"created {doc.relative_to(ROOT).as_posix()}")
    return doc


def render(directory: Path, depth: int, lines: list[str], docs: list[Path]) -> None:
    indent = "  " * depth
    children = list(directory.iterdir())

    md_files = by_name(
        p
        for p in children
        if p.is_file() and p.suffix.lower() == ".md" and p.name != PACKAGE_DOC
    )
    packages = by_name(
        p
        for p in children
        if p.is_dir() and not p.name.startswith(".") and p.name not in EXCLUDE_DIRS
    )

    for md in md_files:
        lines.append(f"{indent}- [{doc_title(md)}]({link(md)})")
        docs.append(md)

    for package in packages:
        doc = ensure_package_doc(package)
        lines.append(f"{indent}- 📁 **[{package.name}]({link(doc)})**")
        docs.append(doc)
        render(package, depth + 1, lines, docs)


def build_toc() -> str:
    lines: list[str] = []
    docs: list[Path] = []
    render(ROOT, 0, lines, docs)

    if not lines:
        return "_아직 추가된 패키지가 없습니다._"

    lines.append("")
    lines.append(f"> 총 {len(docs)}개의 문서")
    return "\n".join(lines).strip()


def main() -> None:
    content = README.read_text(encoding="utf-8")

    if START not in content or END not in content:
        raise SystemExit(
            f"README.md에 목차 마커가 없습니다. 다음 두 줄을 추가하세요:\n{START}\n{END}"
        )

    head, rest = content.split(START, 1)
    _, tail = rest.split(END, 1)

    updated = f"{head}{START}\n\n{build_toc()}\n\n{END}{tail}"

    if updated == content:
        print("목차 변경 사항 없음")
        return

    README.write_text(updated, encoding="utf-8")
    print("README.md 목차를 갱신했습니다")


if __name__ == "__main__":
    main()
