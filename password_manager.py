from sheety_manager import Sheety
from random import choice, randint, shuffle, random


class Password(Sheety):  # This class object is responsible for generating and saving a new password

    def __init__(self):
        super().__init__()
        self.password_generated = ""
        self.sheet_requests = Sheety()
        self.alert_message = ""
        self.alert_title = ""

    def password_generator(self):
        """generate and return a password within random letters, numbers and characters"""

        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                   'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
                   'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

        password_list = []  # let create an empty list

        password_list += [choice(letters) for l_char in range(randint(8, 12))]  # append random list of letters
        password_list += [choice(symbols) for s_char in range(randint(2, 4))]  # append random list of numbers
        password_list += [choice(numbers) for n_char in range(randint(2, 4))]  # append random list of chars

        shuffle(password_list)  # shuffle the whole generated chars in the list
        self.password_generated = "".join(password_list)  # join chars together to form one string

    def save_password(self, website, username, password):
        """save the generated password using the method new_post of the object Sheety and return a status code"""

        if len(website) == 0 or len(username) == 0 or len(password) == 0:  # check all entries are filled
            self.alert_message = "Fill all boxes please!"
            self.alert_title = "Uncompleted form"
        else:
            # check if the website already exists on the sheet
            data_exist = self.sheet_requests.get_data(website=website)

            if not data_exist:  # if the current website not exist
                # run post request
                response = self.sheet_requests.new_post(website=website, username=username, password=password)
                if int(response) == 200:  # if request succeeded
                    self.alert_message = f"Your data have been successfully inserted for {website}"
                    self.alert_title = website

            else:  # if the current website already exist on the Google sheet
                self.alert_message = (f"You already have data for {website} in the database! "
                                      f"You can modify it after 'Search'")
                self.alert_title = "Already exists"
