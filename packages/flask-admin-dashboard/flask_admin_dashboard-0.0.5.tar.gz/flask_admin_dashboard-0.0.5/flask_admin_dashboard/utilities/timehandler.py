from dateutil import parser
from datetime import datetime

class TimeHandler:

    @staticmethod
    def convert_date_string(date_string):
        return parser.parse(date_string)

    @staticmethod
    def reformat_date_string(date_string):
        date = parser.parse(date_string)
        return date.strftime("%m/%d/%Y at %H:%M")
    @staticmethod
    def convert_datestring_to_iso(date_string):
        date = parser.parse(date_string)
        return date.strftime("%Y-%m-%dT%H:%M:%S.%f")

    @staticmethod
    def convert_datestring_to_timestamp(date_string):
        return datetime.timestamp(parser.parse(date_string))
