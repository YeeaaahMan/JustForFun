import os

replayList = os.listdir('replays')
#replayList = os.listdir('.')
#replayList.remove('map_counter.py')

for i in range(len(replayList)):
    splittedReplayName = replayList[i].split('_')
    
    for l in range(1, len(splittedReplayName)):
        if splittedReplayName[-l].isdigit() == True:
            temp = "_".join(splittedReplayName[-l:]).replace('.wotreplay', '')
            break

    replayList[i] = temp

mapCount = dict()
for map in replayList:
    mapCount[map] = mapCount.get(map, 0) + 1

#print mapCount

resultList = list()
for m in mapCount:
    resultList.append( (mapCount[m], m) )

resultList.sort()

print "Total number of battles is " + str(len(replayList)) + ":"
for i in resultList[::-1]:
    print str(i[0]) + ' is count of "' + i[1] + '"'

raw_input("Press Enter.")
