---
name: ppt-regenerate
description: 기존 자료(PPTX/PDF/PDF로 export한 Keynote)를 ALT 통일 디자인으로 재생성한다. 원본에서 텍스트·이미지·표를 추출하고, Claude Design에 바로 넣을 프롬프트 + 이미지 번들을 만들어 통일 서식으로 다시 만들 수 있게 한다. 최종 출력은 PDF.
---

# ppt-regenerate (트랙 A)

기존 덱을 통일 디자인 시스템으로 재생성하기 위한 준비물을 만든다.

## 사전 조건
- `design-system/claude-design-brief.md` 가 준비돼 있어야 한다
  (없으면 먼저 `design-system-extract` 스킬 실행).

## 절차
1. 원본 확보 (Google Drive MCP 또는 로컬). Keynote는 PDF로 export 후 사용.
2. 추출:
   ```bash
   python -m src.extract <원본파일> --out out/<이름>
   ```
   → `deck.json`(콘텐츠 모델) + `assets/`(원본 해상도 이미지)
3. Claude Design 패키지 생성:
   ```bash
   python -m src.design_brief out/<이름>
   ```
   → `out/<이름>/claude-design-package/prompt.md` + `images/`
4. `prompt.md` 를 Claude Design(또는 Claude 앱)에 붙여넣고, `images/` 폴더
   이미지를 첨부한다.
5. Claude Design 캔버스에서 편집·통일한 뒤 **PDF로 export** = 최종 산출물.

## 산출물
- `out/<이름>/claude-design-package/prompt.md` — 붙여넣기용 프롬프트
- `.../images/` — 슬라이드별 콘텐츠 이미지
- (대표님 단계) Claude Design → PDF

## 팁
- `deck.json` 의 `layout_hint` 가 어색하면 수정 후 3단계를 다시 실행.
- 반복되는 로고/배경은 자동으로 `role: logo` 처리되어 콘텐츠 이미지에서 제외됨.
