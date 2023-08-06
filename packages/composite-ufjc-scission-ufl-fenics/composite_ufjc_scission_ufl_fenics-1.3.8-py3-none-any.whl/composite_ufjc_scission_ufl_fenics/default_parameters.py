"""The default parameters module for the composite uFJC scission model
implemented in the Unified Form Language (UFL) for FEniCS.
"""

# import necessary libraries
from dolfin import *


def default_parameters():
    """Save default parameters.
    """
    p = Parameters("user_parameters")
    subset_list = ["post_processing"]
    for subparset in subset_list:
        subparset_is = eval("default_"+subparset+"_parameters()")
        p.add(subparset_is)
    return p

def default_post_processing_parameters():
    """Save default post-processing parameters.
    """
    post_processing = Parameters("post_processing")

    post_processing.add("axes_linewidth", 1.0)
    post_processing.add("font_family", "sans-serif")
    post_processing.add("text_usetex", True)
    post_processing.add("ytick_right", True)
    post_processing.add("ytick_direction", "in")
    post_processing.add("xtick_top", True)
    post_processing.add("xtick_direction", "in")
    post_processing.add("xtick_minor_visible", True)

    return post_processing