import polars as pl

from ..interfaces.conversion_interface import IConversionProcessor


class ConversionProcessor(IConversionProcessor):
    def _get_target_column(
        self, column_name: str, replace: bool, new_column_name: str | None
    ) -> str:
        target_column = column_name if replace else new_column_name
        if not target_column:
            raise ValueError("No 'new_column_name' provided while 'replace' is False.")
        return target_column

    def make_date(
        self,
        df: pl.DataFrame,
        column_day: str,
        column_month: str,
        column_year: str,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:
        # Build the date
        expr = pl.date(
            year=pl.col(column_year).cast(pl.Int32),
            month=pl.col(column_month).cast(pl.Int32),
            day=pl.col(column_day).cast(pl.Int32),
        ).alias(new_column_name)

        return df.with_columns(expr)

    def make_time(
        self,
        df: pl.DataFrame,
        column_hour: str,
        column_minute: str,
        column_second: str,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:

        # Expresión para construir el tiempo (Time)
        expr = pl.time(
            hour=pl.col(column_hour).cast(pl.Int32),
            minute=pl.col(column_minute).cast(pl.Int32),
            second=pl.col(column_second).cast(pl.Int32),
        ).alias(new_column_name)

        return df.with_columns(expr)

    def make_date_time(
        self,
        df: pl.DataFrame,
        column_date: str,
        column_hour: str,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:

        # Nota: column_date: pl.Date/pl.Datetime  column_hour: pl.Time
        expr = (
            pl.col(column_date).dt.combine(pl.col(column_hour)).alias(new_column_name)
        )

        return df.with_columns(expr)
