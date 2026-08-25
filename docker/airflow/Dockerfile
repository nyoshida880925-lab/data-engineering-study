FROM apache/airflow:3.3.1

RUN pip install --no-cache-dir \
    "apache-airflow==${AIRFLOW_VERSION}" \
    "apache-airflow-providers-amazon==9.35.0" \
    "botocore[crt]"
