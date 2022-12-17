import json
from tkinter import messagebox
from tkinter import *
from random import shuffle, choice, randint
import pyperclip


# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = website_entry.get()
    try:
        with open('data.json', 'r') as data_file:
            old_data = json.load(data_file)
        data_dict = old_data[website]
    except KeyError:
        messagebox.showinfo(title='No Website Exist', message="Website you are trying to search do not exist"
                                                              " in database.\nTry putting the correct website name.")
    except FileNotFoundError:
        messagebox.showinfo(title='No Data Exist', message="You haven't entered any data till now.")
    else:
        website_data = f'Email: {data_dict["email"]}\nPassword: {data_dict["password"]}'
        messagebox.showinfo(title=website, message=website_data)


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    password_entry.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [choice(letters) for _ in range(randint(8, 10))]
    password_list += (choice(symbols) for _ in range(randint(2, 4)))
    password_list += (choice(numbers) for _ in range(randint(2, 4)))

    shuffle(password_list)
    password = "".join(password_list)
    pyperclip.copy(password)
    password_entry.insert(0, password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    website = website_entry.get()

    try:
        with open('data.json') as data_file:
            if website in json.load(data_file):
                already_exist_msg = f'You have already entered this website name.\nTry some different name such as ' \
                                    f'{website}_a or {website}_1, etc'
                messagebox.showinfo(title='Website Already Exist', message=already_exist_msg)
                return
    except FileNotFoundError:
        pass

    email = username_entry.get()
    password_entered = password_entry.get()
    new_data = {website:
        {
            'email': email,
            'password': password_entered
        }
    }

    if website == '' or email == '' or password_entered == '':
        messagebox.showinfo(title='Oops', message="Please don't leave any fields empty.")
        return

    check_details_msg = f'These are the details entered.\n\n Email: {email}\n Password: {password_entered}' \
                        f'\n\nAre you sure to save it?'
    is_ok = messagebox.askokcancel(title=website,
                                   message=check_details_msg)

    if is_ok:
        try:
            with open('data.json', 'r') as data_file:
                # Reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            with open('data.json', 'w') as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # Updating the old data
            data.update(new_data)
            with open('data.json', 'w') as data_file:
                # Saving the updated data
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)
            messagebox.showinfo(title=website, message='Your password has been saved successfully.')


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title('Password Manager')
window.config(padx=50, pady=50)

logo = PhotoImage(file='logo.png')
canvas = Canvas(width=200, height=200)
canvas.create_image(100, 100, image=logo)
canvas.grid(column=1, row=0)

website_label = Label(text='Website:')
website_label.grid(column=0, row=1)

website_entry = Entry(width=30)
website_entry.grid(column=1, row=1)
website_entry.focus()

search_button = Button(text='Search', width=8, command=find_password)
search_button.grid(column=2, row=1)

username_label = Label(text='Email/Username:')
username_label.grid(column=0, row=2)

username_entry = Entry(width=41)
username_entry.grid(column=1, row=2, columnspan=2)
username_entry.insert(0, 'example@gmail.com')

password_label = Label(text='Password:')
password_label.grid(column=0, row=3)

password_entry = Entry(width=31)
password_entry.grid(column=1, row=3, columnspan=1)

generate_button = Button(text='Generate', width=8, command=generate_password)
generate_button.grid(column=2, row=3)

add_button = Button(text='Add', width=36, command=save_password)
add_button.grid(column=1, row=4, columnspan=2)

window.mainloop()
