# Islamic Writing HBKU

A private research codebase for computational analysis of Islamic writing using both qualitative and quantitative language-model agents.

## Project Overview
This project explores automated methods for assessing style, authenticity, and thematic consistency in Islamic texts and user-generated responses. It combines:

* **Qualitative Agent** – Performs faith-aligned critique and generates narrative feedback.
* **Quantitative Agent** – Scores responses against multiple rubrics and statistical measures.
* **Search Tools** – Fast lookup utilities for Qurʼānic āyāt, ḥadith, and open-web references.

The goal is to develop reproducible evaluation pipelines that aid researchers in studying Islamic writing quality at scale while preserving scholarly rigor.

## Repository Layout
* `Agents/` – Agent classes orchestrating calls to LLMs.
* `Configs/` – Centralised parameter settings (models, temperature, etc.).
* `Dataset/` – Raw CSV files containing prompt/response pairs.
* `Prompts/` – System prompts that condition each agent.
* `Tools/` – Domain-specific retrieval helpers (āyah, ḥadith, internet).
* `Results/` – Cached JSON outputs produced by each run.
* `Utils/` – Generic helpers (dataset loaders, etc.).

## Quick Start
1. Clone this **private** repository (access required).
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the main entry point:
   ```bash
   python main.py
   ```
4. Outputs will be written to `Results/`.

## Customising Experiments
* **Datasets** – Add new CSVs to `Dataset/` following the existing column format.
* **Prompts** – Edit Markdown files in `Prompts/` to tweak evaluation criteria.
* **Config Flags** – Adjust `model settings`, `paths`, and other settings via `Configs/configs.py`.

## Reproducing Figures
Visualization scripts (forthcoming) will read JSON results and output graphs into `Vis_Graphs/`.
