import pytest
from take_home.data.process_data import BaseETL
from config import FilePaths, PatientsConfig


@pytest.fixture
def sample_patients_data():
    """Returns a BaseETL with a sample dataset from patients.csv"""
    return BaseETL(
        FilePaths.TEST_DATA, PatientsConfig.COLUMNS, PatientsConfig.DATE_COLUMNS
    )


def test_default_initial_shape(sample_patients_data):
    assert sample_patients_data.df.shape[0] == 10
    assert sample_patients_data.df.shape[1] == 5


def test_column_date_types(sample_patients_data):
    cols = PatientsConfig.DATE_COLUMNS
    assert sample_patients_data.df[cols[0]].dtype.name == "datetime64[ns]"
    assert sample_patients_data.df[cols[1]].dtype.name == "datetime64[ns]"
