# Import libraries
import time
import argparse
from BBoxes import BBoxes
from pathlib import Path

# Import third-party libraries
from skimage import io, exposure, transform, restoration
# from aicsimageio import AICSImage
import numpy as np
from tqdm import tqdm


# Get arguments
def get_arguments():
    # Start with the description
    description = "Converts all the masks in a folder to bounding boxes."

    # Add parser
    parser = argparse.ArgumentParser(description=description)

    # Add a group of arguments for input
    input = parser.add_argument_group(title="Input", description="Input arguments for the script.")
    input.add_argument("-m", "--mask", dest="mask", action="store", type=str, required=True,
                       help="Path to the mask file.")

    # Add a group of arguments for output
    output = parser.add_argument_group(title="Output", description="Output arguments for the script.")
    output.add_argument("-o", "--output", dest="output", action="store", type=str, required=True,
                        help="Path to the output file with the bounding boxes.")

    # Parse arguments
    args = parser.parse_args()

    # Standardize paths
    args.mask = Path(args.mask).resolve()
    args.output = Path(args.output).resolve()

    # Return arguments
    return args


# Main
def main(args):
    # Create a BBoxes object and get the bounding boxes
    all_BBoxes = BBoxes(args.mask)
    print(all_BBoxes.bboxes)

    all_BBoxes.expand(n=10)
    print(all_BBoxes.bboxes)

    # Save file
    all_BBoxes.save_csv(args.output)




# Run main
if __name__ == "__main__":
    # Get arguments
    args = get_arguments()

    # Run main and time it
    st = time.time()
    main(args)
    rt = time.time() - st
    print(f"Script finish in {rt // 60:.0f}m {rt % 60:.0f}s")