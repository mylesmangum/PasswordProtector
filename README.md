# PasswordProtector
Authors: 
Dominic Gordillo, Dylan Edwards, Joe Zink, Myles Mangum, Tyler Whittaker

How to develop a secure program.  This is a programming project for CS-3100 at UVU from Group 9
# Requirements
This program was written in Python 3.10.
# How to run
The current project is run through an executable file in the repo.  To launch the project simply execute the file `manager.exe` within the `dist` folder.

Depending on how Python was installed, the usage of python3 or py3 may differ, if you run into any issues try changing the initial command
1. Start in the base folder of this project and input 
```console
cd ./src
python3 manager.py
```
2. The program has multiple files, but is executed through the manager.py file
3. All command inputs within the terminal application are scrubbed for capitalization, so to quit the program, simply input `exit`
# Known Issues
This project is fairly bare bones at the moment, currently it is not very secure.  To access all information, you can download an SQLite3 database manager and see all available tables within the database. 

The passwords are also stored in plaintext, so don't put any actual passwords into this please!
