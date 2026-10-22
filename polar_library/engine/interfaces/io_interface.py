from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import polars as pl


class IOInterface(ABC):
      
    def execute(self, operation: str, df: pl.DataFrame, **kwargs: Any) -> pl.DataFrame:
        """
        Busca el método por su nombre y lo ejecuta pasando los argumentos.

        """
        # Validate interface
        if not hasattr(self, operation):
            raise AttributeError(f"La operación '{operation}' no está soportada por esta interfaz.")
        
        # Obtiene el método abstracto (o implementado en la hija)
        method = getattr(self, operation)
        
        # Lo ejecuta pasándole el DataFrame y el resto de parámetros desempaquetados
        return method(df=df, **kwargs)

    @abstractmethod
    def read_csv(self, filepath) -> pl.DataFrame:  
        """Allows to receive a data and convert it to dataset"""

    @abstractmethod
    def read_xlsx(self, filepath) -> pl.DataFrame:  
        """Allows to receive a data and convert it to dataset"""
    
    
    @abstractmethod
    def write_csv(self, df: pl.DataFrame, filepath: str | Path, index: bool = False) -> pl.DataFrame:  
        """ Overwrite the target CSV and return the dataframe unchanged."""