import polars as pl

from ..interfaces.text_interface import ITextProcessor


class TextProcessor(ITextProcessor):
    def _get_target_column(
        self, column_name: str, create_new_column: bool, new_column_name: str | None
    ) -> str:
        target_column = column_name if create_new_column else new_column_name
        if not target_column:
            raise ValueError("No 'new_column_name' provided while 'create_new_column' is False.")
        return target_column

    def concat_text(
        self,
        df: pl.DataFrame,
        column_name: str,
        value: str,
        create_new_column: bool = True,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:
        target_column = self._get_target_column(column_name, create_new_column, new_column_name)
        return df.with_columns(
            (pl.col(column_name).cast(pl.String) + pl.lit(value)).alias(target_column)
        )

    def concat(
        df: pl.DataFrame,
        columns: list[str],
        separator: str = "",
        create_new_column: bool = False,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:
        if not columns:
            raise ValueError("columns must not be empty")

        target_column = new_column_name if create_new_column and new_column_name else columns[0]

        concat_expr = pl.concat_str([pl.col(c).cast(pl.String) for c in columns], separator=separator)

        return df.with_columns(concat_expr.alias(target_column))

    def contains(
        self,
        df: pl.DataFrame,
        column_name: str,
        value: str,
        create_new_column: bool = True,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:
        target_column = self._get_target_column(column_name, create_new_column, new_column_name)
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
        create_new_column: bool = True,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:
        target_column = self._get_target_column(column_name, create_new_column, new_column_name)
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
        create_new_column: bool = True,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:
        target_column = new_column_name if create_new_column and new_column_name else column_name
        return df.with_columns(
            pl.col(column_name).cast(pl.String).str.slice(0, limit).alias(target_column)
        )

    def len(
        self,
        df: pl.DataFrame,
        column_name: str,
        create_new_column: bool = True,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:
        target_column = self._get_target_column(column_name, create_new_column, new_column_name)
        return df.with_columns(
            pl.col(column_name).cast(pl.String).str.len_chars().alias(target_column)
        )

    def lowercase(
        df: pl.DataFrame,
        column: str,
        create_new_column: bool = True,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:
        target_column = new_column_name if create_new_column and new_column_name else column
        return df.with_columns(
            pl.col(column).cast(pl.String).str.to_lowercase().alias(target_column)
        )

    def left_trim(
        self,
        df: pl.DataFrame,
        column_name: str,
        create_new_column: bool = True,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:
        target_column = self._get_target_column(column_name, create_new_column, new_column_name)
        return df.with_columns(
            pl.col(column_name)
            .cast(pl.String)
            .str.strip_chars_start()
            .alias(target_column)
        )
    
    def proper(self, df: pl.DataFrame, column_name: str, create_new_column: bool = True, new_column_name: str | None = None) -> pl.DataFrame:
        target_column = self._get_target_column(column_name, create_new_column, new_column_name)
        return df.with_columns(
            pl.col(column_name).cast(pl.String).str.to_titlecase().alias(target_column)
        )

    def create_new_column(self, df: pl.DataFrame, column_name: str, search_text: str, create_new_column_field: str, create_new_column: bool = True, new_column_name: str | None = None) -> pl.DataFrame:
        target_column = self._get_target_column(column_name, create_new_column, new_column_name)
        return df.with_columns(
            pl.col(column_name).cast(pl.String).str.create_new_column_all(pl.lit(search_text), pl.lit(create_new_column_field), literal=True).alias(target_column)
        )

    def right(self, df: pl.DataFrame, column_name: str, limit: int, create_new_column: bool = True, new_column_name: str | None = None) -> pl.DataFrame:
        target_column = self._get_target_column(column_name, create_new_column, new_column_name)
        return df.with_columns(
            pl.col(column_name).cast(pl.String).str.slice(-limit).alias(target_column)
        )

    def right_trim(self, df: pl.DataFrame, column_name: str, create_new_column: bool = True, new_column_name: str | None = None) -> pl.DataFrame:
        target_column = self._get_target_column(column_name, create_new_column, new_column_name)
        return df.with_columns(
            pl.col(column_name).cast(pl.String).str.strip_chars_end().alias(target_column)
        )
    
    def split(self, df: pl.DataFrame, column_name: str, delimiter: str, position: int, create_new_column: bool = True, new_column_name: str | None = None) -> pl.DataFrame:
        target_column = self._get_target_column(column_name, create_new_column, new_column_name)
        return df.with_columns(
            pl.col(column_name).cast(pl.String).str.split(delimiter).list.get(position).alias(target_column)
      )

    def starts_with(self, df: pl.DataFrame, column_name: str, search_value: str, create_new_column: bool = True, new_column_name: str | None = None) -> pl.DataFrame:
        target_column = self._get_target_column(column_name, create_new_column, new_column_name)
        return df.with_columns(
            pl.col(column_name).cast(pl.String).str.starts_with(pl.lit(search_value)).alias(target_column)
        )
    import polars as pl

    def substring(
        df: pl.DataFrame, 
        column: str, 
        start: int, 
        length: int, 
        create_new_column: bool = False, 
        new_column_name: str | None = None,
    ) -> pl.DataFrame:
        target_column = new_column_name if (create_new_column and new_column_name) else column
        
        if length < 0:
            raise ValueError("length must be nonnegative")
        
        return df.with_columns(
            pl.col(column)
            .cast(pl.String)
            .str.slice(start, length)
            .alias(target_column)
        )


    def trim(self, df: pl.DataFrame, column_name: str, create_new_column: bool = True, new_column_name: str | None = None) -> pl.DataFrame:
        target_column = self._get_target_column(column_name, create_new_column, new_column_name)
        return df.with_columns(
            pl.col(column_name).cast(pl.String).str.strip_chars().alias(target_column)
        )

    def uppercase(self, df: pl.DataFrame, column_name: str, create_new_column: bool = True, new_column_name: str | None = None) -> pl.DataFrame:
        target_column = self._get_target_column(column_name, create_new_column, new_column_name)
        return df.with_columns(
            pl.col(column_name).cast(pl.String).str.to_uppercase().alias(target_column)
        )
