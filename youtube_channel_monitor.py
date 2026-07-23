#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
youtube_channel_monitor.py - Monitor multiple YouTube channels for new videos,
pull the (auto-generated) transcript, summarize the FULL content in Korean with
Claude (subscription CLI; DeepSeek fallback), and post to Telegram.

semidoped_youtube_monitor.py를 다채널로 일반화한 후속. 자막이 없는 영상은
6회(약 3시간) 재시도 후 제목만 알림.
"""

import os
import sys
import json
import time
import argparse
import logging
import xml.etree.ElementTree as ET
from urllib.parse import quote
from llm_client import deepseek_chat, claude_cli_chat
import requests

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("youtube_channel_monitor")

def load_env():
    """Loads environment variables from local .env file."""
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ[k.strip()] = v.strip().strip("'\"")

load_env()

# Telegram configurations
TELEGRAM_BOT4_TOKEN = os.getenv("TELEGRAM_BOT4_TOKEN")
TELEGRAM_TEST_CHAT_ID = os.getenv("TELEGRAM_TEST_CHAT_ID", "-1003843549676")

# 모니터링 채널 목록. context는 요약 프롬프트에 들어가는 채널 소개.
CHANNELS = [
    {"id": "UCqIzK82kDT3zpA5OcPDg3Rg", "name": "Semi Doped",
     "context": "반도체 산업 뉴스·분석 채널 (Vik Sekar, Austin Lyons)"},
    {"id": "UC1r0DG-KEPyqOeW6o79PByw", "name": "TechTechPotato",
     "context": "Ian Cutress 박사의 반도체 기술·업계 심층 분석 채널"},
    {"id": "UCf_KhBXw5TIV0A7butjgFhg", "name": "SemiAnalysis",
     "context": "Dylan Patel의 반도체·AI 인프라 리서치 채널 (Tokenomics 팟캐스트 포함)"},
    {"id": "UCXl4i9dYBrFOabk0xGmbkRA", "name": "Dwarkesh Patel",
     "context": "AI·과학·경제 심층 인터뷰 팟캐스트 채널"},
]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# LLM 컨텍스트 보호용 상한 (영어 전사 ~30만자 ≈ 75k 토큰)
MAX_TRANSCRIPT_CHARS = 300000
MAX_PER_CHANNEL = 2       # 실행당 채널별 최대 처리 영상 수
TRANSCRIPT_MAX_ATTEMPTS = 6  # 30분 크론 기준 약 3시간 대기 후 제목만 알림

def translate_en_to_ko(text):
    """Translates English text to Korean using the free Google Translate API."""
    if not text:
        return ""
    text = " ".join(text.split())
    if not text.strip():
        return ""
    try:
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=ko&dt=t&q={quote(text)}"
        resp = requests.get(url, headers=HEADERS, timeout=10)
        if resp.status_code == 200:
            result = resp.json()
            translated_sentences = []
            if result and len(result) > 0 and result[0]:
                for part in result[0]:
                    if part and len(part) > 0 and part[0]:
                        translated_sentences.append(part[0])
            return "".join(translated_sentences)
    except Exception as e:
        logger.warning(f"Translation error: {e}")
    return text

def fetch_feed_videos(channel_id):
    """
    Fetches a channel RSS feed. Returns videos newest to oldest:
    [{'video_id', 'title', 'link', 'date'}]
    """
    videos = []
    feed_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    try:
        resp = requests.get(feed_url, headers=HEADERS, timeout=20)
        if resp.status_code != 200:
            logger.error(f"Failed to fetch YouTube RSS feed for {channel_id}. HTTP {resp.status_code}")
            return videos
        ns = {
            "atom": "http://www.w3.org/2005/Atom",
            "yt": "http://www.youtube.com/xml/schemas/2015",
        }
        root = ET.fromstring(resp.content)
        for entry in root.findall("atom:entry", ns):
            vid = (entry.findtext("yt:videoId", default="", namespaces=ns) or "").strip()
            title = (entry.findtext("atom:title", default="", namespaces=ns) or "").strip()
            published = (entry.findtext("atom:published", default="", namespaces=ns) or "").strip()
            if not vid or not title:
                continue
            videos.append({
                'video_id': vid,
                'title': title,
                'link': f"https://www.youtube.com/watch?v={vid}",
                'date': published,
            })
    except Exception as e:
        logger.error(f"Error fetching/parsing YouTube RSS feed for {channel_id}: {e}")
    return videos

def fetch_transcript_text(video_id):
    """Fetches the transcript (manual first, else auto-generated). Returns text or ""."""
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        api = YouTubeTranscriptApi()
        try:
            tr = api.fetch(video_id, languages=["en", "en-US", "en-GB", "ko"])
        except Exception:
            # 언어 지정 실패 시 목록에서 첫 자막 사용
            tl = api.list(video_id)
            first = next(iter(tl), None)
            if first is None:
                return ""
            tr = first.fetch()
        text = " ".join(s.text.strip() for s in tr.snippets if s.text and s.text.strip())
        return " ".join(text.split())
    except Exception as e:
        logger.warning(f"Transcript unavailable for {video_id}: {type(e).__name__} {e}")
        return ""

def summarize_transcript(channel, title, transcript):
    """전사 전체를 커버하는 한국어 구조화 요약 생성. 실패 시 "".

    LLM 우선순위(사용자 지정): 1) Claude(구독 CLI, force로 전역 DeepSeek 정책 예외)
    → 2) DeepSeek 폴백. 유튜브 영상 요약이 유일한 Claude 사용처다.
    """
    if len(transcript) > MAX_TRANSCRIPT_CHARS:
        transcript = transcript[:MAX_TRANSCRIPT_CHARS]
    # 출력 형식: 텔레그램 Markdown 파싱 오류 방지 위해 *, _, [ ] 금지
    prompt = (
        f"다음은 유튜브 채널 '{channel['name']}'({channel['context']}) 영상의 자동 생성 자막 전사이다.\n"
        f"영상 제목: {title}\n\n"
        "이 영상의 내용을 한국어로 최대한 이해하기 쉽게 정리해줘. 요구사항:\n"
        "- 영상 전체 내용을 빠짐없이 커버해. 앞부분만 요약하고 끝내지 마.\n"
        "- 주제 흐름에 따라 소제목으로 구간을 나눠 정리해.\n"
        "- 소제목 줄은 '■ '로 시작하고, 세부 내용은 '• ' 불릿으로 써.\n"
        "- 수치·기업명·제품명·기술 용어는 정확히 보존해. (자동 자막이라 고유명사 오인식이 있을 수 있으니 문맥상 명백한 것은 바로잡아)\n"
        "- 마지막에 '■ 핵심 시사점' 구간을 두고 투자·산업 관점에서 중요한 포인트 2~4개를 정리해.\n"
        "- 별표(*), 밑줄(_), 대괄호 등 마크다운 특수문자는 쓰지 마. 평문과 ■, • 만 사용해.\n"
        "- 설명 없이 정리 결과만 출력해.\n\n"
        "=== 전사 시작 ===\n"
        f"{transcript}\n"
        "=== 전사 끝 ==="
    )
    out = claude_cli_chat(prompt, model="sonnet", timeout=600, force=True)
    if out:
        return out
    logger.warning("Claude CLI unavailable/failed; falling back to DeepSeek.")
    return deepseek_chat(prompt, temperature=0.3, max_tokens=8000, timeout=600)

def format_pub_date(iso_date):
    """Converts ISO8601 published date to 'YYYY-MM-DD HH:MM (KST)'."""
    try:
        import datetime as _dt
        dt = _dt.datetime.fromisoformat(iso_date.replace("Z", "+00:00"))
        kst = dt.astimezone(_dt.timezone(_dt.timedelta(hours=9)))
        return kst.strftime("%Y-%m-%d %H:%M (KST)")
    except Exception:
        return iso_date

def send_telegram_message(token, chat_id, text):
    """Sends a markdown-formatted message to Telegram (plain-text fallback on parse error)."""
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    try:
        resp = requests.post(url, json=payload, timeout=15)
        result = resp.json()
        if not result.get("ok") and "parse" in str(result.get("description", "")).lower():
            payload.pop("parse_mode", None)
            resp = requests.post(url, json=payload, timeout=15)
            result = resp.json()
        return result
    except Exception as e:
        logger.error(f"Failed to send telegram request: {e}")
        return None

def send_telegram_long(token, chat_id, header, body, footer):
    """Sends header+body+footer, chunking body paragraphs at ~4000 chars."""
    limit = 4000
    paragraphs = [p for p in body.split("\n\n") if p.strip()] if body else []
    current_chunk = header + "\n\n"
    for p in paragraphs:
        if len(current_chunk) + len(p) + 2 > limit:
            send_telegram_message(token, chat_id, current_chunk.strip())
            time.sleep(1.0)
            current_chunk = p + "\n\n"
        else:
            current_chunk += p + "\n\n"
    if len(current_chunk) + len(footer) + 2 > limit:
        send_telegram_message(token, chat_id, current_chunk.strip())
        time.sleep(1.0)
        current_chunk = footer
    else:
        current_chunk += footer
    if current_chunk.strip():
        send_telegram_message(token, chat_id, current_chunk.strip())

def process_channel(channel, seen_map, pending, chat_id):
    """한 채널의 신규 영상을 처리한다. seen_map/pending은 in-place 갱신."""
    cid = channel['id']
    name = channel['name']
    logger.info(f"[{name}] Fetching RSS feed...")
    videos = fetch_feed_videos(cid)
    if not videos:
        logger.warning(f"[{name}] No videos found in feed.")
        return

    # 채널 첫 등장: 알림 없이 현재 영상들로 초기화
    if cid not in seen_map:
        seen_map[cid] = [v['video_id'] for v in videos]
        logger.info(f"[{name}] First appearance. Initialized with {len(videos)} videos, no alerts.")
        return

    seen_list = seen_map[cid]
    new_videos = [v for v in reversed(videos) if v['video_id'] not in seen_list]
    if not new_videos:
        logger.info(f"[{name}] No new videos.")
        return

    if len(new_videos) > MAX_PER_CHANNEL:
        logger.info(f"[{name}] {len(new_videos)} new videos; limiting to {MAX_PER_CHANNEL} most recent.")
        to_process = new_videos[-MAX_PER_CHANNEL:]
        # 초과분(오래된 것)은 스팸 방지 위해 seen 처리
        for v in new_videos[:-MAX_PER_CHANNEL]:
            if v['video_id'] not in seen_list:
                seen_list.append(v['video_id'])
    else:
        to_process = new_videos

    for v in to_process:
        vid = v['video_id']
        title = v['title']
        link = v['link']
        logger.info(f"[{name}] Processing new video: {title} ({vid})")

        transcript = fetch_transcript_text(vid)
        if not transcript:
            attempts = pending.get(vid, 0) + 1
            if attempts >= TRANSCRIPT_MAX_ATTEMPTS:
                logger.info(f"[{name}] No transcript for {vid} after {attempts} attempts. Title-only alert.")
                translated_title = translate_en_to_ko(title)
                notice = (
                    f"🎬 *[{name} 유튜브 - 새 영상]*\n\n"
                    f"📌 *{translated_title}*\n({title})\n\n"
                    f"_(자막 미제공으로 내용 정리 생략)_\n\n"
                    f"🔗 [영상 보기]({link})\n📅 {format_pub_date(v['date'])}"
                )
                if TELEGRAM_BOT4_TOKEN and chat_id:
                    send_telegram_message(TELEGRAM_BOT4_TOKEN, chat_id, notice)
                seen_list.append(vid)
                pending.pop(vid, None)
            else:
                pending[vid] = attempts
                logger.info(f"[{name}] No transcript yet for {vid} (attempt {attempts}/{TRANSCRIPT_MAX_ATTEMPTS}). Will retry.")
            continue
        pending.pop(vid, None)

        logger.info(f"[{name}] Transcript fetched: {len(transcript)} chars. Summarizing with Claude (DeepSeek fallback)...")
        summary = summarize_transcript(channel, title, transcript)
        translated_title = translate_en_to_ko(title)

        header_text = (
            f"🎬 *[{name} 유튜브 - 영상 정리]*\n\n"
            f"📌 *{translated_title}*\n"
            f"({title})"
        )
        footer_text = (
            f"=============================\n"
            f"🔗 [영상 보기]({link})\n"
            f"📅 {format_pub_date(v['date'])}"
        )

        if not summary:
            summary = "_(요약 생성 실패 — 영상 링크 참조)_"
            logger.warning(f"[{name}] Summary generation failed for {vid}.")

        if TELEGRAM_BOT4_TOKEN and chat_id:
            logger.info(f"[{name}] Sending video summary to Telegram chat {chat_id}...")
            send_telegram_long(TELEGRAM_BOT4_TOKEN, chat_id, header_text, summary, footer_text)
            logger.info(f"[{name}] Telegram alert sent successfully.")
        else:
            logger.warning("Telegram bot token or chat ID is missing. Alert skipped.")

        seen_list.append(vid)
        time.sleep(2.0)

    # 채널별 seen 상한
    if len(seen_list) > 300:
        seen_map[cid] = seen_list[-300:]

def main():
    parser = argparse.ArgumentParser(description="Multi-channel YouTube Monitor")
    parser.add_argument("--test", action="store_true", help="Run in test mode with a separate seen file.")
    parser.add_argument("--init", action="store_true", help="Initialize the seen lists with current videos without sending alerts.")
    args = parser.parse_args()

    state_dir = os.path.dirname(os.path.abspath(__file__))
    suffix = "_test" if args.test else ""
    state_file = os.path.join(state_dir, f"youtube_channels_seen{suffix}.json")
    pending_file = os.path.join(state_dir, f"youtube_channels_pending{suffix}.json")

    # seen: {channel_id: [video_ids]}
    seen_map = {}
    if os.path.exists(state_file):
        try:
            with open(state_file, "r", encoding="utf-8") as f:
                seen_map = json.load(f)
        except Exception as e:
            logger.error(f"Failed to load seen state file: {e}")

    pending = {}
    if os.path.exists(pending_file):
        try:
            with open(pending_file, "r", encoding="utf-8") as f:
                pending = json.load(f)
        except Exception:
            pending = {}

    if args.init:
        for ch in CHANNELS:
            videos = fetch_feed_videos(ch['id'])
            seen_map[ch['id']] = [v['video_id'] for v in videos]
            logger.info(f"[{ch['name']}] Initialized with {len(videos)} videos.")
        with open(state_file, "w", encoding="utf-8") as f:
            json.dump(seen_map, f, indent=2, ensure_ascii=False)
        logger.info("State initialized. Exiting.")
        return

    chat_id = TELEGRAM_TEST_CHAT_ID
    for ch in CHANNELS:
        try:
            process_channel(ch, seen_map, pending, chat_id)
        except Exception as e:
            logger.error(f"[{ch['name']}] Unexpected error: {e}")

    try:
        with open(state_file, "w", encoding="utf-8") as f:
            json.dump(seen_map, f, indent=2, ensure_ascii=False)
        with open(pending_file, "w", encoding="utf-8") as f:
            json.dump(pending, f, indent=2, ensure_ascii=False)
        logger.info(f"State saved ({sum(len(v) for v in seen_map.values())} seen across "
                    f"{len(seen_map)} channels, {len(pending)} pending).")
    except Exception as e:
        logger.error(f"Failed to save state file: {e}")

if __name__ == "__main__":
    main()
