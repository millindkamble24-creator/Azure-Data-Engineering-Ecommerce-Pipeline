\# E-Commerce Data Engineering Pipeline



\## Project Overview



This project simulates an e-commerce data engineering workflow using synthetic retail data.



The project currently focuses on generating datasets, profiling source data, and preparing the foundation for data-quality validation and cloud-based data processing.



\## Current Implementation



\* Generated 316,000 synthetic records across seven datasets.

\* Created customer, product, order, order-item, payment, return, and website-event datasets.

\* Generated incremental datasets to simulate new orders and changed customer records.

\* Created sample data containing intentional quality issues for testing.

\* Implemented a Python dataset-profiling script.

\* Examined dataset dimensions, data types, missing values, duplicate rows, unique values, numeric statistics, and sample records.



\## Datasets



| Dataset        |     Records |

| -------------- | ----------: |

| Customers      |      10,000 |

| Products       |       1,000 |

| Orders         |      50,000 |

| Order Items    |     100,000 |

| Payments       |      50,000 |

| Returns        |       5,000 |

| Website Events |     100,000 |

| \*\*Total\*\*      | \*\*316,000\*\* |



\## Technologies



\* Python

\* pandas

\* NumPy

\* Git and GitHub



\## Planned Enhancements



\* Validate primary and foreign key relationships.

\* Implement data-quality rules.

\* Convert raw date and timestamp fields to appropriate data types.

\* Ingest source data into Azure Data Lake Storage.

\* Develop Bronze, Silver, and Gold data layers.

\* Orchestrate the pipeline using Azure Data Factory.

\* Implement transformations using Azure Databricks and Apache Spark.

\* Add logging, error handling, and pipeline monitoring.



\## Project Status



\*\*Current stage:\*\* Synthetic data generation and dataset profiling.



The Azure ingestion, transformation, and orchestration stages are planned enhancements and should not be considered implemented until they are built and tested.



