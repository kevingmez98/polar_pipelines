from abc import ABC, abstractmethod

import polars as pl


class INumericProcessor(ABC):
    """Converts the data on the column to float"""

    @abstractmethod
    def clean_float(
        self,
        df: pl.DataFrame,
        column_name: str,
        replace: bool = True,
        new_column_name: str | None = None,
    ) -> pl.Expr:
        """ Set the column data to the absolute value"""
        

    @abstractmethod
    def absolute(
        self,
        df: pl.DataFrame,
        column_name: str,
        replace: bool = True,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:
        """ Set the column data to the smallest integer greater than or equal to the data """
        

    @abstractmethod
    def ceiling(
        self,
        df: pl.DataFrame,
        column_name: str,
        replace: bool = True,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:
        """ Set the column data to the smallest integer lower than or equal to the data """
        

    @abstractmethod
    def floor(
        self,
        df: pl.DataFrame,
        column_name: str,
        replace: bool = True,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:
        """ Set the column data to the smallest integer lower than or equal to the data """
        

    @abstractmethod
    def max(
        self,
        df: pl.DataFrame,
        column_a: str,
        column_b: str,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:
        """ Creates a new column with the bigger value between the data of two columns """

    @abstractmethod
    def min(
        self,
        df: pl.DataFrame,
        column_a: str,
        column_b: str,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:
        """ Creates a new column with the lesser value between the data of two columns """

    @abstractmethod
    def power(
        self,
        df: pl.DataFrame,
        column_name: str,
        power_value: int,
        replace: bool = True,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:
        """ Creates a new column with the column's values powered to the power value """

    @abstractmethod
    def round_column(
        self,
        df: pl.DataFrame,
        column_name: str,
        decimals: int = 0,
        replace: bool = True,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:
        """ Round the column data to a given number of decimals """
    
    @abstractmethod
    def arithmetic(
		df: pl.DataFrame, column_a: str, operator: str,
		column_b_or_value: str | float, create_new_column: bool = False,
		new_column_name: str | None = None,
	) -> pl.DataFrame: ...