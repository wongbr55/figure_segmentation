"""
Contains code to run evaluation metrics for image segmentations
"""

from image_segmentation import segment_image
from typing import List
import os

def evaluate_image_segmentation(images: List[str], path_to_dir: str="") -> None:
    """
    Evaluates image segmentatiin algorithim by running image segmentaion on images
    """
    if path_to_dir != "":
        for filename in os.listdir(path_to_dir):
            try:
                segment_image(path_to_dir + "/" + filename, \
                    "evaluation/evaluation_results/" + filename + "reaction_image",\
                        "evaluation/evaluation_results/" + filename + "substrate")
            except:
                print("ERROR WITH FILE " + filename)
    else:
        for image in images:
            try:
                segment_image(image, image + "reaction_image", image + "substrate")
            except:
                print("ERROR WITH FILE " + image)


if __name__ == "__main__":
    test_set = [
        "./test/Wiley36_scheme_2.jpg",
        "./test/Wiley26_scheme_2.jpg",
        "./test/Wiley20_figure_1.jpg",
        "./test/Wiley14_scheme_2.jpg",
        "./test/Wiley2_table_3.png",
        "./test/RSC18_scheme_2.gif",
        "./test/RSC14_scheme_2.gif",
        "./test/test_scheme1.jpeg",
        "./test/Wiley41_scheme_3.jpg",
        "./test/Wiley16_scheme_2.jpg"
    ]
    negative_controls = [
        "./test/cs8b03302_0007.png",
        "./test/Wiley30_table_3.gif",
        "./test/Wiley39_scheme_2_rxn.jpg"
    ]

    evaluate_image_segmentation([], "./evaluation")