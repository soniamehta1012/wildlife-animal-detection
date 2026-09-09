# Wildlife Dataset Report

**Last generated:** 2026-09-09 08:52:42

## 1. Dataset Overview

| Metric | Value |
|---|---:|
| Training label files | 9,764 |
| Validation label files | 1,778 |
| Final selected classes | 40 |
| Training annotations | 9,981 |
| Validation annotations | 1,635 |
| Total selected annotations | 11,616 |
| Images containing selected animals | 7,771 |
| Images with 2+ animals | 2,018 |
| Images with 3+ animals | 718 |
| Maximum annotated animals in one image | 91 |

## 2. Objects Per Image

| Objects in image | Number of images |
|---|---:|
| 1 | 5,753 |
| 2 | 1,300 |
| 3 | 362 |
| 4 | 147 |
| 5 | 77 |
| 6+ | 132 |

## 3. Final 40 Classes

| New ID | Class | Train | Validation | Total |
|---:|---|---:|---:|---:|
| 0 | lion | 305 | 0 | 305 |
| 1 | tiger | 174 | 46 | 220 |
| 2 | bear | 113 | 33 | 146 |
| 3 | elephant | 384 | 72 | 456 |
| 4 | giraffe | 963 | 88 | 1,051 |
| 5 | rhinoceros | 452 | 78 | 530 |
| 6 | hippopotamus | 299 | 16 | 315 |
| 7 | zebra | 585 | 145 | 730 |
| 8 | gorilla | 598 | 34 | 632 |
| 9 | monkey | 197 | 55 | 252 |
| 10 | deer | 215 | 0 | 215 |
| 11 | mule_deer | 222 | 52 | 274 |
| 12 | moose | 296 | 0 | 296 |
| 13 | bison | 267 | 70 | 337 |
| 14 | pronghorn | 381 | 71 | 452 |
| 15 | wild_boar | 147 | 32 | 179 |
| 16 | fox | 101 | 0 | 101 |
| 17 | coyote | 146 | 40 | 186 |
| 18 | bobcat | 122 | 13 | 135 |
| 19 | mongoose | 239 | 27 | 266 |
| 20 | alligator | 187 | 0 | 187 |
| 21 | rattlesnake | 122 | 44 | 166 |
| 22 | western_diamondback_rattlesnake | 163 | 46 | 209 |
| 23 | california_sea_lion | 276 | 73 | 349 |
| 24 | elephant_seal | 169 | 40 | 209 |
| 25 | river_otter | 86 | 18 | 104 |
| 26 | raccoon | 95 | 18 | 113 |
| 27 | porcupine | 122 | 31 | 153 |
| 28 | marten | 103 | 23 | 126 |
| 29 | jackrabbit | 156 | 40 | 196 |
| 30 | chipmunk | 106 | 28 | 134 |
| 31 | muskrat | 83 | 22 | 105 |
| 32 | crow | 237 | 29 | 266 |
| 33 | goldfinch | 665 | 53 | 718 |
| 34 | sparrow | 295 | 52 | 347 |
| 35 | bald_eagle | 145 | 37 | 182 |
| 36 | golden_eagle | 180 | 39 | 219 |
| 37 | peacock | 159 | 55 | 214 |
| 38 | turkey_vulture | 187 | 49 | 236 |
| 39 | wild_turkey | 239 | 66 | 305 |

## 4. Dataset Validation Status

- Train images and labels were previously verified to match.
- Validation images and labels were previously verified to match.
- No malformed YOLO annotation entries were found.
- No invalid class IDs were found.
- No invalid bounding boxes were found.
- 528 empty label files were identified during validation.
- Empty-label images require review before final cleaning.

## 5. Multi-Animal Analysis

The current dataset contains **2,018 images with two or more selected animals**.
There are **718 images with three or more selected animals**.
Therefore, the current dataset already contains a substantial amount of multi-animal training data. Replacing the dataset solely to obtain group-animal images is not currently justified.

## 6. Current Task 5 Status

- Final target: 40 wildlife classes
- Class names standardized
- Original dataset preserved
- Class-selection dry run completed
- Train/validation class analysis completed
- Multi-animal image analysis completed
- Next step: inspect highly crowded images and then create the cleaned 40-class dataset.