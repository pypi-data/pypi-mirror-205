import logging

from bs4 import BeautifulSoup

from .names import CountryProperties

logger = logging.getLogger(__name__)


class Extractor:

    COLUMN_MAP = {
        0: CountryProperties.NAME,
        3: CountryProperties.ALPHA2_CODE,
        4: CountryProperties.ALPHA3_CODE,
        5: CountryProperties.IDENTIFIER,
    }

    def __init__(self):
        pass

    def _make_record(self, cols):
        record = {}
        for j, col in enumerate(cols):
            if j in self.COLUMN_MAP:
                anchors = col.find_all("a")
                for anchor in anchors:
                    text = anchor.text.strip()
                    if text:
                        the_index = text.find(" (the)")
                        if the_index > 0:
                            text = text[0:the_index] + text[the_index+6:]
                        record[self.COLUMN_MAP[j]] = text
                        break
        logger.info(f"extracted record {record}")
        return record

    def extract_data(self, text):
        soup = BeautifulSoup(text, "html.parser")
        data_table = soup.find("table")
        logger.debug("found table in the page")
        records = []
        for i, row in enumerate(data_table.find_all("tr")):
            logger.debug(f"processing row {i + 1}")
            cols = row.find_all("td")
            if len(cols) < 2:
                continue
            records.append(self._make_record(cols))
        return records
