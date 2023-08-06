from enum import Enum


class FuncType(Enum):
    agg = 1
    window = 2
    unknown = 3
    bitwise = 4
    conditional = 5
    context = 6
    conversion = 7
    data_generation = 8
    datetime = 9
    encryption = 10
    file = 11
    geospatial = 12
    hash = 13
    metadata = 14
    numeric = 15
    regexp = 16
    semi_structured_data = 17
    string_binary = 18
    system = 19
    table = 20

