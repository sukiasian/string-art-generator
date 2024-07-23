# String Art Generator by Sam Sukiasian

This repository does not include canvas. It only processes a source image and finds points to connect.

## How it works? 

1. An input is given 
2. An empty matrix with 0 values is created. Then a random point is picked up on a canvas.
3. The algorithm draws hypothetical lines and calculates L2 norm between the initial (empty matrix) and the source image matrix. For better results, upsampling and downsampling techniques are used
4. The best point on a step is written in the output.