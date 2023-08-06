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

        # Get the shape of the mask image
        self.mask_shape = self.mask.shape

        # Get the bounding boxes
        self.bboxes = self.original_bboxes = self._get_bboxes()
        self.nboxes = self.original_nboxes = self.bboxes.shape[0]

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

        # Since the bounding boxes are calculated from the group identities we can add column with the identities
        bboxes = np.column_stack((np.unique(stacked[:, 0]), bboxes))

        # Return the bounding boxes
        return bboxes

    def expand(self, n):
        # Expand the bounding boxes by n pixels, but not beyond the image size.
        self.bboxes = np.array(list(map(lambda x: np.array([x[0],
                                                            max(x[1] - n, 0),
                                                            min(x[2] + n, self.mask_shape[0]),
                                                            max(x[3] - n, 0),
                                                            min(x[4] + n, self.mask_shape[1])]), self.bboxes)))

    def remove_edge_boxes(self):
        # Removes the bonds that are on the edge of the image
        self.bboxes = self.bboxes[np.where((self.bboxes[:, 1] > 0) &
                                           (self.bboxes[:, 2] < self.mask_shape[0]) &
                                           (self.bboxes[:, 3] > 0) &
                                           (self.bboxes[:, 4] < self.mask_shape[1]))]
        self.nboxes = self.bboxes.shape[0]

    def get_bbox_dims(self):
        # Get the sides of the bounding boxes
        return np.array([self.bboxes[:, 0],
                         self.bboxes[:, 2] - self.bboxes[:, 1],
                         self.bboxes[:, 4] - self.bboxes[:, 3]]).T

    def get_bbox_areas(self):
        # Get the areas of the bounding boxes
        return np.array([self.bboxes[:, 0],
                         (self.bboxes[:, 2] - self.bboxes[:, 1]) * (self.bboxes[:, 4] - self.bboxes[:, 3])]).T

    def get_bbox_ratios(self):
        # Get the aspect ratios of the bounding boxes
        return np.array([self.bboxes[:, 0],
                         (self.bboxes[:, 2] - self.bboxes[:, 1]) /
                         (self.bboxes[:, 4] - self.bboxes[:, 3])]).T

    def get_bbox_centers(self):
        # Get the centers of the bounding boxes
        return np.array([self.bboxes[:, 0],
                         (self.bboxes[:, 2] + self.bboxes[:, 1]) // 2,
                         (self.bboxes[:, 4] + self.bboxes[:, 3]) // 2]).T

    def save_csv(self, output_file):
        # Save the bounding boxes to a csv file
        np.savetxt(output_file, self.bboxes, delimiter=",", fmt="%d")
