---
name: design-system-extract
description: 기존 잘 만든 덱(PPTX/PDF)에서 ALT 통일 디자인 시스템을 추출해 tokens.yaml 과 claude-design-brief.md 를 만들거나 갱신한다. 브랜드 색·폰트·레이아웃 기준을 처음 정하거나 업데이트할 때 사용.
---

# design-system-extract

기준이 될 우수 덱에서 ALT 통일 디자인 시스템을 뽑아 자산화한다.

## 언제 쓰나
- 디자인 시스템을 처음 만들 때 (참조 덱 1~2개에서 추출)
- 브랜드가 바뀌어 토큰/브리프를 갱신할 때

## 절차
1. 참조 덱을 확보한다 (Google Drive MCP 또는 로컬 업로드). PPTX가 이상적이고,
   PDF/Keynote-export도 가능.
2. 추출 실행:
   ```bash
   python -m src.extract <참조덱> --out out/reference
   ```
   `out/reference/deck.json` 과 `out/reference/assets/`(이미지) 생성.
3. 이미지·표지 슬라이드를 보고 색/폰트/여백/레이아웃을 판단해
   `design-system/tokens.yaml` 을 채운다. 로고·대표 참조 이미지는
   `design-system/assets/` 로 복사한다.
4. `tokens.yaml` 확정값을 `design-system/claude-design-brief.md` 에 반영한다
   (이 브리프가 Claude Design에 붙여넣는 실제 통일 장치).
5. 육안 검증: 브리프 규칙이 참조 덱의 실제 스타일과 일치하는지 확인.

## 산출물
- `design-system/tokens.yaml` — 기계가 읽는 토큰
- `design-system/claude-design-brief.md` — Claude Design용 브랜드 브리프
- `design-system/assets/` — 로고·참조 이미지

## 주의
- 색은 실제 슬라이드에서 스포이드로 확인한 값을 우선한다(자리표시 값 교체).
- Keynote(.key)는 직접 못 읽으니 Keynote에서 PDF로 export 후 사용.
