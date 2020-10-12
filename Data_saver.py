import os
from tkinter import *
import time
import sqlite3

root = Tk()
root.title('Data Saver')
root.configure(bg="#424242")
copyright = Label(root, text='© 2020 Kbala Youssef', fg='#fafafa', bg='#424242')
connect = sqlite3.connect("Database.db")
cursor = connect.cursor()

#check if table already exeist
cursor.execute('''SELECT count(name) FROM sqlite_master where type='table' AND name='Logins' ''')


if cursor.fetchone()[0] == 1:
    pass
else:
    cursor.execute('''CREATE TABLE Logins (user TEXT,pwd TEXT,emails TEXT,contacts TEXT,data TEXT)''')

connect.commit()
connect.close()

class Data_bases():
    @staticmethod
    def Add_logins(user, pwd):
        params = (user, pwd)
        connect = sqlite3.connect("Database.db")
        cursor = connect.cursor()
        cursor.execute("INSERT INTO Logins(user,pwd) VALUES (?,?)", params)
        connect.commit()
        connect.close()

    @staticmethod
    def Existing_User_or_Not(user, pwd):
        connect = sqlite3.connect("Database.db")
        cursor = connect.cursor()
        cursor.execute("""SELECT user,pwd From Logins WHERE user=? AND pwd=?""", (user, pwd))
        if cursor.fetchone():
            res = True
        else:
            res = False
        connect.close()
        return res

    @staticmethod
    def Existing_Details_or_Not(user, pwd):
        connect = sqlite3.connect("Database.db")
        cursor = connect.cursor()
        cursor.execute("""SELECT user,pwd From Logins WHERE user=? OR pwd=?""", (user, pwd))
        if cursor.fetchone():
            res = True
        else:
            res = False
        connect.close()
        return res

    @staticmethod
    def Data_inserting(data, type, user):
        temp = ''
        connect = sqlite3.connect("Database.db")
        cursor = connect.cursor()
        if type == 'mail':
            cursor.execute("SELECT * FROM Logins")
            for row in cursor:
                if row[0] == user:
                    if row[2] != None:
                        temp = "{},{},".format(row[2], data)
                    else:
                        temp = data
            connect.close()
            connect = sqlite3.connect("Database.db")
            cursor = connect.cursor()
            cursor.execute('''UPDATE Logins SET "emails"=? WHERE user=?''', (temp, user))

        elif type == 'contact':
            cursor.execute("SELECT * FROM Logins")
            for row in cursor:
                if row[0] == user:
                    if row[3] != None:
                        temp = "{},{},".format(row[3], data)
                    else:
                        temp = data
            connect.close()
            connect = sqlite3.connect("Database.db")
            cursor = connect.cursor()
            cursor.execute('''UPDATE Logins SET "contacts"=? WHERE user=?''', (temp, user))

        else:
            cursor.execute("SELECT * FROM Logins")
            for row in cursor:
                if row[0] == user:
                    if row[4] != None:
                        temp = "{},{},".format(row[4], data)
                    else:
                        temp = data
            connect.close()
            connect = sqlite3.connect("Database.db")
            cursor = connect.cursor()
            cursor.execute('''UPDATE Logins SET "data"=? WHERE user=?''', (temp, user))
        connect.commit()
        connect.close()


Dataclass = Data_bases()

class Formating():
    def user_mails(email, pwd):
        if (email != '') and (pwd != ''):
            maillist = []
            mailstr = "Email: {} || Password: {}".format(email, pwd)
            maillist.append(mailstr)
            return mailstr
        else:
            pass
    def user_data(data):
        if data != '':
            datalist = []
            datastr = "<<{}>>".format(data)
            datalist.append(datastr)
            return datastr
        else:
            pass

    def user_contact(name, GSM):
        if (name != '') and (GSM != ''):
            contactlist = []
            contactstr = "Name: {} || Phone: {}".format(name, GSM)
            contactlist.append(contactstr)
            return contactstr
        else:
            pass

obj = Formating()

class App():

    def __init__(self):
        copyright.grid(row=4, column=0)
        self.current_user = ''
        self.signup_username = Entry(root, fg='#fafafa', bg='#424242', width=50)
        self.signup_pwd = Entry(root, show='*', fg='#fafafa', bg='#424242', width=50)
        self.signup_submit = Button(root, text="Sign up", bg='#424242', height=1, width=18, fg='#fafafa', command=lambda: self.add_member(self.signup_username.get(), self.signup_pwd.get()))
        self.signin_username = Entry(root, fg='#fafafa', bg='#424242', width=50)
        self.signin_pwd = Entry(root, show='*', fg='#fafafa', bg='#424242', width=50)
        self.signin_submit = Button(root, text="Log in", bg='#424242', height=1, width=18, fg='#fafafa', command=lambda: self.check_member(self.signin_username.get(), self.signin_pwd.get()))
        self.space1stusr = Label(root, text=' User name : ', fg='#fafafa', bg='#424242')
        self.space1stpwd = Label(root, text=' Password : ', fg='#fafafa', bg='#424242')
        self.space2nd = Label(root, text='             ', fg='#fafafa', bg='#424242')
        self.menu = Button(root, text="Menu", width=18, fg='#fafafa', bg='#424242', command=lambda: self.menu_click(), height=4)
        self.menu.grid(row=0, column=0)
        self.Sign_up = Button(root, text="Sign up", bg='#424242', height=4, width=18, fg='#fafafa', command=lambda: self.sign_up_form())
        self.Sign_in = Button(root, text="Log in", bg='#424242', height=4, width=18, fg='#fafafa', command=lambda: self.sign_in_form())
        self.Quit = Button(root, text="Quit", bg='#424242', width=18, height=4, fg='#fafafa', command=lambda: self.quit())
        self.exesting = Label(root, text="Already exesting email/password", bg='#424242', fg='#fafafa')
        self.success = Label(root, text="Success", bg='#424242', fg='#fafafa')
        self.login_error = Label(root, text="User name or password is incorrect!", bg='#424242', fg='#fafafa')
        self.scrollbar = Scrollbar(root, orient='vertical', bg='#424242')
        self.scrollbar1 = Scrollbar(root, orient='vertical', bg='#424242')
        self.scrollbar2 = Scrollbar(root, orient='vertical', bg='#424242')
        self.maildata_list = Listbox(root, height=12, width=90, bg='#424242', yscrollcommand=self.scrollbar.set, fg='#fafafa')
        self.contactdata_list = Listbox(root, height=12, width=90, bg='#424242', yscrollcommand=self.scrollbar.set, fg='#fafafa')
        self.randomdata_list = Listbox(root, height=12, width=90, bg='#424242', yscrollcommand=self.scrollbar.set, fg='#fafafa')
        self.scrollbar.config(command=self.maildata_list.yview)
        self.scrollbar1.config(command=self.contactdata_list.yview)
        self.pick = Label(root, text="Pick One :", fg='#fafafa', bg='#424242')
        self.scrollbar2.config(command=self.randomdata_list.yview)
        self.mail_button = Button(root, text="Email", width=22, fg='#fafafa',
                                  bg='#424242', height=4, command=lambda: self.data_list('mail'))
        self.contact_button = Button(root, text="Contact", width=22, fg='#fafafa',
                                     bg='#424242', height=4, command=lambda: self.data_list('contact'))
        self.randomdata_button = Button(root, text="Random Data", width=22, fg='#fafafa',
                                        bg='#424242', height=4, command=lambda: self.data_list('random'))
        self.add_mail_button = Button(root, text="Add E-mail", width=22, height=2,
                                      fg='#fafafa', bg='#424242', command=lambda: self.adding_mail())
        self.add_contact_button = Button(root, text="Add Contact", bg='#424242', height=2,
                                         width=15, fg='#fafafa', command=lambda: self.adding_contact())
        self.add_random_button = Button(root, text="Add Random data", bg='#424242', width=15,
                                        height=2, fg='#fafafa', command=lambda: self.adding_random_data())
        self.back_choice_data = Button(root, text="Back", bg='#424242', width=10,
                                        height=1, fg='#fafafa', command=lambda: self.choice_data())
        self.back_mail_data = Button(root, text="Back", bg='#424242', width=10,
                                       height=1, fg='#fafafa', command=lambda: self.data_list('mail'))
        self.back_contact_data = Button(root, text="Back", bg='#424242', width=10,
                                       height=1, fg='#fafafa', command=lambda: self.data_list('contact'))
        self.back_random_data = Button(root, text="Back", bg='#424242', width=10,
                                       height=1, fg='#fafafa', command=lambda: self.data_list('random'))
        self.submit_add_mail = Button(root, text="Add it", bg='#424242',
                                      height=1, width=15, fg='#fafafa', command=lambda: self.mail_added(self.signin_username.get(), self.signin_pwd.get()))
        self.submit_add_contact = Button(root, text="Add it", bg='#424242',
                                         height=1, width=15, fg='#fafafa', command=lambda: self.contact_added(self.contactnamefield.get(), self.contactpwdfield.get()))
        self.submit_add_random = Button(root, text="Add it", bg='#424242', height=1,
                                        width=15, fg='#fafafa', command=lambda: self.random_added(self.signin_username.get()))

        self.contactnamespace = Label(root, text=' Name : ', fg='#fafafa', bg='#424242')
        self.contactpwdspace = Label(root, text=' Phone : ', fg='#fafafa', bg='#424242')
        self.contactnamefield = Entry(root, fg='#fafafa', bg='#424242', width=50)
        self.contactpwdfield = Entry(root, fg='#fafafa', bg='#424242', width=50)
        self.tempvar = ''

    def clear_side(self):
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

    def menu_click(self):
        self.Sign_up.grid(row=1, column=0)
        self.Sign_in.grid(row=2, column=0)
        self.Quit.grid(row=3, column=0)

    def sign_up_form(self):
        self.clear_side()
        self.signup_username.grid(row=1, column=2)
        self.signup_pwd.grid(row=2,column=2)
        self.signup_submit.grid(row=3, column=2)
        self.space1stusr.grid(row=1, column=1)
        self.space1stpwd.grid(row=2, column=1)
        self.space2nd.grid(row=1, column=3)

    def sign_in_form(self):
        self.clear_side()
        self.signin_username.grid(row=1, column=2)
        self.signin_pwd.grid(row=2, column=2)
        self.signin_submit.grid(row=3, column=2)
        self.space1stusr.grid(row=1, column=1)
        self.space1stpwd.grid(row=2, column=1)
        self.space2nd.grid(row=1, column=3)

    def add_member(self, key, value):
        self.signup_username.delete(0, END)
        self.signup_pwd.delete(0, END)
        if Dataclass.Existing_Details_or_Not(key, value):
            self.exesting.grid(row=4, column=2)
            self.exesting.after(2000, lambda: self.exesting.grid_forget())
        else:
            Dataclass.Add_logins(key, value)
            self.success.grid(row=4, column=2)
            self.success.after(2000, lambda: self.success.grid_forget())
        
    def check_member(self, key, value):
        self.signin_username.delete(0, END)
        self.signin_pwd.delete(0, END)
        if Dataclass.Existing_User_or_Not(key, value):
            self.choice_data()
            self.current_user = key
        else:
            self.login_error.grid(row=4, column=2)
            self.login_error.after(2500, lambda: self.login_error.grid_forget())

    def choice_data(self):
        self.clear_side()
        self.pick.grid(row=0, column=1, columnspan=2)
        self.mail_button.grid(row=1, column=1, columnspan=2)
        self.contact_button.grid(row=2, column=1)
        self.randomdata_button.grid(row=2, column=2)

    def data_list(self, type):
        self.maildata_list.delete(0, END)
        self.contactdata_list.delete(0, END)
        self.randomdata_list.delete(0, END)
        self.clear_side()
        if type == 'mail':
            self.add_mail_button.grid(row=0, column=1, columnspan=2)
            self.maildata_list.grid(row=1, column=1, rowspan=3)
            self.scrollbar.grid(row=1, column=2, rowspan=3, sticky='ns')
            self.back_choice_data.grid(row=4, column=1)
            temp = ''
            connect = sqlite3.connect("Database.db")
            cursor = connect.cursor()
            cursor.execute("SELECT * FROM Logins")
            for row in cursor:
                if row[0] == self.current_user:
                    if row[2] != None:
                        temp = row[2]
            connect.close()
            index = 0
            for charindex in range(len(temp)):
                if temp[charindex] == ',':
                    dummy = temp[index:charindex]
                    index = charindex + 1
                    self.maildata_list.insert(END, dummy)

        elif type == 'contact':
            self.add_contact_button.grid(row=0, column=1, columnspan=2)
            self.contactdata_list.grid(row=1, column=1, rowspan=3)
            self.scrollbar1.grid(row=1, column=2, rowspan=3, sticky='ns')
            self.back_choice_data.grid(row=4, column=1)
            temp = ''
            connect = sqlite3.connect("Database.db")
            cursor = connect.cursor()
            cursor.execute("SELECT * FROM Logins")
            for row in cursor:
                if row[0] == self.current_user:
                    if row[3] != None:
                        temp = row[3]
            connect.close()
            index = 0
            for charindex in range(len(temp)):
                if temp[charindex] == ',':
                    dummy = temp[index:charindex]
                    index = charindex + 1
                    if (dummy != ''):
                        self.contactdata_list.insert(END, dummy)
                    else:
                        pass

        else:
            self.add_random_button.grid(row=0, column=1, columnspan=2)
            self.randomdata_list.grid(row=1, column=1, rowspan=3)
            self.scrollbar2.grid(row=1, column=2, rowspan=3, sticky='ns')
            self.back_choice_data.grid(row=4, column=1)
            temp = ''
            connect = sqlite3.connect("Database.db")
            cursor = connect.cursor()
            cursor.execute("SELECT * FROM Logins")
            for row in cursor:
                if row[0] == self.current_user:
                    if row[4] != None:
                        temp = row[4]
            connect.close()
            index = 0
            for charindex in range(len(temp)):
                if temp[charindex] == ',':
                    dummy = temp[index:charindex]
                    index = charindex + 1
                    if (dummy != ''):
                        self.randomdata_list.insert(0, dummy)
                    else:
                        pass

    def adding_mail(self):
        self.clear_side()
        self.back_mail_data.grid(row=4, column=1)
        self.signin_username.grid(row=1, column=2)
        self.success.grid(row=4, column=2, columnspan=2)
        self.success.after(2000, lambda: self.success.grid_forget())
        self.signin_pwd.grid(row=2, column=2)
        self.submit_add_mail.grid(row=3, column=2)
        self.space1stusr.grid(row=1, column=1)
        self.space1stpwd.grid(row=2, column=1)
        self.space2nd.grid(row=1, column=3)

    def mail_added(self, user, usrpwd):
        mailstr = Formating.user_mails(user, usrpwd)
        if mailstr != None:
            Dataclass.Data_inserting(mailstr, 'mail', self.current_user)
            self.tempvar = mailstr
            self.adding_mail()
        else:
            pass

    def adding_contact(self):
        self.clear_side()
        self.success.grid(row=4, column=2)
        self.success.after(2000, lambda: self.success.grid_forget())
        self.back_contact_data.grid(row=4, column=1)
        self.contactnamefield.grid(row=1, column=2)
        self.contactpwdfield.grid(row=2, column=2)
        self.contactnamespace.grid(row=1, column=1)
        self.contactpwdspace.grid(row=2, column=1)
        self.space2nd.grid(row=1, column=3)
        self.submit_add_contact.grid(row=3, column=2)


    def contact_added(self, name, gsm):
        contactstr = Formating.user_contact(name, gsm)
        if contactstr != None:
            Dataclass.Data_inserting(contactstr, 'contact', self.current_user)
            self.tempvar = contactstr
            self.adding_contact()
        else:
            pass

    def adding_random_data(self):
        self.clear_side()
        self.success.grid(row=4, column=2)
        self.success.after(2000, lambda: self.success.grid_forget())
        self.back_random_data.grid(row=4, column=1)
        self.space2nd.grid(row=1, column=1)
        self.space2nd.grid(row=1, column=3)
        self.signin_username.grid(row=1, column=2)
        self.submit_add_random.grid(row=3, column=2)

    def random_added(self, data):
        randomstring = Formating.user_data(data)
        if randomstring != Nnone:
            Dataclass.Data_inserting(randomstring, 'data', self.current_user)
            self.tempvar = randomstring
            self.adding_random_data()
        else:
            pass

    def quit(self):
        print(self.data_list)
        root.destroy()


obj_princip = App()
root.resizable(0, 0)

root.mainloop()