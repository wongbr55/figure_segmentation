"""
Parsing json utility
"""
import json

####################################
# get yield from labels
####################################


def get_yield_from_comment(labels: list[list[str]]):
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
    seen_percent = False
    for i in range(0, len(str)):
        if comment[i] == '%' or (not comment[i].isalnum() and comment[i] != " "):
            seen_percent = True
        elif seen_percent and comment[i] != ' ':
            curr_yield += comment[i]
        elif seen_percent and comment[i] == ' ':
            break
    return int(curr_yield) / 100


####################################
# get reactant and product info
####################################


def get_smiles_from_list(info: list[dict]):
    """
    Gets the SMILEs from a list contatingin, SMILEs, labels, and panels
    Expects format from ReactionDataExtractor
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

        all_information["reactant"] = get_smiles_from_list(json_reaction[0])
        all_information["product"] = get_smiles_from_list(json_reaction[2])

    # write data to new json
    with open('reaction_information.json', 'w') as f:
        json.dump(all_information, f)
