# Chemical Structure Extraction Benchmark

**Author:** Sanika Mahesh Potphode  
**Assignment:** 1.2 Individual Benchmarking Code

## Project overview

This project evaluates a pipeline that detects chemical drawings in
scientific PDFs and converts them into SMILES.

- MolDetv2 locates molecular drawings.
- MolGlyph recognizes each cropped drawing.
- BioMiner conversion utilities produce SMILES.
- RDKit validates predictions and calculates comparison metrics.

The pretrained models run on a CPU. No model training is performed.

## Dataset

The course-provided Dataset.zip contains six PDFs:
1, 2, 4, 6, 16, and 19, totaling 104 pages.

The reference CSV contains 222 entries representing 220 unique
structures when duplicates are removed within each paper.

Obtain the PDFs and reference CSV from the course page.

## Required local files

Place the following beside the notebook:

- `Dataset 2/Dataset/`: the six PDFs and reference CSV.
- `BioMiner-main/`: the extracted BioMiner source repository.
- `BioMiner-main/molglyph_large.pt`: MolGlyph weights.
- `moldet_v2_yolo11n_960_doc.pt`: MolDetv2 weights.

Keep the reference filename unchanged:
`ground_truth_SMILES_confirmed_1,2,4,6,16,19.csv`

Download sources:

- BioMiner: https://github.com/jiaxianyan/BioMiner
- MolGlyph: https://huggingface.co/jiaxianustc/MolGlyph
- MolDetv2: https://huggingface.co/UniParser/MolDetv2

Model weights and source downloads are required separately.

## Setup and execution

Use Python 3.10. From the project folder, after extracting BioMiner:

```bash
python -m pip install -r requirements_course.txt
```

Open `Sanika Potphode_1.2_Individual_Benchmarking_Code.ipynb`
in VS Code or Jupyter and select the environment containing these packages.

Restart the kernel and run all cells from top to bottom.
Keep the working directory set to the project folder.

The notebook was successfully run from a fresh kernel on Windows
with Python 3.10.22 and CPU inference.

Running it again replaces the generated results.

## Methods

PDF pages are rendered at 200 DPI. Detection uses an input size of
960 and confidence threshold of 0.5. Crops include a 10-pixel margin.

Predictions are converted using BioMiner utilities and canonicalized
with RDKit using isomeric SMILES.

Exact structure recovery measures the proportion of unique reference
structures appearing among predictions from the same paper.
Repeated predictions do not increase recovery.

Best available Tanimoto similarity compares each reference with its
closest valid prediction from the same paper, using Morgan fingerprints
with radius 2, 2,048 bits, and chirality enabled.

This similarity metric allows prediction reuse. It is a diagnostic
measure, not paired recognition accuracy or molecule-label accuracy.

## Results

| Metric | Result |
|---|---:|
| PDFs processed | 6 |
| Pages processed | 104 |
| Detected crops | 235 |
| Valid predictions | 229 |
| Unresolved predictions | 4 |
| Invalid predictions | 2 |
| Recognition exceptions | 0 |
| Exact structure recovery | 60/220 (27.3%) |
| Mean best available Tanimoto | 0.7583 |
| Detection stage time | 30.04 seconds |
| Recognition stage time | 715.97 seconds |

Timing excludes model loading and CSV checkpoint writes.
Detection stage time includes page rendering and crop saving.

| Paper | Exactly recovered / unique references |
|---|---:|
| 1 | 17/17 |
| 2 | 9/34 |
| 4 | 14/60 |
| 6 | 0/1 |
| 16 | 1/4 |
| 19 | 19/104 |

## Output files

Generated files are saved in `course_results/`:

- `detected_crops.csv`: crop locations and detector confidence.
- `page_detection_summary.csv`: page-level detection counts and times.
- `course_predictions.csv`: raw outputs, SMILES, statuses, and times.
- `exact_structure_recovery.csv`: recovery results by paper.
- `reference_recovery_details.csv`: reference-level recovery and similarity.
- `course_benchmark_summary.csv`: overall results.
- `exact_recovery_by_paper.png`: results chart.
- `crops/`: detected molecular images.

## Limitations

Valid SMILES do not guarantee correct recognition.

The evaluation does not automatically connect structures to molecule names,
expand Markush structures, or extract bioactivity information.
It evaluates selected BioMiner components rather than the full system.

Unrecovered references can reflect detection, recognition, conversion,
or representation differences. Detection accuracy cannot be measured
separately without annotated bounding boxes.

Only six papers and one pipeline configuration were evaluated.
Training-data overlap was not audited.