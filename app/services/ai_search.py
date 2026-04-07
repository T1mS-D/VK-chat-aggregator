import httpx
from app.config import OPENROUTER_API_KEY, OPENROUTER_MODEL

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


async def is_relevant(message_text: str, user_prompt: str) -> bool:
    system = (
        "Ты — интеллектуальный фильтр сообщений из VK-бесед. "
        "Определи, соответствует ли сообщение критерию пользователя. "
        "Критерий может описывать жалобы, недовольства, конфликты, "
        "упоминания сроков, обязательств или любую другую тему. "
        "Отвечай строго одним словом: ДА или НЕТ."
    )
    user_content = (
        f"Критерий: {user_prompt}\n\n"
        f"Сообщение: {message_text}"
    )

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user_content},
        ],
        "max_tokens": 5,
    }

    async with httpx.AsyncClient(timeout=20) as client:
        resp = await client.post(OPENROUTER_URL, json=payload, headers=headers)
        resp.raise_for_status()
        data = resp.json()

    answer = data["choices"][0]["message"]["content"].strip().upper()
    return answer.startswith("ДА")