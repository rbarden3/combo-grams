# %%
import copy

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


# %%
def get_corpus(in_chosen_nodes):
    """Function used to create a corpus of partitions already used.
    This is used to calculate the cost of nodes"""
    local_corpus = set()
    for level_ind, node_ind in enumerate(in_chosen_nodes):
        local_corpus |= set([tuple(val) for val in levels[level_ind][node_ind]])
    return local_corpus


# %%
# dataset = ["A B", "A C", "B A", "C A"]

dataset = ["A B", "A C", "B A", "B C", "C A", "C B"]
levels = [list(partition(level.split())) for level in dataset]
levels2 = []
for level in dataset:
    levels2.append([part for part in partition(level.split()) if len(part) < 3])
levels = [
    [part for part in partition(level.split()) if len(part) < 3] for level in dataset
]


# %%
def get_node_cost(in_node, corpus):
    """Used to get the cost of a node, the cost of the node is reduced if it
    is made up of grams that have been selected already"""
    node = in_node[:]
    for gram_ind, gram in enumerate(node):
        if tuple(gram) in corpus:
            node[gram_ind] = 0
        else:
            node[gram_ind] = 1

    return sum(node)


# %%
def get_level_cost(level, corpus):
    level_vals = copy.deepcopy(level)
    for ind, node in enumerate(level_vals):
        level_vals[ind] = get_node_cost(node, corpus)
    return level_vals


print(get_level_cost(levels[0], []))

#%%
def get_indices(map):
    """Used to get the indices of the nodes in the map"""
    indices = []
    for level in map:
        level_indices = []
        for node_ind, _ in enumerate(level):
            level_indices.append(node_ind)
        indices.append(level_indices)
    return indices


get_indices(levels[0])

# %%
from itertools import product


def get_paths(map):
    return list(product(*get_indices(map)))


get_paths(levels)

# %%
def get_seq_cost(map, seq):
    """Returns the cost of a sequence where in enumerated form,
    The index is the index in 'levels' of a sentance's partitions,
    the value is the partition set selected"""
    seq_vals = copy.deepcopy(seq)
    seq_costs = []
    for lev_ind, nod_ind in enumerate(seq_vals):
        seq_costs.append(
            get_node_cost(map[lev_ind][nod_ind], get_corpus(tuple(seq_vals[:lev_ind])))
        )
    return seq_costs


singles = get_seq_cost(levels, [0, 0, 0, 0])
doubles = get_seq_cost(levels, [1, 1, 1, 1])
hybrid = get_seq_cost(levels, [1, 0, 1, 0])

print(f"Node Scores: {singles} \t Sum:{sum(singles)}")
print(f"Node Scores: {doubles} \t Sum:{sum(doubles)}")
print(f"Node Scores: {hybrid} \t Sum:{sum(hybrid)}")
# %%
def get_paths_cost(map):
    costs = []
    for node_set in get_paths(map):
        cost = get_seq_cost(map, node_set)
        costs.append((cost, sum(cost)))
    return costs


# from combo_funcs import get_paths_cost

for path_cost in get_paths_cost(levels):
    print(f"Node Scores: {path_cost[0]} \t Sum:{path_cost[1]}")

# %%
chosen_nodes = [1, 1, 1, 1]

# %%
distances = {}

for level_ind, level in enumerate(levels):
    for node_ind, node in enumerate(level):
        distances[(level_ind, node_ind)] = get_node_cost(node, get_corpus(chosen_nodes))


# %%
def dijkstras():
    """Initial implementation, I am currently encountering issues dynamically
    cycling through nodes. It is instead selecting the first node no matter what"""
    visited = []
    current = None
    while True:
        levs = [lev[0] for lev in visited]
        neighbors = [
            levs[:] + [node_ind] for node_ind, _ in enumerate(levels[len(visited)])
        ]
        unvisited = {tuple(node): None for node in neighbors[:]}
        for neighbor in neighbors:
            neighbor = tuple(neighbor)
            newDistance = get_seq_cost(neighbor)
            if unvisited[neighbor] is None or unvisited[neighbor] > newDistance:
                unvisited[neighbor] = newDistance
        if current is not None:
            visited.append(current)
        if not unvisited or len(visited) == len(levels):
            break
        candidates = [node for node in unvisited.items() if node[1]]
        current = sorted(candidates, key=lambda x: x[1])[0]
        # current = current[0] + 1

    print(visited)


# %%
# dijkstras()
# %%
# import itertools

# graph = [[1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]]
# test_list = list(itertools.permutations(range(4), 4))
# # %%
# for nod in test_list:
#     get_node_cost(levels[len(nod) - 1][nod[-1]], get_corpus(tuple(visited)))


# %%
