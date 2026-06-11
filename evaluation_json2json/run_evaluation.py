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

from evaluation.config import (  # noqa: E402
    EvaluationSettings,
    LLMBridgeSettings,
    apply_model_selection,
    default_evaluation_settings,
    dump_evaluation_settings,
    list_outputs_exp_models,
    load_evaluation_settings,
)
from evaluation.framework import run_evaluation  # noqa: E402


def _default_config_path() -> Path:
    return _EVAL_ROOT.parent / "config" / "eval_config.json"


def parse_args() -> argparse.Namespace:
    available_models = list_outputs_exp_models(_EVAL_ROOT / "outputs_exp")
    parser = argparse.ArgumentParser(
        description="比较 outputs_exp 中两套模型抽取结果（text_extraction.json），计算结构化评估指标。",
    )
    parser.add_argument(
        "--config",
        default=str(_default_config_path()),
        help="评估配置 JSON 路径，默认 ../config/eval_config.json",
    )
    parser.add_argument(
        "--truth",
        default=None,
        choices=available_models or None,
        metavar="MODEL",
        help="真值模型目录名（outputs_exp/<MODEL>/），例如 deepseek、doubao、kimi",
    )
    parser.add_argument(
        "--pred",
        default=None,
        choices=available_models or None,
        metavar="MODEL",
        help="预测模型目录名（outputs_exp/<MODEL>/），例如 doubao、deepseek、kimi",
    )
    parser.add_argument("--outputs-exp-root", default=None, help="模型输出根目录，默认 outputs_exp")
    parser.add_argument("--output-root", default=None, help="评估结果根目录，默认 output")
    parser.add_argument("--truth-dir", default=None, help="直接指定真值目录（覆盖 --truth）")
    parser.add_argument("--prediction-root", default=None, help="直接指定预测目录（覆盖 --pred）")
    parser.add_argument("--output-path", default=None, help="总报告 JSON 路径（覆盖自动命名）")
    parser.add_argument("--per-paper-output-dir", default=None, help="单篇报告目录（覆盖自动命名）")
    parser.add_argument("--field-rules-path", default=None, help="字段规则 JSON 路径")
    parser.add_argument(
        "--paper-ids",
        default=None,
        help="逗号分隔的 paper id，例如 A0,A19,A28",
    )
    parser.add_argument("--enable-llm-bridge", action="store_true", help="启用 LLM 样本对齐桥接")
    parser.add_argument("--llm-model", default=None, help="LLM bridge 模型名")
    parser.add_argument("--llm-base-url", default=None, help="LLM bridge base URL")
    parser.add_argument("--llm-api-key", default=None, help="LLM bridge API key")
    parser.add_argument("--llm-prompt-path", default=None, help="LLM bridge prompt 模板路径")
    parser.add_argument("--force", action="store_true", help="即使单篇输出已存在也重新评估")
    parser.add_argument("--quiet", action="store_true", help="关闭进度条与详细日志，仅保留启动时的路径信息")
    parser.add_argument(
        "--no-progress-bar",
        action="store_true",
        help="保留日志但不用单行进度条（非 TTY 或重定向时自动退化为逐行日志）",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=None,
        help="并行评估线程数，默认 4（配置文件 workers 可覆盖）",
    )
    return parser.parse_args()


def build_settings(args: argparse.Namespace) -> EvaluationSettings:
    config_path = Path(args.config).expanduser().resolve()
    if not config_path.exists():
        dump_evaluation_settings(default_evaluation_settings(_EVAL_ROOT), config_path)
    settings = load_evaluation_settings(config_path)
    settings = apply_model_selection(
        settings,
        truth_model=args.truth,
        pred_model=args.pred,
        outputs_exp_root=args.outputs_exp_root,
        output_root=args.output_root,
    )
    llm = settings.llm_bridge
    paper_ids = tuple(
        item.strip()
        for item in (args.paper_ids.split(",") if args.paper_ids else settings.paper_ids)
        if item and item.strip()
    )
    return EvaluationSettings(
        truth_dir=args.truth_dir or settings.truth_dir,
        prediction_root=args.prediction_root or settings.prediction_root,
        output_path=args.output_path or settings.output_path,
        per_paper_output_dir=args.per_paper_output_dir or settings.per_paper_output_dir,
        field_rules_path=args.field_rules_path or settings.field_rules_path,
        outputs_exp_root=args.outputs_exp_root or settings.outputs_exp_root,
        truth_model=settings.truth_model,
        pred_model=settings.pred_model,
        output_root=args.output_root or settings.output_root,
        paper_ids=paper_ids,
        force=args.force or settings.force,
        workers=max(1, args.workers) if args.workers is not None else settings.workers,
        llm_bridge=LLMBridgeSettings(
            enabled=args.enable_llm_bridge or llm.enabled,
            model=args.llm_model or llm.model,
            base_url=args.llm_base_url or llm.base_url,
            api_key=args.llm_api_key or llm.api_key,
            temperature=llm.temperature,
            prompt_path=args.llm_prompt_path or llm.prompt_path,
            verify_ssl=llm.verify_ssl,
        ),
    )


def main() -> None:
    args = parse_args()
    settings = build_settings(args)
    if not settings.truth_model or not settings.pred_model:
        if args.truth_dir and args.prediction_root:
            pass
        else:
            raise SystemExit(
                "请通过 --truth 与 --pred 指定模型，或在配置文件中设置 truth_model / pred_model；"
                "也可使用 --truth-dir 与 --prediction-root 直接指定目录。"
            )
    print(f"真值 (truth): {settings.truth_dir}", flush=True)
    print(f"预测 (pred):  {settings.prediction_root}", flush=True)
    print(f"输出目录:     {Path(settings.output_path).parent}", flush=True)
    run_evaluation(
        settings,
        verbose=not args.quiet,
        use_progress_bar=not args.no_progress_bar,
        workers=settings.workers,
    )


if __name__ == "__main__":
    main()
