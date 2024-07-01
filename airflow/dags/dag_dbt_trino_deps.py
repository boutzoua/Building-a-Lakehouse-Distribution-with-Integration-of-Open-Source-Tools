"""
### dbt dag -- dbt deps
"""
from __future__ import annotations

import datetime as dt
from pathlib import Path

import pendulum
from airflow.operators.dummy import DummyOperator
from airflow.decorators import dag
from airflow_dbt.operators.dbt_operator import (
  DbtDepsOperator,

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

    task_dbt_deps = DbtDepsOperator(
        task_id="task_dbt_deps",
        dir=dbt_home,
        profiles_dir=dbt_home,
        target=dbt_target,
        full_refresh=False,
    )

    
    start >> task_dbt_deps 
    task_dbt_deps >> end

generate_dag()

if __name__ == "__main__":
    dag.test()
