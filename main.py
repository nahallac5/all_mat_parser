#!/usr/bin/env python3.9

#############################
# Libraries
#############################

import re

#############################
# Global Vars
#############################

globalVars = {
    "path": "E:\\Docs Storage\\School\\Classes\\Spring 2021\\ind study\\problemdata",
    "file_mat": "\\all_fullsort_GaInAs_HSE06.mat",
    "file_json": "\\all_fullsort_GaInAs_HSE06.json"
}


# Opening function
# Saves to list
def TextRead(path, file):
    f = open(path + file, "r")
    return [line.split('\n') for line in f.readlines()]

#############################
# READ IN TO JSON
#############################
# TextRead()
# |_> ListClean()
#   |_> ListToString()
#     |_> ExportJson()
#############################

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
                    # Dealing with an arbitary depth between these lines
                    lineFind = 1
                    # Loop until next non-blank line is found
                    while not lineFind == -1:
                        # Found the next line
                        if not len(dirtyList[index + lineFind][0].strip()) == 0:
                            currLine = currLine + " " + dirtyList[index + lineFind][0].strip()
                            dirtyList[index + lineFind][0] = ""
                            break
                        # Itterates to next line if needed
                        else:
                            lineFind = lineFind + 1
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
    return outString


# Uses the produced dictionary to output a json file
def exportJson(outString, path, file):
    newFile = file.split(".")[0]
    with open(path + newFile + ".json", "w") as outFile:
        outFile.write(outString)
    print("JSON Created\n")


#############################
# READ OUT TO ALL.MAT
#############################
# TextRead()
# |_> JsonToString()
#   |_> ExportMat() 
#############################

# Convert input list into all.mat string
def JsonToString(jsonRaw):
    # Start mat out string
    matOutString = ""

    # Parse over JSON incase multiple lines
    for index in range(len(jsonRaw)):
        # Grabs current line for ease
        currLine = jsonRaw[index][0]
        
        # Soo Regex...
        # \s calls out a whitespace
        # ? is 0 or more of previous call
        # thr4 \s? is 0 or more spaces
        # \s? used to make sure json is read no matter if it is put through a converter or not

        # Also, result is not tabulated so... readbality is not great
        # Should still work though
        
        # 1. Change all : after a " to a =
        currLine = re.sub('"\s?:\s?"', '" = "', currLine)

        # 2. Change all ", to a ";\n
        currLine = re.sub('"\s?,\s?', '";\n', currLine)

        # 3. Change all '": {' to ' {\n'
        currLine = re.sub('"\s?:\s?{', '" {\n', currLine)

        # 4. Change all '"},' to '";\n}\n'
        currLine = re.sub('"\s?}\s?,', '";\n}\n', currLine)

        # 5. Remove all " marks
        currLine = re.sub('"', '', currLine)

        # Append to string
        matOutString = matOutString + currLine

    # Returns formatted string
    return matOutString[1:-1]


# Uses the produced string to output a mat file
def ExportMat(outString, path, file):
    newFile = file.split(".")[0]
    with open(path + newFile + "_new.mat", "w") as outFile:
        outFile.write(outString)
    print("mat Created\n")


#############################
# EXECUTE
#############################
# ProgramExec()
#############################

# Exectuion function
def ProgramExec(globalVars):
    print("================================\n")
    print("Welcome to JSON<->MAT converter!\n")
    print("Version 1.0 - LJC\n")
    print("================================\n")
    print("Would you like to:\n")
    print("1. Convert Mat -> JSON\n")
    print("2. Convert JSON -> Mat\n")
    # Selects exec type
    execType = input("Input (1 or 2): ")
    print(execType)

    # Execute selected path

    # Execute Mat -> JSON
    if execType == "1":
        fileIn = TextRead(globalVars["path"], globalVars["file_mat"])
        cleanFile = ListClean(fileIn)
        outString = ListToString(cleanFile)
        exportJson(outString, globalVars["path"], globalVars["file_mat"])
    
    # Execute JSON -> Mat
    elif execType == "2":
        fileIn = TextRead(globalVars["path"], globalVars["file_json"])
        outString = JsonToString(fileIn)
        ExportMat(outString, globalVars["path"], globalVars["file_json"])

    # System error
    else: 
        print("Invalid entry...\nRestarting...\n\n")


ProgramExec(globalVars)
