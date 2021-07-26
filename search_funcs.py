#%%
import copy
from itertools import product

#%%
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
def get_paths(map, prepend_paths=[]):
    """Function used to get all possible paths from the map"""
    if len(prepend_paths) > 0:
        for pre_path in prepend_paths:
            for path in product(*get_indices(map)):
                yield pre_path + path
    else:
        for path in product(*get_indices(map)):
            yield path


#%%
def get_paths_cost(map, paths):
    """Function used to get the cost of each path,
    the cost is the sum of the cost of each node"""
    for path in paths:
        cost = get_seq_cost(map, path)
        yield (path, cost, sum(cost))


# %%
