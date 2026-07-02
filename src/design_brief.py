"""Turn an extracted deck (or a structured plan) into a Claude Design-ready
package: one paste-in prompt plus a curated image bundle.

Because Claude Design has no API and cannot import a brand template, brand
consistency is driven by (a) a reusable brand brief and (b) a precise per-slide
content spec. The CEO pastes prompt.md into Claude Design and attaches the images
from the package's images/ folder, then edits on the canvas and exports to PDF.

Usage:
    python -m src.design_brief DECK_DIR [--brief design-system/claude-design-brief.md] [--out DIR]

DECK_DIR is the folder produced by src.extract (contains deck.json + assets/).
"""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from .content_model import Deck, Slide

DEFAULT_BRIEF = Path("design-system/claude-design-brief.md")


def _slide_block(s: Slide, img_names: dict[str, str]) -> str:
    lines = [f"### Slide {s.index + 1} — layout: {s.layout_hint.value}"]
    if s.title:
        lines.append(f"- **Title:** {s.title}")
    if s.subtitle:
        lines.append(f"- **Subtitle:** {s.subtitle}")
    for b in s.bullets:
        indent = "  " * b.level
        lines.append(f"{indent}- {b.text}")
    for t in s.tables:
        if not t.rows:
            continue
        lines.append("- **Table:**")
        header = " | ".join(t.rows[0])
        lines.append(f"  | {header} |")
        lines.append("  | " + " | ".join(["---"] * len(t.rows[0])) + " |")
        for row in t.rows[1:]:
            lines.append("  | " + " | ".join(row) + " |")
    content_imgs = [i for i in s.images if i.role == "content"]
    if content_imgs:
        names = ", ".join(img_names.get(i.id, i.path) for i in content_imgs)
        lines.append(f"- **Images (attach these):** {names}")
    if s.notes:
        lines.append(f"- **Speaker notes:** {s.notes}")
    return "\n".join(lines)


def build_package(deck_dir: Path, brief_path: Path, out: Path) -> Deck:
    deck = Deck.model_validate_json((deck_dir / "deck.json").read_text("utf-8"))
    brief = (
        brief_path.read_text("utf-8")
        if brief_path.exists()
        else "> (브랜드 브리프 없음: design-system/claude-design-brief.md 를 먼저 만드세요)"
    )

    images_out = out / "images"
    images_out.mkdir(parents=True, exist_ok=True)

    # Copy only content images (skip repeated logos/chrome), keep stable names.
    img_names: dict[str, str] = {}
    for s in deck.slides:
        for img in s.images:
            if img.role != "content":
                continue
            src = deck_dir / img.path
            if not src.exists():
                continue
            name = f"s{s.index + 1:02d}_{Path(img.path).name}"
            shutil.copy2(src, images_out / name)
            img_names[img.id] = name

    body = "\n\n".join(_slide_block(s, img_names) for s in deck.slides)
    n_content_imgs = len(img_names)

    prompt = f"""# Claude Design 지시 프롬프트 — {deck.title or deck.source_path}

아래 **브랜드 시스템**을 반드시 지켜 프레젠테이션을 제작해줘. 각 슬라이드의
내용·레이아웃은 뒤의 **슬라이드 명세**를 따르고, 표시된 이미지는 이 패키지의
`images/` 폴더 파일을 첨부해 사용해줘. 완료 후 **PDF로 export**할 예정이야.

---

## 브랜드 시스템 (통일 서식)

{brief}

---

## 슬라이드 명세 ({deck.slide_count}장, 이미지 {n_content_imgs}개)

{body}

---

## 제작 규칙
- 위 브랜드 시스템의 색·폰트·여백·레이아웃 규칙을 **모든 슬라이드에 일관 적용**.
- 슬라이드별 `layout` 힌트를 우선 존중하되, 내용에 더 맞는 브랜드 레이아웃이 있으면 조정.
- 이미지는 원본 비율을 유지하고 임의 왜곡/크롭 금지.
- 텍스트는 위 명세를 의미 손실 없이 사용하되, 브랜드 톤에 맞게 다듬어도 됨.
- 최종 산출물은 PDF export 기준으로 가독성/정렬을 최적화.
"""
    out.mkdir(parents=True, exist_ok=True)
    (out / "prompt.md").write_text(prompt, encoding="utf-8")
    (out / "images_manifest.json").write_text(
        json.dumps(img_names, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return deck


def main() -> None:
    ap = argparse.ArgumentParser(description="Build a Claude Design package from an extracted deck")
    ap.add_argument("deck_dir", type=Path, help="folder from src.extract (has deck.json)")
    ap.add_argument("--brief", type=Path, default=DEFAULT_BRIEF)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    out = args.out or (args.deck_dir / "claude-design-package")
    deck = build_package(args.deck_dir, args.brief, out)
    n = len(list((out / "images").glob("*")))
    print(
        f"[design_brief] {deck.slide_count} slides · {n} images bundled → "
        f"{out}/prompt.md  (+ images/)"
    )


if __name__ == "__main__":
    main()
