import LDLoop as ldl
import MidiEd
from mido import MidiFile
import os, multiprocessing, time



def partialDB(dataBase, directory, inTrack, n, m, mpQueue): #m = id of the Process
    
    #List of all tracks (already transformed to delta-lists)
    #Format = [<filepath and Track no.>, [d1, d2, ... ,d(n-1), d(n)]]   , d1 being the distance between note1 and note2, d2 between note2 and note3 and so on.
    tracks = []
    
    #Separation of different processes
    for k in range(int(m * (len(dataBase)/n)), int((m+1) * (len(dataBase)/n))):
        filename = dataBase[k]
        if filename.endswith(".mid"): 
            
            #creates the exact filepath of the current file (filename)
            fp = directory + "/" + filename
            
            absolute = MidiEd.getTracks(fp)
            
            deltas = MidiEd.findDeltas(absolute, fp)

            tracks.extend(deltas)
            
    #makes a delta-list from the input-Track
    track = MidiEd.getTrack(inTrack, 1)
    inDeltas = MidiEd.findDelta(track)

    #calculates the distances between all tracks in the <tracks> list  and the <inDeltas> list
    #the number indicates how close the input-Track is to the DB-Tracks (smaller Number means less different)
    mpQueue.put(ldl.distanceAll(tracks, inDeltas, 1, 1, 1))

def main():
    
    #number of Processes used
    n = 10
    
    #list of Process-Objects
    Processes = []
    
    for i in range(n):
        Processes.append(0)
        
    #Queue for Multiprocessing results
    mpQueue = multiprocessing.Queue()
    
    #final list of results
    distances = []
    
    #input Track, Monophone MIDI-File  
    inTrack = "input.mid"

    #File-Directory for the Tracks to compare with (Database)
    directory = "DB"


    #reading all the filenames ending with ".mid", hence all MIDI Files in the Database Directory (specified in the <directory> variable)
    dataBase = os.listdir(directory)
    
    for i in range(n):
        Processes[i] = multiprocessing.Process(target= partialDB, args= (dataBase, directory, inTrack, n, i, mpQueue))
        Processes[i].start()
        #print("Process " + str(i) + " initiated")
    
    #append returned values of Processes to distances list
    for i in range(n):
        distances.extend(mpQueue.get())
        
    #closes all Processes
    for p in Processes:
        p.join()
        p.terminate()
    
    #sorts the list by the distances in descending order
    distances.sort()
    distances.reverse()

    
    #Code for collecting all track and channel data of each Song in one list 
    
    songs = []
    for i in range(len(dataBase)):
        filename = dataBase[i]
        if filename.endswith(".mid"):
            fp = directory + "/" + filename
            song = [fp, [], 0]
            for j in range(len(distances)):
                if distances[j][1][1] == fp:
                    song[1].append([distances[j][0], distances[j][1][0]])
                    
            maximum  = max(song[1], key=lambda x: x[0])
            song[2] = maximum[0]
            songs.append(song)
    
    songs.sort(key=lambda x: x[2])
    songs.reverse()
        
    #sorts the list in descending order 
    for i in range(len(songs)):
        songs[i][1].sort(key=lambda x: x[0])
        songs[i][1].reverse()
        
        
    #Code for the "UI"
     
    def showSongs(songs):
        print("\n\n\n\n\n\n\n\n\n\n\n\n")
        for i in range(len(songs)):
            print(str(i + 1) + ". " + str(songs[i][2]) + "%", songs[i][0])
            
    def showTracks(songs, num):
        print("\n\n\n\n\n\n\n\n\n\n\n\n")
        for i in range(len(songs[num][1])):
            print(str(songs[num][1][i][0]) + "%", songs[num][1][i][1])
    
    end = time.time()
    print(end-start)
    
    while True:
        showSongs(songs)
        print("\nSelect Song by entering number to see details")
        selection = input()
        
        try:
            selection = int(selection)
        except:
            print("Please enter a number")
            continue
            
        if selection > len(songs):
            print("Song not found. Reenter number")
        else:
            showTracks(songs, selection - 1)
            print("\nPress Enter to go back to Song selection Screen")
            
        enter = input()
            
            
    
    
    return
    
    
if __name__ == '__main__':
    start = time.time()
    main()

    
    

    






