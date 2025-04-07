# (WiP) Leveraging LLM to turn Unstructured Data to Data Ontologies

DRAFT README.md

This project showcases an end-to-end data science and NLP pipeline that transforms 
unstructured regulatory text into structured, ontology-driven insights to support drug 
launch strategy and market access planning.

Using large language models (LLMs), we extract key concepts such as access decisions,
clinical evidence gaps, and cost-related concerns, and map them into a custom-built
ontology of access barriers. This enables analytics teams and market access strategists
to quickly identify trends and recurring issues that impact pricing, reimbursement,
and approval outcomes across different regions.

# Project Highlights

- Real-world unstructured data
- ETL Pipeline
- LLM-based concept extraction + classification
- Hybrid data architecture (SQL + graph model)
- Custom ontology creation + iterative refinement

# Technologies & Concepts

- Data Engineering – ETL workflows, structured output in SQL format, graph-based 
knowledge modeling
- Large Language Models (LLMs) – Fine-Tuning Models and Prompt Engineering 
(zero-shot/few-shot/chain-of-though) prompting with OpenAI
- NLP Pipeline – PDF parsing, sentence segmentation, prompt engineering, entity 
normalization
- Ontology Engineering – create and expand a domain-specific taxonomy (access barriers),
 supported by GPT and semantic clustering
- Analytics & Visualization – aggregation of barrier frequency, cross-country comparison,
 time series of decisions