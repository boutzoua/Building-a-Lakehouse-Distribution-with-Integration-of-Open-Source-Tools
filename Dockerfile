FROM apache/airflow:2.8.2-python3.10

RUN pip install plyvel ckanapi pendulum