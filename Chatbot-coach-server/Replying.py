import random
import urllib.request
import json

api_key = "feRjDyiF1DZIMqAzMJFCwGePYZPg1RHaa8JgbjYR"
cardio_exercises = {}
muscle_exercises = {}
depth = 0
workout = []
data_dict = {}
tempList=[] #Temporary lists where all the data will be saved in the txt file.

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#

## Alex contributed
def exercisesToDict():
    """Reads in a file, returns dictionary
        with muscles as key and exercises as
        values"""
    f=open("StrengthExercises.txt" , "r")
    file_string = f.read()
    file_list = file_string.splitlines()
    for line in file_list:
        temp_list = line.split(",")
        exercise, muscle = temp_list[0], temp_list[1]
        if muscle in muscle_exercises:
            # If it exists add to already existing list
            muscle_exercises[muscle].append(exercise)
        else:
            # Create new list and assign first exercise
            muscle_exercises[muscle] = [exercise]
    f.close()
    f=open("ConditioningExercises.txt", "r")
    file_string = f.read()
    file_list = file_string.splitlines()
    for line in file_list:
        temp_list = line.split(",")
        intensity, exercise = temp_list[0], temp_list[1]
        if intensity in cardio_exercises:
            cardio_exercises[intensity].append(exercise)
        else:
            cardio_exercises[intensity] = [exercise]
    f.close()

## Chris, Alex, Angus contributed
def handleReply(tupleIn):
    returnString = ""
    primaryList = tupleIn[0]
    greet = tupleIn[1]
    secondaryList = tupleIn[2]
    calorieCount = tupleIn[3]
    foodList = tupleIn[4]
    date = tupleIn[5]
    hour = tupleIn[6]
    depthIn = tupleIn[7]
    setDepth(depthIn)
    print("Primary\t{}\nGreet\t{}\nSec\t{}\ncalor\t{}\nFood\t{}\nDate\t{}\nHour\t{}\nDepth\t{}\n".format(primaryList, greet, secondaryList, calorieCount, foodList, date, hour, depthIn))
    if greet==True:
        returnString += "Hello I am your personal trainer, Ciri!"+ "<br />"

    if primaryList != False:
        returnString += generatePrimaryReply(primaryList) + "<br />"

    if secondaryList != False:
        returnString += generateSecondaryReply(secondaryList) + "<br />"
    if calorieCount != False:
        setDepth(2)
        returnString += "Enter what foods you want me to count calories for!"

    if foodList != False:
        for food in foodList:
            returnString += "{}: {}kcal per 100g<br />".format(food[0], getCalories(food))
        setDepth(0)

    if date != False:
        returnString += storeDate(date[0][0],date[1][0])

    if hour != False:
        returnString += storeHours(hour)

    if not (primaryList or greet or secondaryList or calorieCount or foodList or date or hour):
        returnString += "Sorry you have not given me anything I understand or can work with."

    return returnString, getDepth()

## Chris and Alex contributed
def generatePrimaryReply(muscleList):
    """Takes in a list of muscles that the user has inputed
    and returns a statement for an individual exercise or
    queries the user for an individual exercise"""
    returnString = ""
    for muscle in muscleList:
        reply = muscle
        replyLower = reply.lower()
        if replyLower in muscle_exercises.keys():
            returnString = "You could try these exercises!:<br />"

            #Add the exercises and a break to the end of the message string
            for exercise in muscle_exercises[replyLower]:
                returnString += exercise + "<br />"
    returnString += "What exercises would you like me to add to your workout?"
    setDepth(1)
    return returnString

## Chris and Alex contributed
def generateSecondaryReply(exerciseList):
    """Input is list of exercises that have been
       stated after primary reply,
       Add the inputs as items in the list "Workout"
       Set depth to 0; reseting the depth.
    """
    returnString = ""
    global workout
    workout += exerciseList
    setDepth(0)
    if len(workout) > 2:
        returnString += "Here is your workout list!:<br />"
        for exercise in workout:
            returnString += "{}<br />".format(exercise)
        returnString += motivationQuote()
        return returnString
    return "Thank you"

## Alex contributed
def motivationQuote():
    quote = ["No pain, no gain!" , "You the man/woman!", "Hit it champ!" , "Just do it!(copyright NIKE)"]
    return random.choice(quote)

def setDepth(depthIn):
    global depth
    depth = depthIn

def getDepth():
    global depth
    return depth

def search(foodName):
    """Takes in foodName as a string
    and returns the ndbno"""
    url = "https://api.nal.usda.gov/ndb/search/?format=json&q={}&max=50&sort=r&ds=Standard+Reference&offset=0&api_key={}".format(foodName,api_key)
    page = urllib.request.urlopen(url)
    data_bytes = page.read()
    data_string = data_bytes.decode('utf-8')
    page.close()
    data_dict = json.loads(data_string)
    # In format: dict: ( dict: list: ( dict: value ) )
    # ["item"][0] will return first search item
    ndbno = data_dict["list"]["item"][0]["ndbno"]
    return ndbno

def calURL(ndbno):
    """Takes in ndbno as a string and
    returns a url for a JSON list"""
    return "https://api.nal.usda.gov/ndb/V2/reports?ndbno={}&type=f&format=json&api_key={}".format(ndbno, api_key)

def calList(ndbno):
    """Takes in a food number and returns the list of foods"""
    url = calURL(ndbno)
    page = urllib.request.urlopen(url)
    data_bytes = page.read()
    data_string = data_bytes.decode('utf-8')
    page.close()
    data_dict = json.loads(data_string)
    return data_dict

def getCalories(foodName):
    """Takes in foodName as a string and
    returns the calorie value"""
    data_dict = calList(search(foodName))
    # In the format of: dict: ( list ( dict: ( dict: ( list: dict:value ) ) ) )
    # ['nutrients'][1] as calories is second item in dict
    return data_dict['foods'][0]['food']['nutrients'][1]['value']


def storeDate(month,day): # Mariya & Antonio
    if month in data_dict:# If the month is already in the dict it checks if the day is in it too
        if day in data_dict[month]:
            pass # If there is already a day in the dict it skips it.
        else:
            data_dict[month] = {str(day):0} #If not it adds it and adds hours as 0.

    else:
        data_dict[month] = {str(day):0} # If not, it appends it as a key to the dict, the variable day as a key to the value of month and hours as a value of day where it is initialized as 0.

    tempList.append(month) #Adds the month to the list to write it in the txt file.
    tempList.append(str(day)) #Adds the day to the lsit to write it in the txt file.
    setDepth(3)
    return("How many hours did you work on {} {}?".format(month,day))

def storeHours(hour):#Joao
    data_dict[tempList[0]][tempList[1]] += int(hour) # put the data(hours) in position data[0][1]
    setDepth(0)
    tempList.clear() #clean the tempList created
    return("Thank you!")

#Joao
def writeToFile():
    f=open('log.txt','w') # Opens the file,converts the list into a json string, writes on it and closes it
    f.write(json.dumps(data_dict))
    f.close()

def ReadFile():
    f=open('log.txt','r')# Opens the file, converts the string back into list, reads it, prints it and closes it.
    data_dict = f.read()
    f.close()
