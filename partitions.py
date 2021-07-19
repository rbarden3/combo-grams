# %%
import pandas as pd

# from nltk import ngrams


def partition(collection):
    """Basic Partition function.
    This was used from https://stackoverflow.com/a/30134039/13419030
    Since partitioning was not the main focus of the project, and this seemed to
    be a common implementation, I figured there was no issue using this function"""
    global counter
    if len(collection) == 1:
        yield [collection]
        return
    first = collection[0]
    for smaller in partition(collection[1:]):
        for n, subset in enumerate(smaller):
            yield smaller[:n] + [[first] + subset] + smaller[(n + 1) :]  # noqa: E203
        yield [[first]] + smaller


# %%
df = pd.read_csv(r"abcnews-date-text\abcnews-date-text.csv")

# %%
partitions = partition(df["headline_text"][0].split())

# %%
for part in partitions:
    print(part)

# %%
