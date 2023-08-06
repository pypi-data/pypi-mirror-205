# mask2bbox

For a given mask, gets the coordinates of bounding box of each element of the mask. It will also allow for more operations in the future.

## Instalation

`pip install mask2bbox`

## Usage

```python
from mask2bbox import BBoxes

# Create a BBoxes object
all_BBoxes = BBoxes(args.mask)

# Expand the bounding boxes
all_BBoxes.expand(n=10)

# Save your bounding boxes
all_BBoxes.save_csv(args.output)
```

 
