# Repository Guidelines

## Project Structure & Module Organization
`app.py` is the Streamlit entry point; it loads the freshest CSV from `data/` and renders all charts inline for fast iteration. `crawl_data.py` scrapes the 경기도교육청 portal, normalizes 국립/공립/사립 columns, and saves timestamped files such as `data/20221102.csv`. Keep raw datasets under `data/`, exploratory notes in `221027_노트_안산시 학교현황 시각화하기.ipynb`, and pin third-party deps in `requirements.txt`. Use `readme.md` for roadmap items so the root stays minimal.

## Build, Test, and Development Commands
- `python -m venv .venv && source .venv/bin/activate`: create/enter an isolated interpreter.
- `pip install -r requirements.txt`: install Streamlit, Plotly, pandas, and friends.
- `python crawl_data.py`: regenerate the CSV snapshot; run before demoing numbers.
- `streamlit run app.py`: start the dashboard; append `--server.headless true` on servers.

## Coding Style & Naming Conventions
Stick to PEP 8, 4 spaces, and `lowercase_with_underscores` for functions plus ALL_CAPS for simple constants (e.g., `DATE`). Group imports as stdlib / third-party / local, and keep Streamlit widgets near the chart logic they control. Use docstrings when helpers do more than one transform, and keep Korean chart labels consistent with the dataset headers.

## Testing Guidelines
There is no automated suite yet. Add pytest-based modules under `tests/test_<feature>.py` for any new data munging—assert type conversions and ordering. For UI changes, rely on manual verification via `streamlit run app.py`, confirm the sidebar defaults to the newest CSV, and capture screenshots for major visual shifts. Include regression notes in PRs until formal tests exist.

## Commit & Pull Request Guidelines
History shows concise subjects like `Update : 그래프 타이틀 입력`; continue using imperative verbs plus a short Korean or English context. Keep commits scoped to one concern (scraper, visualization, refactor). Pull requests should cover purpose, bullet list of changes, reproduction steps (`streamlit run app.py`), and before/after visuals when plots change. Reference related issues or notebooks so reviewers can trace assumptions quickly.

## Improvement Tracking Workflow
모든 개선 요구사항은 `DOC/251109_개선사항.md`에 날짜와 구체적 작업으로 누가기록한다. 코딩 작업을 완료한 뒤에는 결과와 확인 방법을 `DOC/251109_개선완료_LOG.md`에 같은 날짜/항목 명으로 적어 트레이싱이 가능하도록 한다. 문서는 Markdown 리스트나 테이블 어떤 형식이든 일관성만 유지하면 되며, PR 설명에서 해당 로그 라인을 참조해 리뷰어가 변경 내역을 쉽게 찾게 한다.

## Data & Configuration Tips
Version CSV snapshots so reviewers can reproduce charts, but prune obsolete files when a newer scrape lands to keep the repo lean. The scraper targets a public endpoint, so never embed credentials and consider adding simple throttling if request volume grows. When deploying, manage Streamlit secrets outside the repo and set `STREAMLIT_SERVER_PORT` when hosting on managed platforms.
