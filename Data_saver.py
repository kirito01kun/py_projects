from tkinter import *

# IMPORT THE SQLITE3
import sqlite3

# Create the main window.
root = Tk()

# Give it a title. 
root.title('Data Saver')

# Edit the window color.
root.configure(bg="#424242")

copyright = Label(root, text='© 2020 Kbala Youssef', fg='#fafafa', bg='#424242')

# Connect to a database called "Database.db" if it's already exist
# And if not it will be created.
connect = sqlite3.connect("Database.db")
cursor = connect.cursor()

# check if the table where data will be stored is already exist or not.
cursor.execute('''SELECT count(name) FROM sqlite_master
        where type='table' AND name='Logins' ''')

# The cursor.fetchone() method will return
# A tuple '(1,)' if the table exists and 'None' if not.

if cursor.fetchone()[0] == 1:
    # if the table exists -> pass.
    pass
else:
    # And if not -> Create one.
    cursor.execute('''CREATE TABLE Logins (user TEXT,pwd TEXT,
            emails TEXT,contacts TEXT,data TEXT)''')

# Commit the changes.
connect.commit()

# Close the connection that we open.
connect.close()


class DataBases():
    # This Class will check the logins and store the data using Sqlie3.
    
    @staticmethod
    def add_logins(user, pwd):
        # This method will add new users if they are not already exist. 
        
        params = (user, pwd)
        # Open a salite3 connection to the Database that we create already.
        connect = sqlite3.connect("Database.db")
        cursor = connect.cursor()
        # Add username and pwd to the Database.
        cursor.execute("INSERT INTO Logins(user,pwd) VALUES (?,?)", params)
        connect.commit()
        connect.close()

    @staticmethod
    def existing_user_or_not(user, pwd):
        # Check if user is new.

        connect = sqlite3.connect("Database.db")
        cursor = connect.cursor()
        # Point to user and pwd feild in table.
        cursor.execute("""SELECT user,pwd From Logins
                WHERE user=? AND pwd=?""", (user, pwd))
        if cursor.fetchone():
            res = True
        else:
            res = False
        connect.close()
        return res

    @staticmethod
    def data_inserting(data, type, user):
        # Insert data into the 'Logins' table in Database.
        
        temp = ''
        connect = sqlite3.connect("Database.db")
        cursor = connect.cursor()
        # First case the data type passing
        # to this method is 'mail'.
        
        if type == 'mail':
            # connection to data base is already opened.
            
            # select all from table.
            cursor.execute("SELECT * FROM Logins")
            
            # Looping into all table rows.
            for row in cursor:
                # row[0] contain the user name field. 
                if row[0] == user:
                    # getting data from 'emails' column and 
                    # the data inserted by user and store it in temp var.
                    if row[2] != None:
                        temp = "{},({})".format(row[2], data)
                    else:
                        temp = "({})".format(data)
            connect.close()
            connect = sqlite3.connect("Database.db")
            cursor = connect.cursor()
            
            # inserting data into emails column of the specific user.
            cursor.execute('''UPDATE Logins SET "emails"=?
                    WHERE user=?''', (temp, user))
        
        # Second case the data type passing 
        # to this method is 'contact'.
        elif type == 'contact':
            # select all from table.
            
            cursor.execute("SELECT * FROM Logins")            
            
            # Looping into all table rows.
            for row in cursor:
                # getting data from 'contacts' column and
                # the data inserted by user and store it in temp var.
                if row[0] == user:
                    if row[3] != None:
                        temp = "{},({})".format(row[3], data)
                    else:
                        temp = "({})".format(data)
            connect.close()
            connect = sqlite3.connect("Database.db")
            cursor = connect.cursor()

            # inserting data into contacts column of the specific user.
            cursor.execute('''UPDATE Logins SET
                    "contacts"=? WHERE user=?''', (temp, user))

        else:
            cursor.execute("SELECT * FROM Logins")
            for row in cursor:
                # getting data from 'random' column and
                # the data inserted by user and store it in temp var.
                if row[0] == user:
                    if row[4] != None:
                        temp = "{},({})".format(row[4], data)
                    else:
                        temp = "({})".format(data)
            connect.close()
            connect = sqlite3.connect("Database.db")
            cursor = connect.cursor()
            
            # inserting data into the 'random' column of the specific user.
            cursor.execute('''UPDATE Logins SET
                    "data"=? WHERE user=?''', (temp, user))
        
        # commit the changes.
        connect.commit()
        # close the connection.
        connect.close()


DataBases = DataBases()

class Formating():
    # this class will format the data in specific format.
    
    def user_mails(email, pwd):
        # Formatting the 'emails' data.

        # check if data not NOTHING.
        if (email != '') and (pwd != ''):
            maillist = []
            mailstr = "Email: {} || Password: {}".format(email, pwd)
            maillist.append(mailstr)
            return mailstr
        else:
            pass

    def user_data(data):
        # Formatting the 'random' data.

        if data != '':
            datalist = []
            datastr = "<<{}>>".format(data)
            datalist.append(datastr)
            return datastr
        else:
            pass

    def user_contact(name, GSM):
        # Formatting the 'contact' data.
        
        if (name != '') and (GSM != ''):
            contactlist = []
            contactstr = "Name: {} || Phone: {}".format(name, GSM)
            contactlist.append(contactstr)
            return contactstr
        else:
            pass

obj = Formating()

class App():
    # this is the main class.

    def __init__(self):

        # Design images used.
        # Icons made by <a href="https://www.flaticon.com/authors/freepik"
        # title="Freepik">Freepik</a> from 
        # <a href="https://www.flaticon.com/"
        # title="Flaticon"> www.flaticon.com</a>

        self.Login_img = PhotoImage(file='img\login_m.png')

        copyright.grid(row=4, column=0)
        # this var will contain the name of current user.
        self.current_user = ''
        
        # making sign-up form.
        self.signup_username = Entry(root, fg='#fafafa',
                bg='#424242', width=50)
        self.signup_pwd = Entry(root, show='*', fg='#fafafa',
                bg='#424242', width=50)

        # the sign-up submit button will call the add_member
        # method and pass user name and pwd intered to it.
        self.signup_submit = Button(root, text="Sign up",
                bg='#424242', height=1, width=18, fg='#fafafa',
                command=lambda: self.add_member(self.signup_username.get(),
                    self.signup_pwd.get()))
        
        # making sign-in form.
        self.signin_username = Entry(root, fg='#fafafa',
                bg='#424242', width=50)
        self.signin_pwd = Entry(root, show='*',
                fg='#fafafa', bg='#424242', width=50)
        
        # the sign-in submit button will call the check_member
        # method and pass user name and pwd intered to it.
        self.signin_submit = Button(root, image=self.Login_img, bg='#424242',
                fg='#fafafa', activebackground='#424242',
                height=20, border=0, text="Log in ",
                font="Helvetica 10 bold", compound=RIGHT,
                command=lambda: self.check_member(self.signin_username.get(),
                    self.signin_pwd.get()))
        
        # side spaces.
        self.space1stusr = Label(root, text=' User name : ',
                fg='#fafafa', bg='#424242')
        self.space1stpwd = Label(root, text=' Password : ',
                fg='#fafafa', bg='#424242')
        self.space2nd = Label(root, text='             ',
                fg='#fafafa', bg='#424242')
        
        # create menu buuton.
        self.menu = Button(root, text="Menu", width=18, fg='#fafafa',
                bg='#424242', font="Helvetica 10 bold",
                command=lambda: self.menu_click(), height=4)
        
        # show menu button on window.
        self.menu.grid(row=0, column=0)
        
        # make sign-up button option.
        self.Sign_up = Button(root, text="Sign up", bg='#424242',
                height=4, width=18, fg='#fafafa', font="Helvetica 10 bold",
                command=lambda: self.sign_up_form())

        # make sign-in button option.
        self.Sign_in = Button(root, text="Log in", bg='#424242',
                height=4, width=18, fg='#fafafa', font="Helvetica 10 bold",
                command=lambda: self.sign_in_form())
        
        # make sign-out button option.
        self.Sign_out = Button(root, text="Log out", bg='#424242',
                height=1, width=10, fg='#fafafa',
                command=lambda: self.menu_click())
        
        # make quit button option.
        self.Quit = Button(root, text="Quit", bg='#424242',
                width=18, height=4, fg='#fafafa', font="Helvetica 10 bold",
                command=lambda: self.quit())
        
        # making the 'existing sign-up error' text label.
        self.exesting = Label(root, text="Already exesting email/password",
                bg='#424242', fg='#fafafa')

        # making the 'success' text label.
        self.success = Label(root, text="Success",
                bg='#424242', fg='#fafafa')
        
        # making the 'existing sign-in error' text label.
        self.login_error = Label(root,
                text="User name or password is incorrect!",
                bg='#424242', fg='#fafafa')
        
        # making the 3 scrollbars for listboxs.
        self.scrollbar = Scrollbar(root, orient='vertical',
                bg='#424242')
        self.scrollbar1 = Scrollbar(root, orient='vertical',
                bg='#424242')
        self.scrollbar2 = Scrollbar(root, orient='vertical',
                bg='#424242')
        
        # making the listboxs where data will shows up.
        self.maildata_list = Listbox(root, height=12,
                width=90, bg='#424242',
                yscrollcommand=self.scrollbar.set, fg='#fafafa')
        self.contactdata_list = Listbox(root, height=12,
                width=90, bg='#424242',
                yscrollcommand=self.scrollbar.set, fg='#fafafa')
        self.randomdata_list = Listbox(root, height=12,
                width=90, bg='#424242',
                yscrollcommand=self.scrollbar.set, fg='#fafafa')
        
        # licking scrollbars to listboxs.
        self.scrollbar.config(command=self.maildata_list.yview)
        self.scrollbar1.config(command=self.contactdata_list.yview)
        self.scrollbar2.config(command=self.randomdata_list.yview)
        
        # make 'Pick one :' text label.
        self.pick = Label(root, text="Pick One :",
                fg='#fafafa', font="Helvetica 10 bold", bg='#424242')
        
        # make 'Email', 'Contact', 'Random Data' option buttons.
        self.mail_button = Button(root, text="Email",
                width=22, font="Helvetica 11 bold", fg='#fafafa',
                bg='#424242', height=4, border=0,
                command=lambda: self.data_list('mail'))
        self.contact_button = Button(root, text="Contact",
                width=22, fg='#fafafa', bg='#424242', height=4,
                font="Helvetica 11 bold", border=0,
                command=lambda: self.data_list('contact'))
        self.randomdata_button = Button(root, text="Random Data",
                width=22, fg='#fafafa', bg='#424242', height=4,
                font="Helvetica 11 bold", border=0,
                command=lambda: self.data_list('random'))

        # make go to data entring menu buttons.
        self.add_mail_button = Button(root, text="Add E-mail",
                width=22, height=2, fg='#fafafa', bg='#424242',
                font="Helvetica 10 bold",
                command=lambda: self.adding_mail())
        self.add_contact_button = Button(root, text="Add Contact",
                bg='#424242', height=2, width=15, fg='#fafafa',
                font="Helvetica 10 bold",
                command=lambda: self.adding_contact())
        self.add_random_button = Button(root, text="Add Random data",
                bg='#424242', width=15, height=2, fg='#fafafa',
                font="Helvetica 10 bold",
                command=lambda: self.adding_random_data())

        # make back buttons.
        self.back_choice_data = Button(root, text="Back",
                bg='#424242', width=10, height=1, fg='#fafafa',
                font="Helvetica 10 bold",
                command=lambda: self.choice_data())
        self.back_mail_data = Button(root, text="Back",
                bg='#424242', width=10, height=1, fg='#fafafa',
                font="Helvetica 10 bold",
                command=lambda: self.data_list('mail'))
        self.back_contact_data = Button(root, text="Back",
                bg='#424242', width=10, height=1, fg='#fafafa',
                font="Helvetica 10 bold",
                command=lambda: self.data_list('contact'))
        self.back_random_data = Button(root, text="Back",
                bg='#424242', width=10, height=1, fg='#fafafa',
                font="Helvetica 10 bold",
                command=lambda: self.data_list('random'))
        
        # making submit buttons for every option.
        self.submit_add_mail = Button(root, text="Add it",
                bg='#424242', height=1, width=15, fg='#fafafa',
                font="Helvetica 10 bold",
                command=lambda: self.mail_added(self.signin_username.get(),
                    self.signin_pwd.get()))
        self.submit_add_contact = Button(root, text="Add it",
                bg='#424242',height=1, width=15, fg='#fafafa',
                font="Helvetica 10 bold",
                command=lambda: self.contact_added(self.contactnamefield.get(),
                    self.contactpwdfield.get()))
        self.submit_add_random = Button(root, text="Add it",
                bg='#424242', height=1, width=15, fg='#fafafa',
                font="Helvetica 10 bold",
                command=lambda: self.random_added(self.signin_username.get()))
        
        # make contact data entering form.
        self.contactnamespace = Label(root, text=' Name : ',
                fg='#fafafa', bg='#424242')
        self.contactpwdspace = Label(root, text=' Phone : ',
                fg='#fafafa', bg='#424242')
        self.contactnamefield = Entry(root, fg='#fafafa',
                bg='#424242', width=50)
        self.contactpwdfield = Entry(root, fg='#fafafa',
                bg='#424242', width=50)
        self.tempvar = ''


    def clear_side(self):
        # this method will clear the window to refresh it.

        self.contactpwdfield.delete(0, END)
        self.contactnamefield.delete(0, END)
        self.signin_username.grid_forget()
        self.signup_username.grid_forget()
        self.signin_pwd.grid_forget()
        self.signup_pwd.grid_forget()
        self.signin_submit.grid_forget()
        self.signup_submit.grid_forget()
        self.space2nd.grid_forget()
        self.space1stusr.grid_forget()
        self.space1stpwd.grid_forget()
        self.pick.grid_forget()
        self.add_mail_button.grid_forget()
        self.add_mail_button.grid_forget()
        self.add_contact_button.grid_forget()
        self.add_random_button.grid_forget()
        self.mail_button.grid_forget()
        self.contact_button.grid_forget()
        self.randomdata_button.grid_forget()
        self.maildata_list.grid_forget()
        self.randomdata_list.grid_forget()
        self.contactdata_list.grid_forget()
        self.back_choice_data.grid_forget()
        self.scrollbar.grid_forget()
        self.scrollbar1.grid_forget()
        self.scrollbar2.grid_forget()
        self.back_mail_data.grid_forget()
        self.back_contact_data.grid_forget()
        self.back_random_data.grid_forget()
        self.submit_add_random.grid_forget()
        self.submit_add_contact.grid_forget()
        self.submit_add_mail.grid_forget()
        self.contactpwdspace.grid_forget()
        self.contactnamespace.grid_forget()
        self.contactpwdfield.grid_forget()
        self.contactnamefield.grid_forget()
        self.success.grid_forget()
        self.login_error.grid_forget()
        self.exesting.grid_forget()
        self.signin_username.delete(0, END)
        self.signin_pwd.delete(0, END)
        self.signup_username.delete(0, END)
        self.signup_pwd.delete(0, END)
        self.Sign_out.grid_forget()

    def menu_click(self):
        # show up the first window form. 
        
        self.clear_side()
        self.Sign_up.grid(row=1, column=0)
        self.Sign_in.grid(row=2, column=0)
        self.Quit.grid(row=3, column=0)


    def sign_up_form(self):
        # making the sign-up form.

        self.clear_side()
        self.signup_username.grid(row=1, column=2)
        self.signup_pwd.grid(row=2,column=2)
        self.signup_submit.grid(row=3, column=2)
        self.space1stusr.grid(row=1, column=1)
        self.space1stpwd.grid(row=2, column=1)
        self.space2nd.grid(row=1, column=3)


    def sign_in_form(self):
        # making the sign-in form.

        self.clear_side()
        self.signin_username.grid(row=1, column=2)
        self.signin_pwd.grid(row=2, column=2)
        self.signin_submit.grid(row=3, column=2)
        self.space1stusr.grid(row=1, column=1)
        self.space1stpwd.grid(row=2, column=1)
        self.space2nd.grid(row=1, column=3)

    def add_member(self, key, value):
        # this method will add new users.

        self.signup_username.delete(0, END)
        self.signup_pwd.delete(0, END)

        # call the DataClass to check if user is already exist.
        if DataBases.existing_user_or_not(key, value):
            self.exesting.grid(row=4, column=2)
            # show up the error for only 2 sec.
            self.exesting.after(2000,
                    lambda: self.exesting.grid_forget())

        else:
            # add new user to database.
            DataBases.add_logins(key, value)
            self.success.grid(row=4, column=2)
            self.success.after(2000,
                    lambda: self.success.grid_forget())
        

    def check_member(self, key, value):
        # in log-in field check if account is exist or not.

        self.signin_username.delete(0, END)
        self.signin_pwd.delete(0, END)

        if DataBases.existing_user_or_not(key, value):
            self.choice_data()
            self.current_user = key
        
        else:
            self.login_error.grid(row=4, column=2)
            self.login_error.after(2500,
                    lambda: self.login_error.grid_forget())


    def choice_data(self):
        # showing up the data choice form.

        self.clear_side()
        self.pick.grid(row=0, column=1, columnspan=2)
        self.mail_button.grid(row=1, column=1, columnspan=2)
        self.contact_button.grid(row=2, column=1)
        self.randomdata_button.grid(row=2, column=2)


    def data_list(self, type):
        # making data list form by the type given.

        self.maildata_list.delete(0, END)
        self.contactdata_list.delete(0, END)
        self.randomdata_list.delete(0, END)
        self.clear_side()

        if type == 'mail':
            # case of mails data.

            # making mails listbox and scrollbar.
            # back button and the add mail option.
            self.add_mail_button.grid(row=0,
                    column=1, columnspan=2)
            self.maildata_list.grid(row=1,
                    column=1, columnspan=2, rowspan=3)
            self.scrollbar.grid(row=1,
                    column=3, rowspan=3, sticky='ns')
            self.back_choice_data.grid(row=4, column=1)
            self.Sign_out.grid(row=4, column=2)

            # getting data from the 'emails'
            # column in database.
            temp = ''
            connect = sqlite3.connect("Database.db")
            cursor = connect.cursor()
            cursor.execute("SELECT * FROM Logins")
            for row in cursor:
                # specify by the current user.
                if row[0] == self.current_user:
                    if row[2] != None:
                        temp = row[2]
            connect.close()
            
            # list the emails in listbox.
            index = 0
            for charindex in range(len(temp)):
                if (temp[charindex] == ',') and temp[charindex + 1] == '(':
                    dummy = temp[index + 1:charindex - 1]
                    index = charindex + 1
                    if dummy != '':
                        self.maildata_list.insert(END, dummy)

                if (temp[charindex] == ')') and (charindex == len(temp) - 1):
                    dummy = temp[index + 1:charindex]
                    self.maildata_list.insert(END, dummy)

        elif type == 'contact':
            # case of 'cotacts' data.

            # making contacts form.
            self.add_contact_button.grid(row=0,
                    column=1, columnspan=2)
            self.contactdata_list.grid(row=1,
                    column=1, columnspan=2, rowspan=3)
            self.scrollbar1.grid(row=1, column=3,
                    rowspan=3, sticky='ns')
            self.back_choice_data.grid(row=4, column=1)
            self.Sign_out.grid(row=4, column=2)

            # getting data from the 'contacts' column
            # in the data base.
            temp = ''
            connect = sqlite3.connect("Database.db")
            cursor = connect.cursor()
            cursor.execute("SELECT * FROM Logins")
            for row in cursor:
                # where the user is the current user.
                if row[0] == self.current_user:
                    if row[3] != None:
                        temp = row[3]
            connect.close()
            
            # list contacts in listbox.
            index = 0
            for charindex in range(len(temp)):
                if (temp[charindex] == ',') and temp[charindex + 1] == '(':
                    dummy = temp[index + 1:charindex - 1]
                    index = charindex + 1
                    if (dummy != ''):
                        self.contactdata_list.insert(END, dummy)

                if (temp[charindex] == ')') and (charindex == len(temp) - 1):
                    dummy = temp[index + 1:charindex]
                    self.contactdata_list.insert(END, dummy)

        else:
            # case of random data.

            # make 'random' form.
            self.add_random_button.grid(row=0,
                    column=1, columnspan=2)
            self.randomdata_list.grid(row=1,
                    column=1, columnspan=2, rowspan=3)
            self.scrollbar2.grid(row=1, column=3,
                    rowspan=3, sticky='ns')
            self.back_choice_data.grid(row=4, column=1)
            self.Sign_out.grid(row=4, column=2)
            

            # getting data from random column
            # in the data base.
            temp = ''
            connect = sqlite3.connect("Database.db")
            cursor = connect.cursor()
            cursor.execute("SELECT * FROM Logins")
            for row in cursor:
                # where the user -> current user.
                if row[0] == self.current_user:
                    if row[4] != None:
                        temp = row[4]
            connect.close()

            # list data in listbox.
            index = 0
            for charindex in range(len(temp)):
                if (temp[charindex] == ',') and temp[charindex + 1] == '(':
                    dummy = temp[index + 1:charindex - 1]
                    index = charindex + 1
                    if (dummy != ''):
                        self.randomdata_list.insert(END, dummy)
                    else:
                        pass
                if (temp[charindex] == ')') and (charindex == len(temp) - 1):
                    dummy = temp[index + 1:charindex]
                    self.randomdata_list.insert(END, dummy)


    def adding_mail(self):
        # make adding mail form.

        self.clear_side()
        self.back_mail_data.grid(row=4, column=1)
        self.signin_username.grid(row=1, column=2)
        self.signin_pwd.grid(row=2, column=2)
        self.submit_add_mail.grid(row=3, column=2)
        self.space1stusr.grid(row=1, column=1)
        self.space1stpwd.grid(row=2, column=1)
        self.space2nd.grid(row=1, column=3)


    def mail_added(self, user, usrpwd):
        # this method will call the Formatting class
        # to format the emails data and then insert it to data base.
        
        mailstr = Formating.user_mails(user, usrpwd)
        
        # only if the string not equal to None.
        if mailstr != None:
            DataBases.data_inserting(mailstr,
                    'mail', self.current_user)
            self.tempvar = mailstr
            self.adding_mail()
        else:
            pass

    def adding_contact(self):
        # making the adding contact form.

        self.clear_side()
        self.back_contact_data.grid(row=4, column=1)
        self.contactnamefield.grid(row=1, column=2)
        self.contactpwdfield.grid(row=2, column=2)
        self.contactnamespace.grid(row=1, column=1)
        self.contactpwdspace.grid(row=2, column=1)
        self.space2nd.grid(row=1, column=3)
        self.submit_add_contact.grid(row=3, column=2)


    def contact_added(self, name, gsm):
        # this method will call the Formatting class
        # to format the contact data and then insert it to data base.

        contactstr = Formating.user_contact(name, gsm)
        
        # only if the string not equal to None.
        if contactstr != None:
            DataBases.data_inserting(contactstr,
                    'contact', self.current_user)
            self.tempvar = contactstr
            self.adding_contact()
        else:
            pass


    def adding_random_data(self):
        # making random data form.

        self.clear_side()
        self.back_random_data.grid(row=4, column=1)
        self.space2nd.grid(row=1, column=1)
        self.space2nd.grid(row=1, column=3)
        self.signin_username.grid(row=1, column=2)
        self.submit_add_random.grid(row=3, column=2)

    def random_added(self, data):
        # this method will call the Formatting class
        # to format the data and then insert it to data base.

        randomstring = Formating.user_data(data)
        # only if string != None.
        if randomstring != None:
            self.tempvar = randomstring
            self.adding_random_data()
        else:
            pass


    def quit(self):
        # destroy the window -> exit.
        root.destroy()


obj_princip = App()

# make the window unresizable. 
root.resizable(0, 0)

# keep looping.
root.mainloop()
