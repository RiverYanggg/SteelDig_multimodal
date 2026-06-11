from __future__ import annotations

import sys
import threading
import time
from dataclasses import dataclass, field


@dataclass
class EvaluationProgress:
    """评估过程的终端日志与进度显示（仅依赖标准库）。"""

    total: int
    quiet: bool = False
    use_progress_bar: bool = True
    _start: float = field(default_factory=time.monotonic, init=False)
    _last_bar_width: int = field(default=0, init=False)
    _done: int = field(default=0, init=False)
    _lock: threading.Lock = field(default_factory=threading.Lock, init=False)

    def _is_tty(self) -> bool:
        stream = sys.stderr
        return hasattr(stream, "isatty") and stream.isatty()

    def info(self, message: str) -> None:
        if self.quiet:
            return
        with self._lock:
            self._clear_bar_unlocked()
            elapsed = time.monotonic() - self._start
            sys.stderr.write(f"[eval {elapsed:6.1f}s] {message}\n")
            sys.stderr.flush()

    def _clear_bar(self) -> None:
        with self._lock:
            self._clear_bar_unlocked()

    def _clear_bar_unlocked(self) -> None:
        if self._last_bar_width and self._is_tty():
            sys.stderr.write("\r" + " " * self._last_bar_width + "\r")
            sys.stderr.flush()
            self._last_bar_width = 0

    def _bar_line(self, current: int, total: int, label: str, width: int = 32) -> str:
        total = max(total, 1)
        ratio = min(max(current / total, 0.0), 1.0)
        filled = int(width * ratio)
        bar = "=" * filled + "-" * (width - filled)
        pct = int(ratio * 100)
        label = label[:48]
        return f"[{bar}] {pct:3d}% ({current}/{total}) {label}"

    def update(self, current: int, label: str) -> None:
        if self.quiet:
            return
        with self._lock:
            if self.use_progress_bar and self._is_tty():
                line = self._bar_line(current, self.total, label)
                self._last_bar_width = len(line)
                sys.stderr.write("\r" + line)
                sys.stderr.flush()
            else:
                self._clear_bar_unlocked()
                elapsed = time.monotonic() - self._start
                sys.stderr.write(f"[eval {elapsed:6.1f}s] [{current}/{self.total}] {label}\n")
                sys.stderr.flush()

    def _advance(self, label: str) -> int:
        with self._lock:
            self._done += 1
            current = self._done
        self.update(current, label)
        return current

    def paper_skip(self, paper_id: str) -> None:
        self._advance(f"skip {paper_id}")
        self.info(f"{paper_id}: 跳过（四件套结果已齐全，使用 --force 可重跑）")

    def paper_start(self, paper_id: str) -> None:
        self.info(f"{paper_id}: 开始评估")

    def paper_llm_bridge(
        self,
        paper_id: str,
        *,
        alloy_matches: int,
        process_matches: int,
        sample_matches: int,
        error: str | None,
    ) -> None:
        if error:
            short = error.replace("\n", " ")[:120]
            self.info(f"{paper_id}: LLM 桥接失败 — {short}")
            return
        self.info(
            f"{paper_id}: LLM 桥接 OK — "
            f"alloy={alloy_matches}, process={process_matches}, sample={sample_matches}"
        )

    def paper_empty_prediction(self, paper_id: str, *, skipped: bool) -> None:
        tag = "跳过且为空预测" if skipped else "空预测"
        self.info(f"{paper_id}: {tag}（prediction 无有效 section 或缺少 JSON）")

    def paper_done(
        self,
        paper_id: str,
        *,
        structure_f1: float | None,
        fact_f1: float | None,
        prediction_empty: bool,
    ) -> None:
        self._advance(f"done {paper_id}")
        parts = [f"{paper_id}: 完成"]
        if prediction_empty:
            parts.append("空预测")
        if structure_f1 is not None:
            parts.append(f"structure_f1={structure_f1:.3f}")
        if fact_f1 is not None:
            parts.append(f"fact_f1={fact_f1:.3f}")
        self.info(" | ".join(parts))

    def finish(self, message: str) -> None:
        if self.quiet:
            return
        with self._lock:
            self._clear_bar_unlocked()
        elapsed = time.monotonic() - self._start
        sys.stderr.write(f"[eval {elapsed:6.1f}s] {message}\n")
        sys.stderr.flush()

    @staticmethod
    def format_global_summary(report: dict) -> str:
        global_eval = report.get("global_evaluation", {})
        structure = global_eval.get("structure", {})
        facts = global_eval.get("facts", {})
        summary = report.get("dataset_summary", {})
        processed = summary.get("processed_paper_count", "?")
        empty = summary.get("empty_prediction_count", 0)
        empty_ids = summary.get("empty_prediction_paper_ids") or []
        empty_line = f"已处理 {processed} 篇，空预测 {empty} 篇"
        if empty_ids:
            empty_line += f": {', '.join(empty_ids)}"
        elif empty:
            empty_line += "（未记录 paper_id，请查 paper_index.prediction_empty）"
        lines = [
            empty_line,
            (
                "全局 structure — "
                f"P={structure.get('precision', 0):.3f} "
                f"R={structure.get('recall', 0):.3f} "
                f"F1={structure.get('f1', 0):.3f}"
            ),
            (
                "全局 facts — "
                f"P={facts.get('precision', 0):.3f} "
                f"R={facts.get('recall', 0):.3f} "
                f"F1={facts.get('f1', 0):.3f}"
            ),
        ]
        return "\n".join(lines)
