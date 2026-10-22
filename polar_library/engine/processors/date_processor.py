from datetime import datetime

import polars as pl


def _get_target_column(
     column_name: str, replace: bool, new_column_name: str | None
) -> str:
    target_column = column_name if replace else new_column_name
    if not target_column:
        raise ValueError("No 'new_column_name' provided while 'replace' is False.")
    return target_column


def date_add(
    
    df: pl.DataFrame,
    column_name: str,
    part: str,
    interval: int,
    replace: bool = True,
    new_column_name: str | None = None,
) -> pl.DataFrame:
    target_column = _get_target_column(column_name, replace, new_column_name)

    # Map structural parts to Polars offset strings
    part_mapping = {"year": "y", "month": "mo", "week": "w", "day": "d"}
    p = part_mapping.get(part.lower())
    if not p:
        raise ValueError(
            f"Unsupported part '{part}'. Choose from year, month, week, day."
        )

    offset_str = f"{interval}{p}"
    return df.with_columns(
        pl.col(column_name).dt.offset_by(offset_str).alias(target_column)
    )


def date_sub(
    
    df: pl.DataFrame,
    column_name: str,
    part: str,
    interval: int,
    replace: bool = True,
    new_column_name: str | None = None,
) -> pl.DataFrame:
    target_column = _get_target_column(column_name, replace, new_column_name)

    # Map structural parts to Polars offset strings
    part_mapping = {"year": "y", "month": "mo", "week": "w", "day": "d"}
    p = part_mapping.get(part.lower())
    if not p:
        raise ValueError(
            f"Unsupported part '{part}'. Choose from year, month, week, day."
        )

    offset_str = f"{interval}{p}"
    return df.with_columns(
        pl.col(column_name).dt.offset_by(-offset_str).alias(target_column)
    )


def date_diff(
    
    df: pl.DataFrame,
    column_name_a: str,
    column_name_b: str,
    part: str,
    new_column_name: str,
) -> pl.DataFrame:
    # Computes column_b - column_a
    diff_expr = pl.col(column_name_b) - pl.col(column_name_a)

    if part.lower() in ["day", "days"]:
        expr = diff_expr.dt.total_days()
    elif part.lower() in ["week", "weeks"]:
        expr = diff_expr.dt.total_days() // 7
    elif part.lower() in ["month", "months"]:
        # Calculating via year and month diff
        expr = (
            pl.col(column_name_b).dt.year() - pl.col(column_name_a).dt.year()
        ) * 12 + (pl.col(column_name_b).dt.month() - pl.col(column_name_a).dt.month())
    elif part.lower() in ["year", "years"]:
        expr = pl.col(column_name_b).dt.year() - pl.col(column_name_a).dt.year()
    else:
        raise ValueError(f"Unsupported diff part '{part}'")

    return df.with_columns(expr.alias(new_column_name))


def date_name(
    
    df: pl.DataFrame,
    column_name: str,
    format: str,
    replace: bool = True,
    new_column_name: str | None = None,
) -> pl.DataFrame:
    # Converts date to string format
    target_column = _get_target_column(column_name, replace, new_column_name)
    return df.with_columns(pl.col(column_name).dt.strftime(format).alias(target_column))


def date_parser(
    
    df: pl.DataFrame,
    column_name: str,
    format: str,
    replace: bool = True,
    new_column_name: str | None = None,
) -> pl.DataFrame:
    # Parses a string column back into a Date/Datetime
    target_column = _get_target_column(column_name, replace, new_column_name)
    return df.with_columns(
        pl.col(column_name).str.to_datetime(format=format).alias(target_column)
    )


def date_trunc(
    
    df: pl.DataFrame,
    column_name: str,
    part: str,
    replace: bool = True,
    new_column_name: str | None = None,
) -> pl.DataFrame:
    # Rounds date down to the beginning of the specified part
    target_column = _get_target_column(column_name, replace, new_column_name)
    part_mapping = {"year": "1y", "month": "1mo", "week": "1w", "day": "1d"}
    p = part_mapping.get(part.lower())
    if not p:
        raise ValueError(f"Unsupported truncation part '{part}'")

    return df.with_columns(pl.col(column_name).dt.truncate(p).alias(target_column))


def day(
    
    df: pl.DataFrame,
    column_name: str,
    replace: bool = True,
    new_column_name: str | None = None,
) -> pl.DataFrame:
    target_column = _get_target_column(column_name, replace, new_column_name)
    return df.with_columns(pl.col(column_name).dt.day().alias(target_column))


def iso_quarter(
    
    df: pl.DataFrame,
    column_name: str,
    replace: bool = True,
    new_column_name: str | None = None,
) -> pl.DataFrame:
    target_column = _get_target_column(column_name, replace, new_column_name)

    # Calculate ISO quarter (Q1 to Q4) based on ISO 8601 week (every quarter has 13 weeks).
    expr = (
        (
            (
                # dt.week() get ISO week (1 to 53). Minus 1 to index from 0 (0 to 52).
                (pl.col(column_name).dt.week() - 1)
                # Divide in 13 to group the weeks in quarters (0,1,2,3)
                // 13
            )
            # Add 1 to get back to 1 to 4 quarters
            + 1
        )
        # .clip(max=4) to week 53 (In leap years ISO) stays in Q4.
        .clip(max=4)
        .cast(pl.Int8)
    )  # Convert to an integer

    return df.with_columns(expr.alias(target_column))


def extract_date_part(
    df: pl.DataFrame,
    column: str,
    part: str,
    create_new_column: bool = False,
    new_column_name: str | None = None,
    date_format: str | None = None,  # Permite pasar un formato personalizado
) -> pl.DataFrame:
    if part not in ("year", "month", "day", "weekday"):
        raise ValueError("part must be 'year', 'month', 'day' or 'weekday'")

    target_column = new_column_name if create_new_column and new_column_name else column
    expr = pl.col(column)

    # If column is text la convert it to Datetime
    if df[column].dtype == pl.String:
        if date_format is None:
            # First value to detect format
            sample_value = df[column].drop_nulls().first()

            if sample_value and "/" in sample_value:
                # "12/21/2018 0:00" or "12/21/2018" format
                date_format = "%m/%d/%Y %H:%M" if ":" in sample_value else "%m/%d/%Y"
            else:
                # Standard ISO
                date_format = (
                    "%Y-%m-%d %H:%M:%S"
                    if sample_value and ":" in sample_value
                    else "%Y-%m-%d"
                )

        # Parsing
        date_expr = expr.str.to_datetime(format=date_format, strict=True)
    else:
        # already a date
        date_expr = expr

    # Extract
    part_expr = getattr(date_expr.dt, part)()

    return df.with_columns(part_expr.alias(target_column))


def iso_week(
    
    df: pl.DataFrame,
    column_name: str,
    replace: bool = True,
    new_column_name: str | None = None,
) -> pl.DataFrame:
    target_column = _get_target_column(column_name, replace, new_column_name)
    expr = pl.col(column_name).dt.week().cast(pl.Int8)
    return df.with_columns(expr.alias(target_column))


def iso_week_day(
    
    df: pl.DataFrame,
    column_name: str,
    replace: bool = True,
    new_column_name: str | None = None,
) -> pl.DataFrame:
    target_column = _get_target_column(column_name, replace, new_column_name)
    expr = pl.col(column_name).dt.weekday().cast(pl.Int8)

    return df.with_columns(expr.alias(target_column))


def iso_year(
    
    df: pl.DataFrame,
    column_name: str,
    replace: bool = True,
    new_column_name: str | None = None,
) -> pl.DataFrame:
    target_column = _get_target_column(column_name, replace, new_column_name)

    expr = pl.col(column_name).dt.iso_year().cast(pl.Int32)

    return df.with_columns(expr.alias(target_column))


def month(
    
    df: pl.DataFrame,
    column_name: str,
    replace: bool = True,
    new_column_name: str | None = None,
) -> pl.DataFrame:
    target_column = _get_target_column(column_name, replace, new_column_name)
    return df.with_columns(pl.col(column_name).dt.month().alias(target_column))


def now(
    
    df: pl.DataFrame,
    new_column_name: str,
) -> pl.DataFrame:
    # Appends a column filled with the current system Datetime
    return df.with_columns(pl.lit(datetime.now()).alias(new_column_name))


def quarter(
    
    df: pl.DataFrame,
    column_name: str,
    replace: bool = True,
    new_column_name: str | None = None,
) -> pl.DataFrame:
    target_column = _get_target_column(column_name, replace, new_column_name)
    return df.with_columns(pl.col(column_name).dt.quarter().alias(target_column))


def today(
    
    df: pl.DataFrame,
    new_column_name: str,
) -> pl.DataFrame:
    # Appends a column filled with the current system Date (no time component)
    return df.with_columns(pl.lit(datetime.now().date()).alias(new_column_name))


def week(
    
    df: pl.DataFrame,
    column_name: str,
    replace: bool = True,
    new_column_name: str | None = None,
) -> pl.DataFrame:
    target_column = _get_target_column(column_name, replace, new_column_name)
    return df.with_columns(pl.col(column_name).dt.week().alias(target_column))


def year(
    
    df: pl.DataFrame,
    column_name: str,
    replace: bool = True,
    new_column_name: str | None = None,
) -> pl.DataFrame:
    target_column = _get_target_column(column_name, replace, new_column_name)
    return df.with_columns(pl.col(column_name).dt.year().alias(target_column))
