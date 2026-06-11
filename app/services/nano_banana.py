import asyncio
import logging
import time
from pathlib import Path

import httpx

POYO_BASE_URL = "https://api.poyo.ai"
POLL_INTERVAL_SEC = 3
POLL_TIMEOUT_SEC = 120

logger = logging.getLogger("wav-to-mp3-bot")


async def submit_task(
    prompt: str,
    api_key: str,
    model: str,
    image_urls: list[str] | None = None,
) -> str:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    input_data: dict = {
        "prompt": prompt,
        "size": "1:1",
    }
    if image_urls:
        input_data["image_urls"] = image_urls

    payload = {
        "model": model,
        "input": input_data,
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"{POYO_BASE_URL}/api/generate/submit",
            headers=headers,
            json=payload,
        )
        response.raise_for_status()
        data = response.json()

    return data["data"]["task_id"]


async def wait_for_image_url(task_id: str, api_key: str) -> str:
    headers = {"Authorization": f"Bearer {api_key}"}
    started_at = time.monotonic()

    async with httpx.AsyncClient(timeout=60.0) as client:
        while time.monotonic() - started_at < POLL_TIMEOUT_SEC:
            response = await client.get(
                f"{POYO_BASE_URL}/api/generate/status/{task_id}",
                headers=headers,
            )

            if response.status_code == 429:
                await asyncio.sleep(POLL_INTERVAL_SEC * 2)
                continue

            response.raise_for_status()
            data = response.json()["data"]
            status = data["status"]

            if status == "finished":
                for file in data.get("files", []):
                    if file.get("file_type") == "image":
                        return file["file_url"]
                raise ValueError("No image in task result")

            if status == "failed":
                raise RuntimeError(data.get("error_message") or "Image generation failed")

            await asyncio.sleep(POLL_INTERVAL_SEC)

    raise TimeoutError("Image generation timed out")


async def download_image(url: str, output_path: Path) -> None:
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.get(url)
        response.raise_for_status()
        output_path.write_bytes(response.content)


async def generate_nano_banana_image(
    prompt: str,
    api_key: str,
    output_path: Path,
) -> str:
    task_id = await submit_task(prompt, api_key, model="nano-banana")
    logger.info("Nano Banana task submitted: %s", task_id)

    image_url = await wait_for_image_url(task_id, api_key)
    await download_image(image_url, output_path)
    return image_url


async def edit_nano_banana_image(
    prompt: str,
    image_urls: list[str],
    api_key: str,
    output_path: Path,
) -> str:
    task_id = await submit_task(
        prompt,
        api_key,
        model="nano-banana-edit",
        image_urls=image_urls,
    )
    logger.info("Nano Banana edit task submitted: %s", task_id)

    image_url = await wait_for_image_url(task_id, api_key)
    await download_image(image_url, output_path)
    return image_url
