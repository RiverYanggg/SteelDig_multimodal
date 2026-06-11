# Unit Normalization Module

Implementation:

```text
paper_extractor/unit_normalization/
run_unit_normalization.py
```

## Purpose

Normalize explicit units in `final/text_extraction.json` to canonical engineering units before verification and evaluation.

It is deterministic and does not call an LLM.

## Best Timing

Run it after:

```text
final/text_extraction.json
```

and before:

```text
verify/text_extraction_fixed.json
```

This timing is best because post-parse has already produced stable JSON, and verify/evaluation can then compare values in one unit system.

## Input And Output

Input:

```text
outputs_dataset/<paper_id>/final/text_extraction.json
```

Output:

```text
outputs_dataset/<paper_id>/normalized/text_extraction_units.json
outputs_dataset/<paper_id>/normalized/unit_normalization_report.json
```

The original `final/text_extraction.json` is not modified.

## Run

```bash
python3 steeldig.py units -- \
  --dataset-root outputs_dataset \
  --paper-ids A0,A1 \
  --force
```

`run_verify.py` also runs this automatically unless `--skip-unit-normalization` is passed.

## Canonical Units

- temperature: `°C`
- duration: `h`
- stress, strength, modulus, strain hardening rate: `MPa`
- length, grain size, precipitate size: `μm`
- composition and ratios: `%`
- hardness: `HV`
- density: `g/cm^3`
- mass gain: `mg/cm^2`
- energy density: `mJ/m^2`
- fracture toughness: `MPa·m^0.5`
- rate: `s^-1`

