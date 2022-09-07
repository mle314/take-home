"""
ETL classes for preparing data for modeling.
"""
import numpy as np
import pandas as pd


class BaseETL:
    def __init__(self, file_path, columns, date_columns):
        """A base class to work with patient and encounters data.

        :param file_path: path to csv file
        :param columns: a list of columns to use during ingestion
        :param date_columns: a list of date columns to parse
        """
        self.file_path = file_path
        self.columns = columns
        self.date_columns = date_columns
        self.df = pd.read_csv(
            file_path, usecols=self.columns, parse_dates=self.date_columns
        )

    def save_to_csv(self, path, index=False):
        """Save the processed dataframe to a csv file.

        :param path:
        :param index:
        :return:
        """
        self.df.to_csv(path, index=index)

    def __str__(self):
        shape = self.df.shape
        return f"Number of rows: {shape[0]}\nNumber of columns:{shape[1]}"


class EncountersETL(BaseETL):
    """Inherits the class BaseETL and is used to prepare and merge the patient
    and encounters data for modeling and analysis.
    """

    def __init__(self, file_path, columns, date_columns):
        super(EncountersETL, self).__init__(file_path, columns, date_columns)
        self.parser = lambda x: pd.to_datetime(x.rsplit("T", 1)[0])
        self.df = pd.read_csv(
            file_path,
            usecols=self.columns,
            parse_dates=self.date_columns,
            date_parser=self.parser,
        )
        self.covid_df = None
        self.last_admitted_df = None
        self.research_df = None

    def subset_dataframe(self, column="REASONDESCRIPTION", keyword="COVID"):
        """Subsets a dataframe by searching a column if a string contains a
        keyword.

        :param column: the description field
        :param keyword: a keyword to filter records by
        """
        self.covid_df = self.df[self.df[column].str.contains(keyword, na=False)].copy()

    @staticmethod
    def exclude_death_certificates_(df, column="CODE", code=308646001):
        """Exclude records that have the death certificate code.

        :param df: a pandas dataframe
        :param column: the column name
        :param code: the numeric code for filtering
        """
        return df[df[column] != code].copy()

    def get_last_admitted_records(self, group="PATIENT", date_column="START"):
        """Get the last admitted record for each patient.

        :param group: patient column to gorup by
        :param date_column: The patient admitted date column
        """
        temp_df = self.exclude_death_certificates_(self.covid_df)
        self.last_admitted_df = temp_df[
            (temp_df.groupby(group).START.transform("max") == temp_df[date_column])
        ].copy()

    def merge_encounters_and_patients_data(
        self, df, left="PATIENT", right="Id", join="left"
    ):
        """Merges the processed encounters and patients dataframes.

        :param df: The patient dataframe
        :param left: encounters join column
        :param right: patients join column
        :param join: method of joining
        """
        self.research_df = pd.merge(
            self.last_admitted_df, df, left_on=left, right_on=right, how=join
        )

    @staticmethod
    def check_if_person_died_after_n_days_from_admittance(start, end, n):
        """Checks if a person died n days after being admitted to the hospital.

        :param start: The patients birthdate
        :param end: The patients deathdate
        :param n: Number of days
        :return: a binary response
        """
        label = 0
        days_from = start + pd.Timedelta(days=n)
        if days_from >= end:
            label = 1
        return label

    def label_covid_deaths(
        self, admitted="START", died="DEATHDATE", new_column="covid_death", days=30
    ):
        """Create a new binary variable column for covid deaths.

        :param admitted: Patient admitted date column
        :param died: Patient death date column
        :param new_column: The new column name to be added
        :param days: Number of days from last admitted
        """
        self.research_df[new_column] = self.research_df.apply(
            lambda x: self.check_if_person_died_after_n_days_from_admittance(
                x[admitted], x[died], days
            ),
            axis=1,
        )

    def calculate_age_at_last_admittance(
        self,
        new_column="age_admitted",
        admitted="START",
        birthdate="BIRTHDATE",
        r=0,
        unit="Y",
        t="int",
    ):
        """Creates a new column for the age of each patient using their last
        admitted date.

        :param new_column: A new column for the patient admitted age
        :param admitted: The patient date admitted column name
        :param birthdate: The patient birthdate column name
        :param r: Round the result to r decimal places
        :param unit: The time unit to return
        :param t: The data type to return
        """
        self.research_df[new_column] = (
            (
                self.research_df[admitted].sub(self.research_df[birthdate], axis=0)
                / np.timedelta64(1, unit)
            )
            .round(r)
            .astype(t)
        )
