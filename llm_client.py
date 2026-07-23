# -*- coding: utf-8 -*-
"""
llm_client.py - dataScout 공용 LLM 클라이언트

사용법:
    from llm_client import deepseek_chat, claude_chat, smart_chat
    text = deepseek_chat(prompt)   # DeepSeek (실패 시 "" 반환)
    text = claude_chat(prompt)     # Claude API (ANTHROPIC_API_KEY 필요, 미설정/실패 시 "")
    text = smart_chat(prompt)      # Claude 우선, 미설정/실패 시 DeepSeek 자동 폴백

역할 분담(비용):
  - 대량 번역·저부가 호출(kotra/trendforce 등 30분 주기) → deepseek_chat 유지
  - 분석 품질이 중요한 호출(실적 비교분석, 강세분석, 섹터코멘트 등) → smart_chat
    ANTHROPIC_API_KEY가 .env에 있으면 Claude(기본 claude-sonnet-5)로,
    없으면 기존처럼 DeepSeek으로 동작한다.
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


# ---------------------------------------------------------------------------
# Claude API (Anthropic)
# ---------------------------------------------------------------------------

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
_CLAUDE_DEFAULT_MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-5")


def claude_chat(prompt, model=None, max_tokens=2048, effort="medium", timeout=120):
    """Claude API 호출. 성공 시 응답 텍스트, 미설정/실패 시 "" 반환.

    model: 기본 claude-sonnet-5 (.env CLAUDE_MODEL로 변경 가능).
           고부가 분석은 model="claude-opus-4-8" 지정.
    effort: low/medium/high — 파이프라인 요약은 medium이면 충분.
    참고: Opus 4.8/Sonnet 5는 temperature 미지원(전달 시 400)이라 받지 않는다.
    """
    if not ANTHROPIC_API_KEY:
        return ""
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY, timeout=timeout, max_retries=2)
        resp = client.messages.create(
            model=model or _CLAUDE_DEFAULT_MODEL,
            max_tokens=max_tokens,
            output_config={"effort": effort},
            messages=[{"role": "user", "content": prompt}],
        )
        if resp.stop_reason == "refusal":
            logger.warning("Claude refused the request.")
            return ""
        text = "".join(b.text for b in resp.content if b.type == "text").strip()
        if text:
            logger.info(f"Claude response generated ({resp.model}).")
        return text
    except Exception as e:
        logger.warning(f"Claude request failed: {e}")
        return ""


def smart_chat(prompt, max_tokens=2048, timeout=120, model=None, effort="medium",
               temperature=0.3, json_mode=False):
    """정리·분석용: 1) Claude(구독 CLI, 폴백 API) → 2) DeepSeek. (json_mode는 DeepSeek에서만 적용)"""
    out = claude_cli_chat(prompt, model=CLAUDE_CLI_MODEL_SMART, timeout=max(timeout, 240))
    if out:
        return out
    out = claude_chat(prompt, model=model, max_tokens=max_tokens, effort=effort, timeout=timeout)
    if out:
        return out
    return deepseek_chat(prompt, temperature=temperature, max_tokens=max_tokens,
                         timeout=timeout, json_mode=json_mode)


def llm_translate(paragraphs, src_lang="영어", model="claude-haiku-4-5"):
    """기사 문단 리스트를 통번역 (문맥 유지, 자연스러운 한국어).

    번역 우선순위: 1) DeepSeek 통번역 → 실패 시 [] 반환(호출부가 2) 구글 번역 폴백).
    Claude는 번역에 사용하지 않는다(구독 토큰은 정리·분석 전용).
    """
    paragraphs = [p for p in paragraphs if p and p.strip()]
    if not paragraphs:
        return []
    SEP = "\n<<<P>>>\n"

    def _translate_batch(batch):
        prompt = (
            f"다음 {src_lang} 기사를 자연스러운 한국어로 번역해줘.\n"
            "- 직역투를 피하고 한국 경제지 기사 문체(평서체, '~했다'체)로 옮겨.\n"
            "- 기업명·인명·제품명은 통용되는 한국어 표기가 있으면 쓰고 없으면 원어 유지.\n"
            "- 숫자·단위·날짜는 정확히 보존하고, 반도체·금융 용어는 업계 표준 한국어 용어를 써.\n"
            "- 문단 구분자 <<<P>>>를 그대로 유지하고 문단 수를 바꾸지 마.\n"
            "- 설명 없이 번역문만 출력해.\n\n" + SEP.join(batch)
        )
        out = deepseek_chat(prompt, temperature=0.2, max_tokens=8000, timeout=180)
        if not out:
            return None
        parts = [s.strip() for s in out.split("<<<P>>>") if s.strip()]
        # 문단 수가 어긋나도 내용은 유효 — 그대로 사용
        return parts if parts else None

    # 긴 기사는 ~10,000자 단위로 나눠 번역
    batches, cur, cur_len = [], [], 0
    for p in paragraphs:
        if cur and cur_len + len(p) > 10000:
            batches.append(cur)
            cur, cur_len = [], 0
        cur.append(p)
        cur_len += len(p)
    if cur:
        batches.append(cur)

    result = []
    for b in batches:
        parts = _translate_batch(b)
        if parts is None:
            return []  # 부분 성공은 혼란 — 전체 폴백
        result.extend(parts)
    return result


# ---------------------------------------------------------------------------
# Claude Code CLI (구독 인증 — API 키 불필요)
# ---------------------------------------------------------------------------

CLAUDE_CLI = os.getenv("CLAUDE_CLI_BIN", os.path.expanduser("~/.local/bin/claude"))
CLAUDE_CLI_ENABLED = os.getenv("CLAUDE_CLI_ENABLED", "1") != "0"
CLAUDE_CLI_MODEL_LIGHT = os.getenv("CLAUDE_CLI_MODEL_LIGHT", "haiku")     # 번역 등 대량
CLAUDE_CLI_MODEL_SMART = os.getenv("CLAUDE_CLI_MODEL_SMART", "sonnet")    # 분석


CODEX_CLI = os.getenv("CODEX_CLI_BIN", os.path.expanduser("~/.local/bin/codex"))


def openai_cli_chat(prompt, model=None, timeout=600):
    """OpenAI Codex CLI 헤드리스(exec) 호출 — ChatGPT 구독 토큰 사용 (API 과금 아님).

    프롬프트는 stdin으로 전달(초장문 대응). 실패 시 "" 반환하여 호출부가 폴백한다.
    model 미지정 시 codex 기본 모델(gpt-5 계열)을 쓴다.
    """
    if not os.path.exists(CODEX_CLI):
        return ""
    import subprocess
    import tempfile
    out_path = None
    try:
        fd, out_path = tempfile.mkstemp(prefix="codex_last_", suffix=".txt")
        os.close(fd)
        cmd = [CODEX_CLI, "exec", "--skip-git-repo-check", "-s", "read-only",
               "--ephemeral", "--color", "never", "-o", out_path]
        if model:
            cmd += ["-m", model]
        cmd += ["-"]
        r = subprocess.run(cmd, input=prompt, capture_output=True, text=True,
                           timeout=timeout, cwd=os.path.expanduser("~"))
        if r.returncode == 0:
            with open(out_path, encoding="utf-8") as f:
                txt = f.read().strip()
            if txt:
                logger.info("OpenAI Codex CLI response generated (subscription).")
                return txt
        logger.warning(f"Codex CLI failed rc={r.returncode}: {(r.stderr or '')[:150]}")
    except Exception as e:
        logger.warning(f"Codex CLI error: {e}")
    finally:
        try:
            if out_path and os.path.exists(out_path):
                os.remove(out_path)
        except Exception:
            pass
    return ""


def claude_cli_chat(prompt, model=None, timeout=240, force=False):
    """Claude Code CLI 헤드리스(-p) 호출 — 구독 토큰 사용.

    구독 한도 소진/오류 시 "" 반환하여 호출부가 다음 단계로 폴백한다.
    force=True면 CLAUDE_CLI_ENABLED=0(전역 DeepSeek 정책)을 무시하고 Claude를 쓴다
    — 예외적으로 Claude를 지정한 호출부(semidoped_youtube_monitor) 전용.
    """
    if (not CLAUDE_CLI_ENABLED and not force) or not os.path.exists(CLAUDE_CLI):
        return ""
    try:
        import subprocess
        r = subprocess.run(
            [CLAUDE_CLI, "-p", "--model", model or CLAUDE_CLI_MODEL_SMART],
            input=prompt, capture_output=True, text=True, timeout=timeout)
        if r.returncode == 0 and r.stdout.strip():
            logger.info(f"Claude CLI response generated (subscription, {model or CLAUDE_CLI_MODEL_SMART}).")
            return r.stdout.strip()
        logger.warning(f"Claude CLI failed rc={r.returncode}: {(r.stderr or '')[:150]}")
    except Exception as e:
        logger.warning(f"Claude CLI error: {e}")
    return ""
