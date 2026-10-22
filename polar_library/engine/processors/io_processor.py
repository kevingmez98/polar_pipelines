from pathlib import Path

import polars as pl


def read_csv(filepath: str) -> pl.DataFrame:
    path = Path(filepath)
    extension = path.suffix.lower()

    if extension == ".csv":
        df = pl.read_csv(path)
    else:
        raise ValueError(f"Formato de archivo no soportado: {extension}")

    return df


def read_xlsx(filepath: str) -> pl.DataFrame:
    path = Path(filepath)
    extension = path.suffix.lower()

    if extension == ".xlsx":
        df = pl.read_excel(path)
    else:
        raise ValueError(f"Formato de archivo no soportado: {extension}")

    return df


def input_data(
    source_type: str,
    filepath_or_connection: str | Path,
    table_or_sheet: str | None = None,
    encoding: str = "utf-8",
    delimiter: str = ",",
) -> pl.DataFrame:
    if source_type == "csv":
        return pl.read_csv(
            filepath_or_connection, encoding=encoding, separator=delimiter
        )
    if source_type == "xlsx":
        return pl.read_excel(
            filepath_or_connection,
            sheet_name=table_or_sheet if table_or_sheet is not None else 0,
        )
    if source_type == "parquet":
        return pl.read_parquet(filepath_or_connection)
    if source_type == "sql":
        if not table_or_sheet:
            raise ValueError("SQL input requires table_or_sheet")
        return pl.read_sql_table(table_or_sheet, con=str(filepath_or_connection))
    raise ValueError(f"Unsupported source_type: {source_type!r}")


def output_data(
    df: pl.DataFrame,
    destination_type: str,
    output_path: str | Path,
    write_mode: str = "overwrite",
    *,
    encoding: str = "utf-8",
    delimiter: str = ",",
) -> pl.DataFrame:
    """Persist data; append preserves existing rows and validates column names/order."""
    if destination_type not in ("csv", "excel", "parquet"):
        raise ValueError(f"Unsupported destination_type: {destination_type!r}")
    if write_mode not in ("overwrite", "append"):
        raise ValueError("write_mode must be 'overwrite' or 'append'")
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    append = write_mode == "append" and path.exists() and path.stat().st_size > 0
    if append:
        existing = input_data(
            destination_type, path, encoding=encoding, delimiter=delimiter
        )
        if list(existing.columns) != list(df.columns):
            raise ValueError("append requires matching column names and order")
        values = pl.concat([existing, df], ignore_index=True)
    else:
        values = df
    if destination_type == "csv":
        values.to_csv(path, index=False, encoding=encoding, sep=delimiter)
    elif destination_type == "excel":
        if append:
            with pl.ExcelFile(path) as workbook:
                sheet = workbook.sheet_names[0]
            with pl.ExcelWriter(
                path, engine="openpyxl", mode="a", if_sheet_exists="replace"
            ) as writer:
                values.to_excel(writer, sheet_name=sheet, index=False)
        else:
            values.to_excel(path, index=False)
    else:
        values.to_parquet(path, index=False)
    return df


def write_csv(
    df: pl.DataFrame, filepath: str | Path, index: bool = False
) -> pl.DataFrame:
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)

    # Create column if index
    if index:
        # 0 to N-1
        df_to_write = df.with_row_index(name="index")
    else:
        df_to_write = df

    df_to_write.write_csv(path)

    return df
