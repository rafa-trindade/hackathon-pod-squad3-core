import pandera as pa
import duckdb
from pandera.typing import Series
from typing import Optional

class MetricasCliente(pa.DataFrameModel):

      class Config:
        strict = True
        coerce = True