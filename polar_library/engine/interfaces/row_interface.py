"""Abstract contracts for row selection and sampling operations."""

from abc import ABC, abstractmethod

import polars as pl


class RowInterface(ABC):
	"""Contract implemented by polar row processors."""

	@staticmethod
	@abstractmethod
	def filter_rows(
		df: pl.DataFrame, column: str, operator: str, value: object = None,
	) -> pl.DataFrame: ...

	@staticmethod
	@abstractmethod
	def sample(
		df: pl.DataFrame, sample_type: str, fraction_or_count: float | int,
		random_state: int | None = None,
	) -> pl.DataFrame: ...

	@staticmethod
	@abstractmethod
	def limit_rows(df: pl.DataFrame, limit: int) -> pl.DataFrame: ...
