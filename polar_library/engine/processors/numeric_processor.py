import polars as pl

from polar_library.engine.processors import structural_processor as StructuralProcessor


def clean_float(
        
        df: pl.DataFrame,
        column_name: str,
        create_new_column: bool = True,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:
        # Set the column name
        target_column = column_name if create_new_column else new_column_name

        if not target_column:
            raise ValueError("No 'new_column_name' but 'create_new_column' False.")

        return df.with_columns(
            pl.col(column_name)
            .cast(pl.Float64, strict=False)
            .fill_nan(0)  # create_new_columns floating-point NaN with 0
            .fill_null(0)  # create_new_columns missing/unparseable nulls with 0
            .alias(target_column)
        )

def absolute(
        df: pl.DataFrame,
        column: str,
        create_new_column: bool = True,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:
        # Set the column name
        target_column = column if create_new_column else new_column_name

        if not target_column:
            raise ValueError("No 'new_column_name' but 'create_new_column' False.")

        return df.with_columns(
            pl.col(column).abs().alias(target_column)  # create_new_column original column
        )

def ceiling(
        
        df: pl.DataFrame,
        column_name: str,
        create_new_column: bool = True,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:
        # Set the column name
        target_column = column_name if create_new_column else new_column_name

        if not target_column:
            raise ValueError("No 'new_column_name' but 'create_new_column' False.")
        return df.with_columns(
            pl.col(column_name).ceil().alias(target_column)  # create_new_column original column
        )

def floor(
        
        df: pl.DataFrame,
        column_name: str,
        create_new_column: bool = True,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:
        # Set the column name
        target_column = column_name if create_new_column else new_column_name

        if not target_column:
            raise ValueError("No 'new_column_name' but 'create_new_column' False.")

        return df.with_columns(pl.col(column_name).floor().alias(target_column))

def max(
        
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
        
        df: pl.DataFrame,
        column_name: str,
        value: float,
        create_new_column: bool = True,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:

        # Set the column name
        target_column = column_name if create_new_column else new_column_name

        if not target_column:
            raise ValueError("No 'new_column_name' but 'create_new_column' False.")

        # Calculate max horizontal between the two columns
        return df.with_columns(
            pl.col(column_name).pow(value).alias(target_column)
        )

def round_column(
        
        df: pl.DataFrame,
        column_name: str,
        decimals: int,  # Cambiado de float a int y renombrado para claridad
        create_new_column: bool = True,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:

        # Set the column name
        target_column = column_name if create_new_column else new_column_name

        if not target_column:
            raise ValueError("No 'new_column_name' but 'create_new_column' False.")

        return df.with_columns(
            pl.col(column_name).round(decimals).alias(target_column)
        )
    
def arithmetic(
		df: pl.DataFrame, column_a: str, operator: str, column_b_or_value: str | float,
		create_new_column: bool = False, new_column_name: str | None = None,
	) -> pl.DataFrame:
	
        left = pl.to_numeric(df[column_a], errors="raise")
        right = (
			pl.to_numeric(df[column_b_or_value], errors="raise")
			if isinstance(column_b_or_value, str) else column_b_or_value
		)
        if operator == "+":
        	values = left.add(right)
        elif operator == "-":
        	values = left.sub(right)
        elif operator == "*":
        	values = left.mul(right)
        elif operator == "/":
        	zero_divisor = (right == 0).any() if isinstance(right, pl.Series) else right == 0
        	if zero_divisor:
        		raise ValueError("Division by zero")
        	values = left.div(right)
        else:
        	raise ValueError(f"Unsupported arithmetic operator: {operator!r}")
        return StructuralProcessor.assign_result(df, column_a, values, create_new_column, new_column_name)