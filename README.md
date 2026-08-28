# Data Engineering Study

Python / AWS / Apache Airflow を使用して、データエンジニアリングの基礎から
クラウド上のデータパイプライン構築までを段階的に学習するためのリポジトリです。

CSVを利用したローカルETLから始め、
Parquet、Amazon S3、AWS Glue、Amazon Athena、Apache Spark / PySpark、
Apache Airflowを利用したワークフローオーケストレーションまで実装しています。

現在は、Airflowを中心に

**S3 → AWS Glue → Athena**

を連携したデータパイプラインまで構築しています。

---

## Architecture

現在の主なデータパイプラインは以下の構成です。

```mermaid
flowchart TD
    A[Source Data] --> B[Amazon S3]
    B --> C[Airflow S3KeySensor]
    C --> D[AWS Glue ETL Job]
    D --> E[PySpark]
    E --> F[Amazon S3 / Parquet]
    F --> G[Glue Data Catalog]
    G --> H[Amazon Athena]
    H --> I[Airflow Validation Task]
