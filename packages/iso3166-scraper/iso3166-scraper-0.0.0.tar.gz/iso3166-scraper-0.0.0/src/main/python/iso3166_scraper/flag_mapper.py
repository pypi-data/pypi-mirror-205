
from .names import CountryProperties

REGIONAL_INDICATOR_SYMBOL_START = 0x1F1E6


def map_flags(records):
    def flag_code(country_code):
        code = ""
        for i in range(2):
            code += chr(REGIONAL_INDICATOR_SYMBOL_START + (ord(country_code[i]) - ord('A')))
        return code

    return [record | {CountryProperties.FLAG: flag_code(record[CountryProperties.ALPHA2_CODE])}
            for record in records]
