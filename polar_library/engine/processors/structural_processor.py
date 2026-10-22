from collections.abc import Sequence

import polars as pl

"""Stateless structural operations for dataframe pipelines using Polars."""


def add_column(
    df: pl.DataFrame, column_name: str, value: object = None
) -> pl.DataFrame:
    if column_name in df.columns:
        raise ValueError(f"Column {column_name!r} already exists")
    # En Polars usamos pl.lit() para añadir un valor constante/literal
    return df.with_columns(pl.lit(value).alias(column_name))


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

    if new_type is not None and target_type is not None and new_type != target_type:
        raise ValueError("new_type and target_type must agree")
    dtype_str = target_type if target_type is not None else new_type
    if dtype_str is None:
        raise ValueError("target_type is required")

    target = resolve_output_column(
        df, column, new_column, new_column_name, create_new_column=create_new_column
    )

    # Mapeo básico de strings a Tipos de Datos nativos de Polars
    type_mapping = {
        "datetime": pl.Datetime,
        "int": pl.Int64,
        "float": pl.Float64,
        "str": pl.String,
        "bool": pl.Boolean,
    }

    polars_type = type_mapping.get(dtype_str.lower(), pl.String)

    if dtype_str.lower() == "datetime":
        # str.to_datetime es el equivalente nativo y rápido de Polars
        expr = pl.col(column).str.to_datetime(strict=True)
    else:
        expr = pl.col(column).cast(polars_type)

    return df.with_columns(expr.alias(target))


def drop_column(
    df: pl.DataFrame,
    column: str | Sequence[str] | None = None,
    *,
    columns: Sequence[str] | None = None,
) -> pl.DataFrame:
    """Return a dataframe without the requested column or columns."""
    if column is not None and columns is not None:
        raise ValueError("Use column or columns, not both")
    selected = columns if columns is not None else column
    if selected is None:
        raise ValueError("columns is required")

    names = [selected] if isinstance(selected, str) else list(selected)
    # Polars acepta una lista directamente en .drop()
    return df.drop(names)


def join(
    left: pl.DataFrame,
    right: pl.DataFrame,
    how: str = "inner",
    left_on: str | list[str] | None = None,
    right_on: str | list[str] | None = None,
    suffixes: Sequence[str] = ("_x", "_y"),
) -> pl.DataFrame:
    if left_on is None and right_on is None:
        shared = [column for column in left.columns if column in right.columns]
        if len(shared) != 1:
            raise ValueError(f"Join needs join keys; shared columns are {shared}")
        left_on = right_on = shared[0]
    if left_on is None or right_on is None:
        raise ValueError("Join needs both left_on and right_on")

    # Polars usa .join en vez de .merge, y acepta 'suffix' único o hereda comportamiento
    return left.join(
        right,
        left_on=left_on,
        right_on=right_on,
        how=how,
        suffix=suffixes[1] if len(suffixes) > 1 else "_right",
    )


def resolve_output_column(
    df: pl.DataFrame,
    column: str,
    new_column: bool = False,
    new_column_name: str | None = None,
    *,
    create_new_column: bool | None = None,
) -> str:
    if create_new_column is not None:
        if not isinstance(create_new_column, bool):
            raise ValueError("create_new_column must be a boolean")
        if new_column and not create_new_column:
            raise ValueError("new_column and create_new_column must agree")
        new_column = create_new_column
    if new_column_name is not None and (
        not isinstance(new_column_name, str) or not new_column_name
    ):
        raise ValueError("new_column_name must be a nonempty string")
    if not new_column:
        if new_column_name is not None:
            raise ValueError("new_column_name requires new_column to be true")
        return column
    if new_column_name is not None:
        if new_column_name in df.columns:
            raise ValueError(f"Column {new_column_name!r} already exists")
        return new_column_name
    if create_new_column:
        base = f"{column}_processed"
        target = base
        index = 1
        while target in df.columns:
            target = f"{base}_{index}"
            index += 1
        return target
    index = 1
    while f"{column}_{index}" in df.columns:
        index += 1
    return f"{column}_{index}"


def assign_result(
    df: pl.DataFrame,
    column: str,
    values: pl.Expr | pl.Series,  # <-- Ahora acepta pl.Expr (Recomendado)
    create_new_column: bool = False,
    new_column_name: str | None = None,
) -> pl.DataFrame:
    """Assign an aligned transformation result without changing the input."""
    target = resolve_output_column(
        df, column, new_column_name=new_column_name, create_new_column=create_new_column
    )
    # Convertimos a expresión si nos pasan una Serie para mantener consistencia
    expr = pl.lit(values) if isinstance(values, pl.Series) else values
    return df.with_columns(expr.alias(target))


def union(df_list: Sequence[pl.DataFrame], match_type: str = "auto") -> pl.DataFrame:
    """Concatenate by column name or by position using the first frame's names."""
    if len(df_list) < 2:
        raise ValueError("union requires at least 2 input dataframes")
    if match_type not in ("auto", "manual"):
        raise ValueError("match_type must be 'auto' or 'manual'")

    frames = list(df_list)
    if match_type == "manual":
        if any(len(frame.columns) != len(frames[0].columns) for frame in frames):
            raise ValueError("manual union requires the same number of columns")

        # En Polars cambiamos nombres usando .rename() con un diccionario posicional
        first_cols = frames[0].columns
        frames = [
            frame.rename({old: new for old, new in zip(frame.columns, first_cols)})
            for frame in frames
        ]
    # pl.concat no requiere 'ignore_index=True' porque Polars no tiene índices
    return pl.concat(frames, how="vertical")


def aggregate(
    df: pl.DataFrame,
    group_by: list[str],
    aggregations: dict[str, str | list[str] | pl.Expr],
) -> pl.DataFrame:
    """Aggregate with Polars native syntax, retaining null grouping keys."""
    if not aggregations:
        raise ValueError("aggregations must not be empty")

    # Convertir diccionario de agregaciones Polar a Expresiones nativas de Polars
    pl_aggs = []
    for col, agg_funcs in aggregations.items():
        funcs = [agg_funcs] if isinstance(agg_funcs, str) else agg_funcs
        for func in funcs:
            if isinstance(func, str):
                # Ejemplo: "sum" -> pl.col("col").sum()
                pl_expr = getattr(pl.col(col), func.lower())()
                pl_aggs.append(pl_expr.alias(f"{col}_{func}"))
            else:
                pl_aggs.append(func)

    # En Polars, group_by mantiene nulos por defecto sin necesidad de dropna=False
    if not group_by:
        return df.select(pl_aggs)

    return df.group_by(group_by).agg(pl_aggs)


def pivot(
    df: pl.DataFrame,
    pivot_type: str,
    index_cols: list[str],
    target_col: str,
    values_col: str,
) -> pl.DataFrame:
    """Pivot unique keys or melt all non-index columns into name/value columns."""
    if pivot_type == "columns_to_rows":
        # El equivalente de .melt() en Polars es .unpivot()
        return df.unpivot(
            on=[c for c in df.columns if c not in index_cols],
            index=index_cols,
            variable_name=target_col,
            value_name=values_col,
        )
    if pivot_type == "rows_to_columns":
        # Polars requiere una función de agregación explícita (usamos 'first' por defecto)
        return df.pivot(
            on=target_col,
            index=index_cols,
            values=values_col,
            aggregate_function="first",
        )
    raise ValueError("pivot_type must be 'columns_to_rows' or 'rows_to_columns'")


def rename_column(df: pl.DataFrame, column: str, new_name: str) -> pl.DataFrame:
    """Return a dataframe with ``column`` renamed to ``new_name``."""
    if column not in df.columns:
        raise ValueError(f"Column {column!r} is not present in the input")
    if new_name != column and new_name in df.columns:
        raise ValueError(f"Column {new_name!r} already exists")
    # Polars mapea mediante un diccionario simple {antiguo: nuevo}
    return df.rename({column: new_name})


def sort_rows(df: pl.DataFrame, column: str, direction: str = "asc") -> pl.DataFrame:

    if column not in df.columns:
        raise ValueError(f"La columna '{column}' no existe en el DataFrame.")

    # Map direction from the boolean
    directions = {"asc": False, "desc": True, "des": True}

    try:
        descending = directions[direction.lower()]
    except (AttributeError, KeyError) as error:
        raise ValueError("direction debe ser 'asc', 'desc' o 'des'") from error

    #  Polars native sort
    return df.sort(column, descending=descending)
