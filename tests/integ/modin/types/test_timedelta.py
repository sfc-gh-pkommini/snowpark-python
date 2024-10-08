#
# Copyright (c) 2012-2024 Snowflake Computing Inc. All rights reserved.
#
import datetime
import logging

import modin.pandas as pd
import pandas as native_pd

from snowflake.snowpark.modin.plugin._internal.snowpark_pandas_types import (
    TIMEDELTA_WARNING_MESSAGE,
)
from tests.integ.modin.sql_counter import sql_count_checker
from tests.integ.modin.utils import (
    assert_series_equal,
    create_test_dfs,
    create_test_series,
    eval_snowpark_pandas_result,
)


@sql_count_checker(query_count=1)
def test_create_timedelta_column_from_pandas_timedelta(caplog):
    pandas_df = native_pd.DataFrame(
        {"timedelta_column": [native_pd.Timedelta(nanoseconds=1)], "int_column": [3]}
    )
    with caplog.at_level(logging.DEBUG):
        snow_df = pd.DataFrame(pandas_df)
    assert TIMEDELTA_WARNING_MESSAGE in caplog.text
    eval_snowpark_pandas_result(snow_df, pandas_df, lambda df: df)


@sql_count_checker(query_count=1)
def test_create_timedelta_series_from_pandas_timedelta():
    eval_snowpark_pandas_result(
        *create_test_series(
            [
                native_pd.Timedelta(
                    weeks=5,
                    days=27,
                    hours=23,
                    minutes=59,
                    seconds=59,
                    milliseconds=999,
                    microseconds=999,
                    nanoseconds=1,
                ),
                None,
            ]
        ),
        lambda s: s
    )


@sql_count_checker(query_count=1)
def test_create_timedelta_column_from_datetime_timedelta():
    eval_snowpark_pandas_result(
        *create_test_dfs(
            {"timedelta_column": [datetime.timedelta(days=1)], "int_column": [3]}
        ),
        lambda df: df
    )


@sql_count_checker(query_count=0)
def test_timedelta_dataframe_dtypes():
    eval_snowpark_pandas_result(
        *create_test_dfs(
            {
                "timedelta_column": [native_pd.Timedelta(nanoseconds=1)],
                "int_column": [3],
            }
        ),
        lambda df: df.dtypes,
        comparator=assert_series_equal
    )


@sql_count_checker(query_count=0)
def test_timedelta_series_dtypes():
    eval_snowpark_pandas_result(
        *create_test_series([native_pd.Timedelta(1)]),
        lambda s: s.dtype,
        comparator=lambda snow_type, pandas_type: snow_type == pandas_type
    )
