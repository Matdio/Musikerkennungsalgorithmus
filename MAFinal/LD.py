#Levenshtein Distance, algorithm to find the amount of edits needed to get from one string to another


def distance(str1, str2, subCost, delCost, insCost):
    
    

    #distance-Matrix
    levMatrix = []

    #makes the Matrix a (m+1)*(n+1) Matrix, where m = len(str1) and n = len(str2)
    for i in range(len(str2) + 1):
        row = []
        for j in range(len(str1) + 1):
            row.append(0)
        levMatrix.append(row)


    #fills in the upper row and the left column from 0 to (n+1) or 0 to (m+1)

    #row
    for i in range(1, len(levMatrix[0])):
        levMatrix[0][i] = levMatrix[0][i-1] + delCost

    #column
    for i in range(1, len(levMatrix)):
        levMatrix[i][0] = levMatrix[i-1][0] + insCost
        

    #fills out the other spaces of the Matrix according to the Rules
    for i in range(1, len(levMatrix)):
        for j in range(1, len(levMatrix[i])):
            
            #take the space (either left + delCost, top + insCost or diagonal to it) with the smallest number if the letters match up 
            if str1[j-1] == str2[i-1]:
                levMatrix[i][j] = min(levMatrix[i-1][j] + insCost, levMatrix[i-1][j-1], levMatrix[i][j-1] + delCost)
                
            #take the minimum of the fields  to the left, to the right and on top of the one you're filling out and add the cost for the corresponding action
            else:
                levMatrix[i][j] = min(levMatrix[i-1][j] + insCost, levMatrix[i-1][j-1] + subCost, levMatrix[i][j-1] + delCost)
                   
        
    #result
    return levMatrix[len(levMatrix) - 1][len(levMatrix[0]) - 1]
        

