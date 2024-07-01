"""
### dbt dag -- dbt deps & run
"""
from __future__ import annotations

import datetime as dt
from pathlib import Path

import pendulum
from airflow.operators.dummy import DummyOperator
from airflow.decorators import dag
from airflow_dbt.operators.dbt_operator import (
  DbtDepsOperator,
  DbtRunOperator
)
from config.dag import build_default_args

dag_args = build_default_args()


@dag(
    dag_id=Path(__file__).stem,
    tags=["dbt"],
    description=__doc__[0: __doc__.find(".")],
    doc_md=__doc__,
    default_args=dag_args,
    start_date=pendulum.datetime(2023, 9, 1, tz="Africa/Casablanca"),
    schedule=None,
    catchup=False,
    dagrun_timeout=dt.timedelta(minutes=60),
)
def generate_dag() -> None:
    dbt_home = "/opt/airflow/dbts"
    dbt_target = "dev"

    start = DummyOperator(task_id="start")
    end = DummyOperator(task_id="end")


    start_ingestion = DummyOperator(task_id="start_ingestion")
    end_ingestion = DummyOperator(task_id="end_ingestion")


    task_dbt_run_ingestion = DbtRunOperator(
        task_id="task_dbt_run_ingestion",
        dir=dbt_home,
        profiles_dir=dbt_home,
        target=dbt_target,
        models="ingestion",
        full_refresh=False,
    )

    start_bronze = DummyOperator(task_id="start_bronze")
    end_bronze = DummyOperator(task_id="end_bronze")


    task_dbt_run_bronze = DbtRunOperator(
        task_id="task_dbt_run_bronze",
        dir=dbt_home,
        profiles_dir=dbt_home,
        target=dbt_target,
        models="semantic_layer.bronze",
        full_refresh=False,
    )

    start_silver = DummyOperator(task_id="start_silver")
    end_silver = DummyOperator(task_id="end_silver")

    task_dbt_run_silver = DbtRunOperator(
        task_id="task_dbt_run_silver",
        dir=dbt_home,
        profiles_dir=dbt_home,
        target=dbt_target,
        models="semantic_layer.silver",
        full_refresh=False,
    )

    start_gold = DummyOperator(task_id="start_gold")
    end_gold = DummyOperator(task_id="end_gold")

    task_dbt_run_gold = DbtRunOperator(
        task_id="task_dbt_run_gold",
        dir=dbt_home,
        profiles_dir=dbt_home,
        target=dbt_target,
        models="semantic_layer.gold",
        full_refresh=False,
    )

    start_ingestion >> task_dbt_run_ingestion
    task_dbt_run_ingestion >> end_ingestion
    end_ingestion >> start_bronze
    start_bronze >> task_dbt_run_bronze >> end_bronze
    end_bronze >> start_silver
    start_silver >> task_dbt_run_silver >> end_silver
    end_silver >> start_gold
    start_gold >> task_dbt_run_gold
    task_dbt_run_gold >> end_gold

generate_dag()

if __name__ == "__main__":
    dag.test()
