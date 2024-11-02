import pandas as pd
import json


class DateTimeDecoder(json.JSONDecoder):
    def default(self, obj):
        if isinstance(obj, pd.Timestamp):
            return obj.isoformat()  # Converts to 'YYYY-MM-DDTHH:MM:SS'
        return super().default(obj)
    


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, pd.Timestamp):
            return obj.isoformat()
        return super().default(obj)
    


def conver_date_to_datetime(records_retrieved: list[dict]) -> list[dict]:
    for record in records_retrieved:
        if 'Date' in record:
            record['Date'] = pd.to_datetime(record['Date'])
    return records_retrieved