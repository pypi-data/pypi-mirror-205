
# packages 

import pandas as pd

# function

def common_columns(*dfs):
    """
    Given a list of data frames, finds common columns between all pairs of data frames.

    Parameters:
        dfs: variable-length argument list of pandas data frames.

    Returns:x
        common_cols_all: set containing the names of columns that are common to all data frames, if any.
    """
    # initialize a list of common columns
    common_cols = []

    # get the names of the data frames, assigning a default name to any data frames without a name attribute
    names = [f"df_{i+1}" for i, df in enumerate(dfs)]

    # print correspondence of names with input order
    print("Correspondence of names with input order:")
    for i, name in enumerate(names):
        print(f"{name} is {dfs[i].name if hasattr(dfs[i], 'name') else 'DF number '+str(i+1)}")

    # loop over all pairs of data frames
    for i in range(len(dfs)):
        for j in range(i + 1, len(dfs)):
            # find the common columns between the two data frames
            common_cols_ij = set(dfs[i].columns).intersection(set(dfs[j].columns))
            # if there are common columns, add them to the list of common columns
            if len(common_cols_ij) > 0:
                # print the common columns between the two data frames
                print(f"\n{names[i]} and {names[j]} have the following common columns: {common_cols_ij}")
                common_cols.append((i, j, common_cols_ij))

    # find the common columns across all data frames
    common_cols_all = set.intersection(*[set(c[2]) for c in common_cols]) if len(common_cols) > 0 else set()

    # print the common columns across all data frames, if any
    if len(common_cols_all) > 0:
        print(f"\nCommon columns across all data frames: {common_cols_all}")
    else:
        print("\nThere are no common columns across all data frames.")

