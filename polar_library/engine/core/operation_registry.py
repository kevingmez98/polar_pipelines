"""Map pipeline operation names to the facade that executes them."""
""" from ..interfaces.row_interface import RowInterface """

from ..interfaces.io_interface import IOInterface
from ..interfaces.numeric_interface import INumericProcessor
from ..interfaces.structural_interface import IStructuralProcessor
from ..interfaces.text_interface import ITextProcessor

OPERATION_INTERFACES = {
	"read_csv": IOInterface,
	"write_csv": IOInterface,
	"inner_join": IStructuralProcessor,
	"outer_join": IStructuralProcessor,
	"sort": IStructuralProcessor,
	"drop_column": IStructuralProcessor,
	"rename_column": IStructuralProcessor,
	"change_data_type": IStructuralProcessor,
#	"limit": RowInterface,
#	"filter": RowInterface,
	"uppercase": ITextProcessor,
	"lowercase": ITextProcessor,
	"add_column": IStructuralProcessor,
	"absolute": INumericProcessor,
	"ceiling": INumericProcessor,
	"clean_float": INumericProcessor,
	"floor": INumericProcessor,
	"max": INumericProcessor,
	"min": INumericProcessor,
	"power": INumericProcessor,
	"round": INumericProcessor,
}


def get_interface(operation: str) -> type:
	"""Return the facade registered for an operation name."""
	try:
		return OPERATION_INTERFACES[operation]
	except KeyError as error:
		raise ValueError(f"Unsupported operation {operation!r}") from error
