README

Michael Lam, Shell Hu
HW #1, CS 531, Fall 2012


I. HOW TO RUN

To run a simulation: ./runAgent.py 1|2|3 [n m p]
	where 	1 = memoryless deterministic reflex agent
		2 = randomized reflex agent
		3 = deterministic model-based reflex agent
	and optional parameters
		n by m environment (default 10x10)
			n = columns, m = rows
		probability of dirt p (default 1.0 = 100%)

To run 50 trials of the randomized reflex agent: ./run50Trials.sh
It may not be a good idea to run the program "as is" without 
commenting out lines of code in runAgent.py where the 
popup screen of the performance is shown.

II. REQUIREMENTS

- Linux (we coded using Linux)
- Python
- Python libraries (only for plotting performance):
	- numpy
	- pylab (from matplotlib)

