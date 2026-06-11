#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

PAPER_IDS="${1:-A0,A1,A2,A3,A4}"
WORKERS="${WORKERS:-1}"
FORCE_FLAG="${FORCE_FLAG:-}"

echo "[verify demo] project: $(pwd)"
echo "[verify demo] papers:  ${PAPER_IDS}"
echo "[verify demo] workers: ${WORKERS}"
if [[ -n "${FORCE_FLAG}" ]]; then
  echo "[verify demo] force:   ${FORCE_FLAG}"
else
  echo "[verify demo] force:   disabled; existing outputs will be skipped"
fi

echo
echo "[1/2] Running verify..."
python3 run_verify.py \
  --paper-ids "${PAPER_IDS}" \
  --workers "${WORKERS}" \
  ${FORCE_FLAG}

echo
echo "[2/2] Running verify_eval before/after compare..."
python3 run_verify_eval.py \
  --paper-ids "${PAPER_IDS}" \
  --compare-verify \
  --workers "${WORKERS}" \
  ${FORCE_FLAG}

echo
echo "[verify demo] done"
echo "[verify demo] compare reports:"
IFS=',' read -ra IDS <<< "${PAPER_IDS}"
for paper_id in "${IDS[@]}"; do
  paper_id="$(echo "${paper_id}" | xargs)"
  [[ -z "${paper_id}" ]] && continue
  echo "  outputs_dataset/${paper_id}/verify_compare/compare_report.md"
done
