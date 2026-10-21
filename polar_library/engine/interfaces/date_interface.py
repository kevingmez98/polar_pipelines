from abc import ABC, abstractmethod
from datetime import datetime

import polars as pl


class DateCategoryInterface(ABC):

    @abstractmethod
    def date_add(
        self,
        df: pl.DataFrame,
        column_name: str,
        part: str,
        interval: int,
        replace: bool = True,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:
        """Create or replace a column adding a part of a date into the column data, the interval is the amount of parts added"""
   
    @abstractmethod
    def date_diff(
        self,
        df: pl.DataFrame,
        column_name_a: str,
        column_name_b: str,
        part: str,
    ) -> pl.DataFrame:
        """Create a column with the part difference between two dates"""

    @abstractmethod
    def date_name(
        self,
        df: pl.DataFrame,
        column_name: str,
        format: str,
        replace: bool = True,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:
        """Parse the date to another format"""
        
    @abstractmethod
    def date_parse(
        self,
        df: pl.DataFrame,
        column_name: str,
        format: str,
        replace: bool = True,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:
        """Parse the date to another format"""
        
    @abstractmethod
    def date_trunc(
        self,
        df: pl.DataFrame,
        date: datetime,
        part: str,
    ) -> pl.DataFrame:
        """Round the date to the specified part. Allows to convert a date to first day of week or month"""

    @abstractmethod
    def day(
        self,
        df: pl.DataFrame,
        column_name: str,
        replace: bool = True,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:
        """Return the day of the date of the column data"""

    @abstractmethod
    def iso_quarter(
        self,
        df: pl.DataFrame,
        column_name: str,
        replace: bool = True,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:
        """Return the quarter of the date based on ISO 8601"""

    @abstractmethod
    def iso_week(
        self,
        df: pl.DataFrame,
        column_name: str,
        replace: bool = True,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:
        """Return the week of the date based on ISO 8601"""

    @abstractmethod
    def iso_week_day(
        self,
        df: pl.DataFrame,
        column_name: str,
        replace: bool = True,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:
        """Return the weekday of the date based on ISO 8601"""
    
    @abstractmethod
    def iso_year(
        self,
        df: pl.DataFrame,
        column_name: str,
        replace: bool = True,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:
        """Return the year of the date based on ISO 8601"""
    
    @abstractmethod
    def month(
        self,
        df: pl.DataFrame,
        column_name: str,
        replace: bool = True,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:
        """Return the month of the date"""

    @abstractmethod
    def now(
        self,
        df: pl.DataFrame,
        column_name: str,
        replace: bool = True,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:
        """Return the actual datetime of the system with hour"""

    @abstractmethod
    def quarter(
        self,
        df: pl.DataFrame,
        column_name: str,
        replace: bool = True,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:
        """Return the quarter of the date"""

    @abstractmethod
    def today(
        self,
        df: pl.DataFrame,
        column_name: str,
        replace: bool = True,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:
        """Return the actual date of the system without the hour"""
    
    @abstractmethod
    def week(
        self,
        df: pl.DataFrame,
        column_name: str,
        replace: bool = True,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:
        """Return the week of the date"""
        
    @abstractmethod
    def year(
        self,
        df: pl.DataFrame,
        column_name: str,
        replace: bool = True,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:
        """Return the year of the date"""
