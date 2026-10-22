import polars as pl

from polar_library.engine.interfaces.conversion_interface import IConversionProcessor
from polar_library.engine.processors.structural_processor import StructuralProcessor


class ConversionProcessor(IConversionProcessor):
    def _get_target_column(
        self, column_name: str, replace: bool, new_column_name: str | None
    ) -> str:
        target_column = column_name if replace else new_column_name
        if not target_column:
            raise ValueError("No 'new_column_name' provided while 'replace' is False.")
        return target_column

    @staticmethod
    def _assign(
        df: pl.DataFrame,
        source: str,
        values: pl.Series,
        replace: bool,
        new_column_name: str | None,
    ) -> pl.DataFrame:
        if not isinstance(replace, bool):
            raise ValueError("replace must be a boolean")
        if replace and new_column_name is not None:
            raise ValueError("new_column_name requires replace to be false")
        if not replace and not new_column_name:
            raise ValueError("new_column_name is required when replace is false")
        return StructuralProcessor.assign_result(
            df,
            source,
            values,
            create_new_column=not replace,
            new_column_name=new_column_name if not replace else None,
        )
    @staticmethod
    def _integer_parts(df: pl.DataFrame, columns: tuple[str, ...]) -> dict[str, pl.Series]:
	    parts = {}
	    for name in columns:
	    	values = pl.to_numeric(df[name], errors="raise")
	    	if ((values.dropna() % 1) != 0).any():
	    		raise ValueError(f"{name} values must be integers")
	    	parts[name] = values.astype("Int64")
	    return parts

    @staticmethod
    def to_date(
		df: pl.DataFrame,
		column: str,
		replace: bool = True,
		new_column_name: str | None = None,
	) -> pl.DataFrame:
    	values = pl.to_datetime(df[column], errors="raise").dt.normalize()
    	return ConversionProcessor._assign(df, column, values, replace, new_column_name)

    @staticmethod
    def datetime(
		df: pl.DataFrame,
		column: str,
		replace: bool = True,
		new_column_name: str | None = None,
	) -> pl.DataFrame:
    	values = pl.to_datetime(df[column], errors="raise")
    	return ConversionProcessor._assign(df, column, values, replace, new_column_name)

    @staticmethod
    def to_float(
		df: pl.DataFrame,
		column: str,
		replace: bool = True,
		new_column_name: str | None = None,
	) -> pl.DataFrame:
    	values = pl.to_numeric(df[column], errors="raise").astype("float64")
    	return ConversionProcessor._assign(df, column, values, replace, new_column_name)

    @staticmethod
    def to_int(
		df: pl.DataFrame,
		column: str,
		replace: bool = True,
		new_column_name: str | None = None,
	) -> pl.DataFrame:
    	values = pl.to_numeric(df[column], errors="raise").astype("Int64")
    	return ConversionProcessor._assign(df, column, values, replace, new_column_name)

    @staticmethod
    def to_str(
		df: pl.DataFrame,
		column: str,
		replace: bool = True,
		new_column_name: str | None = None,
	) -> pl.DataFrame:
    	values = df[column].astype("string")
    	return ConversionProcessor._assign(df, column, values, replace, new_column_name)

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
