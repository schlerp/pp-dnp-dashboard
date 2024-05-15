import os

import streamlit as st
import pandas as pd
import plotly.express as px

on_hardship_with_payment_plan_sql = """
SELECT
    ha.account_id,
    ha.start_date,
    ha.end_date,
    CASE
        WHEN pp.status IN ('ACTIVE', 'ACCEPTED') THEN 'ACTIVE'
        ELSE 'INACTIVE'
    END AS payment_plan_status
FROM
    hardship_agreements_hardshipagreement ha
    LEFT JOIN (
        SELECT distinct on (account_id)
            account_id,
            status
        FROM
            payments_paymentplan
        ORDER BY account_id, updated_at desc
    ) pp ON ha.account_id=pp.account_id
WHERE
    (ha.end_date IS NULL OR ha.end_date > CURRENT_DATE)
    --AND
    --pp.status IN ('ACTIVE', 'ACCEPTED', NULL)
--LIMIT 100;
"""


def make_con_string() -> str:
    con_string_template = (
        "postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
    )
    user = os.environ.get("DATABASE_USER")
    password = os.environ.get("DATABASE_PASSWORD")
    host = os.environ.get("DATABASE_HOST")
    port = os.environ.get("DATABASE_PORT", "5432")
    database = os.environ.get("DATABASE_NAME")
    return con_string_template.format(
        user=user, password=password, host=host, port=port, database=database
    )


def show_query_info(sql: str, query_name: str, df: pd.DataFrame):
    with st.expander(f"{query_name}: SQL"):
        st.code(sql, language="sql")
    with st.expander(f"{query_name} Query Result"):
        st.dataframe(df)


def pp_status_for_active_hardship_agreements():
    df = pd.read_sql(on_hardship_with_payment_plan_sql, con=make_con_string())
    st.plotly_chart(
        px.pie(
            df,
            names="payment_plan_status",
            title="Payment Plan status for Active Hardship Agreements",
        )
    )
    show_query_info(
        sql=on_hardship_with_payment_plan_sql,
        query_name="Payment Plan status for Active Hardship Agreements",
        df=df,
    )


st.title("PP & DNP Status Dashboard")
st.header("Payment Plans")
pp_status_for_active_hardship_agreements()
