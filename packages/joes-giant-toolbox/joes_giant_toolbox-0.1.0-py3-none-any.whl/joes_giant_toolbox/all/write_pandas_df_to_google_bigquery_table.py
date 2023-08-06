import pandas as pd
import google.cloud.bigquery


def write_pandas_df_to_google_bigquery_table(
    pandas_df: pd.DataFrame, bigquery_table_path: str, column_schema: list
) -> None:
    """
    Writes a pandas dataframe to a table on Google BigQuery

    Parameters
    ----------
    pandas_df: pandas.DataFrame
        Table to be written to BigQuery
    bigquery_table_path: str
        Path to destination table e.g. "project_name.dataset_name.table_name"
    column_schema: list of google.cloud.bigquery.enums.SqlTypeNames objects
        A list of column data types, informing BigQuery of the data type of each column (refer to the example below)
        This list is passed to the parameter "schema" in the function bigquery.LoadJobConfig()

    Example Usage
    -------------
    import pandas as pd
    from google.cloud import bigquery
    example_df = pd.DataFrame(
      {
        "string_column": ["a","b","c"],
        "integer_column": [-100,0,100],
        "float_column": [3.14159,6.9,4.2],
      }
    )
    write_pandas_df_to_google_bigquery(
      pandas_df = example_df,
      bigquery_table_path = "project_name.dataset_name.table_name",
      column_schema = [
        google.cloud.bigquery.SchemaField("string_column", google.cloud.bigquery.enums.SqlTypeNames.STRING),
        google.cloud.bigquery.SchemaField("integer_column", google.cloud.bigquery.enums.SqlTypeNames.INT64),
        google.cloud.bigquery.SchemaField("float_column", google.cloud.bigquery.enums.SqlTypeNames.FLOAT64),
      ],
    )
    """
    client = google.cloud.bigquery.Client()
    job = client.load_table_from_dataframe(
        pandas_df,
        bigquery_table_path,
        job_config=google.cloud.bigquery.LoadJobConfig(schema=column_schema),
    )
    job.result()  # wait for the job to complete
