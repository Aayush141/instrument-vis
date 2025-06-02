from enum import Enum

class AnnotationType(Enum):
    POINT = 1
    DURATION = 2
    VERTICAL = 3

class Mode(Enum):
    DATA_ACQUISITION = 1
    POST_ACQUISITION = 2