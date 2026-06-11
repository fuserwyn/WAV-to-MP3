import httpx

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

SYSTEM_PROMPT = (
    "Ты профессиональный PR-копирайтер. "
    "По запросу пользователя напиши готовый пресс-релиз на русском языке. "
    "Структура: заголовок, подзаголовок, лид, основной текст, цитата, "
    "блок «О компании/проекте», контакты для СМИ. "
    "Тон: деловой, ясный, без воды. Не добавляй пояснений вне текста релиза."
)

EDIT_SYSTEM_PROMPT = (
    "Ты профессиональный PR-копирайтер. "
    "Пользователь пришлёт текущий пресс-релиз и инструкции по правкам. "
    "Верни полностью обновлённый пресс-релиз на русском языке с той же структурой. "
    "Не добавляй пояснений вне текста релиза."
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


async def generate_press_release(
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


async def edit_press_release(
    current_text: str,
    edit_instructions: str,
    api_key: str,
    model: str,
) -> str:
    user_content = (
        f"Текущий пресс-релиз:\n\n{current_text}\n\n"
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
