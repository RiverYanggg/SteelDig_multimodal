#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
import types
from pathlib import Path


def _ensure_evaluation_package() -> Path:
    eval_root = Path(__file__).resolve().parent
    if "evaluation" not in sys.modules:
        package = types.ModuleType("evaluation")
        package.__path__ = [str(eval_root)]
        package.__file__ = str(eval_root / "__init__.py")
        sys.modules["evaluation"] = package
    return eval_root


_EVAL_ROOT = _ensure_evaluation_package()

from evaluation.config import load_evaluation_settings  # noqa: E402


PLACEHOLDER_VALUES = {"", "EMPTY", "YOUR_API_KEY", "YOUR_BASE_URL"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate evaluation_json2json config without calling the LLM API.")
    parser.add_argument(
        "--config",
        default=str(_EVAL_ROOT.parent / "config" / "eval_config.json"),
        help="Evaluation config JSON path.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config_path = Path(args.config).expanduser().resolve()
    if not config_path.is_file():
        raise SystemExit(f"config not found: {config_path}")

    settings = load_evaluation_settings(config_path)
    errors: list[str] = []
    warnings: list[str] = []

    _require_dir("truth_dir", settings.truth_dir, errors)
    _require_dir("prediction_root", settings.prediction_root, errors)
    _require_file("field_rules_path", settings.field_rules_path, errors)
    if settings.llm_bridge.enabled:
        _require_file("llm_bridge.prompt_path", settings.llm_bridge.prompt_path, errors)
        if settings.llm_bridge.api_key.strip() in PLACEHOLDER_VALUES:
            errors.append("llm_bridge.api_key is still a placeholder.")
        if settings.llm_bridge.base_url.strip() in PLACEHOLDER_VALUES:
            errors.append("llm_bridge.base_url is still a placeholder.")
        if not settings.llm_bridge.base_url.startswith(("http://", "https://")):
            errors.append("llm_bridge.base_url must start with http:// or https://.")
    else:
        warnings.append("llm_bridge.enabled=false; LLM alignment and field judge will not call the API.")

    print(f"config: {config_path}")
    print(f"truth:  {settings.truth_dir}")
    print(f"pred:   {settings.prediction_root}")
    print(f"output: {settings.output_path}")
    print(f"llm:    enabled={settings.llm_bridge.enabled}, model={settings.llm_bridge.model}")
    if warnings:
        for warning in warnings:
            print(f"warning: {warning}")
    if errors:
        for issue in errors:
            print(f"error: {issue}")
        raise SystemExit(1)
    print("OK")


def _require_dir(label: str, value: str, errors: list[str]) -> None:
    if not Path(value).is_dir():
        errors.append(f"{label} does not exist or is not a directory: {value}")


def _require_file(label: str, value: str, errors: list[str]) -> None:
    if not Path(value).is_file():
        errors.append(f"{label} does not exist or is not a file: {value}")


if __name__ == "__main__":
    main()
