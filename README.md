** Please read me **

## TTTTengine project:

This is the Tic Tac Toc Toe playing engine or just TTTTengine for short.

A simple 3 dimensional tic-tac-toe like game that is played on a 4x4x4 grid and requires you to get four in a row to win.

It is made to compile both as an XCode project and with unix make.


## unix:

Assuming you have the proper devlopement tools installed, you should be able to cd to the project directory and type make.
```
% cd TTTTengine
% make
```

A new binary file is created named tttt in the project directory.

Play a new game with:
```
% ./tttt -p
```


## Xcode:

You have to set the argument on the executable otherwise there won't be much to see. 

In the Xcode project select the application under the "Executables" Group and then perform a Get Info. In the dialog presented choose the Arguments Tab and add a new "-p" argument telling the application you want to play a game.

All the output is sent to the "Console"

Good luck with the build and have fun.

Alex Popadich


## License:

Licensed under the MIT License: http://www.opensource.org/licenses/mit-licenses.php