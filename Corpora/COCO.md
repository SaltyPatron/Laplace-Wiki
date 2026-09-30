# COCO

COCO has no recipe yet, so its annotation JSON and images are not ingested and attest nothing.

## Source

No directory under [`recipes/`](https://github.com/SaltyPatron/Laplace-Engine/tree/main/recipes) reads this collection, and `recipes/order` does not name it. Until a recipe exists, nothing in it is decomposed, recorded, or attested; see [Attestations](../Semantics/Attestations.md#observations). The format below is the publisher's, kept so that a recipe can be written from it.

## Format

| Record | Fields in order | What a record is | Specification |
| --- | --- | --- | --- |
| image | id, width, height, file_name, license, flickr_url, coco_url, date_captured | The image record in the annotation JSON. The JPEG files in this drop are the pictures, not that JSON record. | [Data format](https://github.com/cocodataset/cocodataset.github.io/blob/master/dataset/format-data.htm) |
| object annotation | id, image_id, category_id, segmentation, area, bbox, iscrowd | One object instance: category id, segmentation mask, area, enclosing box, and whether the instance is a crowd. | [Data format, object detection](https://github.com/cocodataset/cocodataset.github.io/blob/master/dataset/format-data.htm) |
| category | id, name, supercategory | The mapping of a category id to its name and supercategory. | [Data format, object detection](https://github.com/cocodataset/cocodataset.github.io/blob/master/dataset/format-data.htm) |
| caption annotation | id, image_id, caption | One caption that describes the image named by image_id. | [Data format, image captioning](https://github.com/cocodataset/cocodataset.github.io/blob/master/dataset/format-data.htm) |
