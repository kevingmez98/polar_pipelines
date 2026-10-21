import polars as pl

from ..interfaces.text_interface import ITextProcessor


class TextProcessor(ITextProcessor):
    def _get_target_column(
        self, column_name: str, replace: bool, new_column_name: str | None
    ) -> str:
        target_column = column_name if replace else new_column_name
        if not target_column:
            raise ValueError("No 'new_column_name' provided while 'replace' is False.")
        return target_column

    def concat(
        self,
        df: pl.DataFrame,
        column_name: str,
        value: str,
        replace: bool = True,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:
        target_column = self._get_target_column(column_name, replace, new_column_name)
        return df.with_columns(
            (pl.col(column_name).cast(pl.String) + pl.lit(value)).alias(target_column)
        )

    def contains(
        self,
        df: pl.DataFrame,
        column_name: str,
        value: str,
        replace: bool = True,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:
        target_column = self._get_target_column(column_name, replace, new_column_name)
        return df.with_columns(
            pl.col(column_name)
            .cast(pl.String)
            .str.contains(pl.lit(value), literal=True)
            .alias(target_column)
        )

    def ends_with(
        self,
        df: pl.DataFrame,
        column_name: str,
        value: str,
        replace: bool = True,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:
        target_column = self._get_target_column(column_name, replace, new_column_name)
        return df.with_columns(
            pl.col(column_name)
            .cast(pl.String)
            .str.ends_with(pl.lit(value))
            .alias(target_column)
        )

    def left(
        self,
        df: pl.DataFrame,
        column_name: str,
        limit: int,
        replace: bool = True,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:
        target_column = self._get_target_column(column_name, replace, new_column_name)
        return df.with_columns(
            pl.col(column_name).cast(pl.String).str.slice(0, limit).alias(target_column)
        )

    def len(
        self,
        df: pl.DataFrame,
        column_name: str,
        replace: bool = True,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:
        target_column = self._get_target_column(column_name, replace, new_column_name)
        return df.with_columns(
            pl.col(column_name).cast(pl.String).str.len_chars().alias(target_column)
        )

    def lower(
        self,
        df: pl.DataFrame,
        column_name: str,
        replace: bool = True,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:
        target_column = self._get_target_column(column_name, replace, new_column_name)
        return df.with_columns(
            pl.col(column_name).cast(pl.String).str.to_lowercase().alias(target_column)
        )

    def left_trim(
        self,
        df: pl.DataFrame,
        column_name: str,
        replace: bool = True,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:
        target_column = self._get_target_column(column_name, replace, new_column_name)
        return df.with_columns(
            pl.col(column_name)
            .cast(pl.String)
            .str.strip_chars_start()
            .alias(target_column)
        )
    
    def proper(self, df: pl.DataFrame, column_name: str, replace: bool = True, new_column_name: str | None = None) -> pl.DataFrame:
        target_column = self._get_target_column(column_name, replace, new_column_name)
        return df.with_columns(
            pl.col(column_name).cast(pl.String).str.to_titlecase().alias(target_column)
        )

    def replace(self, df: pl.DataFrame, column_name: str, search_text: str, replace_field: str, replace: bool = True, new_column_name: str | None = None) -> pl.DataFrame:
        target_column = self._get_target_column(column_name, replace, new_column_name)
        return df.with_columns(
            pl.col(column_name).cast(pl.String).str.replace_all(pl.lit(search_text), pl.lit(replace_field), literal=True).alias(target_column)
        )

    def right(self, df: pl.DataFrame, column_name: str, limit: int, replace: bool = True, new_column_name: str | None = None) -> pl.DataFrame:
        target_column = self._get_target_column(column_name, replace, new_column_name)
        return df.with_columns(
            pl.col(column_name).cast(pl.String).str.slice(-limit).alias(target_column)
        )

    def right_trim(self, df: pl.DataFrame, column_name: str, replace: bool = True, new_column_name: str | None = None) -> pl.DataFrame:
        target_column = self._get_target_column(column_name, replace, new_column_name)
        return df.with_columns(
            pl.col(column_name).cast(pl.String).str.strip_chars_end().alias(target_column)
        )
    
    def split(self, df: pl.DataFrame, column_name: str, delimiter: str, position: int, replace: bool = True, new_column_name: str | None = None) -> pl.DataFrame:
        target_column = self._get_target_column(column_name, replace, new_column_name)
        return df.with_columns(
            pl.col(column_name).cast(pl.String).str.split(delimiter).list.get(position).alias(target_column)
      )

    def starts_with(self, df: pl.DataFrame, column_name: str, search_value: str, replace: bool = True, new_column_name: str | None = None) -> pl.DataFrame:
        target_column = self._get_target_column(column_name, replace, new_column_name)
        return df.with_columns(
            pl.col(column_name).cast(pl.String).str.starts_with(pl.lit(search_value)).alias(target_column)
        )

    def trim(self, df: pl.DataFrame, column_name: str, replace: bool = True, new_column_name: str | None = None) -> pl.DataFrame:
        target_column = self._get_target_column(column_name, replace, new_column_name)
        return df.with_columns(
            pl.col(column_name).cast(pl.String).str.strip_chars().alias(target_column)
        )

    def upper(self, df: pl.DataFrame, column_name: str, replace: bool = True, new_column_name: str | None = None) -> pl.DataFrame:
        target_column = self._get_target_column(column_name, replace, new_column_name)
        return df.with_columns(
            pl.col(column_name).cast(pl.String).str.to_uppercase().alias(target_column)
        )
