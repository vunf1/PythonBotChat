"""Sentence Parsing code"""

#Angus

depth = 0

#Defining of lists, strength & conditioning, greeting and months.

conditioningList = ['treadmill','bike','cross trainer','rowing machine','skipping','eliptical','step machine']

strengthList = ['core','back','shoulder','tricep','bicep','glute','calf','quad','chest','lat','trap','leg','forearm']

greetingList = ['hi','hello','sup','hey','chao','bonjour','whad up']

monthList = ['january','feburary','march','april','may','june','july','august','september','october','november','december']

#applies correct suffix to date

dateList = []
for x in range(1,32):
    suffix = ""
    if x % 10 == 0:
        suffix = "th"
    elif x % 10 == 1:
        suffix = "st"
    elif x % 10 == 2:
        suffix = "nd"
    elif x % 10 == 3:
        suffix = "rd"
    elif x % 10 > 3:
        suffix = "th"
    else:
        pass
    dateList.append(str(x) + suffix)

#~~~~~~~~~~# identification of input of exercises #~~~~~~~~~~#

#Angus

keyWords = {}



def matchCategory(word):
    """User string is input, string searched for specific words, outputs categories words associated with"""

    if word[-1] == "s":
        for x in conditioningList:      #removes plural 's' from input
            if word[0:-1]== x:
                return ("Cardio",word[0:-1])

        for x in strengthList:
            if word[0:-1]== x:
                return ("Strength",word[0:-1])

        if word[0:-1] == "calorie":
            return ("Calorie",word[0:-1])

        for x in greetingList:
            if word[0:-1] == x:
                return ("Greeting",word[0:-1])

    else:
        for x in conditioningList:      #no plural then it is returned to either strength, conditioning
            if word == x:               # greeting, calorie, date or month.
                return ("Cardio",word)

        for x in strengthList:
            if word == x:
                return ("Strength",word)

        if word == "calorie":
            return ("Calorie",word)

        for x in greetingList:
            if word == x:
                return ("Greeting",word)

        for x in dateList:
            if word == x:
                return ("Date",word)

        for x in monthList:
            if word == x:
                return ("Month",word)
    return ("N/a",word)                   #Words that do not fit into any category are put into N/A (ignored)

#angus

def identifyOutput(msg,depthIn):
    """input is string, output is dictionary of words associated with categories"""
    clearKeyWords()
    depth = depthIn
    if depth == 0:
        msgList = msg.lower().split()
        for word in msgList:                                 #Depth is used to determine what type information is passed to the server
            if matchCategory(word) in keyWords:              #adds the muscle group/training machine to a list
                addKeyWordsTuple(matchCategory(word))        #if it is in either strengthList or conditioningList
            else:
                setKeyWordsTuple(matchCategory(word))
    elif depth == 1:
        keyWords["Secondary"] = []
        msgList = msg.lower().split(",")
        for exercise in msgList:
            addKeyWords("Secondary", exercise)
    elif depth == 2:
        ##FOOD LIST
        keyWords["Food"] = []
        msgList = msg.lower().split(",")
        for food in msgList:
            addKeyWords("Food", food)
    else:
        msgList = msg.lower().split(",")
        setKeyWords("Hour", msgList[0])
    print (keyWords)
    return keyWords

#Angus,Chris

def returnOutput(depth=0):
    #Assume all variables are not included in the message
    greet = False
    primaryList = False
    secondaryList = False
    calorieCount = False
    hours = False
    foodList = False
    date = False
    # Check if any variables are actually included
    if depth == 0:
        if "Cardio" in keyWords:
            if primaryList == False:
                primaryList = []
            primaryList += getCardioList()
        if "Strength" in keyWords:
            if primaryList == False:
                primaryList = []
            primaryList += getStrengthList()
        if "Calorie" in keyWords:
            calorieCount = True
        if "Date" in keyWords and "Month" in keyWords:
            date = [getMonth(),getDate()]
        if "Greeting" in keyWords:
            greet = True
    elif depth == 1:
        if "Secondary" in keyWords:
            secondaryList = getSecondList()
    elif depth == 2:
        if "Food" in keyWords:
            if foodList == False:
                foodList = []
            foodList += getFoodList()
    elif depth == 3:
        if "Hour" in keyWords:
            hours = getHours()
    return primaryList, greet, secondaryList, calorieCount, foodList, date, hours, depth

#Angus,Chris,Alex

#~~~~~functions for chris' side~~~~~#

def getCardioList():
    return getKeyWord('Cardio')
                                       #returns words from user input string based on cateogry
def getStrengthList():
    return getKeyWord('Strength')

def clearKeyWords():                   #resets list from previous entries
    keyWords.clear()

def setKeyWords(key, value):              #sets keys and values for a dictionary
    keyWords[key] = [value]

def setKeyWordsTuple(tuple):
    keyWords[tuple[0]] = [tuple[1]]

                                       #assigns keys and values to words in defined lists and adds them to a dictionary
def addKeyWords(key, value):
    keyWords[key].append(value)

def addKeyWordsTuple(tuple):
    keyWords[tuple[0]].append(tuple[1])

def getKeyWord():
    return keyWords

def getKeyWord(key):
    return keyWords[key]

def getHours():
    return getKeyWord('Hour')[0]                    #Get's for returning categories

def getFoodList():
    return getKeyWord('Food')

def getDate():
    return getKeyWord('Date')

def getMonth():
    return getKeyWord('Month')

def getSecondList():
    return getKeyWord('Secondary')
