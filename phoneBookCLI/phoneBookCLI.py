import time

phonebook = {}

def is_integer(string):
    try:
        int(string)
        return True
    except:
        return False

def add_entry(entry):
    lastNameInitial = entry[0][0][0].lower()
    phonebook.setdefault(lastNameInitial,[])
    current_entries = phonebook[lastNameInitial]
    phonebook[lastNameInitial] = current_entries.append(entry)
    

def filter_phone_number(phoneNum):
    validIntegers = {"0":"1","1":"1","2":"1","3":"1","4":"1","5":"1","6":"1","7":"1","8":"1","9":"1"}
    numbers = ""
    for char in phoneNum:
        if validIntegers.get(char):
            numbers += char
    return numbers

def get_phone_number():
    phoneInput = input("\nPlease input the 10 digit phone number.\n")
    phoneNum = filter_phone_number(phoneInput)
    while len(phoneNum) != 10:
        print("\nError that is not a valid phone number. Please input a valid number\n")
        phoneInput = input()
        phoneNum = filter_phone_number(phoneInput)
    return phoneNum
    

def get_address():
    street = input("\nPlease input the street\n")
    city = input("\nPlease input the city\n")
    state = input("\nPlease input the state\n")
    zipCode = input("\nPlease input the zip code\n")
    while len(zipCode) != 5 and is_integer(zipCode):
        zipCode = input("\nThat is not a valid zipcode\n")
    address = [street,city,state,zipCode]
    return " ".join(address)            

def create_entry():
    #firstName = input("\nPlease enter the first name of the person.\n")
    #middleName = input("\nPlease input the middle name of the person.\n")
    #lastName = input("\nPlease input the last name of the person.\n")
    phoneNum = get_phone_number()
    address = get_address()
    entry = [[lastName,middleName,firstName],[phoneNum,address]]
    add_entry(entry)

def search_contact(commands):
    if command[0] == "-l":
        if len(command) > 2:
            print("Error last name should be one word")
            return None
        else:
            search_by_last(command[1:])
    if command[0] == "-m":
        if len(command) > 2:
            print("Error middle name should be one word")
            return None
        else:
            search_by_middle(command[1:])
    if command[0] == "-f":
        if len(command) > 2:
            print("Error first name should be one word")
            return None
        else:
            search_by_middle(command[1:])
    else:
        if len(command) > 4:
            print("Error full name should only be 3 words")
            return None
        else:
            search_by_full(command[1:]) 

def search_by_last(lastName):
    bookEntries = phonebook[lastName[0].lower()]
    matches = []
    for entry in bookEntries:
        if lastName = entry[0][0]
            name = entry[0][2] + " " + entry[0][1] + " " + entry[0][0]
            phone = entry[1][0][:3]+"-"entry[1][0][3:6]+ "-"entry[1][0][6:]
            address = entry[1][1]
            matches.append("Name: " + name + " Phone: " + phone + " Address: " + address)
    if len(matches) != 0:
        for match in matches:
            print(match)
    else:
        print("Contact not found")
    return None

def search_by_full(fullName):
    if len(fullName) != 3:
        print("Error a full name should be 3 words")
        return None
    
    

command = ""
while command != "exit":
    command = input("\nPlease enter one of the following command: create, view, modify, search:\n")
    command = command.split()
    if command[0] == "create":
        if len(command) > 1:
            print("Error create does not take any arguments")
        else:
            create_entry()
    if command[0] == "search":
        search_contact(command[1:])
        


print("\nThank you for viewing.")
time.sleep(2)
