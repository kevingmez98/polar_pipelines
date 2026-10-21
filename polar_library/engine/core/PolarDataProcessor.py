from ..processors.conversion_processor import ConversionProcessor
from ..processors.io_processor import IoProcessor
from ..processors.numeric_processor import NumericProcessor
from ..processors.structural_processor import StructuralProcessor
from ..processors.text_processor import TextProcessor


class PolarDataProcessor:
    def __init__(self):
        self.structure = StructuralProcessor()
        self.text = TextProcessor()
        self.number = NumericProcessor()
        self.io = IoProcessor()
        self.conversion = ConversionProcessor()
        
