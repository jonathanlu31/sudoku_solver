# Sudoku Solver

This is a sudoku solver built in Python using the backtracking algorithm. It features a playable GUI with multiple boards of varying difficulty. 

## Instructions

To play the game, run sudoku_GUI.py with a second argument describing the intended difficulty (easy, medium, hard, expert):

```bash
python3 sudoku_GUI.py easy
```

Click on a box to select it and press any number key to write a number in pencil mode. Press ENTER if you wish to input your pencil value as an actual value. If the value is invalid, the box will have a red outline. To remove an actual value, press BACKSPACE. To remove a pencil value, press P to switch to pencil mode and press BACKSPACE. Press P again to revert. If you would like the autosolver to solve the board, press SPACE and watch it go at it. 

</br>
<p align='center'>
  <img src='https://media.giphy.com/media/lnS6A5WJSfjygIFd2a/giphy.gif'/>
</p>
</br>

(Tip: the hard and expert boards take around 4 minutes for the autosolver to solve, but you can force quit to leave early)


## Acknowledgments

* [techwithtim](https://github.com/techwithtim)
