"""Map pipeline operation names directly to concrete processor methods."""

from collections.abc import Callable, Mapping, Sequence
from functools import partial
from typing import Any

import polars as pl

from polar_library.engine.processors.conversion_processor import ConversionProcessor
from polar_library.engine.processors.date_processor import DateTimeProcessor
from polar_library.engine.processors.inputs import require_inputs
from polar_library.engine.processors.io_processor import IOProcessor
from polar_library.engine.processors.logical_processor import LogicalProcessor
from polar_library.engine.processors.numeric_processor import NumericProcessor
from polar_library.engine.processors.row_processor import RowProcessor
from polar_library.engine.processors.structural_processor import StructuralProcessor
from polar_library.engine.processors.text_processor import TextProcessor

Operation = Callable[..., pl.DataFrame]

OPERATION_PROCESSORS: dict[str, Operation] = {
	"input": IOProcessor.input_data,
	"output": IOProcessor.output_data,
	"read_csv": IOProcessor.read_csv,
	"read_xlsx": IOProcessor.read_xlsx,
	"write_csv": IOProcessor.write_csv,
	"date": ConversionProcessor.to_date,
	"datetime": ConversionProcessor.datetime,
	"float": ConversionProcessor.to_float,
	"int": ConversionProcessor.to_int,
	"str": ConversionProcessor.to_str,
	"make_date": ConversionProcessor.make_date,
	"make_time": ConversionProcessor.make_time,
	"make_date_time": ConversionProcessor.make_date_time,
	"date_parser": DateTimeProcessor.date_parser,
	"date_add": DateTimeProcessor.date_add,
	"date_sub": DateTimeProcessor.date_sub,
	"date_diff": DateTimeProcessor.date_diff,
	"extract_date_part": DateTimeProcessor.extract_date_part,
	"coalesce": LogicalProcessor.coalesce,
	"ifnull": LogicalProcessor.coalesce,
	"conditional_map": LogicalProcessor.conditional_map,
	"and": partial(LogicalProcessor.logical, operation="and"),
	"case": partial(LogicalProcessor.logical, operation="case"),
	"if": partial(LogicalProcessor.logical, operation="if"),
	"elseif": partial(LogicalProcessor.logical, operation="elseif"),
	"or": partial(LogicalProcessor.logical, operation="or"),
	"not": partial(LogicalProcessor.logical, operation="not"),
	"absolute": NumericProcessor.absolute,
	"abs": NumericProcessor.absolute,
	"arithmetic": NumericProcessor.arithmetic,
	"ceiling": NumericProcessor.ceiling,
	"clean_float": NumericProcessor.clean_float,
	"floor": NumericProcessor.floor,
	"max": NumericProcessor.max,
	"min": NumericProcessor.min,
	"power": NumericProcessor.power,
	"round": NumericProcessor.round_column,
	"filter": RowProcessor.filter_rows,
	"limit": RowProcessor.limit_rows,
	"sample": RowProcessor.sample,
	"union": StructuralProcessor.union,
	"join": StructuralProcessor.join,
	"inner_join": partial(StructuralProcessor.join, how="inner"),
	"outer_join": partial(StructuralProcessor.join, how="outer"),
	"add_column": StructuralProcessor.add_column,
	"sort": StructuralProcessor.sort_rows,
	"drop-column": StructuralProcessor.drop_column,
	"drop_column": StructuralProcessor.drop_column,
	"rename-column": StructuralProcessor.rename_column,
	"rename_column": StructuralProcessor.rename_column,
	"change-data-type": StructuralProcessor.change_data_type,
	"change_data_type": StructuralProcessor.change_data_type,
	"aggregate": StructuralProcessor.aggregate,
	"pivot": StructuralProcessor.pivot,
	"uppercase": TextProcessor.uppercase,
	"upper": TextProcessor.uppercase,
	"lowercase": TextProcessor.lowercase,
	"lower": TextProcessor.lowercase,
	"trim": TextProcessor.trim,
	"ltrim": TextProcessor.left_trim,
	"rtrim": TextProcessor.right_trim,
	"substring": TextProcessor.substring,
	"replace": TextProcessor.replace,
	"split": TextProcessor.split,
	"concat": TextProcessor.concat,
	"concat_text": TextProcessor.concat_text,
}

_ZERO_INPUT_OPERATIONS = {"input", "read_csv", "read_xlsx"}
_MULTI_INPUT_OPERATIONS = {"union"}
_TWO_INPUT_OPERATIONS = {"join", "inner_join", "outer_join"}


def get_operation(operation: str) -> Operation:
	"""Return the concrete processor method for a pipeline operation name."""
	try:
		return OPERATION_PROCESSORS[operation]
	except KeyError as error:
		raise ValueError(f"Unsupported operation {operation!r}") from error


def execute_operation(
	operation: str,
	inputs: Sequence[pl.DataFrame],
	parameters: Mapping[str, Any] | None = None,
	**overrides: Any,
) -> pl.DataFrame:
	"""Dispatch inputs to the concrete method registered for an operation."""
	function = get_operation(operation)
	arguments = dict(parameters or {})
	arguments.update(overrides)
	if operation in _ZERO_INPUT_OPERATIONS:
		require_inputs(operation, inputs, 0)
		return function(**arguments)
	if operation in _MULTI_INPUT_OPERATIONS:
		return function(inputs, **arguments)
	if operation in _TWO_INPUT_OPERATIONS:
		require_inputs(operation, inputs, 2)
		return function(inputs[0], inputs[1], **arguments)
	require_inputs(operation, inputs, 1)
	return function(inputs[0], **arguments)
