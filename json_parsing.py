"""
Parsing json utility
"""
import json


def read_json(jsondir: str):
    """
    Parses a json file for the SMILEs
    :param jsondir:
    :return: list of smiles
    """

    smiles_so_far = []
    with open(jsondir) as json_data:
        json_file = json.load(json_data)
        for i in range(0, len(json_file)):
            smiles_so_far.append(json_file[i]["smiles"])

    return smiles_so_far


def combine_json(json_reaction_dir: str, json_substrates_dir: str):
    """
    Combines the reaction json and the substrates json
    """
    final_json = {}
    substrates = read_json(json_substrates_dir)
    for i in range(0, len(substrates)):
        final_json["substrate" + str(i)] = substrates[i]
