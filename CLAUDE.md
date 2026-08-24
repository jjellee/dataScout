# CLAUDE.md — dataScout 프로젝트 가이드

## 프로젝트 개요

**dataScout**는 한국·미국·일본 시장의 **주가·수급·공시·무역·산업 뉴스** 데이터를 자동 수집하여
차트/엑셀로 가공한 뒤 **텔레그램으로 리포트**하는 데이터 파이프라인입니다.

- 대부분의 스크립트는 `crontab`으로 예약 실행됩니다.
- 파이썬 인터프리터는 별도 가상환경을 사용합니다:
  `/home/inhyuk/projects/ExportImportAutomation/venv/bin/python`
- 환경변수(API 키, 텔레그램 토큰 등)는 프로젝트 루트의 `.env` 파일에서 로드합니다.
- 시장별 산출물(CSV·엑셀·차트·로그)은 `data_kr/`, `data_us/`, `data_dart/`, `data_jp/`, `data_blog/`에 저장됩니다.

---

## 실행 오케스트레이션

| 스크립트 | 실행 시점 | 하는 일 |
|----------|-----------|---------|
| `run_daily.sh` | 평일 20:30 (한국 장 개장일에만) | 수급 수집 → 차트 → 스크리너 → 내부자 → 일본 수출 → **Git 커밋/푸시** |
| `run_dart_periodic.sh` | 평일 12 / 15:30 / 21시 | DART 공시 수집 + 분류 엑셀 생성/업로드 |
| `crontab` | 각 주기별 | 위 스크립트 및 개별 모니터를 예약 실행 (15~30분 주기 크롤러 포함) |

> `run_daily.sh`는 삼성전자(005930) 최신 거래일을 확인해 **휴장일/주말이면 스킵**합니다.

---

## 🇰🇷 한국 주식 수급·스크리닝

| 파일 | 역할 |
|------|------|
| `collector.py` | pykrx로 **하루치** KRX 데이터(전 종목·섹터별 투자자 매매동향, 지수, 매크로 지표)를 `data_kr/<날짜>/`에 CSV 저장 — 단일 일자 수집기 |
| `batch_collector.py` | 삼성전자 거래일 기준 과거 N개월 거래일을 뽑아 날짜마다 `collector.py`를 subprocess로 반복 실행하는 배치 래퍼 (수집 완료 날짜는 건너뜀) |
| `historical_collector.py` | DART OpenAPI에서 지정 날짜 공시 리스트를 페이지네이션하며 조회하는 과거 공시 수집기 |
| `screener.py` | `data_kr` CSV를 6가지 룰(쌍끌이 매수, 연기금·투신 순매수 누적, 개인 손절, 신고가 돌파, 낙폭과대 스마트머니 유입 등)로 종목 선별·발송 |
| `telegram_reporter.py` | `watchlist.txt` 종목별 누적 매매동향 차트 + 뉴스 헤드라인을 Telethon으로 이미지 업로드 — **실행 중지(2026-07-29 사용자 요청, `run_daily.sh` Step 2 주석 처리)** |
| `telegram_sender.py` | requests로 텔레그램 봇 API에 마크다운 텍스트를 보내는 경량 발송기 |
| `kosdaq_bio_monitor.py` | 코스닥 제약·바이오 업종의 투자자별 누적 순매수 차트 생성·전송 |

---

## 📄 한국 DART 공시

| 파일 | 역할 |
|------|------|
| `dart_collector.py` | DART OpenAPI로 일일 공시 목록을 받아 중요 공시 원문(XML→HTML)을 다운로드 |
| `dart_classifier.py` | 저장된 공시를 유형별(증자·메자닌·계약·자기주식·5%·임원)로 분류해 서식 엑셀 생성·전송 |
| `dart_officer_parser.py` | 임원·주요주주 소유상황보고서 / 5% 대량보유 공시 HTML에서 거래 내역 파싱 (헬퍼 모듈) |
| `kr_insider_collector.py` | 내부자·5% 대량보유 공시를 수집, pykrx 종가와 결합해 누적 엑셀 저장·전송 |
| `download_important_historical.py` | 2023년~현재 과거 중요 공시를 API 키 로테이션으로 대량 백필 다운로드 |
| `dart_report.py` | 공시 HTML 리포트 — 파싱된 상세(조달금액·옵션일·계약상대 등) 인라인 포함, 일일 전체공시(평일 21:40) / 주간 중요공시(토 09:00) 생성·텔레그램 발송 |
| `krx_disclosure_report.py` | **KIND(거래소) 일일 전체공시** — 목록 수집 + **원문 HTML 전량 다운로드** + 분류 리포트. DART에 없는 거래소 고유 공시(매매거래정지·관리종목/상장폐지·조회공시·불성실공시·투자경고/과열·상장안내)까지 전량 수록. **거래소 발행분(제출인=시장본부·시장감시위원회)은 원문 전문을 리포트에 접이식으로 인라인**하고, 지정 5종 시장통계(자기주식매매 신청·체결내역, 대량매매내역, 최근20일 상승/하락율 상위10, 직전1개월 대비 거래량 증가율 상위10)는 **표를 그대로 펼쳐서 표시**(`시장통계` 카테고리, 기본 펼침). 목록 `data_krx/<YYYYMMDD>/disclosures.json` · 원문 `data_krx/<YYYYMMDD>/docs/<접수번호>.html`. **DART와 동일한 2축 보고**: 평일 22:00 일일 전체공시(`--daily`) + 토 09:10 **주간 시장조치 리포트**(`--weekly` — 월~토 저장분에서 조회공시·매매거래정지·관리종목/상장폐지·불성실공시·시장경보·상장안내 등 거래소 조치만 추려 정정공시 dedupe 후 발송, 회사 공시는 DART 주간이 커버) / `--backfill N` 과거분 / `--docs-only` 원문만 / `--no-docs` 목록만. 산출물은 `run_daily.sh`가 매일 git 커밋(원문 `docs/`는 제외) |
| `dart_dividend.py` | **배당 공시 파싱 → 누적 엑셀**(`data_dart/dividend.xlsx`). 현금ㆍ현물배당결정·주식배당결정·주주명부폐쇄(기준일)결정·배당락·리츠 금전배당을 유형별로 표준화. 시트 4개 — **종목별**(한 종목 1행·회차 가로전개) / **공시별**(원장, 미분류 '기타'까지 전량) / **배당추이**(정기보고서 `alotMatter` API 확정치: 주당배당금·배당성향·배당수익률·EPS) / **배당캘린더**(기준일·지급일 임박순). 캐시 `dividend_cache.json`. 평일 21:45 증분(`--daily`) + 매월 1일 05:00 `--alot`. `--backfill FROM TO` 원문 백필 / `--parse` 재파싱 / `--excel` 엑셀만 |
| `quarterly_earnings.py` | 분기 실적 엑셀 — **실적(종목별)**: 한 종목 1행·분기 가로 전개로 잠정(공정공시 파싱)·확정(재무제표 다중회사 API) 통합, 확정치 우선·빈 항목만 잠정치로 보완(주황 배경 표시), 맨 오른쪽에 최신 분기 매출·영업이익 QoQ·YoY 증감률 / **수주잔고**: 한 종목 1행·분기별 잔고 추세. 캐시 누적 (평일 21:35 증분). 잠정실적(공시별) 시트는 2026-08-18 사용자 요청으로 삭제 |
| `periodic_report_saver.py` | 분기·반기·사업보고서 전문을 LLM 분석용 Markdown(`data_dart/periodic/<종목>/<분기>.md`)으로 저장 + 수주상황 표 파싱(`order_backlog_cache.json`) (평일 23:00 증분) |
| `backlog_utils.py` | 수주상황 표 **합계행 판정 공용 모듈**(`is_total_label`/`split_total_rows`) — `"합 계 / -"`·`"(합계)"`·**라벨 없는 합계행**(빈 셀, 나머지 행 합계와 일치)까지 인식. periodic_report_saver·quarterly_earnings·order_backlog_charts가 공유(따로 구현하면 합계행이 품목행에 섞여 잔고 2배 — 2026-08-18 한라IMS 건) |

> ⚠️ **배당 공시 파싱 시 주의 2가지**
> 1. **`(자회사의 주요경영사항)` 공시**는 비상장 자회사의 배당을 모회사 이름으로 냅니다(2026년 233건). 종목별 집계에 섞으면 값이 튑니다(HD현대 중간 11,000원, 하나금융지주 886.26원 등 — 실제 모회사 배당은 1,300원/1,155원). `is_subsidiary()`로 걸러 종목별·캘린더에서 제외하고 원장에는 '자회사' 표시로 남깁니다.
> 2. **결산배당 회계연도**는 배당기준일 연도와 다릅니다. 2024년 배당절차 개선으로 기준일을 주총 뒤(이듬해 1~4월)로 잡는 회사가 절반입니다(2026년 실측: 12월 955건 / 이듬해 1~4월 912건). `period_label()`이 결산배당 기준일이 상반기면 전년도로 되돌립니다.

> ⚠️ **KIND 접수번호(acptno) ≠ DART 접수번호(rcept_no)** — 서로 다른 번호체계입니다.
> 같은 번호가 다른 문서를 가리킵니다(2026-08-21 `20260821000671` = KIND 진에어 매매거래정지 / DART 한울반도체 철회보고서).
> 접수번호로 두 시스템을 대조하거나 DART 원문을 재사용하면 **엉뚱한 공시가 붙습니다**.
> KRX 원문은 반드시 KIND에서 받고, DART 대조는 `(회사명 + 보고서명)`으로 합니다(`_match_key`, 일치율 73%).
> 'DART 미수록 = 거래소 전용' 판정은 번호가 아니라 **제출인**(`is_exchange`)으로 합니다.

---

## 🇺🇸 미국 시장·공시

| 파일 | 역할 |
|------|------|
| `us_market_monitor.py` | S&P500 등락률로 마켓 무버(급등·급락주) 집계해 전송 |
| `us_gainer_analyzer.py` | 미국 전 상장 종목(Nasdaq 스크리너 1회 호출) 등락률 트래킹 → **상승률·거래량 급증·펀더멘털·촉매** 4단 필터로 '비중 실을만한' 종목 선별 → `~/projects/edgar`의 SEC 원문(10-K/10-Q/8-K) **+ `~/projects/sa-transcripts`의 실적콜 transcript**를 함께 LLM에 투입해 종목별 HTML 심층분석 리포트 생성·텔레그램 발송 (화~토 08:50). SEC 원문은 `download_filings.py`로 즉시 수집. transcript는 `manifest.db` 조회 → Drive에서 rclone 복사, 발언 전문이 없으면 sa-transcripts 규칙대로 `run.sh ticker`(발견·우선표시) → `run.sh fetch`(페이싱 유지) 실행 후 재조회(`--sa-fetch-timeout`, 기본 1200초, 0이면 수집 생략 — 미확보 시 우선순위 대기열에 남아 다음 드립이 수집). 같은 종목 재분석은 7일 쿨다운. 발송 채널은 sa-transcripts와 동일(전용 봇 — 토큰·chat_id를 `~/projects/sa-transcripts/secrets.yaml`에서 읽음, `TELEGRAM_SA_BOT_TOKEN`/`TELEGRAM_SA_CHAT_ID`로 재정의 가능). `--chat supply`로 수급데이터 방 전환 |
| `report_html.py` | 공용 HTML 리포트 렌더러 — 마크다운 → 자체 완결형 HTML(라이트/다크 대응, 외부 CSS·폰트 미참조) |
| `us_disclosure_monitor.py` | SEC EDGAR 공시 모니터링 → 한국어 번역 후 알림 |
| `us_disclosure_summary.py` | SEC 공시를 유형별(자금조달·계약·M&A·5%지분·경영진·실적·리스크) 엑셀로 분류·전송 — 시총 $10B+ 및 watchlist, 13D·공개매수·합병은 전 종목 (화~토 12:20) |
| `ipo_monitor.py` | 미국(Nasdaq 캘린더)·한국(38커뮤니케이션) IPO 예정 기업 리포트 — KR은 업종·공모가밴드·주간사, US는 DeepSeek 한줄소개, 스팩 표기/제외 (매주 월 08:30) |
| `download_historical_insiders.py` | SEC Form4 / OpenInsider로 미국 내부자 매매 과거 데이터 수집 |
| `market_indicators.py` | 시장별(`--market US/KR/JP/CN`) 지수·섹터 히트맵·추세 차트 대시보드 — 각국 장마감 후 크론 실행 (US 07:30 / JP 15:50 / KR 16:10 / CN 17:35) |
| `interest_monitor.py` | 관심종목(`interest_watchlist.json`) 주가·뉴스 일일 브리핑 |
| `interest_news.py` | 관심종목을 Google News RSS에서 검색해 뉴스 다이제스트 발송 |

---

## 📰 산업·뉴스 크롤러 (상시, 15~30분 주기)

| 파일 | 역할 |
|------|------|
| `trendforce_monitor.py` | 반도체 조사기관 TrendForce 신규 기사 번역·전송 |
| `dramexchange_scraper.py` | DRAMeXchange DRAM/NAND 현물가를 Selenium으로 스크래핑해 이력 누적 |
| `wallstreetcn_monitor.py` | 월스트리트견문(중국) 기사 DeepSeek 요약·번역 |
| `tech_investing_monitor.py` | Tom's Hardware 전문 번역 + Investing.com 애널리스트 등급 LLM 게이트(`investing_interests.md`, score≥6만 요약+투자함의 발송, 나머지는 17시 다이제스트) |
| `kotra_monitor.py` | KOTRA 해외시장뉴스 신규 기사 DeepSeek 요약 — **크론 중지 상태(2026-07-22 사용자 요청)** |
| `kotra_report_monitor.py` | KOTRA 보고서(PDF) 신규 감지·다운로드·요약 — **크론 중지 상태(2026-07-22 사용자 요청)** |
| `company_blogs_monitor.py` | Nvidia·Google 등 기업 블로그 RSS를 DeepSeek로 번역·게시 |
| `storagereview_monitor.py` | StorageReview 뉴스 RSS 신규 기사 전문 번역·전송 (review·podcast 제외) |
| `semidoped_monitor.py` | Semi Doped 뉴스레터(Substack) 신규 글 전문 번역·전송 (초장문은 18k자 절단) |
| `youtube_channel_monitor.py` | 유튜브 6개 채널(Semi Doped·TechTechPotato·SemiAnalysis·Dwarkesh Patel·Google(I/O·키노트만)·Goldman Sachs(요약+전문)) 새 영상 자막 추출 → Claude(구독 CLI sonnet) → OpenAI(Codex CLI) → DeepSeek 순으로 구조화 정리·전송 |
| `nextplatform_monitor.py` | The Next Platform 신규 포스트 전문 번역·전송 (피드에 본문 없음 → 기사 페이지 curl_cffi 수집) |

---

## 🌏 일본·글로벌 시장

| 파일 | 역할 |
|------|------|
| `fetch_japan_exports.py` | 일본 재무성 무역통계에서 16개 HS코드(MLCC·메모리·InP·포토레지스트 등) 월별 수출 데이터 수집·차트화 |
| `fetch_japan_mlcc.py` | 일본 관세청 MLCC 수출 데이터 수집·차트 (단일 품목) |
| `fetch_osaka_mlcc.py` | Selenium으로 오사카 지역별 MLCC 수출 데이터 크롤링 |
| `global_market_monitor.py` | 미/한/일 시장(`--market` 인자) 섹터·종목 데이터를 엑셀 리포트로 집계 |
| `new_high_monitor.py` | 미/한/일 52주 신고가 종목 탐지·리포트 |

---

## 데이터 폴더

| 폴더 | 내용 |
|------|------|
| `data_kr/` | 날짜별(YYYYMMDD) KRX 투자자 매매동향·매크로 CSV |
| `data_dart/` | 날짜별 DART 공시 원문(HTML) 및 분류 엑셀 |
| `data_us/` | 미국·글로벌 산출물(일별 시세, 지표 차트, dramexchange, 실행 로그) |
| `data_krx/` | 날짜별 KIND 전체공시 JSON + 일일 HTML 리포트 + 원문 `docs/`(하루 약 110MB — **git 제외**, `.gitignore` 참고) |
| `data_jp/` | 일본 수출/부품(MLCC·메모리·ABF 등) 차트 이미지 |
| `data_blog/` | 기업 블로그 크롤링·번역 텍스트 결과 |
| `draw/` | 관심 종목별 누적 매매동향 차트 PNG (`<티커>_cumulative.png`) |

---

## LLM 클라이언트 (`llm_client.py`)

모든 스크립트는 `llm_client.py` 하나만 통해 LLM을 호출합니다.

| 함수 | 경로 | 용도 |
|------|------|------|
| `llm_chat()` (= 기존 이름 `deepseek_chat`) | **`LLM_PROVIDER` 1순위 → 나머지 하나 폴백** | 대량 번역·요약 등 저부가 호출 |
| `smart_chat()` | Claude 구독 CLI → Claude API → `llm_chat()` | 실적 비교분석·강세분석·섹터코멘트 등 고부가 |
| `llm_translate()` | `llm_chat()` 통번역 → 실패 시 호출부가 구글 번역 폴백 | 기사 문단 통번역 |
| `claude_cli_chat()` / `openai_cli_chat()` | Claude Code CLI / Codex CLI (구독 토큰, API 과금 없음) | 유튜브 자막 정리 등 |

저비용 제공자는 `.env`의 `LLM_PROVIDER` 한 줄로 바꿉니다. 1순위가 실패하면 나머지 하나로 자동 폴백합니다.

```
LLM_PROVIDER=deepseek           # 현재 기본. qwen 심사 통과 시 qwen으로 변경
LLM_FALLBACK=1                  # 0이면 1순위 실패 시 폴백 없이 "" 반환

QWEN_API_KEY=sk-ws-...
QWEN_BASE_URL=https://ws-g24qy9e4g4x9k9nq.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1
QWEN_MODEL=qwen3.7-flash        # 최저가 티어. 품질 필요 시 qwen3.7-plus
```

- **2026-08-08**: DeepSeek 가격 인상으로 Qwen(Alibaba Cloud Model Studio) 전환을 준비했으나
  **계정 심사 미통과**(`403 AccessDenied.Unpurchased`)로 보류. 배선은 완료돼 있어 심사 통과 시
  `LLM_PROVIDER=qwen`으로만 바꾸면 됩니다.
- Qwen 엔드포인트는 OpenAI 호환 모드(`/chat/completions`), 리전은 **ap-southeast-1(싱가포르)** 입니다. 중국 본토 엔드포인트에서는 이 키가 인식되지 않습니다.
- 호출부 12개 스크립트는 여전히 `from llm_client import deepseek_chat`을 쓰며, 이는 `llm_chat`의 별칭입니다(제공자 교체 시 호출부 수정 불필요).
- **DeepSeek 잔액 소진 시 `402 Insufficient Balance`** 로 전 파이프라인의 LLM 단계가 조용히 빈 문자열을 반환합니다(2026-07-13~08-08 약 26일간 발생). 요약이 비면 잔액부터 확인하세요.

---

## 설정·상태 파일

- `watchlist.txt` — 한국 관심 종목 6자리 코드 목록
- `interest_watchlist.json`, `interest_sectors.txt` — 미국/글로벌 관심 종목·섹터
- `us_disclosure_watchlist.json` — SEC 공시 모니터링 대상
- `*_seen.json` (kotra, trendforce, tech_investing, company_blogs 등) — 중복 알림 방지용 처리 이력
- `user_requested_hs_codes_list.md` — 추적 대상 HS코드/기업/지표 정리 문서
- `requirements.txt` — 파이썬 의존성
