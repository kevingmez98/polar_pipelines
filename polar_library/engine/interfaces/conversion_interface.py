from abc import ABC, abstractmethod

import polars as pl


class IConversionProcessor(ABC):

    @abstractmethod
    def make_date(
        self,
        df: pl.DataFrame,
        column_day: str,
        column_month: str,
        column_year: str,
    ) -> pl.DataFrame:
        """Takes three columns with data from the day, month and year and creates a date"""
  
    @abstractmethod
    def make_time(
        self,
        df: pl.DataFrame,
        column_hour: str,
        column_minute: str,
        column_second: str,
        replace: bool = True,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:
        """Takes three columns with data from the hour, minute and second, then creates a date"""

    @abstractmethod
    def make_date_time(
        self,
        df: pl.DataFrame,
        column_date: str,
        column_hour: str,
        replace: bool = True,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:
        """Takes two columns, one from the date and one from the hour and creates a date time"""
   