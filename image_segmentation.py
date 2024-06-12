"""
Code to cut a chemical reaction diagram with reaction arrows and substrates in half
to only contain reaction arrow section and substrates
"""
import cv2
import numpy as np
import argparse
import imageio
from typing import List


def check_row_white(image_array: np.array, i: int) -> bool:
    """
    Checks row i to see if it is full of white squares
    :param image_array:
    :param i:
    :return: True or False
    """
    white_amount = 255

    for j in range(0, len(image_array[i])):
        if image_array[i][j][0] < white_amount or image_array[i][j][1] < white_amount\
                or image_array[i][j][2] < white_amount:
            return False
    return True


def check_row_solid_line(image_array: np.array, i: int) -> bool:
    """
    Checks a given row to see if there is a horizontal line
    :param image_array:
    :param i:
    :return: True or False
    """

    base_colour = image_array[i][0]

    for j in range(0, len(image_array[i])):
        if base_colour[0] != image_array[i][j][0] or base_colour[1] != image_array[i][j][1] \
                or base_colour[2] != image_array[i][j][2]:
            return False

    return False


def check_row_line(image: np.array, lines: List[List[int]]):
    """
    Image for a line
    :param image
    :return: True or False
    """
    x_vals = [0, 0]
    y_vals = [0, 0]
    for line in lines:
        for x1, y1, x2, y2 in line:
            if abs(x2 - x1) > abs(x_vals[0] - x_vals[1]):
                x_vals[0], x_vals[1] = x2, x1
                y_vals[0], y_vals[1] = y2, y1

    # check to see if the longest detected line is actually long enough to be a seperating line
    if abs(abs(x_vals[0] - x_vals[1]) - image.shape[1]) < 1 * len(image) // 4:
        return y_vals[0]
    return -1


def save(image_array: np.array, top_file_name: str, bottom_file_name: str, row_after_reaction: int, buffer: int) -> None:
    """
    Saves reaction and substrate images
    :param image_array:
    :param top_file_name:
    :param bottom_file_name:
    :param row_after_reaction:
    :param buffer:
    :return: number of substrate images
    """
    top_image = image_array[:row_after_reaction + buffer]
    bottom_image = image_array[row_after_reaction + buffer:]
    cv2.imwrite(top_file_name, top_image)
    cv2.imwrite(bottom_file_name, bottom_image)


def compare_gaps(gaps: List[List[int]], whitespace_gap_tolerance: int) -> int:
    """
    Compares lengts of gaps of whitespace to each most recent gap to see if there is a valid implicit sepereator
    Returns -1 if none or the row index of most recent gap otherwise (then it is seperator)
    """
    curr_gap = gaps[-1]
    for gap in gaps:
        if gap[0] + whitespace_gap_tolerance <= curr_gap[0]:
            return curr_gap[1]

    return -1


def get_seperation_above_threshold(image: np.array, threshold: int, lines: List[List[int]],
                                   line_difference_threshold: int, whitespace_gap_tolerance: int) -> int:
    """
    Finds the implicit seperation of a reaction portion and substrate scope of a reaction image
    returns the index of implicit seperation
    """

    coord_of_reaction = 0
    for line in lines:
        for x1, y1, x2, y2 in line:
            if abs(y1 - y2) < line_difference_threshold and y1 < threshold and y2 < threshold:
                coord_of_reaction += y1
                break
        if coord_of_reaction != 0:
            break

    # check for whitespace
    # we expect there to be a gap between the molecules and labels in reaction portion
    # we record that gap and move along

    gaps = []
    currently_gap = False
    for row_index in range(0, len(image)):
        # edit current gaps seen
        row_is_white = check_row_white(image, row_index)
        if row_is_white and not currently_gap:
            currently_gap = True
            gaps.append([1, row_index])
        elif row_is_white and currently_gap:
            gaps[-1][0] += 1
        # if we get here, we want to check the values of our current whitespace gaps
        elif not row_is_white and currently_gap:
            currently_gap = False
            # if there is only one gap, we have nothing to compare to so we move along
            # if there are at least two gaps we compare with previous gaps
            possible_seperator = compare_gaps(gaps, whitespace_gap_tolerance)
            if possible_seperator != -1:
                return (possible_seperator + row_index) // 2
    return -1


def segment_reactants_and_substrates(filedir: str, reaction_file_name: str, substrate_file_name: str) -> None:
    """
    Segments the image and saves them as two seperate images
    :param filedir:
    :return:
    """

    image_array = cv2.imread(filedir)
    if image_array is None:
        # if we have some form of gif or animated image, we assume that the information we need is in first slide
        alternate_image = imageio.mimread(filedir)
        image_array = alternate_image[0]

    # check to see if there is a horizontal line of full length
    gray = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)

    # apply Gaussian Blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # apply edge detection (Canny or threshold)
    edges = cv2.Canny(blurred, 50, 150)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=50, minLineLength=50, maxLineGap=10)

    # debugging code
    # for line in lines:
    #     for x1, x2, y1, y2 in line:
    #         cv2.line(image_array, (x1, x2), (y1, y2), (0, 0, 255), 2)
    # cv2.imshow("Image", image_array)
    # cv2.waitKey(0)

    index_of_line = check_row_line(image_array, lines)
    # check for solid line seperating the reactants and products
    if index_of_line != -1:
        print("Used line")
        save(image_array, reaction_file_name + ".jpeg", substrate_file_name + ".jpeg", index_of_line, 10)
        return
    # otherwise there is no seperating line
    index_of_seperator = get_seperation_above_threshold(image_array, len(image_array) // 5, lines, 10, 0)
    if index_of_seperator != -1:
        print("Used whitespace")
        save(image_array, reaction_file_name + ".jpeg", substrate_file_name + ".jpeg", index_of_seperator, 10)
        return

    print("ERROR: Unable to segment image")
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--imgpath', type=str, required=True,
                        help='Path to a single reaction image')
    parser.add_argument('--reactfilename', type=str, required=True,
                        help='Name of reactant json')
    parser.add_argument('--substratefilename', type=str, required=True,
                        help='Name of substrate json')

    options = vars(parser.parse_args())
    segment_reactants_and_substrates(options["imgpath"], options["reactfilename"], options["substratefilename"])
