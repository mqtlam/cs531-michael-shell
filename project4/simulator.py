import os
import os.path

import env
import agent
import logic

#---------------------------------------MAIN--------------------------------------
if __name__ == "__main__":

	directory = "./maps/"

	#create the agent
	player = agent.LogicAgent()

	print "file name, is solveable?, has good start?, map size, success?, died?, num actions, has arrow"

    	fp = open("log.txt", "w")

	#for each of the map files run a simulation
	for ind,aFile in enumerate(os.listdir(directory)):

		if aFile == ".svn":
			continue

        	print '********************************* %d ***********************************' % ind

		#build the environment
		theMap = env.Environment(os.path.join(directory,aFile))

		#create the logic engine
		kb = logic.FluentLogic()

		#run the agent and get the results
		(success, died, actions, hasArrow, rewards, steps, gold) = player.search(theMap, kb)
        	fp.write("[%d] success = %d, gold = %d, kill_wumpus = %d, steps = %d, rewards = %d\n" % (ind,success,gold,hasArrow,steps,rewards))

		#map, possible, can start?, size, success, died?, error?, actions, arrow
		print "%s, %s, %s, %i, %s, %s, %i, %s" %\
		(os.path.basename(theMap.fileName), theMap.isSolveable(),\
		not theMap.noLogicalStart(), theMap.size, success, died,\
		actions, hasArrow)

    	fp.close()

