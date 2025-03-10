# WritingBench: A Comprehensive Benchmark for Generative Writing

## 📖 Overview
WritingBench is a comprehensive benchmark for evaluating LLMs' writing capabilities across **1,239 real-world queries**, spanning:
- 6 primary domains 
- 100 fine-grained subdomains
- 3 core writing requirements: `Style` | `Format` | `Length`

WritingBench integrates diverse sources of materials, averaging 1,546 tokens per source. Each query is paired with 5 instance-specific criteria, scoring either through LLM evaluators or through a finetuned critic model.

![Comaparison](pics/comparision.pdf)

![Statistic](pics/statistic.pdf)

## 📊 Benchmark Construction

![Statistic](pics/construction.pdf)

## 📈 Evaluation Framework

![Statistic](pics/criteria.pdf)

## 🛠 Installation
```bash
git clone https://github.com/yourusername/WritingBench.git
```

## 📂 Repository Structure
```bash
.
├── evaluate_benchmark.py     # Evaluation script
├── prompt.py                 # Prompt templates
├── evaluator/
│   ├── __int__.py
│   └── llm.py                # LLM evaluation interface
└── benchmark_query/
    ├── benchmark_all.jsonl   # Full dataset (1239 queries)
    └── requirement/
        ├── style/            # Style-specific subsets
        │   ├── style_subset.jsonl
        │   └── style_subset_C.jsonl
        ├── format/           # Format-specific subsets
        │   ├── format_subset.jsonl
        │   └── format_subset_C.jsonl
        └── length/           # Length-specific subsets
            ├── length_subset.jsonl
            └── length_subset_C.jsonl
```

## 🚀 Quick Start

1. Add your API credentials:
- For LLM-as-a-Judge, see evaluator/llm.py
```bash
  self.api_key = "your_api_key_here"
  self.url = "Your API endpoint"
  self.model = "Chose your model name"
```
- For critic model (coming soon)

2. Choose appropriate evaluation sets from benchmark_query/
```bash
python evaluate_benchmark.py \
  --query_criteria_file query_set.jsonl \
  --input_file samples.jsonl \
  --output_file scores.jsonl
```

## 📊 Benchmark Construction

📜 Citation
