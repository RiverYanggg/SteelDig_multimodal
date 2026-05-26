from urllib.parse import urlparse, urlunparse

from paper_extractor.config import LocalModelConfig


def create_client(model_config: LocalModelConfig):
    import httpx
    from openai import OpenAI

    api_key = model_config.api_key or "EMPTY"
    base_url = normalize_openai_base_url(model_config.base_url)
    if not api_key and is_local_base_url(base_url):
        api_key = "EMPTY"
    if not api_key:
        raise EnvironmentError(f"Missing API key for local model: {model_config.model}")

    # 强制直连，避免 http_proxy/https_proxy 把本地 127.0.0.1 请求转发走。
    http_client = httpx.Client(trust_env=False, timeout=1800.0)
    return OpenAI(api_key=api_key, base_url=base_url, http_client=http_client)


def build_chat_completion_kwargs(model_config: LocalModelConfig, **kwargs):
    payload = dict(kwargs)
    if model_config.max_tokens is not None:
        payload["max_tokens"] = model_config.max_tokens
    return payload


def normalize_openai_base_url(base_url: str) -> str:
    stripped = base_url.strip().rstrip("/")
    parsed = urlparse(stripped)
    if not parsed.scheme or not parsed.netloc:
        return stripped
    hostname = (parsed.hostname or "").lower()
    needs_v1_base = (
        hostname in {"api.openai.com", "api.moonshot.cn", "api.moonshot.ai", "api.kimi.com"}
        or hostname.endswith(".moonshot.cn")
        or hostname.endswith(".moonshot.ai")
    )
    if parsed.path in {"", "/"} and needs_v1_base:
        return urlunparse(parsed._replace(path="/v1", params="", query="", fragment=""))
    return stripped


def is_local_base_url(base_url: str) -> bool:
    hostname = (urlparse(base_url).hostname or "").lower()
    return hostname in {"127.0.0.1", "localhost", "0.0.0.0"}
