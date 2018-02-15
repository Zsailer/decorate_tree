#!/usr/bin/env python

__author__ = "Zach Sailer"
__email__ = "zachsailer@gmail.com"

import os
import argparse
import dendropy
import pandas as pd

def decorate(
    tree,
    tips,
    tips_cols=['id'],
    ancs=None,
    ancs_cols=None):
    """Map attributes from tip/ancestor datasets onto a dendropy tree.

    Note, this function assumes tips/ancestors are PhyloPandas dataframes.

    Parameters
    ----------
    tree: dendropy.Tree
        Tree to decorate. Assumes the tree labels match the id column in
        the following dataframes.
    tips: phylopandas.DataFrame
        Data for tips of tree.
    tips_col: list
        DataFrame columns to map onto tips of tree.
    tips_col: list
        DataFrame columns to map onto tips of tree.
    ancs: phylopandas.DataFrame
        Data for ancestors of tree.
    ancs_col: list
        DataFrame columns to map onto ancs of tree.

    Returns
    -------
    tree : dendropy.Tree
        Tree decorated with attributes (sets the annotations of each node.)
    """
    ###### Map Taxon info to tree
    for i in tips.index:
        # Get row
        tip = tips.ix[i]

        # Get node in tree
        node = tree.find_node_with_taxon_label(tip.id)

        # Look up labels in df
        for col in tips_cols:
            # add to annotations
            value = tip[col]
            node.taxon.annotations.add_new(col, value)

    # Map ancestors if info is given
    if ancs is not None and ancs_cols is not None:
        for i in ancs.index:
            anc = ancs.ix[i]

            # Get node in tree
            node = tree.find_node_with_label(str(anc.id))

            # If node is not root.
            if node is not None:
                # Look up labels in df
                for col in ancs_cols:
                    # add to annotations
                    value = anc[col]
                    node.annotations.add_new(col, value)

    return tree


def main():
    """Main function used by command line script.
    """
    # Set up parser.
    parser = argparse.ArgumentParser(
        description="Reroot a phylogenetic tree on branch "
                    "with the minimal ancestor deviation.")

    parser.add_argument("tree_file",
                        type=str,
                        help="Input tree file containing UID labels.")
    parser.add_argument("tips_file",
                        type=str,
                        help="Taxon CSV file.")
    parser.add_argument("ancs_file",
                        default=None,
                        type=str,
                        help="Ancestor CSV file.")
    parser.add_argument("--tips_cols",
                        default=["id"],
                        nargs="+",
                        type=str,
                        help="Columns in taxon CSV file to map to tree")
    parser.add_argument("--ancs_cols",
                        default=None,
                        type=str,
                        nargs="+",
                        help="Columns in ancestor CSV file to map to tree")

    # Parse the arguments
    args = parser.parse_args()

    # Built output filename from input tree name.
    output_file, _ = os.path.splitext(args.tree_file)
    output_path = "{}-decorated.nexus".format(output_file)


    # Read tree topology.
    tree = dendropy.Tree.get(path=args.tree_file, schema='newick')

    # Read tree data.
    tips = pd.read_csv(args.tips_file, index_col=0)
    ancs = pd.read_csv(args.ancs_file, index_col=0)

    # Get decorated Tree.
    tree = decorate(tree, tips,
                    tips_cols=args.tips_cols,
                    ancs=ancs,
                    ancs_cols=args.ancs_cols)

    # Write tree.
    tree.write(path=output_path, schema="nexus")


if __name__ == "__main__":
    main()
