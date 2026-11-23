"""Validate and canonicalize molecular SMILES from Stage 3."""

import argparse
import csv
from pathlib import Path

from rdkit import Chem

INPUT_COLUMNS = {"crop_id", "paper_id", "raw_smiles"}
OUTPUT_COLUMNS = ("crop_id", "paper_id", "canonical_smiles", "status")


def validate_smiles(raw_smiles: str | None) -> tuple[str, str]:
    """Return canonical SMILES and a valid, invalid, or wildcard status."""
    smiles = (raw_smiles or "").strip()
    if not smiles:
        return "", "invalid"

    parser_options = Chem.SmilesParserParams()
    parser_options.parseName = False
    molecule = Chem.MolFromSmiles(smiles, parser_options)
    if molecule is None or molecule.GetNumAtoms() == 0:
        return "", "invalid"

    canonical_smiles = Chem.MolToSmiles(
        molecule, canonical=True, isomericSmiles=True
    )
    has_wildcard = any(atom.GetAtomicNum() == 0 for atom in molecule.GetAtoms())
    status = "wildcard" if has_wildcard else "valid"
    return canonical_smiles, status


def validate_csv(input_path: Path, output_path: Path) -> None:
    """Write one validation result per prediction, preserving IDs and order."""
    if input_path.resolve() == output_path.resolve():
        raise ValueError("Input and output must be different files.")

    with input_path.open(encoding="utf-8-sig", newline="") as input_file:
        reader = csv.DictReader(input_file)
        missing_columns = INPUT_COLUMNS.difference(reader.fieldnames or [])
        if missing_columns:
            raise ValueError(
                f"Missing input columns: {', '.join(sorted(missing_columns))}"
            )

        with output_path.open("w", encoding="utf-8", newline="") as output_file:
            writer = csv.DictWriter(output_file, fieldnames=OUTPUT_COLUMNS)
            writer.writeheader()

            for row in reader:
                canonical_smiles, status = validate_smiles(row["raw_smiles"])
                writer.writerow(
                    {
                        "crop_id": row["crop_id"],
                        "paper_id": row["paper_id"],
                        "canonical_smiles": canonical_smiles,
                        "status": status,
                    }
                )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_csv", type=Path, help="Stage 3 predictions CSV")
    parser.add_argument("output_csv", type=Path, help="Stage 4 validation CSV")
    args = parser.parse_args()

    try:
        validate_csv(args.input_csv, args.output_csv)
    except (OSError, ValueError) as error:
        parser.exit(1, f"Error: {error}\n")


if __name__ == "__main__":
    main()
