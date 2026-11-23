# Stage 4 — SMILES Validation

This module validates the SMILES strings produced by Stage 3 and prepares them
for Stage 5 evaluation. It preserves `crop_id` and `paper_id` so each result
can be traced to the original prediction.

## Input and output

- Input: `raw_predictions.csv` with `crop_id`, `paper_id`, `raw_smiles`, and
  `inference_time`. The validator uses the first three columns.
- Output: `validated_predictions.csv` with `crop_id`, `paper_id`,
  `canonical_smiles`, and `status`. The module writes one output row per
  input row in the same order.

## Implementation

`validate_smiles.py` contains `validate_smiles()` for individual predictions
and `validate_csv()` for batch processing.

The module trims surrounding whitespace and uses RDKit to parse each SMILES
string and generate canonical SMILES while retaining stereochemistry where
specified. RDKit was chosen to check whether the prediction can be parsed
as a chemical structure and to standardize its representation. The module
uses no pretrained model, image preprocessing, or data augmentation.

- `valid`: RDKit parsed the SMILES and found no wildcard atoms.
- `invalid`: The prediction was blank or could not be parsed. The canonical
  SMILES field is blank.
- `wildcard`: RDKit parsed the SMILES and found at least one wildcard atom,
  which can indicate an unresolved group.

## Run the module

From the repository root, using Python 3.10 or later:

```bash
python -m pip install rdkit
python stage_4_validation/validate_smiles.py raw_predictions.csv validated_predictions.csv
```

Pass the paths to your input and output files as command-line arguments.

## Test evidence

I ran the committed script in a VS Code notebook using Python 3.10 with
three sample predictions.

Sample input:

```csv
crop_id,paper_id,raw_smiles,inference_time
sample-001,sample,OCC,0.10
sample-002,sample,C1CC,0.12
sample-003,sample,*C,0.09
```

Observed output:

```csv
crop_id,paper_id,canonical_smiles,status
sample-001,sample,CCO,valid
sample-002,sample,,invalid
sample-003,sample,*C,wildcard
```

The run matched all three expected results. `OCC` was canonicalized to `CCO`,
`C1CC` was marked invalid because its ring was unclosed, and `*C` was
retained and flagged as a wildcard.
