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
def get_node_cost(in_node, corpus):
    node = in_node[:]
    for gram_ind, gram in enumerate(node):
        if tuple(gram) in corpus:
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
def get_corpus(in_chosen_nodes):
    local_corpus = set()
    for level_ind, node_ind in enumerate(in_chosen_nodes):
        local_corpus |= set([tuple(val) for val in levels[level_ind][node_ind]])
    return local_corpus


# %%
dataset = df["headline_text"].head()
levels = [list(partition(level.split())) for level in dataset]
chosen_nodes = [3, 4, 5, 6]
# levels = []
# for level in [tuple(partition(level.split())) for level in dataset]:
#     this_level = []
#     for node in level:
#         this_level.append(tuple([tuple(gram) for gram in node]))
#     levels.append(this_level)

# for level in levels:
#     get_cost(level, corpus)
print(get_cost(levels[0], get_corpus(chosen_nodes)))


for level_ind, node_ind in enumerate(chosen_nodes):
    print(f"\n({level_ind}, {node_ind}): {levels[level_ind][node_ind]}")
    base_cost = get_node_cost(levels[level_ind][node_ind], [])
    actual_cost = get_node_cost(levels[level_ind][node_ind], get_corpus(chosen_nodes))
    print(f"Base cost: {base_cost}\tActual Cost: {actual_cost}")

print(get_cost(levels[len(chosen_nodes)], get_corpus(chosen_nodes)))
for level_ind, level in enumerate(levels):
    print(f"\n({level_ind}): {level}")
# %%
distances = {}
# for level_ind, level in enumerate(levels):
#     for node_ind, node in enumerate(level):
#         distances[(level_ind, node_ind)] = get_node_cost(node, get_corpus(chosen_nodes))

for level_ind, level in enumerate(levels):
    {
        (level_ind, node_ind): get_node_cost(node, get_corpus(chosen_nodes))
        for node_ind, node in enumerate(level)
    }

# %%
visited = []
current = 0
distances = dict()
while True:
    neighbors = [
        visited[:] + [node_ind] for node_ind, _ in enumerate(levels[len(visited)])
    ]
    unvisited = {tuple(node): None for node in neighbors[:]}
    for neighbor in neighbors:
        neighbor = tuple(neighbor)
        newDistance = get_node_cost(
            levels[len(neighbor) - 1][neighbor[-1]], get_corpus(tuple(visited))
        )
        if unvisited[neighbor] is None or unvisited[neighbor] > newDistance:
            unvisited[neighbor] = newDistance
    # visited[current] = currentDistance
    visited.append(current)
    # del unvisited[current]
    if not unvisited or len(visited) == len(levels):
        break
    candidates = [node for node in unvisited.items() if node[1]]
    current, currentDistance = sorted(candidates, key=lambda x: x[1])[0]
    current = current[0]


print(visited)

# %%
