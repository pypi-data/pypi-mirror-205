"""Top-level package for titorium EGDA."""

__author__ = """Roberto Arce Aguirre"""
__email__ = 'roberto_arce_@hotmail.com'

#imports
import pandas as pd
import numpy as np
import seaborn as sns
import plotly.graph_objs as go
import matplotlib as plt

# Functions
from .utils import create_fake_dataset # noqa : F401

# Modules
from . import time_series  # noqa : F401
from . import flow  # noqa : F401
from . import proportion  # noqa : F401
from . import distribution  # noqa : F401
from . import correlation  # noqa : F401
from . import ranking  # noqa : F401