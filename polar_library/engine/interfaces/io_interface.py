from abc import ABC, abstractmethod
from pathlib import Path

import polars as pl


class IOInterface(ABC):
      
        
    @abstractmethod
    def read_csv(self, filepath) -> pl.DataFrame:  
        """Allows to receive a data and convert it to dataset"""

    @abstractmethod
    def read_xlsx(self, filepath) -> pl.DataFrame:  
        """Allows to receive a data and convert it to dataset"""
    
    
    @abstractmethod
    def write_csv(self, df: pl.DataFrame, filepath: str | Path, index: bool = False) -> pl.DataFrame:  
        """ Overwrite the target CSV and return the dataframe unchanged."""