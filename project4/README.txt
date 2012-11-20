to run the wumpus world simulator with the random agent use the command:

python simulator.py

Since the included agent is random, it does not reason about the wumpus world.  I've included a module logic.py that has the base functionality to call prover 9 from python.  It is necessary to dynamically create a string or file in python that reflects logic.txt (but with more rules) then pipe it to prover 9. That is, the variable "query" would contain all the text from logic.txt.  Each time a query is asked, prover 9 is invoked as a subprocess and the exit status determines if it was successful 0 - this was the only I was able to call prover 9 from another program, though there might be a C interface for it.

The file logic.txt contains an outline of how to use prover 9.  Prover 9 uses backchaining to reason, so designing your rules in light of this will help it reason more quickly.
