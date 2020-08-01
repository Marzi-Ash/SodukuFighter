# SodukuFighter
                                                          
                                                                                    
                  .-.________                               	 ________.-.                    
             ----/ \_)_______)         Sudoku Fighter        	(_______(_/ \----               
                (    ()___)                                 	  (___()     )                  
                     ()__)                                       	   (__()                        
             ----\___()_)                                       	    (_()___/----                
                                                                
                                                                                         
__________________________________________________________________________________________
The designed soduku fighter agent, will try ti find an answer for the given osduku problem. The agent uses different heuristic approaches consisting Minimum Remaining Value, Degree Heuristic, Least Constraining Value, Constraint Propagation using Forward Checking. Two other practical algorithms are also used in reaching the goal state, Update by Single Value and Update by 2 Variables with 2 Values. The detailed explanation exists in the SodukuFighter.pdf.

To compile:

1)Compile main.py with python 3	

2)Before compile you need to install the math, copy, time and tabulate packages for python (if already installed, fine)

3)Be sure for the compiling write "python3 main.py input_file.txt" input file is a text file with the values between -1 and 24
    
   3.a) Input is 625 (=25x25) integers in the range [-1,24], corresponding to the game-board serialized row-wise. -1 means the corresponding cell is blank, [0-24] corresponds to the number in the cell.

4)Output is time and the solution (if there exists no solution, it will print "No Answer")
