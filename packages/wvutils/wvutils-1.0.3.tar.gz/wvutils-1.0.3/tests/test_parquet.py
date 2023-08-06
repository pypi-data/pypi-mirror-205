import copy
import io
import os

import boto3
import pandas as pd
import pyarrow as pa
import pytest

# import s3fs
# from fsspec.implementations.arrow import ArrowFSWrapper
from moto import mock_s3
from pytz import utc

from tests.fixtures import temp_dir
from wvutils.parquet import (
    clear_parquet_sessions,
    create_pa_schema,
    export_dataset,
    force_dataframe_dtypes,
    get_parquet_session,
)

BASE_TEMPLATE: dict[str, str] = {
    "key_a": "string",
    "key_b": "integer",
    "key_c": "float",
    "key_d": "bool",
    "key_e": "timestamp[s]",
    "key_f": "timestamp[ms]",
    "key_g": "timestamp[ns]",
    "key_h": "string",
    "key_i": "integer",
}


@pytest.fixture(scope="function")
def primary_template():
    return copy.deepcopy(BASE_TEMPLATE)


BASE_DATA: dict[str, list] = {
    "key_a": ["a", "b", "c", "d", "e", "f"],
    "key_b": [1, 2, 3, 4, 5, 6],
    "key_c": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
    "key_d": [True, False, True, False, True, False],
    "key_e": (
        pd.date_range("2021-01-01", "2021-01-06", tz=utc).astype("int64") // 10**9
    )
    .astype("int64")
    .tolist(),
    "key_f": (
        pd.date_range("2021-01-07", "2021-01-12", tz=utc).astype("int64") // 10**6
    )
    .astype("int64")
    .tolist(),
    "key_g": pd.date_range("2021-01-13", "2021-01-18", tz=utc).astype("int64").tolist(),
    "key_h": ["foo", "bar", "baz", "foo", "bar", "baz"],
    "key_i": [1, 2, 3, 3, 2, 1],
}


def test_create_pa_schema():
    template = {
        "key_a": "string",
        "key_b": "integer",
        "key_c": "float",
        "key_d": "bool",
        "key_e": "timestamp[s]",
        "key_f": "timestamp[ms]",
        "key_g": "timestamp[ns]",
    }
    expected = pa.schema(
        [
            ("key_a", pa.string()),
            ("key_b", pa.int64()),
            ("key_c", pa.float64()),
            ("key_d", pa.bool_()),
            ("key_e", pa.timestamp("s", tz=utc)),
            ("key_f", pa.timestamp("ms", tz=utc)),
            ("key_g", pa.timestamp("ns", tz=utc)),
        ]
    )
    actual = create_pa_schema(template)
    assert actual == expected


def test_create_pa_schema_raises_on_invalid_type_name():
    template = {"key_a": "invalid"}
    with pytest.raises(ValueError, match=r"Unknown type name: 'invalid'"):
        create_pa_schema(template)


def test_force_dataframe_dtypes():
    template = {
        "key_a": "string",
        "key_b": "integer",
        "key_c": "float",
        "key_d": "bool",
        "key_e": "timestamp[s]",
        "key_f": "timestamp[ms]",
        "key_g": "timestamp[ns]",
    }
    df = pd.DataFrame(
        {
            "key_a": ["a", "b", "c"],
            "key_b": [1, 2, 3],
            "key_c": [1.0, 2.0, 3.0],
            "key_d": [True, False, True],
            "key_e": [
                pd.Timestamp("2021-01-01", tz=utc).value // 10**9,
                pd.Timestamp("2021-01-02", tz=utc).value // 10**9,
                pd.Timestamp("2021-01-03", tz=utc).value // 10**9,
            ],
            "key_f": [
                pd.Timestamp("2021-01-01", tz=utc).value // 10**6,
                pd.Timestamp("2021-01-02", tz=utc).value // 10**6,
                pd.Timestamp("2021-01-03", tz=utc).value // 10**6,
            ],
            "key_g": [
                pd.Timestamp("2021-01-01", tz=utc).value,
                pd.Timestamp("2021-01-02", tz=utc).value,
                pd.Timestamp("2021-01-03", tz=utc).value,
            ],
        },
        dtype="object",
    )
    expected = df.copy()
    expected = expected.astype(
        {
            "key_a": str,
            "key_b": int,
            "key_c": float,
            "key_d": bool,
        }
    )
    expected["key_e"] = pd.to_datetime(expected["key_e"], unit="s", utc=True)
    expected["key_f"] = pd.to_datetime(expected["key_f"], unit="ms", utc=True)
    expected["key_g"] = pd.to_datetime(expected["key_g"], unit="ns", utc=True)
    actual = force_dataframe_dtypes(df, template)
    pd.testing.assert_frame_equal(actual, expected)


def test_force_dataframe_dtypes_raises_on_invalid_type_name():
    template = {"key_a": "invalid"}
    df = pd.DataFrame({"key_a": ["a", "b", "c"]}).astype(str)
    with pytest.raises(ValueError, match=r"Unknown type name: 'invalid'"):
        force_dataframe_dtypes(df, template)


# TODO: Store by region name and test various regions. Might need region name to be required.


def test_get_parquet_session():
    # Reset the global Parquet sessions
    clear_parquet_sessions()

    # Sessions should be cached by `use_s3`
    fs_local1 = get_parquet_session(use_s3=True)
    fs_local2 = get_parquet_session(use_s3=True)
    fs_s3 = get_parquet_session(use_s3=False)
    # Check that the same session is returned for the same `use_s3` value
    assert fs_local1 is fs_local2
    # Check that a different session is returned for a different `use_s3` value
    assert fs_local1 is not fs_s3


@pytest.mark.xfail(reason="Global sessions are not being cleared for S3 filesystems.")
def test_clear_parquet_sessions():
    # Reset the global Parquet sessions
    clear_parquet_sessions()

    # TODO: This test is currently failing because the global sessions are not being cleared for S3 filesystems.
    #
    # These sessions will persist for the duration of this method after clearing the global sessions
    fs_s31 = get_parquet_session(use_s3=True)
    fs_local1 = get_parquet_session(use_s3=False)
    num_sessions_cleared = clear_parquet_sessions()
    # Check that the correct number of sessions were cleared
    assert num_sessions_cleared == 1
    # assert num_sessions_cleared == 2
    # Any new sessions will be different from the previous ones
    fs_s32 = get_parquet_session(use_s3=True)
    fs_local2 = get_parquet_session(use_s3=False)
    # Check that the sessions are different before/after clearing
    assert fs_s31 is not fs_s32
    assert fs_local1 is not fs_local2


@pytest.mark.parametrize(
    "partitions_template",
    [
        {"key_h": "string", "key_i": "integer"},
        {"key_h": "string"},
        {"key_i": "integer"},
        {},
    ],
)
@pytest.mark.parametrize("basename_template", ["test-filename-{i}.parquet", None])
@mock_s3
def test_export_dataset_s3(
    partitions_template,
    basename_template,
):
    region_name = "us-east-1"
    bucket_name = "my-bucket"
    bucket_path = "path/to/my/file"

    s3_client = boto3.client("s3", region_name=region_name)
    s3_client.create_bucket(Bucket=bucket_name)

    orig_df = force_dataframe_dtypes(
        pd.DataFrame(BASE_DATA),
        BASE_TEMPLATE | partitions_template,
    )

    export_dataset(
        orig_df,
        bucket_name + "/" + bucket_path,
        primary_template=BASE_TEMPLATE,
        partitions_template=partitions_template,
        basename_template=basename_template,
        use_s3=True,
        region_name=region_name,
        use_threads=False,
        overwrite=False,
    )

    # Check each key combo only once
    for i in orig_df[list(partitions_template)].drop_duplicates().index:

        def _prepare_expected_dataframe(_df):
            df_copy = _df.copy()
            for key in partitions_template:
                df_copy = df_copy[df_copy[key] == orig_df[key].iloc[i]]
            df_copy = df_copy.reset_index(drop=True)
            df_copy = df_copy.drop(columns=list(partitions_template))
            return df_copy

        expected_df = _prepare_expected_dataframe(orig_df)

        def _prepare_expected_path(partition_key):
            path_parts = []
            for partition_key in partitions_template:
                part_value = orig_df[partition_key].iloc[i]
                path_parts.append(f"{partition_key}={part_value}")
            if basename_template is not None:
                path_parts.append(basename_template.format(i=0))
            else:
                path_parts.append("part-0.parquet")
            return "/".join(
                [bucket_path.removeprefix("/").removesuffix("/"), *path_parts]
            )

        expected_path = _prepare_expected_path(partitions_template)

        # Read the actual dataframe
        resp = s3_client.get_object(Bucket=bucket_name, Key=expected_path)
        actual_df = pd.read_parquet(io.BytesIO(resp["Body"].read()), engine="pyarrow")
        # Check that the dataframes are equal
        pd.testing.assert_frame_equal(actual_df, expected_df)


@pytest.mark.parametrize(
    "partitions_template",
    [
        {"key_h": "string", "key_i": "integer"},
        {"key_h": "string"},
        {"key_i": "integer"},
        {},
    ],
)
@pytest.mark.parametrize("basename_template", ["test-filename-{i}.parquet", None])
def test_export_dataset_local(temp_dir, partitions_template, basename_template):
    orig_df = force_dataframe_dtypes(
        pd.DataFrame(BASE_DATA),
        BASE_TEMPLATE | partitions_template,
    )
    export_dataset(
        orig_df,
        temp_dir,
        primary_template=BASE_TEMPLATE,
        partitions_template=partitions_template,
        basename_template=basename_template,
        use_s3=False,
        region_name=None,
        use_threads=False,
        overwrite=False,
    )

    def _prepare_expected_dataframe(_df):
        df_copy = _df.copy()
        for key in partitions_template:
            df_copy = df_copy[df_copy[key] == orig_df[key].iloc[i]]
        df_copy = df_copy.reset_index(drop=True)
        df_copy = df_copy.drop(columns=list(partitions_template))
        return df_copy

    def _prepare_expected_path(partition_key):
        path_parts = []
        for partition_key in partitions_template:
            part_value = orig_df[partition_key].iloc[i]
            path_parts.append(f"{partition_key}={part_value}")
        if basename_template is not None:
            path_parts.append(basename_template.format(i=0))
        else:
            path_parts.append("part-0.parquet")
        return os.path.join(temp_dir, *path_parts)

    for i in orig_df[list(partitions_template)].drop_duplicates().index:
        expected_df = _prepare_expected_dataframe(orig_df)
        expected_path = _prepare_expected_path(partitions_template)
        actual_df = pd.read_parquet(expected_path, engine="pyarrow")
        # Check that the dataframes are equal
        pd.testing.assert_frame_equal(actual_df, expected_df)
