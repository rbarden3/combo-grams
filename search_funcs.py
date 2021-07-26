# %%
from helper_funcs import get_paths_cost, get_paths

# %%
def k_best_paths(part_ds, start_k=0, k=2, buffer=1, prepend_paths=[]):
    """Returns the best paths in the first k entries in the given partitioned dataset"""
    tree = {}
    lowest_cost = float("inf")
    for path, node_cost, tot_cost in get_paths_cost(
        map=part_ds, paths=get_paths(part_ds[start_k:k], prepend_paths)
    ):
        tree[path] = {"node_cost": node_cost, "tot_cost": tot_cost}
        if tot_cost < lowest_cost:
            lowest_cost = tot_cost
    filtered_dict = {k: v for k, v in tree.items() if v["tot_cost"] <= lowest_cost}
    return filtered_dict


# %%
def find_best_paths(map, incr=3, buffer=1):
    """Finds the best paths in the given map"""
    best_paths = [()]
    start_ind = 0
    far_ind = incr
    while far_ind <= len(map):
        best_paths = list(
            k_best_paths(
                map,
                start_k=start_ind,
                k=far_ind,
                buffer=buffer,
                prepend_paths=best_paths,
            ).keys()
        )
        print(best_paths, start_ind, far_ind)
        start_ind = far_ind
        if far_ind < len(map) and far_ind + incr >= len(map):
            far_ind = len(map)
        else:
            far_ind += incr
    return best_paths
