# COCO

COCO is a large-scale object detection, segmentation, and captioning dataset: each caption describes the specified image, each object instance annotation contains the category id and segmentation mask of the object and an enclosing bounding box measured from the top left image corner, and the image files are the pictures those annotations name.

## Value

| Attestation | What it means | Lands on | Value | Witness | Proof |
| --- | --- | --- | --- | --- | --- |
| category | The categories field stores the mapping of category id to category and supercategory names. A category object has id, name, and supercategory. An object annotation's category_id is that id. | an object annotation | category_id, and categories[].name | COCO annotation JSON | [Data format, object detection](https://github.com/cocodataset/cocodataset.github.io/blob/master/dataset/format-data.htm) |
| bbox | An enclosing bounding box is provided for each object. Box coordinates are measured from the top left image corner and are 0-indexed. The field is [x, y, width, height]. | an object annotation, on the picture | [x, y, width, height] | COCO annotation JSON | [Data format, object detection](https://github.com/cocodataset/cocodataset.github.io/blob/master/dataset/format-data.htm) |
| segmentation | Each object instance annotation contains the segmentation mask of the object. For a single object (iscrowd=0) the mask is polygons; for a collection of objects (iscrowd=1) it is RLE. A single object may require multiple polygons. | an object annotation, on the picture | RLE or [polygon] | COCO annotation JSON | [Data format, object detection](https://github.com/cocodataset/cocodataset.github.io/blob/master/dataset/format-data.htm) |
| caption | Each caption describes the specified image. Each image has at least 5 captions (some images have more). | the picture named by image_id | a string | COCO caption annotation | [Data format, image captioning](https://github.com/cocodataset/cocodataset.github.io/blob/master/dataset/format-data.htm) |

## Format

| Record | Fields in order | What a record is | Proof |
| --- | --- | --- | --- |
| image | id, width, height, file_name, license, flickr_url, coco_url, date_captured | The image record in the annotation JSON. The JPEG files in this drop are the pictures, not that JSON record. | [Data format](https://github.com/cocodataset/cocodataset.github.io/blob/master/dataset/format-data.htm) |
| object annotation | id, image_id, category_id, segmentation, area, bbox, iscrowd | One object instance: category id, segmentation mask, area, enclosing box, and whether the instance is a crowd. | [Data format, object detection](https://github.com/cocodataset/cocodataset.github.io/blob/master/dataset/format-data.htm) |
| category | id, name, supercategory | The mapping of a category id to its name and supercategory. | [Data format, object detection](https://github.com/cocodataset/cocodataset.github.io/blob/master/dataset/format-data.htm) |
| caption annotation | id, image_id, caption | One caption that describes the image named by image_id. | [Data format, image captioning](https://github.com/cocodataset/cocodataset.github.io/blob/master/dataset/format-data.htm) |
