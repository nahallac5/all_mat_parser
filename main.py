# ============== #
# Libraries
# ============== #

import re
import json
import ast


# ============== #
# Gloabal Vars
# ============== #

# Gets path to starting files
path = "E:\Docs Storage\School\Classes\Spring 2021\ind study"
file = "\AlGaSb_Alp4.in"


# ============== #
# Functions
# ============== #

# ************** #
# TextRead(path, file)
# ************** #
# Import and read in text file
# Path variable used so that we can modify later
def TextRead(path, file):
    f = open(path + file, "r")
    fList = [line.split('\n') for line in f.readlines()]
    #print(fList)
        
    # Cleaning up List
    cleanList = []
    # Remove all commentted out data lines and remove extranious white space
    termVars = "//"
    # Set up solver incrimenting
    solveInc = 0
    for index in range(len(fList)):
        # Fixes solver repeition issues (json cant have the same term in the same layer)
        if fList[index][0].strip() == "solver":
            cleanList.append("solver_" + str(solveInc))
            solveInc = solveInc + 1
        # Checks for empty lines or commented lines
        elif not (fList[index][0].strip().startswith(termVars) | len(fList[index][0].strip()) == 0):
            # Strips extra whitespace from inside of list
            cleanList.append(re.sub(" +", " ", fList[index][0].strip()))
    # Remove comments from first few lines
    comStart = [i for i, item in enumerate(cleanList) if item.startswith('/*')]
    comEnd = [i for i, item in enumerate(cleanList) if item.startswith('*/')]
    del cleanList[comStart[0]:comEnd[0]+1]
    # Returns cleaned list
    return cleanList


# ************** #
# dataGrab(currVar, fullDataList)
# ************** #
# Pinged when Data entry is needed into dict
# Uses current variable to get subdata
def dataGrab(currVar, fullDataList):
    # Use currVar to get correct index for start of data (skips definition and { )
    startIndex = fullDataList.index(currVar) + 2
    # Find next occurance of } to end data
    endIndex = fullDataList.index("}", startIndex) - 1
    # Splice fullDataList into sub list
    dataList = fullDataList[startIndex:endIndex]

    # Assemble dictionary for data
    outDict = {}
    # Loop over dataList
    for index in range(len(dataList)):
        # Split at equals sign
        lineSplit = dataList[index].split("=")
        lineSplit[0] = lineSplit[0].strip()
        lineSplit[1] = lineSplit[1].strip()
        # Append to dict
        outDict[lineSplit[0]] = lineSplit[1]

    # Returns list split of equals lines
    return outDict


# ************** #
# backGrab(varList, fullDataList)
# ************** #
# Goes back and nests dict correctly
def backGrab(varList, fullDataList):
    # Adding "?" to end of list x2 so that errors stop
    varList.append("?")
    varList.append("?")
    # Make output dict
    dataDict = {}
    # Set indexing variables
    layerLevel = 0
    indexLevel = 0
    # Exit condition
    levelSortStop = 0

    # While loop to repeate condition
    while levelSortStop != -1:
        # Kills loop at the end of list
        if varList[indexLevel] == "?":
            levelSortStop = -1
            break

        #Handles all other indexes
        else:
            # Skip if { or } (layer handling)
            if varList[indexLevel] == "{" or varList[indexLevel] == "}":
                # if closing bracket, check if layer need to be deincrimented
                if varList[indexLevel] == "}" and varList[indexLevel + 1] == "}":
                    layerLevel = layerLevel - 1
                    indexLevel = indexLevel + 1
                else:
                    indexLevel = indexLevel + 1
            # Continues down loop
            # Only handles layers down to 4 deep
            else:

                # Layer level zero handling
                if layerLevel == 0:
                    # Sets leveel zero call so that it can be retrived later
                    levelZeroVar = varList[indexLevel]
                    # If data is present, get it
                    if varList[indexLevel + 2] == "}":
                        dataDict[levelZeroVar] = {"Data": dataGrab(levelZeroVar, fullDataList)}
                        indexLevel = indexLevel + 1
                    # More layers under it
                    else:
                        dataDict[levelZeroVar] = {}
                        # Bump index level and layer level
                        layerLevel = layerLevel + 1
                        indexLevel = indexLevel + 1
                
                # Layer level one handling
                elif layerLevel == 1:
                    # Sets leveel zero call so that it can be retrived later
                    levelOneVar = varList[indexLevel]
                    # If data is present, get it
                    if varList[indexLevel + 2] == "}":
                        dataDict[levelZeroVar][levelOneVar] = {"Data": dataGrab(levelOneVar, fullDataList)}
                        indexLevel = indexLevel + 1
                    # More layers under it
                    else:
                        dataDict[levelZeroVar][levelOneVar] = {}
                        # Bump index level and layer level
                        layerLevel = layerLevel + 1
                        indexLevel = indexLevel + 1
                
                # Layer level two handling
                elif layerLevel == 2:
                    # Sets leveel zero call so that it can be retrived later
                    levelTwoVar = varList[indexLevel]
                    # If data is present, get it
                    if varList[indexLevel + 2] == "}":
                        dataDict[levelZeroVar][levelOneVar][levelTwoVar] = {"Data": dataGrab(levelTwoVar, fullDataList)}
                        indexLevel = indexLevel + 1
                    # More layers under it
                    else:
                        dataDict[levelZeroVar][levelOneVar][levelTwoVar] = {}
                        # Bump index level and layer level
                        layerLevel = layerLevel + 1
                        indexLevel = indexLevel + 1
                
                # Layer level three handling
                elif layerLevel == 3:
                    # Sets leveel zero call so that it can be retrived later
                    levelThreeVar = varList[indexLevel]
                    # If data is present, get it
                    if varList[indexLevel + 2] == "}":
                        dataDict[levelZeroVar][levelOneVar][levelTwoVar][levelThreeVar] = {"Data": dataGrab(levelThreeVar, fullDataList)}
                        indexLevel = indexLevel + 1
                    # More layers under it
                    else:
                        dataDict[levelZeroVar][levelOneVar][levelTwoVar][levelThreeVar] = {}
                        # Bump index level and layer level
                        layerLevel = layerLevel + 1
                        indexLevel = indexLevel + 1
                
                # Layer level four handling
                elif layerLevel == 4:
                    # Sets leveel zero call so that it can be retrived later
                    levelFourVar = varList[indexLevel]
                    # If data is present, get it
                    if varList[indexLevel + 2] == "}":
                        dataDict[levelZeroVar][levelOneVar][levelTwoVar][levelThreeVar][levelFourVar] = {"Data": dataGrab(levelFourVar, fullDataList)}
                        indexLevel = indexLevel + 1
                    # More layers under it
                    else:
                        dataDict[levelZeroVar][levelOneVar][levelTwoVar][levelThreeVar][levelFourVar] = {}
                        # Bump index level and layer level
                        layerLevel = layerLevel + 1
                        indexLevel = indexLevel + 1

                # Layer level five handling
                elif layerLevel == 5:
                    # Sets leveel zero call so that it can be retrived later
                    levelFiveVar = varList[indexLevel]
                    # If data is present, get it
                    if varList[indexLevel + 2] == "}":
                        dataDict[levelZeroVar][levelOneVar][levelTwoVar][levelThreeVar][levelFourVar][levelFiveVar] = {"Data": dataGrab(levelFiveVar, fullDataList)}
                        indexLevel = indexLevel + 1
                    # More layers under it
                    else:
                        dataDict[levelZeroVar][levelOneVar][levelTwoVar][levelThreeVar][levelFourVar][levelFiveVar] = {}
                        # Bump index level and layer level
                        layerLevel = layerLevel + 1
                        indexLevel = indexLevel + 1

                # Error Condition
                else:
                    print("Figure out how to use recursion you fool...")
                    indexLevel = indexLevel + 1
    
    # Returns the complete dataDict
    return dataDict


# ************** #
# assembleDicts(inList)
# ************** #
# Assembles dicts for relevents vars
# Attempting to be as modular as possible with no mandatory inclusions
def assembleDicts(inList):
    # Find all dict headers ie. Domain, geometry, etc.
    # Will not include = 
    dataFlags = ["="]
    dictHeader = []
    for index in range(len(inList)):
        if not any(x in inList[index] for x in dataFlags):
            dictHeader.append(inList[index])
    # Now that we have the list of dicr headers, lets make a Dict with their levels
    # Example:
    # dict = {"Structure": {"Material": {Data: {}}, "Domain": {Data: {}}, "Geometry": {"Region": {Data: {}}}}, "Solvers": {etc.}}
    dataDict = backGrab(dictHeader, inList)
    # Returns dict. Can be exported to json
    return dataDict


# ************** #
# exportJson(outDict)
# ************** #
# Uses the produced dictionary to output a json file
def exportJson(outDict, path, file):
    #json_object = json.dumps(outDict, indent = 2)
    #print(json_object)
    newFile = file.split(".")[0]
    with open(path + newFile + ".json", "w") as outFile:
        json.dump(outDict, outFile)
    print("JSON Created")
6

# ============== #
# Run Program
# ============== #

data = TextRead(path, file)
dataDict = assembleDicts(data)
exportJson(dataDict, path, file)