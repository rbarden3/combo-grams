#%%
import copy
from itertools import product

#%%
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


#%%
def get_corpus(map, in_chosen_nodes):
    """Function used to create a corpus of partitions already used.
    This is used to calculate the cost of nodes"""
    local_corpus = set()
    for level_ind, node_ind in enumerate(in_chosen_nodes):
        local_corpus |= set([tuple(val) for val in map[level_ind][node_ind]])
    return local_corpus


#%%
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


#%%
def get_level_cost(level, corpus):
    level_vals = copy.deepcopy(level)
    for ind, node in enumerate(level_vals):
        level_vals[ind] = get_node_cost(node, corpus)
    return level_vals


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


#%%
def get_paths(map, prepend_paths=[]):

    if len(prepend_paths) > 0:
        for pre_path in prepend_paths:
            for path in product(*get_indices(map)):
                yield pre_path + path
    else:
        for path in product(*get_indices(map)):
            yield path


#%%
# ds = ["A B", "A C", "B A", "C A"]
# part_ds = [list(partition(level.split())) for level in ds]

# list(get_paths(part_ds))
#%%
def get_seq_cost(map, seq):
    """Returns the cost of a sequence where in enumerated form,
    The index is the index in 'levels' of a sentance's partitions,
    the value is the partition set selected"""
    seq_vals = copy.deepcopy(seq)
    seq_costs = []
    for lev_ind, nod_ind in enumerate(seq_vals):
        seq_costs.append(
            get_node_cost(
                map[lev_ind][nod_ind],
                get_corpus(map=map, in_chosen_nodes=tuple(seq_vals[:lev_ind])),
            )
        )
    return seq_costs


#%%
def get_paths_cost(map, paths):
    for path in paths:
        cost = get_seq_cost(map, path)
        yield (path, cost, sum(cost))


# for path_cost in get_paths_cost(part_ds):
#     print(f"Node Scores: {path_cost[0]} \t Sum:{path_cost[1]}")

#%%
def dijkstras(map):
    """Initial implementation, I am currently encountering issues dynamically
    cycling through nodes. It is instead selecting the first node no matter what"""
    visited = []
    current = None
    while True:
        levs = [lev[0] for lev in visited]
        neighbors = [
            levs[:] + [node_ind] for node_ind, _ in enumerate(map[len(visited)])
        ]
        unvisited = {tuple(node): None for node in neighbors[:]}
        for neighbor in neighbors:
            neighbor = tuple(neighbor)
            newDistance = get_seq_cost(neighbor)
            if unvisited[neighbor] is None or unvisited[neighbor] > newDistance:
                unvisited[neighbor] = newDistance
        if current is not None:
            visited.append(current)
        if not unvisited or len(visited) == len(map):
            break
        candidates = [node for node in unvisited.items() if node[1]]
        current = sorted(candidates, key=lambda x: x[1])[0]
        # current = current[0] + 1

    print(visited)
