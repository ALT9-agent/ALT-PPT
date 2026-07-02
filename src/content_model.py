"""Neutral slide content model shared across the ALT-PPT pipeline.

Every input format (PPTX / PDF / PDF-exported Keynote) is parsed into this
format-agnostic model. Downstream steps — Claude Design brief generation and any
optional deterministic rendering — consume the model instead of the original
file, so content and brand rules stay decoupled from the source format.
"""
from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class LayoutHint(str, Enum):
    """Design-system layout families. Extraction guesses one per slide; a human
    or Claude can override before the deck is rebuilt in Claude Design."""

    TITLE = "title"            # 표지
    SECTION = "section"        # 섹션 구분
    CONTENT = "content"        # 제목 + 본문
    TWO_COLUMN = "two_column"  # 2단
    IMAGE_TEXT = "image_text"  # 이미지 + 텍스트
    IMAGE_FULL = "image_full"  # 전면 이미지
    CHART = "chart"            # 차트
    TABLE = "table"            # 데이터 표
    QUOTE = "quote"            # 인용 / 강조
    UNKNOWN = "unknown"


class BulletItem(BaseModel):
    text: str
    level: int = 0             # 0 = top level, 1+ = nested


class ImageRef(BaseModel):
    id: str
    path: str                  # path relative to the deck's asset bundle
    width: Optional[int] = None   # original pixel width
    height: Optional[int] = None  # original pixel height
    sha1: Optional[str] = None    # content hash, used to detect repeated chrome
    role: str = "content"      # content | logo | background | icon | chart
    alt: str = ""


class Table(BaseModel):
    rows: list[list[str]] = Field(default_factory=list)


class Slide(BaseModel):
    index: int
    layout_hint: LayoutHint = LayoutHint.UNKNOWN
    title: str = ""
    subtitle: str = ""
    bullets: list[BulletItem] = Field(default_factory=list)
    images: list[ImageRef] = Field(default_factory=list)
    tables: list[Table] = Field(default_factory=list)
    notes: str = ""
    raw_text: str = ""         # everything, for fallback / search


class Deck(BaseModel):
    """Format-agnostic representation of a source deck."""

    title: str = ""
    source_path: str = ""
    source_format: str = ""    # pptx | pdf | keynote-pdf
    slide_count: int = 0
    slides: list[Slide] = Field(default_factory=list)

    def dedupe_images(self) -> None:
        """Drop repeated logos/backgrounds that appear on most slides so the
        Claude Design brief keeps content images and treats chrome separately."""
        from collections import Counter

        counts: Counter[str] = Counter()
        for s in self.slides:
            for img in s.images:
                counts[_img_key(img)] += 1
        threshold = max(3, int(0.6 * max(self.slide_count, 1)))
        for s in self.slides:
            for img in s.images:
                if counts[_img_key(img)] >= threshold and img.role == "content":
                    img.role = "logo"


def _img_key(img: ImageRef) -> str:
    return img.sha1 or f"{img.width}x{img.height}"
