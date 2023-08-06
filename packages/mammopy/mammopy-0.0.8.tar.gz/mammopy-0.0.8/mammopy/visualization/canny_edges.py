import os
import numpy as np
from skimage import feature


def canny_edges(image_array):
    """
    Detect edges using the Canny algorithm.
    
    Parameters:
    image_array (numpy.ndarray): The input image array
    
    Returns:
    edges (numpy.ndarray): A binary edge map with detected edges marked with 1.
    
    Raises:
    TypeError: If the input image is not a numpy array.
    """
    if not isinstance(image_array, np.ndarray):
        raise TypeError("Input image must be a numpy array.")
    
    # Detect edges using Canny algorithm with sigma value of 3.
    edges = feature.canny(image_array, sigma=3)
    
    return edges