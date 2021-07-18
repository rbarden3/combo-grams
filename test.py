# %%
import pandas as pd
from nltk import ngrams
import copy

df = pd.read_csv(r"abcnews-date-text\abcnews-date-text.csv")

# %%
df["headline_text"].head()

sent = ["How", "are", "you", "doing", "today"]
sentence = "How are you doing today"

for sentence in df["headline_text"].head():
    sent = sentence.split()
    c_grams = []
    for n in range(len(sent)):
        sent_grams = ngrams(sent, n + 1)
        c_grams.append(list(sent_grams))

# %%
for n_gram in c_grams:
    print(n_gram)

# %%
for n_gram in c_grams:
    for gram in n_gram:
        # print(gram)
        print(sentence.partition(" ".join(gram)))

# %%


def partition(collection):
    global counter
    if len(collection) == 1:
        yield [collection]
        return
    first = collection[0]
    for smaller in partition(collection[1:]):
        for n, subset in enumerate(smaller):
            yield smaller[:n] + [[first] + subset] + smaller[(n + 1) :]  # noqa: E203
        yield [[first]] + smaller


# for sentence in df["headline_text"].head():
#     for partitions in partition(sentence.split()):
#         print(partitions)

# %%
partitions = list(partition(df["headline_text"][0].split()))

# %%
for part in partitions:
    print(part)


# %%
def get_node_cost(node, corpus):
    for gram_ind, gram in enumerate(node):
        if gram in corpus:
            node[gram_ind] = 0
        else:
            node[gram_ind] = 1

    return sum(node)


# %%
def get_cost(level, corpus):
    level_vals = copy.deepcopy(level)
    for ind, node in enumerate(level_vals):
        level_vals[ind] = get_node_cost(node, corpus)
    return level_vals


print(get_cost(partitions, []))

# %%


# %%
