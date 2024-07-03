def strength_checker(password):
    #Special character list 
    special_characters = set("()-+?_=,/!@#^&*<>$%")
    #Following conditions to be validated for a strong password
    rules = {
        "length": len(password) >= 8,  #Condition to make sure password length is 8 or more than 8.
        "upper-case": any(char.isupper() for char in password),  #Looping thru the password char by char to check it anyone char is upercase.
        "lower-case": any(char.islower() for char in password),  #Same case as above but for lower case char this time.
        "number": any(char.isdigit() for char in password),  #Atleast one digit
        "special_character": any(char in special_characters for char in password)  #Atleast on special character
    }

    #Proper feedback prompts for the user in case passoword not strong
    prompts = {
        "length": "at least 8 characters long.",
        "upper-case": "at least one character should be in upper-case.",
        "lower-case": "at least one character should be in lower-case.",
        "number": "at least one character should be a number please.",
        "special_character": "at least one special character."
    }
    #Declring the variable all_rules_met to TRUE
    all_rules_met = True

    #Check if the user password is strong enough or not
    for specs, conditions in rules.items():
        if not conditions:
            all_rules_met = False #If password weak, setting the variable False

    #This snippet will provide the fedback to the user if password is weak and also will return either TRUE OR FALSE
    if not all_rules_met:
        #printing the feedback in a catchy phrase.
        print("Uh-Oh! Your password is as fragile as a spider's web. Strengthen it!")
        print("")
        print("Please find the feedback below for your password:")
        for specs, conditions in rules.items():
            if not conditions:
                #Printing the feedback in bold
                print(f"\033[1mYour password should have {prompts[specs]}\033[0m")  

        return False
    else:
        return True

#Setting up a while loop to continoulsy ask the user for a password till he/she makes a good and strong password:)
while True:
    password = input("Enter your password : ")
    if strength_checker(password):
        print("Great! Your password is as solid as a rock. Rock on!")
        break
    else:
        print("")
        print("Enter a robust password this time :)")
