#!/usr/bin/env bash

# segment figures
echo "Segmenting figures..."
python figure_segmentation/image_segmentation.py --imgpath $1 --reactfilename reaction --substratefilename substrates
# call reactiondataextractor2 on both reaction and substrate images
echo "Extracting SMILEs from reaction..."
python reactiondataextractor2/reactiondataextractor/extract.py --path ./reaction.jpeg --output_dir ./ > /dev/null 2> /dev/null
echo "Extracting SMILEs from substrates..."
python reactiondataextractor2/reactiondataextractor/extract.py --path ./substrates.jpeg --output_dir ./ > /dev/null 2> /dev/null
# combine both jsons into one final json
echo "Combining jsons..."
python figure_segmentation/json_parsing.py --reactantspath ./reaction.json --substratepath ./substrates.json
# clean up and remove unused images and jsons
echo "Cleaning up..."
rm substrates.jpeg
rm reaction.jpeg
rm reaction.json
rm substrates.json
echo "Done! All SMILEs and yield information can now be found in reaction_information.json"
