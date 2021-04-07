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
#path = "C:\\Users\\liamc\\Documents\\School\\Class Files\\Spring 2021\\Independent Study\\YodaAlGaSbExample"
path = "E:\\Docs Storage\\School\\Classes\\Spring 2021\\ind study"
#file = "\AlGaSb_Alp4.in"
#file = "\\InGaAsEsaki5_HSE06VCA_sp3d5sstar_SO_noKpointsSym.in"
#file = "\\all_fullsort_AlGaSb.mat"
file = "\\all_fullsort_AlGaSb_Hegde.mat"

"""
Alright, lets try and figure this out
How to recursivly dig into json list

Curly count attempt:
1. Start on top level
2. Count every { once it hits, and count every } once its hit
3. Once they are even, you have completed loop
** How do we get levels?
** List maybe?
ex. 
    a. fcb hit
    b. [0]
    c. fcb hit
    d. [0,1]
    e. bcb hit
    f. [0,1]
    g. fcb hit
    h. [0,1,1]
    i. fcb hit
    j. fcb hit
    k. [0,1,1,2]
    l. bcb hit
    m. [0,1,1,2]

What do we need to run this?
~Level dict
    {0: "0l name", 1: "1l name", 2: "2l name", etc.}
    This will let us keep the names of the levels and allow easy writes
~Curr Level
    currLevel = 0
    Lets us know what level you are on
    fcb will incriment this
    bcb will deincriment this

    currLevelVar = lastLevel[currLevelKey]
    Alows easy cycling of dict levels
    lastLevel is actual the previous address, may be super nested

How do we handle lines that are the "data areas"?
    if not cb, check if it has = sign in it 
    *** This is an assumption, we may just get screwed by this ***
    if it has equal sign, split and ship boys

We need to first format and clean the loop
    We dont want any comments anywhere
    We want curly brackets to be on their own levels
    blank lines are the devil
    This seems like it maybe be a ineffeicnt idea but idk should be fine

Lets make a dumby loop
This should save like 100 lines and yikes
AKA Liam pretends to know recursion
Goals, loops over an addition function depending on scenarious

# Hey kids we have a new level
def noEqual():
    currLevel
    dict[currLevel] = {}

# Data time
def yesEqual():
    split string at equals
    dict[string[0]] = string[1]   

# Looooooop
while exit != True:

OK LETS BUILD THIS BOI
1. Rebuild the cleaning function
"""


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
    inlineClean = "//"
    
    # Loop over list
    for index in range(len(dirtyList)):
        # Strip current level down to string and remove white space
        currLine = dirtyList[index][0].strip()
        
        # Checks line against inital deletes or just whitespace
        # This will eventually just skip lines that hit these conditions
        if not (currLine.startswith(initClean) or len(currLine) == 0):
            
            # Now we remove inline comments. Looks like "//"
            # Weird small loop, will resave curr line if a inline comment is found
            if not currLine.find(inlineClean) == -1:
                # Gets location of start of inline
                inLineLoc = currLine.find(inlineClean)
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
                cleanList.append(currLine)

    # Returns cleanList
    print(cleanList)
    return cleanList


# Ok lets run this 
fileIn = TextRead(path, file)
cleanFile = ListClean(fileIn)

"""
# ============== #
# Functions
# ============== #

# ************** #
# headerIterator(input, itrVars)
# ************** #
# Handles multiple instances of the same header
# JSON needs unqiue headers
def headerIterator(input, itrVars):
    # Probably could be more condesed...
    # Material
    if input == "Material":
        output = "Material_" + str(itrVars["Material"])
        itrVars["Material"] = itrVars["Material"] + 1
    # Domain
    elif input == "Domain":
        output = "Domain_" + str(itrVars["Domain"])
        itrVars["Domain"] = itrVars["Domain"] + 1
    # Region
    elif input == "Region":
        output = "Region_" + str(itrVars["Region"])
        itrVars["Region"] = itrVars["Region"] + 1
    # solver
    elif input == "solver":
        output = "solver_" + str(itrVars["solver"])
        itrVars["solver"] = itrVars["solver"] + 1
    # everything else
    else:
        output = input
    return output, itrVars

# ************** #
# TextRead(path, file)
# ************** #
# Import and read in text file
# Path variable used so that we can modify later
def TextRead(path, file):
    f = open(path + file, "r")
    commentList = [line.split('\n') for line in f.readlines()]
    #print(fList)
    # Cleaning out * lines...
    fList = []
    for index in range(len(commentList)):
        if not commentList[index][0].strip().startswith("*"):
            if not commentList[index][0].strip().startswith("/"):
                if not commentList[index][0].strip().startswith("#"):
                    fList.append(commentList[index])
    # Cleaning up List
    cleanList = []
    # Remove all commentted out data lines and remove extranious white space
    termVars = "//"
    # Set up header incrimenting
    itrDict = {"Material": 0, "Domain": 0, "Region": 0, "solver": 0}

    # Lets send the loop
    for index in range(len(fList)):

        # Fixes { and } on the same line
        if "{" in fList[index][0].strip() and "}" in fList[index][0].strip():
            cleanList.append("{")
            if not "/*" in fList[index][0].strip():
                input = fList[index][0].strip()[1:len(fList[index][0].strip())-1]
                output, itrDict = headerIterator(input, itrDict)
                cleanList.append(output)
            cleanList.append("}")

        # Fixes { bracket issues
        # Checks to see if there is a { in a line with other text
        elif len(fList[index][0].strip()) > 1 and "{" in fList[index][0].strip():
            # Checks if starts or ends with {
            if fList[index][0].strip().startswith("{"):
                cleanList.append("{")
                commentCheck = fList[index][0].strip()[1:]
                if not commentCheck.strip().startswith("//"):
                    input = commentCheck
                    output, itrDict = headerIterator(input, itrDict)
                    cleanList.append(output)
            else:
                commentCheck = fList[index][0].strip()[:len(fList[index][0].strip())-1]
                if not commentCheck.strip().startswith("//"):
                    input = commentCheck
                    output, itrDict = headerIterator(input, itrDict)
                    cleanList.append(output)
                cleanList.append("{")

        # Fixes } bracket issues
        elif len(fList[index][0].strip()) > 1 and "}" in fList[index][0].strip():
            # Checks if starts or ends with }
            if fList[index][0].strip().startswith("}"):
                cleanList.append("}")
                commentCheck = fList[index][0].strip()[1:]
                if not commentCheck.strip().startswith("//"):
                    input = commentCheck
                    output, itrDict = headerIterator(input, itrDict)
                    cleanList.append(output)
            else:
                commentCheck = fList[index][0].strip()[:len(fList[index][0].strip())-1]
                if not commentCheck.strip().startswith("//"):
                    input = commentCheck
                    output, itrDict = headerIterator(input, itrDict)
                    cleanList.append(output)
                cleanList.append("}")

        # Checks for empty lines or commented lines
        elif not fList[index][0].strip().startswith(termVars) and len(fList[index][0].strip()) != 0:
            # Removes lines that look like '/* TEXT */'
            if not (fList[index][0].strip().startswith("/*") and fList[index][0].strip().endswith("*/")):
                # Strips extra whitespace from inside of list
                input = re.sub(" +", " ", fList[index][0].strip())
                output, itrDict = headerIterator(input, itrDict)
                cleanList.append(output)

    # Remove comments from first few lines
    comStart = [i for i, item in enumerate(cleanList) if item.startswith('/*')]
    comEnd = [i for i, item in enumerate(cleanList) if item.startswith('*/')]
    if comStart == 0:
        del cleanList[comStart[0]:comEnd[0]+1]
    # Returns cleaned list
    #print(cleanList)
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
        if "=" in dataList[index]:
            lineSplit = dataList[index].split("=")
            lineSplit[0] = lineSplit[0].strip()
            lineSplit[1] = lineSplit[1].strip()
            # Append to dict
            outDict[lineSplit[0]] = lineSplit[1]
        else:
            print("use rep recrustion")
            # *** Why does it get killed here? ***
            # This gets hit with multiline "*" comments...
            # ex. ['crystal_def = "zb";', 'luttinger_gamma1 = 13.38;', 'luttinger_gamma2 = 4.24;', 'luttinger_gamma3 = 5.69;', 'Pcv = 100;', 'Ev = 0;', 'Eg = 0.67;', 'SO_Coupling = 0.29;', 'Ch_eff_mass = 1.0;', 'ac = 0;', 'av = 1.5;//1.5;//-1.24;//4.2;', 'b = -3;//-4.2;//-2.9;//4.2;', 'd = 0;//-5.3;//.7;', 'kx = 0.0;', 'ky = 0.0;', 'kz = 0.0;', 'E = 0.0;', 'band_ind = 14.0;', 'group Misc ', '{', 'bandmodel = 6.0;', 'nparam = 18;', 'Ec_ind = 12;', 'Ehh_ind = 10;', 'Elh_ind = 8;']
            # Can fix by looping over whole file and instantly killing these lines...
            #outDict["comment"] = dataList[index]
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

                # Layer level five handling
                elif layerLevel == 6:
                    # Sets leveel zero call so that it can be retrived later
                    levelSixVar = varList[indexLevel]
                    # If data is present, get it
                    if varList[indexLevel + 2] == "}":
                        dataDict[levelZeroVar][levelOneVar][levelTwoVar][levelThreeVar][levelFourVar][levelFiveVar][levelSixVar] = {"Data": dataGrab(levelFiveVar, fullDataList)}
                        indexLevel = indexLevel + 1
                    # More layers under it
                    else:
                        dataDict[levelZeroVar][levelOneVar][levelTwoVar][levelThreeVar][levelFourVar][levelFiveVar][levelSixVar] = {}
                        # Bump index level and layer level
                        layerLevel = layerLevel + 1
                        indexLevel = indexLevel + 1

                # Layer level five handling
                elif layerLevel == 7:
                    # Sets leveel zero call so that it can be retrived later
                    levelSevenVar = varList[indexLevel]
                    # If data is present, get it
                    if varList[indexLevel + 2] == "}":
                        dataDict[levelZeroVar][levelOneVar][levelTwoVar][levelThreeVar][levelFourVar][levelFiveVar][levelSixVar][levelSevenVar] = {"Data": dataGrab(levelFiveVar, fullDataList)}
                        indexLevel = indexLevel + 1
                    # More layers under it
                    else:
                        dataDict[levelZeroVar][levelOneVar][levelTwoVar][levelThreeVar][levelFourVar][levelFiveVar][levelSixVar][levelSevenVar] = {}
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
    json_object = json.dumps(outDict, indent = 2)
    print(json_object)
    newFile = file.split(".")[0]
    with open(path + newFile + ".json", "w") as outFile:
        json.dump(outDict, outFile)
    print("JSON Created")


# ============== #
# Run Program
# ============== #

data = TextRead(path, file)
dataDict = assembleDicts(data)
exportJson(dataDict, path, file)

"""