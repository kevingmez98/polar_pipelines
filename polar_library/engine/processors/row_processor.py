import polars as pl

"""Stateless row operations for dataframe pipelines using Polars."""


def condition_mask(series: pl.Series, operator: str, value: object = None) -> pl.Series:
    """Build a reusable polar comparison mask, excluding missing comparisons."""
    if operator == "==":
        mask = series == value
    elif operator == "!=":
        mask = series != value
    elif operator == ">":
        mask = series > value
    elif operator == "<":
        mask = series < value
    elif operator == ">=":
        mask = series >= value
    elif operator == "<=":
        mask = series <= value
    elif operator == "contains":
        mask = series.cast(pl.String).str.contains(str(value), literal=True)
    elif operator == "isnull":
        return series.is_null()
    else:
        raise ValueError(f"Unsupported filter operator: {operator!r}")

    return mask.fill_null(False) & series.is_not_null()


def filter_rows(
    df: pl.DataFrame, column: str, operator: str, value: object = None
) -> pl.DataFrame:
    """Return rows matching a comparison, literal contains, or null test."""
    # Polars idiomatic way: Use expressions inside .filter()
    if operator == "==":
        return df.filter(pl.col(column) == value)
    elif operator == "!=":
        return df.filter(pl.col(column) != value)
    elif operator == ">":
        return df.filter(pl.col(column) > value)
    elif operator == "<":
        return df.filter(pl.col(column) < value)
    elif operator == ">=":
        return df.filter(pl.col(column) >= value)
    elif operator == "<=":
        return df.filter(pl.col(column) <= value)
    elif operator == "contains":
        return df.filter(
            pl.col(column).cast(pl.String).str.contains(str(value), literal=True)
        )
    elif operator == "isnull":
        return df.filter(pl.col(column).is_null())
    else:
        raise ValueError(f"Unsupported filter operator: {operator!r}")


def sample(
    df: pl.DataFrame,
    sample_type: str,
    fraction_or_count: float,
    seed: int | None = None,  # Polars uses 'seed' instead of 'random_state'
) -> pl.DataFrame:
    """Sample a fraction (float in) or an absolute count (integer)."""
    if isinstance(fraction_or_count, bool) or not isinstance(
        fraction_or_count, (int, float)
    ):
        raise TypeError(
            "fraction_or_count must be an integer count or a float fraction"
        )

    is_fraction = isinstance(fraction_or_count, float)

    if is_fraction and not 0 <= fraction_or_count <= 1:
        raise ValueError("A fraction must be between 0 and 1")
    if fraction_or_count < 0:
        raise ValueError("A count must not be negative")

    if sample_type == "head":
        count = (
            int(len(df) * fraction_or_count) if is_fraction else int(fraction_or_count)
        )
        return df.head(count)

    if sample_type == "random":
        if is_fraction:
            return df.sample(fraction=fraction_or_count, seed=seed)
        return df.sample(n=int(fraction_or_count), seed=seed)

    raise ValueError("sample_type must be random or head")


def limit_rows(df: pl.DataFrame, limit: int) -> pl.DataFrame:
    """Return a copy containing at most limit rows."""
    limit = int(limit)
    if limit < 0:
        raise ValueError("limit must be zero or greater")
    return df.head(limit)
