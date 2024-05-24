#!/usr/bin/env bash

# activate conda envrionment
conda activate rde2
# segment figures
python figure_segmentation/image_segmentation.py --imgpath $1 --reactfilename reactaction --substratefilename substrates
# call reactiondataextractor2 on both reaction and substrate images
python reactiondataextractor2/reactiondataextractor/extract.py --path ./reaction.jpeg --outdir ./
python reactiondataextractor2/reactiondataextractor/extract.py --path ./products.jpeg --outdir ./
# combine both jsons into one final json
python figure_segmentation/json_parsing.py --reactantspath ./reaction.json --substratepath ./substrates.json
# deactivate json
conda deactivate
