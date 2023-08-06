import datetime
import dataclasses
import abc
from typing import List


@dataclasses.dataclass
class TimeSeriesInterval:
    """Helper class to wrap time series values"""
    start_timestamp: int
    end_timestamp: int
    tenant_id: str
    asset_id: str
    perception: str
    columns: List[str] = dataclasses.field(default_factory=list)  # Represents the columns that we want to download

    def __post_init__(self):
        self.start_datetime = datetime.datetime.fromtimestamp(self.start_timestamp // 1e6)
        self.end_datetime = datetime.datetime.fromtimestamp(self.end_timestamp // 1e6)
