"""
Contains code to run evaluation metrics for image segmentations
"""

from image_segmentation import segment_image
from typing import List

def evaluate_image_segmentation(images: List[str]) -> None:
    """
    Evaluates image segmentatiin algorithim by running image segmentaion on images
    """
    for image in images:
        try:
            segment_image(image, image + "reaction_image", image + "substrate")
        except:
            print("ERROR WITH FILE " + image)


if __name__ == "__main__":
    images = [
        "./evaluation/Wiley36_scheme_2.jpg",
        "./evaluation/Wiley26_scheme_2.jpg",
        "./evaluation/Wiley20_figure_1.jpg",
        "./evaluation/Wiley14_scheme_2.jpg",
        "./evaluation/Wiley2_table_3.png",
        "./evaluation/RSC18_scheme_2.gif",
        "./evaluation/RSC14_scheme_2.gif",
        "./evaluation/10.1021_acs_orglett.2c01930_figure3.jpeg",
        "./evaluation/Wiley41_scheme_3.jpg",
        "./evaluation/Wiley16_scheme_2.jpg"
    ]
    for image in images:
        evaluate_image_segmentation(images)