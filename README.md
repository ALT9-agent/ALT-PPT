# ALT-PPT — 통일 디자인 PPT 제작 에이전트

컨설팅 자료를 **통일된 디자인**으로 만드는 에이전트입니다. 대표님은 **Claude 앱 +
Claude Design** 에서 생성·편집하고, 이 레포는 그 뒤를 받쳐주는 **입력 추출 · 브랜드
자산 · 재사용 스킬** 을 제공합니다.

- **입력**: PPTX · PDF · Keynote(→PDF export) — 이미지 다수 지원
- **편집**: Claude Design 캔버스 안에서
- **최종 출력**: **PDF** 로 통일

## 왜 이런 구조인가
Claude Design은 브랜드 템플릿 파일 업로드 강제나 공개 API 자동화를 지원하지 않습니다.
그래서 통일감은 **재사용 브랜드 브리프 + 정밀한 슬라이드 명세 + 이미지 번들**로
유도하고, 이질적 입력 파싱/이미지 추출은 로컬 파이썬(python-pptx·PyMuPDF)이 맡습니다.

## 두 가지 워크플로우

### 트랙 A — 기존 자료 재생성 (`ppt-regenerate` 스킬)
```bash
python -m src.extract <원본.pptx|원본.pdf> --out out/deckA   # 추출
python -m src.design_brief out/deckA                          # Claude Design 패키지
```
→ `out/deckA/claude-design-package/prompt.md` 를 Claude Design에 붙여넣고
`images/` 첨부 → 편집 → **PDF export**.

### 트랙 B — 신규 기획안 → 덱 (`ppt-from-plan` 스킬)
기획안을 슬라이드 콘텐츠 모델(`deck.json`)로 구조화 → `src.design_brief` 로 패키지
생성 → Claude Design → PDF. (상세: `.claude/skills/ppt-from-plan/SKILL.md`)

### 사전 준비 — 디자인 시스템 (`design-system-extract` 스킬)
기존 우수 덱에서 `design-system/tokens.yaml` 과 `claude-design-brief.md` 를 채웁니다.

## 구성
```
design-system/     # tokens.yaml, claude-design-brief.md, assets/  (브랜드 자산)
src/               # content_model.py, extract.py, design_brief.py (파이프라인)
.claude/skills/    # design-system-extract, ppt-regenerate, ppt-from-plan
.claude/hooks/     # session-start.sh (웹 세션 의존성 설치)
out/               # 실행 산출물 (git 제외)
```

## 로컬 실행 준비
```bash
python3 -m pip install -r requirements.txt
export PYTHONPATH=.
```
웹 세션에서는 `.claude/hooks/session-start.sh` 가 자동으로 설치합니다.

## Keynote 처리
`.key` 는 직접 읽지 않습니다. Keynote에서 **PDF로 export** 후 그 PDF를 입력으로
주세요 (최종 출력도 PDF라 자연스럽습니다).

## 현재 범위 / 다음 단계
- 1차: 추출 엔진 + 디자인 시스템 자산 + Claude Design 패키지 생성 + 샘플 리허설
- 다음: 트랙 B 자동화 고도화, 배치 처리, diff/품질 리포트, (선택) python-pptx→PDF
  결정적 백업 경로
