#Levenshtein-Distance applied to many different "windows"
import LD

def distanceAll(dataIn, searchIn, subCost, delCost, insCost):
    
    #defines the size of the searching-Window as the length of the input-Track
    winSize = len(searchIn)
    
    #list of the lowest found distance in each track
    distancesBest = []
    
    #loops through the tracks
    for i in range(len(dataIn)):
        #goes to the next track if the current track is shorter than the input track
        if len(dataIn[i][1]) <= winSize:
            continue
        
        #list of all distances for different search-windows
        distances = []
        
        j = 0
        
        #loops as long as the search-window fits into the track with the starting-position <j>
        while j + winSize < len(dataIn[i][1]):
            
            #creates a temporary list of just the part of the track inside the search-window
            temp = dataIn[i][1][j:j+winSize]
            
            #calculates the distance between the temporary list and the input-Track (which have the same length, meaning the distance can be 0)
            dis = LD.distance(temp, searchIn, subCost, delCost, insCost)
            distances.append(dis)
            
            #shifts the window forward by one position
            j += 1
        
        #sorts the distances from lowest to highest and adds the lowest value, the filepath and the track no. to the <distanceBest> list
        distances.sort()
        
        distancePercent =  int((1 - (distances[0]/winSize))*100)
        distancesBest.append([distancePercent, dataIn[i][0]])
        
    return  distancesBest
            
    
    
        