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
| `telegram_reporter.py` | `watchlist.txt` 종목별 누적 매매동향 차트 + 뉴스 헤드라인을 Telethon으로 이미지 업로드 |
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

---

## 🇺🇸 미국 시장·공시

| 파일 | 역할 |
|------|------|
| `us_market_monitor.py` | S&P500 등락률로 마켓 무버(급등·급락주) 집계해 전송 |
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
| `tech_investing_monitor.py` | Tom's Hardware / Investing.com 애널리스트 등급 RSS 모니터링 |
| `kotra_monitor.py` | KOTRA 해외시장뉴스 신규 기사 DeepSeek 요약 |
| `kotra_report_monitor.py` | KOTRA 보고서(PDF) 신규 감지·다운로드·요약 |
| `company_blogs_monitor.py` | Nvidia·Google 등 기업 블로그 RSS를 DeepSeek로 번역·게시 |

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
| `data_jp/` | 일본 수출/부품(MLCC·메모리·ABF 등) 차트 이미지 |
| `data_blog/` | 기업 블로그 크롤링·번역 텍스트 결과 |
| `draw/` | 관심 종목별 누적 매매동향 차트 PNG (`<티커>_cumulative.png`) |

---

## 설정·상태 파일

- `watchlist.txt` — 한국 관심 종목 6자리 코드 목록
- `interest_watchlist.json`, `interest_sectors.txt` — 미국/글로벌 관심 종목·섹터
- `us_disclosure_watchlist.json` — SEC 공시 모니터링 대상
- `*_seen.json` (kotra, trendforce, tech_investing, company_blogs 등) — 중복 알림 방지용 처리 이력
- `user_requested_hs_codes_list.md` — 추적 대상 HS코드/기업/지표 정리 문서
- `requirements.txt` — 파이썬 의존성
