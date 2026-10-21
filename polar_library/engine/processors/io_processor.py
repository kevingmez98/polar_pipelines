from pathlib import Path

import polars as pl

from ..interfaces.io_interface import IOInterface


class IoProcessor(IOInterface):
  
    def read_csv(self, file_path: str) -> pl.DataFrame:
        path = Path(file_path)
        extension = path.suffix.lower()

        if extension == ".csv":
            df = pl.read_csv(path)
        else:
           raise ValueError(f"Formato de archivo no soportado: {extension}")
    
        return df

    def read_xlsx(self, file_path: str) -> pl.DataFrame:
        path = Path(file_path)
        extension = path.suffix.lower()

        if extension == ".xlsx":
            df = pl.read_excel(path)
        else:
           raise ValueError(f"Formato de archivo no soportado: {extension}")
    
        return df



    def write_csv(df: pl.DataFrame, filepath: str | Path, index: bool = False) -> pl.DataFrame:
	   
	    path = Path(filepath)
	    path.parent.mkdir(parents=True, exist_ok=True)
	    df.to_csv(path, index=index)
	    return df



  