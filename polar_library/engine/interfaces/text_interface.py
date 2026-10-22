from abc import ABC, abstractmethod

import polars as pl


class ITextProcessor(ABC):

    @abstractmethod
    def concat(
        self,
        df: pl.DataFrame,
        column_name: str,
        value: str,
        replace: bool = True,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:
        """ concat at the end of the column the value """

    @abstractmethod
    def concat_text(
        self,
        df: pl.DataFrame,
        column_name: str,
        value: str,
        replace: bool = True,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:
        """ concat at the end of the column the value """

    @abstractmethod
    def contains(
        self,
        df: pl.DataFrame,
        column_name: str,
        value: str,
        replace: bool = True,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:
        """ Create a column or replaces with a true or false value if finds the value in the row data """

    @abstractmethod
    def ends_with(
        self,
        df: pl.DataFrame,
        column_name: str,
        value: str,
        replace: bool = True,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:
        """ Create a column or replaces with a true or false value if the row data ends with the value """

    @abstractmethod
    def left(
        self,
        df: pl.DataFrame,
        column_name: str,
        limit: int,
        replace: bool = True,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:
        """ Get the left side of a value until it reaches the limit """

    @abstractmethod
    def len(
        self,
        df: pl.DataFrame,
        column_name: str,
        replace: bool = True,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:
        """ Get the length of the string value with empty spaces and create a new column or replaces the old one """

    @abstractmethod
    def lowercase(
        self,
        df: pl.DataFrame,
        column_name: str,
        replace: bool = True,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:
        """ Set the column data in lower case """

    @abstractmethod
    def left_trim(
        self,
        df: pl.DataFrame,
        column_name: str,
        replace: bool = True,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:
        """ Delete empty spaces at the left """

    @abstractmethod
    def proper(
        self,
        df: pl.DataFrame,
        column_name: str,
        replace: bool = True,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:
        """ Delete empty spaces at the left and right """

    @abstractmethod
    def replace(
        self,
        df: pl.DataFrame,
        column_name: str,
        search_text: str,
        replace_field: str,
        replace: bool = True,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:
        """ Replace the search text on the columns with the replace_field data """

    @abstractmethod
    def right(
        self,
        df: pl.DataFrame,
        column_name: str,
        limit: int,
        replace: bool = True,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:
        """ Get the right side of a value until it reaches the limit """

    @abstractmethod
    def right_trim(
        self,
        df: pl.DataFrame,
        column_name: str,
        replace: bool = True,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:
        """ Delete empty spaces at the right """

    @abstractmethod
    def split(
        self,
        df: pl.DataFrame,
        column_name: str,
        delimiter: str,
        position: int,
        replace: bool = True,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:
        """ Divide the column data using the delimiter and convert the content (or create a new column) to the find position or the first one"""

    @abstractmethod
    def starts_with(
        self,
        df: pl.DataFrame,
        column_name: str,
        search_value: str,
        replace: bool = True,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:
        """ Creates or replaces a column with true or false values it the field contains the search value """

    @abstractmethod
    def trim(
        self,
        df: pl.DataFrame,
        column_name: str,
        replace: bool = True,
        new_column_name: str | None = None,
    ) -> pl.DataFrame:
        """Delete space blank in the text"""



    @abstractmethod
    def uppercase(
        self,
        df: pl.DataFrame,
        column_name: str,
        replace: bool = True,
        new_column_name: str | None = None,
    ) -> str:   
        """ Set the column data in upper case """
