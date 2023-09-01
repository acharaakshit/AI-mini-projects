# AI-mini-projects
AI projects for learning concepts

This respository contains the toy projects chosen from this [course](https://cs50.harvard.edu/extension/ai/2020/spring/#knowledge) understanding the concepts of Artificial Intelligence with Python.

- **tictactoe**  contains the implementation of minimax algorithm for tic-tac-toe. The complete description of the problem can be found [here](https://cs50.harvard.edu/extension/ai/2020/spring/projects/0/tictactoe/).

- **minesweeper** contains the implementation of an AI for Minesweeper which uses the concept of knowledge and logic. The description of the problem can be found [here](https://cs50.harvard.edu/extension/ai/2020/spring/projects/1/minesweeper/).

- **heredity** uses the concept of Uncertainty (joint probability in specific). The desciption of the problem can be found [here](https://cs50.harvard.edu/extension/ai/2020/spring/projects/2/heredity/). To run the script use: `python heredity.py data/family0.csv` (any of the csv files in the data folder can be used as an argument).

- **crossword** uses constraint programming to generate a crossword puzzle. The problem description can be found [here](https://cs50.harvard.edu/extension/ai/2020/spring/projects/3/crossword/). To run the script use `python generate.py data/structure1.txt data/words1.txt output.png` where the first agrument is a structure, second argument is the words file and third is for generating the output.png file for the puzzle.

- **nim** contains the implementation of nim game using Q-Learning. The problem description is [here](https://cs50.harvard.edu/extension/ai/2020/spring/projects/4/nim/).

- **traffic** uses convolutional neural networks to identify traffic signs. The problem description is [here](https://cs50.harvard.edu/extension/ai/2020/spring/projects/5/traffic/). The dataset can be downloaded from [here](https://cdn.cs50.net/ai/2020/spring/projects/5/gtsrb.zip). To run the script use `python traffic.py /full/path/to/dataset/`.

- **parser** shows the noun phrase chunks for a sentence using natural language processing. The problem description is [here](https://cs50.harvard.edu/extension/ai/2020/spring/projects/6/parser/). To run the script use `python parser.py sentences/3.txt` where txt file can be any text file from sentences folder, or alternatively you can just use
`python parser.py` and provide a custom sentence as input.
