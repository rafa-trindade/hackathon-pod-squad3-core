import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import duckdb
import numpy as np
import pandera as pa

from scripts.quality.contracts.silver_contract import MetricasCliente