"""Null handling and vectorized conditional transformations."""

import json
import operator
import re
from collections.abc import Callable, Mapping

import polars as pl

from polar_library.engine.processors.row_processor import RowProcessor


class LogicalProcessor:
    """Stateless logical operations for dataframe pipelines."""

    _CONDITION_PATTERN = re.compile(
        r"^\s*(?P<column>.+?)\s*(?P<operator>==|!=|>=|<=|>|<|contains|isnull)\s*(?P<value>.*?)\s*$",
        re.IGNORECASE,
    )

    @staticmethod
    def _parse_condition(
        df: pl.DataFrame,
        column: str,
        statement: str,
    ) -> tuple[pl.Expr, str]:
        if not isinstance(statement, str):
            raise TypeError(
                "Conditions must be strings in 'column operator value' format"
            )

        match = LogicalProcessor._CONDITION_PATTERN.fullmatch(statement.strip())
        if match is None:
            raise ValueError("Condition must use 'column operator value' format")

        if match.group("column").strip() != column:
            raise ValueError(f"Condition column must match source column {column!r}")

        operator = match.group("operator").lower()
        raw_value = (match.group("value") or "").strip()

        if operator == "isnull":
            if raw_value:
                raise ValueError("The isnull condition does not accept a value")
            value = None
        else:
            if not raw_value:
                raise ValueError("Condition value is required")
            try:
                value = json.loads(raw_value)
            except json.JSONDecodeError:
                if re.fullmatch(r"[\w .-]+", raw_value) is None:
                    raise ValueError(
                        "Condition value must be a literal, not an expression"
                    )
                value = raw_value

            if not isinstance(value, (str, int, float, bool, type(None))):
                raise ValueError("Condition value must be a scalar literal")

        return RowProcessor.condition_mask(pl.col(column), operator, value), operator

    @staticmethod
    def logical(
        df: pl.DataFrame,
        operation: str,
        column: str,
        sentencia1: str,
        sentencia2: str | None = None,
        reemplazar_campo: bool = True,
        nombre_nueva_columna: str | None = None,
    ) -> pl.DataFrame:
        """Evaluate a logical operation and assign its boolean result in Polars."""

        # Dictionary keys to strings and map to Polars bitwise operators
        operators = {
            "and": operator.and_,
            "if": operator.and_,
            "or": operator.or_,
            "case": operator.or_,
            "elseif": operator.or_,
        }

        # Input Validations
        if operation not in (*operators, "not"):
            raise ValueError(f"Unsupported logical operation: {operation!r}")

        if not isinstance(reemplazar_campo, bool):
            raise TypeError("reemplazar_campo must be a boolean")

        if reemplazar_campo:
            if nombre_nueva_columna is not None:
                raise ValueError(
                    "nombre_nueva_columna requires reemplazar_campo to be false"
                )
        else:
            if not isinstance(nombre_nueva_columna, str) or not nombre_nueva_columna:
                raise ValueError(
                    "nombre_nueva_columna is required when reemplazar_campo is false"
                )

        # Parse conditions
        first_mask, first_operator = LogicalProcessor._parse_condition(
            df, column, sentencia1
        )

        first_mask = first_mask.fill_null(False)

        # Process Logical Operations
        if operation == "not":
            values = ~first_mask
            if first_operator != "isnull":
                values = values & pl.col(column).is_not_null()
        else:
            if sentencia2 is None:
                raise ValueError(f"{operation} requires sentencia2")

            second_mask, _ = LogicalProcessor._parse_condition(df, column, sentencia2)
            values = operators[operation](first_mask, second_mask.fill_null(False))

        target_column = column if reemplazar_campo else nombre_nueva_columna
        values_expr = values.cast(pl.Boolean)

        return df.with_columns(values_expr.alias(target_column))

    @staticmethod
    def coalesce(
        df: pl.DataFrame,
        column: str,
        default_value: object,
        create_new_column: bool = False,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:
        """Fill nulls and empty strings, without treating zero/False as missing."""
        target_column = new_column_name if create_new_column else column
        if create_new_column and not target_column:
            raise ValueError(
                "new_column_name is required when create_new_column is True"
            )

        expr = pl.when(pl.col(column) == "").then(None).otherwise(pl.col(column))

        if default_value is not None:
            expr = pl.coalesce(expr, pl.lit(default_value))

        return df.with_columns(expr.alias(target_column))

    @staticmethod
    def conditional_map(
        df: pl.DataFrame,
        column: str,
        condition_func: Callable[[pl.Expr], pl.Expr] | Mapping[str, object],
        true_value: object,
        false_value: object,
        create_new_column: bool = False,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:
        """Evaluate a Series callable or a JSON operator/value condition; never eval code."""

        target_column = new_column_name if create_new_column else column
        if create_new_column and not target_column:
            raise ValueError(
                "new_column_name is required when create_new_column is True"
            )

        if isinstance(condition_func, Mapping):
            if (
                set(condition_func) - {"operator", "value"}
                or "operator" not in condition_func
            ):
                raise ValueError(
                    "condition_func must contain operator and optional value"
                )
            operator = condition_func["operator"]
            if not isinstance(operator, str):
                raise TypeError("condition operator must be a string")

            # Pasamos pl.col(column) en lugar de la Serie completa
            mask = RowProcessor.condition_mask(
                pl.col(column), operator, condition_func.get("value")
            )

        elif callable(condition_func):
            # En Polars las expresiones son inmutables por diseño, no hace falta .copy()
            mask = condition_func(pl.col(column))
        else:
            raise TypeError(
                "condition_func must be a callable or an operator/value mapping"
            )

        mask_expr = mask.fill_null(False).cast(pl.Boolean)

        values_expr = (
            pl.when(mask_expr).then(pl.lit(true_value)).otherwise(pl.lit(false_value))
        )

        return df.with_columns(values_expr.alias(target_column))
