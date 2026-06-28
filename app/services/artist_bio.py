import httpx

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

SYSTEM_PROMPT = (
    "Ты профессиональный музыкальный PR-копирайтер. "
    "Пользователь пришлёт информацию о себе как об артисте. "
    "На её основе напиши красивое, ёмкое описание артиста (bio) для релиза, соцсетей и площадок. "
    "Объём небольшой: 1-2 абзаца, примерно 80-150 слов, без воды и штампов. "
    "По умолчанию пиши на русском языке. "
    "Если автор просит на английском (или прислал информацию на английском), пиши на английском. "
    "Не добавляй пояснений вне текста описания."
)

EDIT_SYSTEM_PROMPT = (
    "Ты профессиональный музыкальный PR-копирайтер. "
    "Пользователь пришлёт текущее описание артиста и инструкции по правкам. "
    "Верни полностью обновлённое описание, сохранив небольшой объём (1-2 абзаца). "
    "Сохраняй язык исходного описания, если автор не просит сменить язык. "
    "Не добавляй пояснений вне текста описания."
)


async def _call_openrouter(
    messages: list[dict[str, str]],
    api_key: str,
    model: str,
) -> str:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/fuserwyn/WAV-to-MP3",
        "X-Title": "WAV-to-MP3 Telegram Bot",
    }
    payload = {
        "model": model,
        "messages": messages,
    }

    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(OPENROUTER_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

    try:
        return data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, TypeError) as exc:
        raise ValueError("Unexpected OpenRouter response format") from exc


async def generate_artist_bio(
    prompt: str,
    api_key: str,
    model: str,
) -> str:
    return await _call_openrouter(
        [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        api_key,
        model,
    )


async def edit_artist_bio(
    current_text: str,
    edit_instructions: str,
    api_key: str,
    model: str,
) -> str:
    user_content = (
        f"Текущее описание артиста:\n\n{current_text}\n\n"
        f"Правки:\n{edit_instructions}"
    )
    return await _call_openrouter(
        [
            {"role": "system", "content": EDIT_SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
        ],
        api_key,
        model,
    )
