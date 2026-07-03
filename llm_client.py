# -*- coding: utf-8 -*-
"""
llm_client.py - dataScout 공용 DeepSeek 클라이언트

기존 각 모니터의 Gemini(generateContent) 호출을 대체하는 경량 헬퍼.
사용법:
    from llm_client import deepseek_chat
    text = deepseek_chat(prompt)            # 실패 시 "" 반환
"""
import os
import time
import logging

import requests

logger = logging.getLogger(__name__)

# .env 로더 (각 스크립트와 동일한 방식, 이미 로드돼 있으면 no-op)
_env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
if os.path.exists(_env_path) and not os.getenv("DEEPSEEK_API_KEY"):
    with open(_env_path, "r", encoding="utf-8") as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                _k, _v = _line.split("=", 1)
                os.environ.setdefault(_k.strip(), _v.strip().strip("'\""))

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
_API_URL = "https://api.deepseek.com/chat/completions"
_MODEL = "deepseek-chat"  # DeepSeek-V3


def deepseek_chat(prompt, temperature=0.3, max_tokens=2048, timeout=60, retries=2, json_mode=False):
    """
    DeepSeek chat 호출. 성공 시 응답 텍스트, 실패 시 "" 반환.
    (기존 summarize_with_gemini 계열과 동일한 실패 시멘틱: 빈 문자열)
    json_mode=True면 JSON 객체 출력을 강제한다 (프롬프트에 'JSON' 언급 필요).
    """
    if not DEEPSEEK_API_KEY:
        logger.warning("DEEPSEEK_API_KEY is not set.")
        return ""
    payload = {
        "model": _MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    if json_mode:
        payload["response_format"] = {"type": "json_object"}
    headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"}
    for attempt in range(retries):
        try:
            resp = requests.post(_API_URL, json=payload, headers=headers, timeout=timeout)
            if resp.status_code == 200:
                content = resp.json()["choices"][0]["message"]["content"].strip()
                if content:
                    logger.info("DeepSeek response generated.")
                    return content
            elif resp.status_code in (429, 503):
                logger.warning(f"DeepSeek API busy: HTTP {resp.status_code}, retry {attempt + 1}/{retries}")
                time.sleep(5)
                continue
            else:
                logger.warning(f"DeepSeek API error: HTTP {resp.status_code} {resp.text[:200]}")
                return ""
        except Exception as e:
            logger.warning(f"DeepSeek request failed: {e}")
            if attempt < retries - 1:
                time.sleep(3)
    return ""
