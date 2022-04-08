# String Art Portraits
A greedy algorithm for generating string art portraits.

# Set-up Instructions

1) Clone the repository

        https://github.com/akshatphumbhra/StringArt.git

2) Install the requirements

        $ pip install -r requirements.txt

3) Adjust parameters in parameters.py. This includes all options for variations in hyper-parameters as well as different functionality. 

4) To create a portrait based on a single target image with defined parameters, run the python script.

        $ python3 stringArt.py

5) To run simulations of multiple images with changing parameters, adjust the paramDict variable in generateArt.py and run:

        $ python3 generateArt.py

The imgs/ directory contains the target images used in my simulations. The simulations/ directory contains the results of the simulations in both png and eps formats. 