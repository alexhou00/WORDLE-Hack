# WORDLE-Hack
Crack the WORDLE game by optimizing the strategy with the help of Python.

## Installation
Since the author is too lazy to pack the project as a .exe file, use the .py file to run instead.<br>
But first, you need to install the necessary packages.

### Installing wordfreq
This project uses the module wordfreq to access the data of every word's frequency in English.<br>
You can install the module through the command:
``` 
pip install wordfreq
```
For more information about installing the module, see [here](https://pypi.org/project/wordfreq/).

## Running the project
It offers you two ways to execute this project, either through the GUI (Graphic User Interface) or the terminal. Just follow the steps in the program, and you'll figure out how.<br>

### Execute through GUI
Execute the _wordle_hack_gui.py_ file. Below is an example when you run the program. <br>
<img src="/assets/example.png" alt="execution example" width="300"/> <br>
First, select the number of letters on the left.<br>
Then enter both the word entered in the wordle game and the color results the game gave you. Note that you can either use the virtual keyboard on the screen or use your keyboard to enter (the number 1, 2, 3 keys are for colors, the 0 key for the color backspace). <br>
Hit enter then the program will tell you possible answers. The program will give you the ten most likely results. <br>
Repeat the above steps until you win (probably).<br>
Note that you can access Google Translate by hitting the Transl. button when you don't know the meaning of the current word.

### Execute through the terminal 
Execute the _wordle_hack_terminal.py_ file. 
First, enter how many numbers are there in a word, default is 5. Second, it will ask you if you want to get some recommended words to start, just answer yes or no in any form (which mean entering y/n/yes/no will all be fine and it is case insensitive). <br>
Third, enter the green (orange in the colorblind mode) letters with wildcards, wildcards are `.`. For example, if the word is **LEAST**, and you got green on the letter L, S and T, then enter `l..st`. If there are no green letters then enter as many dots (`.`) as the length of the word. <br>
After that, enter the yellow (blue in the colorblind mode) letters with their positions and seperate each group of them with one space. For example, if the word is **LEAST**, and you got yellow on the letter E and A, then enter `e2 a3` since the letter E is on the second position and the letter A is on the third position. <br>
Then, enter the dark gray letters in any order. For example, if the word is **LEAST**, and you got dark gray on the letter L, S and T, then enter `lst`.
Type in the number of words you want to print out, and if you don't continue with the game, the program will exit.

## Notes

### Credits
Thanks to [dwyl](https://github.com/dwyl) for the text file containing 479k English words for my dictionary.
