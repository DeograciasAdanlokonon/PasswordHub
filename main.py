from tkinter import *
from tkinter import messagebox
import pyperclip
from password_manager import Password


# ---------------------------- PASSWORD MANAGER OBJECT ------------------------------- #

this_password = Password()  # initialize the password object


def generate_password():
    """Use the method password_generator of the object Password and fill the password entry"""

    # get entry password cleaned first
    entry_password.delete(0, END)

    this_password.password_generator()  # run the methode password generator

    # insert the generated password into the password entry
    entry_password.insert(END, this_password.password_generated)

    # call pyperclip to copy the generated password in the clipboard
    pyperclip.copy(this_password.password_generated)
    lb_password.config(text="Password Copied:", foreground='green')


def save_new_password():
    """Use the methode new_post of the object Password to post a new data on Google sheet"""

    # get data from entries
    website = entry_website.get()
    username = entry_username.get()
    password = entry_password.get()

    if len(website) == 0 or len(username) == 0 or len(password) == 0:
        messagebox.showwarning(title="Uncompleted form", message="Fill in all boxes please!")
    else:
        is_save_ok = messagebox.askokcancel(title="Password Manager",
                                            message=f"These are the details entered: \n\nEmail: "
                                                    f"{username}\nPassword: {password}\n\nIs it "
                                                    f"ok to save? If not cancel.")
        if is_save_ok:
            this_password.save_password(website=website, username=username, password=password)  # run methode new post
            messagebox.showinfo(title=this_password.alert_title, message=this_password.alert_message)

            # empty all entries
            entry_website.delete(0, END)
            entry_password.delete(0, END)
            entry_username.delete(0, END)


def find_password():
    """Use the methode get_data of the object Password to search a website on the Google sheet and return
    its data if found"""

    # empty entries before usage
    entry_password.delete(0, END)
    entry_username.delete(0, END)
    id_container.delete(0, END)

    # get data from entries
    website = entry_website.get()

    if len(website) == 0:
        # let inform user to fill in entry_website
        messagebox.showwarning(title="No website provided", message="Please provide the website to search on!")
    else:
        data = this_password.get_data(website=website)  # run get_data methode and store the returned data

        if data:  # if data not empty
            entry_username.insert(END, data[0]['username'])  # fill username from data
            entry_password.insert(END, data[0]['password'])  # fill password from data

            id_container.insert(END, data[0]['id'])  # get data id in the hidden entry
            btn_modify.grid(column=1, row=4, columnspan=2)  # change Add button to Modify
        else:  # if data empty
            # let inform user no website found
            messagebox.showwarning(title="No website found", message=f"No website named {website} found!")


def modify_password():
    """Modify an existed website data on the Google sheet"""

    # get data from entries
    website = entry_website.get()
    username = entry_username.get()
    password = entry_password.get()
    data_id = id_container.get()

    if len(website) == 0 or len(username) == 0 or len(password) == 0:
        messagebox.showwarning(title="Uncompleted form", message="Fill in all boxes please!")
    else:
        is_save_ok = messagebox.askokcancel(title="Password Manager",
                                            message=f"These are the details entered: \n\nEmail: "
                                                    f"{username}\nPassword: {password}\n\nwill be modified, is it ok? "
                                                    f"If not cancel.")
        if is_save_ok:
            response = this_password.put_data(website=website, username=username,
                                              password=password, data_id=data_id)  # run methode new post
            if int(response) == 200:
                messagebox.showinfo(title=website, message="Your data have been successfully updated!")


# ---------------------------- UI SETUP ------------------------------- #

FONT_NAME = 'Arial'
PRIMARY_COLOR = '#009990'
SECONDARY_COLOR = '#3E4A56'


window = Tk()
window.title('Password Manager')
window.config(padx=50, pady=50, background='white')

# canvas with password logo
canvas = Canvas(width=200, height=200, background='white', highlightthickness=0)
password_logo = PhotoImage(file='pass-logo.png')
canvas.create_image(100, 100, image=password_logo)
canvas.grid(column=1, row=0)

# labels
lb_website = Label(text='Website:', background='white')
lb_website.grid(column=0, row=1)

lb_username = Label(text='Email/Username:', background='white')
lb_username.grid(column=0, row=2)

lb_password = Label(text='Password:', background='white')
lb_password.grid(column=0, row=3)

# Entries
entry_website = Entry(width=32, highlightthickness=1)
entry_website.grid(column=1, row=1)
entry_website.focus()

entry_username = Entry(width=50, highlightthickness=1)
entry_username.grid(column=1, row=2, columnspan=2)

entry_password = Entry(width=32, highlightthickness=1)
entry_password.grid(column=1, row=3)

id_container = Entry(width=10, highlightthickness=1)  # hidden entry to contain data id for put request

# buttons
btn_generate = Button(text='Generate Password', highlightthickness=0, foreground='white', background=PRIMARY_COLOR,
                      command=generate_password)
btn_generate.grid(column=2, row=3)

btn_add = Button(text='Add', width=43, highlightthickness=0, background=PRIMARY_COLOR, foreground='white',
                 command=save_new_password)
btn_add.grid(column=1, row=4, columnspan=2)

btn_search = Button(width=14, text='Search', highlightthickness=0, background=SECONDARY_COLOR, foreground='white',
                    command=find_password)
btn_search.grid(column=2, row=1)

btn_modify = Button(text='Modify', width=43, highlightthickness=0, background=PRIMARY_COLOR, foreground='white',
                    command=modify_password)

window.mainloop()
