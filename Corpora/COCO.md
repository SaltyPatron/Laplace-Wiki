# COCO

COCO is a multi-modal image, object-detection, segmentation, and captioning corpus queued for declarative `.recipe` and lossless image codec admission (`Batch 2`, `Laplace#1134`), pairing 2D image decompositions with grounded object instances, category hierarchies, and natural-language caption trajectories.

## Source & `Batch 2` admission queue

COCO ([Common Objects in Context](https://cocodataset.org/)) is queued for `Batch 2` multi-modal admission (`Laplace#1134`). Once its image codec and JSON `.recipe` land in [`recipes/`](https://github.com/SaltyPatron/Laplace-Engine/tree/main/recipes) and `recipes/order`, every image file decomposes into its canonical 2D spatial/pixel hierarchy while the companion annotation JSON files bind captions, categories, bounding boxes, and segmentation polygons/RLE masks onto that exact image content entity under one `COCO` witness trunk (`class AcademicCurated`).

Under the Recording Law ([Corpora](README.md#page-shape)):

- **Internal pointers resolved via `key`/`refer`:** `image.id`, `category.id`, and annotation `id` are COCO-internal integer pointers: `image_id` resolves directly to the decomposed image trunk (matched via `file_name`), `category_id` resolves to the category's canonical `name`, and raw numeric IDs are recorded nowhere.
- **Cross-modal collision:** Every natural-language `caption` decomposes by UAX #29 to sentences, words, graphemes, and Tier-0 codepoints, colliding directly with lexical, WordNet, Wiktionary, and Wikipedia entities on the same `lp_id`s, while `category` → `supercategory` attests taxonomic hierarchy (`[dog, supercategory, animal]`).

## Publisher record format

| Record | Fields | Target Laplace semantics | Specification |
| --- | --- | --- | --- |
| `images[]` | `id`, `width`, `height`, `file_name`, `license`, `flickr_url`, `coco_url`, `date_captured` | `id` (`key`) binds `file_name`'s decomposed image entity (`[width, height]` intrinsic dimensions; `date_captured` and mirror URLs are capture/hosting metadata) | [COCO Data Format](https://github.com/cocodataset/cocodataset.github.io/blob/master/dataset/format-data.htm) |
| `categories[]` | `id`, `name`, `supercategory` | `id` (`key`) resolves to category `name`, attesting `[name, supercategory]` taxonomic link | [COCO Object Detection](https://github.com/cocodataset/cocodataset.github.io/blob/master/dataset/format-data.htm) |
| `annotations[]` (instances) | `id`, `image_id`, `category_id`, `segmentation`, `area`, `bbox`, `iscrowd` | `id` omitted (`key`); `image_id` → image entity (`refer`); `category_id` → category `name` (`refer`); attests grounded region `[image, bbox / segmentation]` labeled with `category` (`iscrowd` qualifier, `area` observation) | [COCO Object Detection](https://github.com/cocodataset/cocodataset.github.io/blob/master/dataset/format-data.htm) |
| `annotations[]` (captions) | `id`, `image_id`, `caption` | `id` omitted (`key`); `image_id` → image entity (`refer`); attests `[image, caption_sentence]` linking visual structure to UAX #29 text | [COCO Image Captioning](https://github.com/cocodataset/cocodataset.github.io/blob/master/dataset/format-data.htm) |
