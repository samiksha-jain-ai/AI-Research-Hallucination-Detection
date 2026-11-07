# Dataset and scored records

Original data: HaluEval `general_data.json`, project source https://github.com/RUCAIBox/HaluEval . Confirm its current license/terms before redistributing the original text. The original full file and sampled text are **not included** here.

Included: train/validation/test **derived numeric scores and labels**, 420/90/90 records. Original source IDs were lost in Prompt 09A; split-prefixed `ID` values are synthetic. This means source-level overlap cannot be independently ruled out from these CSVs. The earlier notebook recorded no normalized-question overlap, but text is absent from these files.

Scoring: DistilGPT-2 as a surrogate for another model's generated answers; answer-only token NLL; first boundary-crossing token excluded. The 600 scores were not independently recomputed in full. See `results/baseline_validation.md`.
