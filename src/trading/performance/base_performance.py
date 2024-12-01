from pandas import DataFrame


class BasePerformance:
    def __init__(self, data: DataFrame) -> None:
        self.data = data
