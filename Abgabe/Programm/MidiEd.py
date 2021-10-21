from mido import MidiFile
import mido


def findDelta(list):
    deltaList = []
    for i in range(1, len(list)):
        delta = list[i] - list[i-1]
        deltaList.append(delta)
    return deltaList

def findDeltas(list, fp):
    trackList = []
    for i in range(len(list)):
        channelList = []
        for k in range(len(list[i])):
            deltalist = []
            for j in range(1, len(list[i][k][0])):
                delta = list[i][k][0][j] - list[i][k][0][j-1]
                deltalist.append(delta)
            trackList.append([(fp + ", Track no." + str(i) + " ch." + str(k) + " inst." + str(list[i][k][1]), fp), deltalist])
    return trackList

        

def getTrack(name, num):
    
    
    #Defining MIDI File
    midFile = MidiFile(name)


    #Separating specific track from MIDI File
    track = midFile.tracks[num]
        
        
    #List of MIDI Events
    music = []
        
    #Separating Events and only saving the ones that are ON-Type events with Notes assigned to them
    for msg in track:
        try:
            if msg.type == "note_on":
                note = msg.note
                music.append(note)
            pass
        except:
            pass
    
    return music

def getTracks(name):
    
    
    #Defining MIDI File
    midFile = MidiFile(name)


    #List of input-Tracks
    tracks = midFile.tracks
        
        
    #List of output-Tracks
    music = []
    
    channelTemplate = []
    for i in range(16):
        channelTemplate.append([[], 0])
        
    #Looping through all tracks and Separating Events and only saving the ones that are ON-Type events with Notes assigned to them
    for i, track in enumerate(tracks):
        #List of messages in current track
        channelsAll = channelTemplate
        channels = []
        for msg in track:
            if type(msg) is  mido.messages.messages.Message:
                
                #adds note when received note_on message
                if msg.type == "note_on":
                    note = msg.note
                    ch = msg.channel
                    channelsAll[ch][0].append(note)
                    
                #sets the instrument number of the channel when received program_change message
                elif msg.type == "program_change":
                    ch = msg.channel
                    number = msg.program
                    channelsAll[ch][1] = number
                    
        for k in range(len(channelsAll)):
            if len(channelsAll[k][0]) > 0:
                channels.append(channelsAll[k])
        music.append(channels)
    return music

