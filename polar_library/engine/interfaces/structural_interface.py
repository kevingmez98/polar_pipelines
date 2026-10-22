from abc import ABC, abstractmethod
from collections.abc import Sequence

import polars as pl


class IStructuralProcessor(ABC):
   
    

    
    @abstractmethod
    def add_column(df: pl.DataFrame, column_name: str, value: object = None) -> pl.DataFrame:
        """Return a copy with a new column filled with a constant value."""

    
    @abstractmethod
    def change_data_type(
		df: pl.DataFrame,
		column: str,
		new_type: str | None = None,
		*,
		target_type: str | None = None,
		create_new_column: bool | None = None,
		new_column: bool = False,
		new_column_name: str | None = None,
	) -> pl.DataFrame:
        """Return a copy with the selected column cast to ``new_type``."""

    @abstractmethod
    def drop_column(df: pl.DataFrame,
		column: str | Sequence[str] | None = None,
		*,
		columns: Sequence[str] | None = None,) -> pl.DataFrame: 
        """ Allows to drop a column from the dataset"""

    @abstractmethod
    def join(
		left: pl.DataFrame,
		right: pl.DataFrame,
		how: str = "inner",
		left_on: str | list[str] | None = None,
		right_on: str | list[str] | None = None,
		suffixes: Sequence[str] = ("_x", "_y"),
	) -> pl.DataFrame:
	    """Join two dataframes, inferring the key only when exactly one column is shared."""

    @abstractmethod
    def resolve_output_column(
		df: pl.DataFrame,
		column: str,
		new_column: bool = False,
		new_column_name: str | None = None,
		*,
		create_new_column: bool | None = None,
	) -> str:
	    """Resolve modern processed names while retaining legacy indexed names."""

    
    @abstractmethod
    def assign_result(
		df: pl.DataFrame,
		column: str,
		values: pl.Series,
		create_new_column: bool = False,
		new_column_name: str | None = None,
	) -> pl.DataFrame:
	    """Assign an aligned transformation result without changing the input."""

    @abstractmethod
    def union(df_list: Sequence[pl.DataFrame], match_type: str = "auto") -> pl.DataFrame:
	    """Concatenate by column name or by position using the first frame's names."""


    @abstractmethod
    def aggregate(
		df: pl.DataFrame,
		group_by: list[str],
		aggregations: dict[str, str | list[str]],
	) -> pl.DataFrame:
	    """Aggregate with polar functions, retaining null grouping keys."""
		

    @abstractmethod
    def pivot(
		df: pl.DataFrame,
		pivot_type: str,
		index_cols: list[str],
		target_col: str,
		values_col: str,
	) -> pl.DataFrame:
    	"""Pivot unique keys or melt all non-index columns into name/value columns."""


    @abstractmethod
    def rename_column(df: pl.DataFrame, column: str, new_name: str) -> pl.DataFrame:
        """Return a copy with ``column`` renamed to ``new_name``."""
		


    @abstractmethod
    def sort_rows(
		df: pl.DataFrame,
		column: str,
		direction: str = "asc",
	) -> pl.DataFrame:
        """Return a copy sorted by ``column`` in ascending or descending order."""
		