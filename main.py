# ============== #
# Libraries
# ============== #

import re
import json
import ast
import sys


# ============== #
# Gloabal Vars
# ============== #

# Gets path to starting files
#path = "E:\Docs Storage\School\Classes\Spring 2021\ind study"
#path = "C:\\Users\\liamc\\Documents\\School\\Class Files\\Spring 2021\\Independent Study\\json_conversion"
path = "C:\\Users\\liamc\\Documents\\School\\Class Files\\Spring 2021\\Independent Study\\YodaAlGaSbExample"
#path = "E:\\Docs Storage\\School\\Classes\\Spring 2021\\ind study"
#file = "\AlGaSb_Alp4.in"
#file = "\\InGaAsEsaki5_HSE06VCA_sp3d5sstar_SO_noKpointsSym.in"
file = "\\all_fullsort_AlGaSb.mat"
#file = "\\all_fullsort_AlGaSb_Hegde.mat"


# Opening function
# Saves to list
def TextRead(path, file):
    f = open(path + file, "r")
    return [line.split('\n') for line in f.readlines()]
    

# Clean list
# Kills: comments, blank space
# seperates cb into seperate lines
def ListClean(dirtyList):
    # Makes the cleanList for output
    cleanList = []
    
    # Set up some vars
    # Initial deletes (first check, easiest to find)
    initClean = ("*", "/", "#")
    # Inline comment indicator
    inlineClean = ["//", "#"]
    
    # Loop over list

    for index in range(len(dirtyList)):
        # Strip current level down to string and remove white space
        #print(index)
        currLine = dirtyList[index][0].strip()
        currLine = re.sub(" +", " ", currLine)
        
        # Checks line against inital deletes or just whitespace
        # This will eventually just skip lines that hit these conditions
        if not (currLine.startswith(initClean) or len(currLine) == 0):
            
            # Now we remove inline comments. Looks like "//"
            # Weird small loop, will resave curr line if a inline comment is found
            for flag in inlineClean:
                if not currLine.find(flag) == -1:
                    # Gets location of start of inline
                    inLineLoc = currLine.find(flag)
                    # Removes inline and restrips
                    currLine = currLine[:inLineLoc].strip()

            # Ok, so now we can deal with fcb and bcb
            # Four condtions, both are in here, fcb only, or bcb only, else i guess
            # Fixes { and } on the same line
            if "{" in currLine and "}" in currLine:
                cleanList.append("{")
                # Get output via removing cb and stripping it
                fcbLoc = currLine.find("{")
                bcbLoc = currLine.find("}")
                cleanList.append(currLine[fcbLoc:bcbLoc].strip())
                cleanList.append("}")
            # Fixes just { inline, must have len > 1
            elif "{" in currLine and len(currLine) > 1:
                # Check location of {
                if currLine.startswith("{"):
                    cleanList.append("{")
                    cleanList.append(currLine[1:].strip())
                else:
                    cleanList.append(currLine[:-1].strip())
                    cleanList.append("{")
            # Fixes just } inLine, must have len > 1
            elif "}" in currLine and len(currLine) > 1:
                # Check loaction of }
                if currLine.endswith("}"):
                    cleanList.append(currLine[:-1].strip())
                    cleanList.append("}")
                else:
                    cleanList.append("}")
                    cleanList.append(currLine[1:].strip())
            # Wow, the line is acually correctly formatted
            else:
                # WHY ARE PEOPLE LIKE THIS
                # Some data lines are split between two lines so thats super sad
                # if line begins with rule, try and check it
                if not currLine.find("=") == -1 and not currLine.endswith(";"):
                    currLine = currLine + " " + dirtyList[index + 2][0].strip()
                    dirtyList[index + 2][0] = ""
                cleanList.append(currLine)

    # Adds a termination symbol at end of list
    cleanList.append("?END?")
    # Returns cleanList
    return cleanList


# I might just be dumb, lets try and cheat the system
# String to json
# Need to change = to :
#   add , to equals line if  next elel isnt fcb
#   add : to line if no equals and no cb
def ListToString(cleanList):
    # Huge Outstring to append to
    outString = '{'
    for index in range(len(cleanList) - 1):
        #Break condtion

        # Easy finding of relevent vars
        currEle = cleanList[index].strip()
        nextEle = cleanList[index + 1].strip()

        # Condition checking
        # Four conditions:
        # 1. FCB, skip 
        # 2 .BCB, skip 
        # 3. Contains equal sign
        # 4. Else (headers)

        # If fcb found
        if "{" in currEle:
            # Append the cb
            outString = outString + currEle

        elif "}" in currEle:
            if not (nextEle == "}" or nextEle == "?END?"):
                outString = outString + currEle + ","
            else:
                outString = outString + currEle

        # Data line is found
        elif "=" in currEle:
            # Cuts off ;
            currEle = currEle[:-1]
            # Replaces = sign with :
            currEle = currEle.replace("=", ":", 1)
            # Removes space around :
            sepIndex = currEle.index(":")
            if currEle[sepIndex + 1] == " " and currEle[sepIndex - 1] == " ":
                currEle = currEle.replace(" : ", ":", 1)
            elif currEle[sepIndex - 1] == " ":
                currEle = currEle.replace(" :", ":", 1)
            elif currEle[sepIndex + 1 ] == " ":
                currEle = currEle.replace(": ", ":", 1)
            # Replaces " with '
            currEle = currEle.replace('"', "'")
            # split and appends a "" onto line data
            sepIndex = currEle.index(":")
            startString = '"' + currEle[:sepIndex].strip() + '"'
            endString = '"' + currEle[sepIndex + 1:].strip() + '"'
            currEle = startString + ":" + endString


            # If not last element in list, adds a comma
            if not ("{" in nextEle or "}" in nextEle):
                currEle = currEle + ","
            # Append string
            outString = outString + currEle

        # Just header line
        else:
            # Append :
            currEle = '"' + currEle + '":'
            outString = outString + currEle
    
    # Returns completed json formated outstring
    outString = outString + "}"
    #outString = ast.literal_eval(outString)
    #print(outString)
    return outString


# Uses the produced dictionary to output a json file
def exportJson(outString, path, file):
    #json_object = json.dumps(outString, indent = 4)
    #print(json_object)
    newFile = file.split(".")[0]
    with open(path + newFile + ".json", "w") as outFile:
        outFile.write(outString)
        #json.dump(outString, outFile)
    print("JSON Created")


# Ok lets run this 
fileIn = TextRead(path, file)
cleanFile = ListClean(fileIn)
outString = ListToString(cleanFile)
exportJson(outString, path, file)
