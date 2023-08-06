# Import libraries
import time
import argparse
from pathlib import Path

# Import third-party libraries
from skimage import io
import numpy as np

# Create a bbox class
class BBoxes:
    """Class to calculate and represent bounding boxes from a mask file"""
    # Constructor
    def __init__(self, mask_file):
        # Read in the mask file
        self.mask = io.imread(mask_file)

        # Get the shape of the mask
        self.shape = self.mask.shape

        # Get the bounding boxes
        self.bboxes = self._get_bboxes()

    def _get_bboxes(self):
        # Get indexes of nonzero elements
        nonzero = np.array(np.nonzero(self.mask)).T

        # Get cell identities of nonzero matrix
        identities = np.array(list(map(lambda x: self.mask[x[0]][x[1]], nonzero)))

        # Stack identities with the nonzero matrix
        stacked = np.column_stack((identities, nonzero))

        # sort them by identity
        stacked = stacked[stacked[:, 0].argsort()]

        # Group them by identity
        grouped = np.split(stacked[:, 1:], np.unique(stacked[:, 0], return_index=True)[1][1:])

        # Get the bounding boxes for each identity
        bboxes = np.array(list(map(lambda x: np.array([min(x[:, 0]), max(x[:, 0]), min(x[:, 1]), max(x[:, 1])]),
                                    np.array(grouped, dtype=object))))

        # Return the bounding boxes
        return bboxes

    def expand(self, n):
        # Expand the bounding boxes by n pixels, but not beyond the image size.
        self.bboxes = np.array(list(map(lambda x: np.array([max(x[0] - n, 0),
                                                            min(x[1] + n, self.shape[0]),
                                                            max(x[2] - n, 0),
                                                            min(x[3] + n, self.shape[1])]), self.bboxes)))

    def save_csv(self, output_file):
        # Save the bounding boxes to a csv file
        np.savetxt(output_file, self.bboxes, delimiter=",", fmt="%d")
