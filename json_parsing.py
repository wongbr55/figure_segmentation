"""
Parsing json utility
"""
import json
import argparse
from typing import List

####################################
# get yield from labels
####################################


def get_yield_from_comment(labels: List[List[str]]):
    """
    Gets the yield information from the list of labels provided
    Returns the proper yield in an integer format
    """
    final_candidate = -1
    for list_of_labels in labels:
        candidate = -1
        for string in list_of_labels:
            curr_candidate = get_yield_from_comment_helper(string)
            if candidate == -1:
                candidate = curr_candidate
            elif candidate != curr_candidate:
                candidate = curr_candidate
        if final_candidate == -1:
            final_candidate = candidate
        elif final_candidate != candidate:
            final_candidate = candidate

    return final_candidate


def get_yield_from_comment_helper(comment: str):
    """
    Gets yield information from comment
    """
    curr_yield = ""
    for i in range(0, len(comment)):
        if comment[i] == '%' or (not comment[i].isalnum() and comment[i] != " "):
            if i - 2 >= 0 and comment[i - 2].isnumeric():
                curr_yield += comment[i - 2]
            if i - 1 >= 0 and comment[i - 1].isnumeric():
                curr_yield += comment[i - 1]
            break

    if curr_yield != "":
        return int(curr_yield) / 100
    else:
        return -1


####################################
# get reactant and product info
####################################


def get_smiles_from_list(info: List[dict]):
    """
    Gets the SMILEs from a list containing SMILEs, labels, and panels
    Expects json format from ReactionDataExtractor
    """
    smiles_so_far = []
    for dictionary in info:
        smiles_so_far.append(dictionary["smiles"])

    return smiles_so_far


####################################
# combining json main function
####################################


def combine_json(json_reaction_dir: str, json_substrates_dir: str):
    """
    Combines the reaction json and the substrates json
    Puts all relevant information in a json file
    """
    # read substrate information
    all_information = {}
    substrate_smiles_and_yields = []
    with open(json_substrates_dir) as json_substrate_data:
        json_substrate = json.load(json_substrate_data)

        for i in range(0, len(json_substrate)):
            curr_smiles = json_substrate[i]["smiles"]
            curr_yield = get_yield_from_comment(json_substrate[i]["labels"])
            curr_substrate_dict = {"smiles": curr_smiles, "yield": curr_yield}
            substrate_smiles_and_yields.append(curr_substrate_dict)

    all_information["substrates"] = substrate_smiles_and_yields

    # read reactants and products information
    with open(json_reaction_dir) as json_raction_data:
        json_reaction = json.load(json_raction_data)

        all_information["reactant"] = get_smiles_from_list(json_reaction["nodes"][0])
        all_information["product"] = get_smiles_from_list(json_reaction["nodes"][2])

    # write data to new json
    with open('reaction_information.json', 'w') as f:
        json.dump(all_information, f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--reactantspath', type=str, required=True,
                        help='Path to reaction json')
    parser.add_argument('--substratepath', type=str, required=True,
                        help='Path to substrate json')

    arguments = vars(parser.parse_args())
    combine_json(arguments['reactantspath'], arguments["substratepath"])
