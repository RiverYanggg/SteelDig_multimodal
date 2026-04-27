from urllib.parse import urlparse

import httpx
from openai import OpenAI

from paper_extractor.config import LocalModelConfig


def create_client(model_config: LocalModelConfig) -> OpenAI:
    api_key = model_config.api_key or "EMPTY"
    if not api_key and is_local_base_url(model_config.base_url):
        api_key = "EMPTY"
    if not api_key:
        raise EnvironmentError(f"Missing API key for local model: {model_config.model}")

    # 强制直连，避免 http_proxy/https_proxy 把本地 127.0.0.1 请求转发走。
    http_client = httpx.Client(trust_env=False, timeout=1800.0)
    return OpenAI(api_key=api_key, base_url=model_config.base_url, http_client=http_client)


def is_local_base_url(base_url: str) -> bool:
    hostname = (urlparse(base_url).hostname or "").lower()
    return hostname in {"127.0.0.1", "localhost", "0.0.0.0"}
