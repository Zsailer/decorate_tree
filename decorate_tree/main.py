import pandas as pd

def decorate(tree, taxon_dataframe, anc_dataframe=None, taxon_labels=["accver"], anc_labels=[]):
    """Map taxon attributes from dataframe to a dendropy tree."""
    df = taxon_dataframe
    
    ###### Map Taxon info to tree
    # Iterate over index
    for uid in df.index:
        # Get node in tree
        node = tree.find_node_with_taxon_label(uid)
        
        # Look up labels in df
        for label in taxon_labels:
            # add to annotations
            value = df[label][uid]
            node.taxon.annotations.add_new(label, value)
            
    # Map ancestors if info is given
    df = anc_dataframe
    if anc_dataframe != None and len(anc_labels) != 0:
        for uid in df.index:

            # Get node in tree
            node = tree.find_node_with_label(uid)

            # Look up labels in df
            for label in taxon_labels:
                
                # add to annotations
                value = df[label][uid]
                node.taxon.annotations.add_new(label, value)
                
    return tree



            