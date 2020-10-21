import time
import copy

phonebook = {'s':[[['Smith','middle','first'],['32453124','agh']]]}

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
    current_entries.append(entry)
    phonebook[lastNameInitial] = current_entries

def collect_entry(entry):
    name = entry[0][2] + " " + entry[0][1] + " " + entry[0][0]
    phone = entry[1][0][:3] + "-" + entry[1][0][3:6] + "-" + entry[1][0][6:]
    address = entry[1][1]
    entry = "Name: " + name + " Phone: " + phone + " Address: " + address
    return entry
    

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
    firstName = input("\nPlease enter the first name of the person.\n")
    middleName = input("\nPlease input the middle name of the person.\n")
    lastName = input("\nPlease input the last name of the person.\n")
    phoneNum = get_phone_number()
    address = get_address()
    entry = [[lastName,middleName,firstName],[phoneNum,address]]
    add_entry(entry)

def search_contact(command):
    if command[0] == "-l":
        if len(command) > 2:
            print("Error last name should be one word\n")
            return None
        else:
            search_by_last(command[1:])
            return None
    else:
        if len(command) != 3:
            print("Error full name should be 3 words\n")
            return None
        else:
            search_by_full(command) 

def search_by_last(lastName):
    lastName = lastName[0]
    bookEntries = phonebook.get(lastName[0].lower())
    matches = []
    if len(bookEntries) != 0:
        for entry in bookEntries:
            if lastName.lower() == entry[0][0].lower():
                collection = collect_entry(entry)
                matches.append(collection)
        for match in matches:
            print(match)
    else:
        print("No contacts found")
    return None

def search_by_full(fullName):
    if len(fullName) != 3:
        print("Error full name should be 3 words\n")
        return None
    matches = []
    bookEntries = phonebook.get(fullName[2][0].lower())
    if len(bookEntries) != 0:
        for entry in bookEntries:
            if fullName[0].lower() == entry[0][2].lower() and fullName[1].lower() == entry[0][1].lower() and fullName[2].lower() == entry[0][0].lower():
                collection = collect_entry(entry)
                matches.append(collection)
        for match in matches:
            print(match)
    else:
        print("No contacts found\n")
    return None

def show_book():
    keys = phonebook.keys()
    entries = []
    print("\n")
    for key in keys:
        entries = phonebook[key]
        for entry in entries:
            entry = collect_entry(entry)
            print(entry)

def modify_contact(fullName):
    if len(fullName) != 3:
        print("Error full name should be 3 words\n")
        return None
    matches = []
    entries = []
    bookEntries = phonebook.get(fullName[2][0].lower())
    index = 0
    if len(bookEntries) != 0:
        for entry in bookEntries:
            if fullName[0].lower() == entry[0][2].lower() and fullName[1].lower() == entry[0][1].lower() and fullName[2].lower() == entry[0][0].lower():
                collection = collect_entry(entry)
                entries.append(entry)
                matches.append([collection,str(index+1)])
        for match in matches:
            print(match[1] + ".",match[0])
    if len(matches) == 0:
        print("No matches.\n")
        return None
    contact = input("Which entry would you like to modify?\n")
    if is_integer(contact):
        while int(contact) > len(matches):
            contact = input("That entry is outside the range of options. Please select a contact to modify.\n")
        continueModify = "yes"
        while continueModify.lower() != "no":
            option = input("What would you like to modify? First, middle, last, phone or address?\n")
            while option.lower() not in ["first","middle","last","phone","address"]:
                option = input("Error, that is not a valid option. Please type: first, middle, last, phone or address")
            option = option.lower()

            if option == "first":
                newFirst = input("Enter the new first name.\n")
                entries[int(contact)-1][0][2] = newFirst
                phonebook[fullName[2][0].lower()] = entries
            if option == "middle":
                newMiddle = input("Enter the new middle name.\n")
                entries[int(contact)-1][0][1] = newMiddle
                phonebook[fullName[2][0].lower()] = entries
            if option == "last":
                newLast = input("Enter the new last name.\n")
                overwriting = copy.deepcopy(entries)
                overwriting[int(contact)-1] = None
                overwriting = [over for over in overwriting if over]
                phonebook[fullName[2][0].lower()] = overwriting
                entries[int(contact)-1][0][0] = newLast
                add_entry(entries[int(contact)-1])
                return None
            if option == "phone":
                phoneNum = get_phone_number()
                entries[int(contact)-1][1][0] = phoneNum
                phonebook[fullName[2][0].lower()] = entries
            if option == "address":
                address = get_address()
                entries[int(contact)-1][1][1] = address
                phonebook[fullName[2][0].lower()] = entries
            

            continueModify = input("Would you like to modify anything else? Yes or no?")
    else:
        print("Please try again by selecting a vaild option.\n")
        return None
    

command = ""
while command != "exit":
    command = input("\nPlease enter one of the following command: create, view, modify, search, show:\n")
    command = command.split()
    if command[0] == "create":
        if len(command) > 1:
            print("Error create does not take any arguments\n")
        else:
            create_entry()
    if command[0] == "search":
        search_contact(command[1:])
    if command[0] == "show":
        if len(command) > 1:
            print("Error show does not take any arguments\n")
        else:
            show_book()
    if command[0] == "view":
        search_by_full(command[1:])
    if command[0] == "modify":
        modify_contact(command[1:])
    command = "".join(command)
        


print("\nThank you for viewing.")
time.sleep(2)
