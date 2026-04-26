# 🏦 Real-Time Bank Fraud Detection Platform

> A production-grade, end-to-end data engineering pipeline built on AWS — detecting fraudulent transactions in real-time using event streaming, serverless computing, and modern data transformation.

---

## 🏗️ Architecture Overview

```
Bank Transactions
      │
      ▼
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Amazon Kinesis  │────▶│  AWS Lambda      │────▶│   Amazon S3     │
│  Data Streams    │     │  (Fraud Detector)│     │  (Bronze Layer) │
└─────────────────┘     └──────────────────┘     └────────┬────────┘
                                                           │
                                                           ▼
                                                ┌─────────────────────┐
                                                │  Redshift Spectrum   │
                                                │  (External Table)    │
                                                └──────────┬──────────┘
                                                           │
                                                           ▼
                                                ┌─────────────────────┐
                                                │       dbt            │
                                                │  Silver: Clean+Dedup │
                                                │  Gold: Features      │
                                                └──────────┬──────────┘
                                                           │
                                                           ▼
                                                ┌─────────────────────┐
                                                │   Apache Airflow     │
                                                │  (Orchestration)     │
                                                └─────────────────────┘
```

---

## 🚀 Tech Stack

| Layer | Technology |
|-------|-----------|
| **Streaming** | Amazon Kinesis Data Streams |
| **Processing** | AWS Lambda (Docker/ECR) |
| **Storage** | Amazon S3 (Data Lake) |
| **Query Engine** | Amazon Redshift Serverless + Spectrum |
| **Transformation** | dbt (data build tool) |
| **Orchestration** | Apache Airflow 3.x |
| **Infrastructure** | Terraform |
| **Security** | AWS IAM |
| **Containerization** | Docker |

---

## 📐 Data Architecture (Medallion)

### 🥉 Bronze Layer — Raw Ingestion
- Real-time transactions streamed via **Kinesis** and processed by **Lambda**
- Raw JSON files stored in S3 partitioned by `year/month/day/hour`
- Schema: `transaction_id`, `account_id`, `amount`, `currency`, `transaction_type`, `timestamp`, `device_id`, `location`, `is_fraud`, `processed_at`

### 🥈 Silver Layer — Cleaned Data (dbt)
- Deduplication using `transaction_id` with `ROW_NUMBER()`
- Type casting for all columns
- Materialized as **table** in Redshift

### 🥇 Gold Layer — Feature Engineering (dbt)
- ML-ready features per account:
  - `avg_transaction_7d` — Average transaction amount over last 7 days
  - `total_spent_30d` — Total spending over last 30 days
  - `transaction_count_per_day` — Daily transaction frequency (30-day avg)
  - `location_diversity_30d` — Number of unique locations in last 30 days
  - `fraud_count` / `fraud_amount` — Fraud aggregations

---

## 📁 Project Structure

```
Fraud-Detection-AWS/
├── terraform/                    # Infrastructure as Code
│   ├── main.tf                   # Root module
│   ├── variables.tf
│   ├── terraform.tfvars.example  # Template (no secrets)
│   └── modules/
│       ├── streaming/            # Kinesis + Lambda + ECR
│       │   └── assets/
│       │       ├── lambda_function.py
│       │       └── Dockerfile
│       ├── storage/              # S3 + Redshift Serverless
│       └── security/             # IAM Roles + Security Groups
├── dbt/
│   ├── profiles.yml.example      # Template (no secrets)
│   └── fraud_detection/
│       └── models/
│           ├── bronze/           # Source definitions
│           ├── silver/           # stg_transactions.sql
│           └── gold/             # fct_fraud_features.sql
├── dags/
│   └── fraud_detection_dag.py    # Airflow DAG
├── simulator/
│   └── producer.py               # Transaction data simulator
├── docker-compose.yaml           # Airflow stack
└── .gitignore
```

---

## ⚙️ Infrastructure (Terraform)

All AWS resources are provisioned via Terraform with modular design:

- **`module.streaming`** — Kinesis stream, ECR repository, Lambda function, event source mapping
- **`module.storage`** — S3 data lake bucket, Redshift Serverless namespace & workgroup
- **`module.security`** — IAM roles for Lambda & Redshift Spectrum, Security Groups

> VPC and subnets are referenced via `data sources` — no hardcoded IDs.

---

## 🔄 Airflow Pipeline

The DAG `fraud_detection_full_pipeline` runs **hourly** and orchestrates:

```
dbt_run ──▶ dbt_test
```

- `dbt_run` — Executes Silver and Gold transformations via **DockerOperator**
- `dbt_test` — Runs dbt data quality tests, halts pipeline on failure

---

## 🛠️ Getting Started

### Prerequisites
- AWS CLI configured
- Terraform >= 1.0
- Docker Desktop
- Python 3.9+

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/Fraud-Detection-AWS.git
cd Fraud-Detection-AWS
```

### 2. Configure credentials
```bash
# Terraform
cp terraform/terraform.tfvars.example terraform/terraform.tfvars
# Fill in your values

# dbt
cp dbt/profiles.yml.example dbt/profiles.yml
# Fill in your Redshift credentials

# Airflow
cp .env.example .env
# Fill in FERNET_KEY and other secrets
```

### 3. Deploy infrastructure
```bash
# Login to ECR first
TOKEN=$(aws ecr get-login-password --region ap-southeast-1)
docker login --username AWS --password $TOKEN <account_id>.dkr.ecr.ap-southeast-1.amazonaws.com

cd terraform
terraform init
terraform apply
```

### 4. Start Airflow
```bash
docker-compose up -d
```

Access Airflow UI at `http://localhost:8080` (default: `airflow/airflow`)

### 5. Run dbt manually
```bash
docker run --rm \
  -v "$(pwd)/dbt:/usr/app/dbt" \
  -v "$(pwd)/dbt/profiles.yml:/root/.dbt/profiles.yml" \
  -w /usr/app/dbt/fraud_detection \
  ghcr.io/dbt-labs/dbt-redshift:1.8.0 \
  run
```

---

## 🔒 Security Notes

- All secrets managed via `.env` and `terraform.tfvars` — **never committed to git**
- IAM roles follow **least privilege** principle
- Redshift Spectrum role has **read-only** S3 access
- ECR token rotates every **12 hours** — re-login required before each deploy

---

## 👤 Author

**Suriya** — Data Engineer  
Built with ☕ and a lot of Terraform debugging