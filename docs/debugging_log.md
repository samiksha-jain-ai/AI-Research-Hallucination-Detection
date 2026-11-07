# Prompt 11 — Debugging and AI-Assistance Log

## Case: Overlapping identifiers and failed ID restoration

**Project:** Token-Level Uncertainty as a Predictor of Hallucination in Large Language Models  
**Stage:** Prompt 10 validation / Prompt 11 debugging  
**Model:** DistilGPT-2 (surrogate uncertainty scorer)  
**Data:** HaluEval general dataset, 600 sampled responses; train 420, validation 90, test 90

### 1. Relevant code

The attempted repair loaded the Prompt 09A split CSVs and assumed that they retained original dataset IDs:

```python
assert len(original) == len(scored)
assert "ID" in original.columns
assert original["ID"].notna().all()
assert original["ID"].astype(str).is_unique
```

The earlier Prompt 09A preprocessing had selected only:

```python
required = ["user_query", "chatgpt_response", "hallucination"]
df = raw[required].copy()
```

The Prompt 09B scoring code used a fallback row index when the `ID` field was missing:

```python
"ID": str(rec["ID"]) if "ID" in frame.columns else str(idx)
```

### 2. Actual observed output

During validation, the user observed `ID overlap across splits: True`. The first repair attempt failed:

```text
AssertionError
...
25 assert "ID" in original.columns
```

The corrected repair produced:

```text
train example IDs: ['train_0', 'train_1', 'train_2']
validation example IDs: ['validation_0', 'validation_1', 'validation_2']
test example IDs: ['test_0', 'test_1', 'test_2']
=== SCORE INTEGRITY === PASS
Total unique IDs: 600
Total scored rows: 600
```

A subsequent Prompt 10 notebook reported `Overlapping input IDs: True`, followed by `ID INTEGRITY: PASS`, per-split audits marked PASS, `SCORE INTEGRITY: PASS`, and `INDEPENDENT SMOKE AUDIT: PASS`. The original-row audit was explicitly reported as `NOT PERFORMED`.

### 3. Expected behavior

Each scored response should have a stable identifier unique across train, validation, and test. Identifier repair must preserve all labels, scores, and row order. Ideally original HaluEval source IDs would also be preserved, but they were absent from the exported split CSVs.

### 4. Confirmed evidence and hypotheses

**Confirmed from supplied code and outputs**
- Prompt 09A dropped the `ID` field before exporting splits.
- Prompt 09B used per-split row positions as fallback IDs, allowing collisions between splits.
- The attempted restoration assumed `ID` existed in Prompt 09A CSVs; the assertion failed.
- Split-prefixed identifiers yielded 600 unique experiment IDs without changing saved score values.
- An independent arithmetic smoke test compared cross-entropy and negative gathered log-softmax losses on a synthetic example and passed.

**Not established / possible follow-up**
- Original HaluEval source IDs might be reconstructed by exact matching against the source dataset, subject to uniqueness checks; this was not performed.
- The independent arithmetic smoke test does not establish that every saved NLL value was correctly computed for its source row.
- The optional nine-row original-response recomputation was not run.

### 5. Minimal safe correction

```python
for split in ["train", "validation", "test"]:
    df = frames[split].copy()
    assert df["row_index"].notna().all()
    assert df["row_index"].is_unique
    assert set(df["row_index"].astype(int)) == set(range(len(df)))
    df["ID"] = split + "_" + df["row_index"].astype(int).astype(str)
    repaired[split] = df
```

**Why each change is needed:**
1. `notna()` prevents missing row indices from silently producing invalid identifiers.
2. `is_unique` prevents duplicate IDs *within* a split.
3. The range check ensures indices represent one complete local row sequence.
4. Prefixing with `split` prevents collisions *between* splits.
5. Copying the DataFrame and modifying only `ID` preserves the original scores and labels.

These are **synthetic experiment-specific IDs**, not recovered HaluEval source IDs.

### 6. Verification test

```python
import pandas as pd
import numpy as np

all_ids = pd.concat([repaired[s]["ID"] for s in ["train", "validation", "test"]], ignore_index=True)
assert len(all_ids) == 600
assert all_ids.is_unique
for split in ["train", "validation", "test"]:
    for col in ["label", "mean_nll", "p90_nll", "answer_token_length"]:
        assert np.array_equal(repaired[split][col].to_numpy(), frames[split][col].to_numpy())
print("ID AND SCORE PRESERVATION: PASS")
```

**Reported verification outcome:** The user ran the ID repair and obtained `SCORE INTEGRITY: PASS` with 600 unique IDs. The Prompt 10 score-file audit and independent arithmetic smoke audit also passed. The exact verification snippet above is supplied for reproducibility; no claim is made that this exact snippet was separately executed.

### 7. Edge case

If `row_index` is duplicated inside `train`, both rows would become `train_<same index>`, so split prefixes alone would not solve the problem. The uniqueness assertion must stop the repair in that case. A second edge case is a missing or non-integer index; do not silently coerce it into a fabricated source ID.

### 8. Effect on earlier results

**No rerun required:** Model inference and token-level scoring for the 600 responses, because only identifiers were changed and score columns were verified unchanged.

**May need rerun:** Any downstream aggregation, merge, or deduplication keyed on the original overlapping `ID` field. Such results should be regenerated using the repaired files. This does not apply to downstream evaluations that were not yet performed.

**Still optional:** Recompute a sample of original rows using `AITR_Prompt09_data.zip` to verify alignment between source text and saved scores. This was not performed in the shared Prompt 10 run.

### 9. AI-assistance disclosure

AI assistance was used to diagnose the overlapping IDs, propose an initial restoration strategy, identify the mistaken assumption after the user supplied the actual `AssertionError`, and provide a minimal split-prefix repair plus validation code. The first AI-suggested repair was incorrect because it assumed the split CSVs contained original `ID` values. The user ran the code in Google Colab and supplied actual outputs. No execution logs or benchmark results have been invented.

### 10. Resolution status

**Resolved:** ID collision and score-file integrity checks.  
**Passed:** Independent NLL arithmetic smoke test on a synthetic example.  
**Not performed:** Original-row score recomputation and original HaluEval ID recovery.  
**Next stage:** Prompt 12, after retaining the repaired score ZIP and this debugging log.
