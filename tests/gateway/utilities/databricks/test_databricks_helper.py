import os
import pytest
import pandas as pd
from typing import Dict, Generator
from unittest.mock import Mock, patch, MagicMock

from language_model_gateway.gateway.utilities.databricks.databricks_helper import (
    DatabricksHelper,
)


@pytest.fixture
def databricks_helper() -> DatabricksHelper:
    """Fixture to create a DatabricksHelper instance for testing"""
    databricks_helper = Mock(spec=DatabricksHelper)
    databricks_helper.catalog = "bronze"
    databricks_helper.schema = "fhir_rpt"
    databricks_helper.logger = Mock()
    return databricks_helper


@pytest.fixture
def mock_workspace_client(
    mock_env_vars: Dict[str, str],
) -> Generator[MagicMock, None, None]:
    """Fixture to mock WorkspaceClient with comprehensive mocking"""
    with patch(
        "language_model_gateway.gateway.utilities.databricks.databricks_helper.WorkspaceClient"
    ) as mock_client:
        # Create a mock client instance
        mock_instance = MagicMock()
        mock_client.return_value = mock_instance

        # Create a mock SQL warehouse with a custom execute method
        mock_sql_warehouse = MagicMock()

        # Create a mock result that mimics the structure of a Databricks SQL result
        mock_result = MagicMock()
        mock_result.rows = [{"column1": "value1", "column2": "value2"}]

        # Configure the execute method to either raise an exception or return a result
        def mock_execute() -> MagicMock:
            # Simulate a long-running query by checking the current time
            current_time = os.environ.get("MOCK_CURRENT_TIME", 2)
            if float(current_time) > 1:
                raise Exception("Simulated long-running query")
            return mock_result

        mock_sql_warehouse.execute = MagicMock(side_effect=mock_execute)
        mock_instance.sql = mock_sql_warehouse

        yield mock_client


@pytest.fixture
def mock_env_vars() -> Generator[Dict[str, str], None, None]:
    """Fixture to set up comprehensive mock environment variables for Databricks"""
    original_env = os.environ.copy()
    try:
        # Set all required environment variables
        env_vars = {
            "DATABRICKS_HOST": "https://mock-databricks-host.cloud.databricks.com",
            "DATABRICKS_TOKEN": "mock-token",
            "DATABRICKS_SQL_WAREHOUSE_ID": "12345",
        }

        # Update environment with mock variables
        for key, value in env_vars.items():
            os.environ[key] = value

        yield env_vars
    finally:
        # Restore original environment
        os.environ.clear()
        os.environ.update(original_env)


def test_init(databricks_helper: DatabricksHelper) -> None:
    """Test the initialization of DatabricksHelper"""
    assert databricks_helper.catalog == "bronze"
    assert databricks_helper.schema == "fhir_rpt"
    assert databricks_helper.logger is not None


def test_parse_databricks_statement_response() -> None:
    """Test parsing of Databricks statement response"""
    # Create a mock StatementResponse
    mock_schema = Mock()
    mock_schema.columns = [Mock(name="column1"), Mock(name="column2")]
    mock_manifest = Mock()
    mock_manifest.schema = mock_schema

    mock_statement_response = Mock(
        manifest=mock_manifest,
        result=Mock(data_array=[["value1", "value2"], ["value3", "value4"]]),
    )

    helper = DatabricksHelper()
    result_df = helper.parse_databricks_statement_response(mock_statement_response)

    assert isinstance(result_df, pd.DataFrame)
    assert result_df.shape == (2, 2)


def test_dataframe_to_markdown() -> None:
    """Test conversion of DataFrame to markdown"""
    df = pd.DataFrame({"Name": ["Alice", "Bob"], "Age": [30, 25]})

    helper = DatabricksHelper()
    markdown_table = helper.dataframe_to_markdown(df)

    assert "| Name | Age |" in markdown_table
    assert "| --- | --- |" in markdown_table
    assert "| Alice | 30 |" in markdown_table
    assert "| Bob | 25 |" in markdown_table
