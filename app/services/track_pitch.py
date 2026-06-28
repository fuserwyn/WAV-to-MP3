import httpx

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

SYSTEM_PROMPT = (
    "Ты профессиональный музыкальный маркетолог. "
    "Пользователь пришлёт информацию о треке. "
    "На её основе напиши цепляющий питч трека для редакторов плейлистов и площадок "
    "(Spotify for Artists, кураторы, лейблы). "
    "Раскрой жанр, настроение, звучание, фишку трека и почему он подойдёт в плейлисты; "
    "при наличии — похожие артисты и референсы. "
    "Объём короткий: 3-5 предложений, до ~500 символов, цепляюще и по делу, без воды. "
    "По умолчанию пиши на русском языке. "
    "Если автор просит на английском (или прислал информацию на английском), пиши на английском. "
    "Не добавляй пояснений вне текста питча."
)

EDIT_SYSTEM_PROMPT = (
    "Ты профессиональный музыкальный маркетолог. "
    "Пользователь пришлёт текущий питч трека и инструкции по правкам. "
    "Верни полностью обновлённый питч, сохранив короткий объём (до ~500 символов). "
    "Сохраняй язык исходного питча, если автор не просит сменить язык. "
    "Не добавляй пояснений вне текста питча."
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


async def generate_track_pitch(
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


async def edit_track_pitch(
    current_text: str,
    edit_instructions: str,
    api_key: str,
    model: str,
) -> str:
    user_content = (
        f"Текущий питч трека:\n\n{current_text}\n\n"
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
