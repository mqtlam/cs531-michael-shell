import os
import os.path

import env
import agent
import logic

#---------------------------------------MAIN--------------------------------------
if __name__ == "__main__":

	directory = "./test_maps/"

	#create the agent
	player = agent.LogicAgent()

	print "file name, is solveable?, has good start?, map size, success?, died?, num actions, has arrow"

	#for each of the map files run a simulation
	for aFile in os.listdir(directory):

		if aFile == ".svn":
			continue

		#build the environment
		theMap = env.Environment(os.path.join(directory,aFile))
	
		#create the logic engine
		kb = logic.FluentLogic()
	
		#run the agent and get the results
		(success, died, actions, hasArrow) = player.search(theMap, kb)

		#map, possible, can start?, size, success, died?, error?, actions, arrow
		print "%s, %s, %s, %i, %s, %s, %i, %s" %\
		(os.path.basename(theMap.fileName), theMap.isSolveable(),\
		not theMap.noLogicalStart(), theMap.size, success, died,\
		actions, hasArrow)
		
