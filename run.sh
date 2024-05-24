#!/usr/bin/env bash

# segment figures
python figure_segmentation/image_segmentation.py --imgpath $1 --reactfilename reactaction --substratefilename substrates
# call reactiondataextractor2 on both reaction and substrate images
python reactiondataextractor2/reactiondataextractor/extract.py --path ./reaction.jpeg --output_dir ./
python reactiondataextractor2/reactiondataextractor/extract.py --path ./products.jpeg --output_dir ./
# combine both jsons into one final json
python figure_segmentation/json_parsing.py --reactantspath ./reaction.json --substratepath ./substrates.json
