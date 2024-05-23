"""
Code to cut a chemical reaction diagram with reaction arrows and substrates in half
to only contain reaction arrow section and substrates
"""
import cv2
import numpy as np
import chemschematicresolver.extract as extract


def check_row_white(image_array: np.array, i: int):
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


def check_row_solid_line(image_array: np.array, i: int):
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


def check_row_line(image: np.array):
    """
    checks row i for dotted line
    :param image
    :return: True or False
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian Blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # Apply edge detection (Canny or threshold)
    edges = cv2.Canny(blurred, 50, 150)

    lines = cv2.HoughLinesP(edges, 15, np.pi / 180, threshold=50, minLineLength=50, maxLineGap=10)

    line_image = image.copy()
    max_diffs = [0, 0]
    y_vals = [0, 0]
    for line in lines:
        for x1, y1, x2, y2 in line:
            if abs(x2 - x1) > abs(max_diffs[0] - max_diffs[1]):
                max_diffs[0], max_diffs[1] = x2, x1
                y_vals[0], y_vals[1] = y2, y1

    cv2.line(line_image, (max_diffs[1], y_vals[1]), (max_diffs[0], y_vals[1]), (0, 255, 0), 2)
    cv2.waitKey(0)

    for index in range(0, len(line_image)):
        if check_row_solid_line(line_image, index):
            return index
    return -1


def save(image_array: np.array, top_file_name: str, bottom_file_name: str, row_after_reaction: int, buffer: int):
    """
    Saves reaction and substrate images
    :param image_array:
    :param top_file_name:
    :param bottom_file_name:
    :param row_after_reaction:
    :param buffer:
    :return: number of substrate images
    """
    top_image = image_array[:row_after_reaction]
    bottom_image = image_array[row_after_reaction + buffer:]
    cv2.imwrite(top_file_name, top_image)
    cv2.imwrite(bottom_file_name, bottom_image)


def segment_reactants_and_substrates(filedir: str):
    """
    Segments the image and saves them as two seperate images
    :param filedir:
    :return:
    """
    image_array = cv2.imread(filedir)

    # check for dotted line
    row_after_reaction = 0
    have_seen_top = False

    # check for line via opencv
    dotted_index = check_row_line(image_array)
    if dotted_index != -1:
        row_after_reaction = dotted_index
        save(image_array, "reaction.jpeg", "substrates.jpeg", row_after_reaction, 20)
        return

    # if we get nothing we check manually
    for i in range(0, len(image_array)):
        # check for horizontal line
        if check_row_solid_line(image_array, i):
            row_after_reaction = i
            break
        # if there is no line, check for white horizontal lines
        if check_row_white(image_array, i) and not have_seen_top:
            have_seen_top = True
        elif check_row_white(image_array, i) and have_seen_top:
            row_after_reaction = i
            break

    # save images
    save(image_array, "reaction.jpeg", "substrates.jpeg", row_after_reaction, 20)
    return extract.extract_image("substrates.jpeg")
