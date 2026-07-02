---
name: ppt-from-plan
description: 텍스트 기반 기획안(Notion/Drive/채팅)을 슬라이드 아웃라인과 슬라이드별 콘텐츠 모델로 구조화한 뒤, ALT 브랜드 브리프를 입힌 Claude Design 프롬프트를 만들어 신규 덱을 생성한다. 최종 출력은 PDF.
---

# ppt-from-plan (트랙 B)

텍스트 기획안을 Claude Design용 슬라이드 프롬프트로 변환한다.

## 사전 조건
- `design-system/claude-design-brief.md` 준비 (없으면 `design-system-extract` 먼저).

## 절차
1. 기획안 수집 (Notion MCP / Google Drive MCP / 채팅 붙여넣기).
2. **프롬프트 변환(핵심)**: 기획안을 슬라이드 단위로 구조화한다. 각 슬라이드에 대해
   `src/content_model.py` 의 `Slide` 형태(제목·bullets·layout_hint·표·이미지 슬롯)를
   따르는 `deck.json` 을 만든다. 아웃라인 → 슬라이드 매핑은 Claude가 내용 의미를 보고
   결정한다. 결과를 `out/<이름>/deck.json` 으로 저장한다.
   (스키마 참고: `Deck { slides: [Slide{index,title,bullets,layout_hint,...}] }`)
3. 사용할 이미지가 있으면 `out/<이름>/assets/` 에 넣고 `deck.json` 의
   해당 슬라이드 `images` 에 참조를 추가한다.
4. Claude Design 패키지 생성:
   ```bash
   python -m src.design_brief out/<이름>
   ```
5. `prompt.md` 를 Claude Design/앱에 붙여넣어 시안 생성·편집 → **PDF export**.

## 산출물
- `out/<이름>/deck.json` — 구조화된 슬라이드 콘텐츠 모델
- `out/<이름>/claude-design-package/prompt.md` (+ images/)
- (대표님 단계) Claude Design → PDF

## 팁
- 슬라이드 수는 기획안 분량에 맞추되 "한 슬라이드 한 메시지" 원칙 유지.
- 데이터가 있으면 `layout_hint: chart` / `table` 로 지정해 브리프의 차트 규칙 유도.
