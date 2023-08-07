import logging
from typing import Any, Hashable, Iterable
import pandas as pd

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)-8s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

debug = logger.debug
info = logger.info
warning = logger.warning
error = logger.error
critical = logger.critical


# Create some sample data
# data = {
#     'Name': ['Alice', 'Bob', 'Charlie', 'Dave'],
#     'Age': [25, 31, 35, 19],
#     'Score': [85, 94, 76, 95]
# }

# # Create a DataFrame from the data
# df = pd.DataFrame(data)

# # Print the DataFrame to display the data as a table
# print(df)


def printTable(data: pd.DataFrame | dict[Any, Any] | Iterable[dict[Any, Any]]):
    df = pd.DataFrame(data)
    print(df)
