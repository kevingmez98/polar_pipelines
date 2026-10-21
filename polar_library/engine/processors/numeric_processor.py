import polars as pl

from ..interfaces.numeric_interface import INumericProcessor


class NumericProcessor(INumericProcessor):
    
    def clean_float(
        self,
        df: pl.DataFrame,
        column_name: str,
        replace: bool = True,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:
        # Set the column name
        target_column = column_name if replace else new_column_name

        if not target_column:
            raise ValueError("No 'new_column_name' but 'replace' False.")

        return df.with_columns(
            pl.col(column_name)
            .cast(pl.Float64, strict=False)
            .fill_nan(0)  # Replaces floating-point NaN with 0
            .fill_null(0)  # Replaces missing/unparseable nulls with 0
            .alias(target_column)
        )

    def absolute(
        self,
        df: pl.DataFrame,
        column_name: str,
        replace: bool = True,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:
        # Set the column name
        target_column = column_name if replace else new_column_name

        if not target_column:
            raise ValueError("No 'new_column_name' but 'replace' False.")

        return df.with_columns(
            pl.col(column_name).abs.alias(target_column)  # Replace original column
        )

    def ceiling(
        self,
        df: pl.DataFrame,
        column_name: str,
        replace: bool = True,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:
        # Set the column name
        target_column = column_name if replace else new_column_name

        if not target_column:
            raise ValueError("No 'new_column_name' but 'replace' False.")
        return df.with_columns(
            pl.col(column_name).ceil().alias(target_column)  # Replace original column
        )

    def floor(
        self,
        df: pl.DataFrame,
        column_name: str,
        replace: bool = True,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:
        # Set the column name
        target_column = column_name if replace else new_column_name

        if not target_column:
            raise ValueError("No 'new_column_name' but 'replace' False.")

        return df.with_columns(pl.col(column_name).floor().alias(target_column))

    def max(
        self,
        df: pl.DataFrame,
        column_a: str,
        column_b: str,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:

        if not new_column_name:
            raise ValueError("No 'new_column_name'")

        # Calculate max horizontal between the two columns
        return df.with_columns(
            pl.max_horizontal(column_a, column_b).alias(new_column_name)
        )

    def min(
        self,
        df: pl.DataFrame,
        column_a: str,
        column_b: str,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:

        if not new_column_name:
            raise ValueError("No 'new_column_name'")

        # Calculate max horizontal between the two columns
        return df.with_columns(
            pl.min_horizontal(column_a, column_b).alias(new_column_name)
        )

    def power(
        self,
        df: pl.DataFrame,
        column_name: str,
        value: float,
        replace: bool = True,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:

        # Set the column name
        target_column = column_name if replace else new_column_name

        if not target_column:
            raise ValueError("No 'new_column_name' but 'replace' False.")

        # Calculate max horizontal between the two columns
        return df.with_columns(
            pl.col(column_name).pow(value).alias(target_column)
        )

    def round(
        self,
        df: pl.DataFrame,
        column_name: str,
        decimals: int,  # Cambiado de float a int y renombrado para claridad
        replace: bool = True,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:

        # Set the column name
        target_column = column_name if replace else new_column_name

        if not target_column:
            raise ValueError("No 'new_column_name' but 'replace' False.")

        return df.with_columns(
            pl.col(column_name).round(decimals).alias(target_column)
        )