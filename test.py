# %%
from search_funcs import find_best_paths
from helper_funcs import partition
import pandas as pd

# %%
def partition_dataset(dataset, max_part_size=3):
    """Partitions the given dataset into partitions of size <= max_part_size"""
    return [
        [part for part in partition(level.split()) if len(part) <= max_part_size]
        for level in dataset
    ]


# %%
news_dataset = (
    pd.read_csv(r"abcnews-date-text\abcnews-date-text.csv")["headline_text"]
    .head(15)
    .tolist()
)
news_partitioned = partition_dataset(news_dataset)

ABC_dataset = ["A B", "A C", "B A", "B C", "C A", "C B", "A C"]
ABC_partitioned = partition_dataset(ABC_dataset)

# %%
find_best_paths(ABC_partitioned, incr=3, buffer=3)

# %%
find_best_paths(news_partitioned, incr=2, buffer=1)

# %%
