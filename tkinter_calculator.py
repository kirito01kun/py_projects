import math
from tkinter import *
#importing the lib of tkinte
root = Tk()
root.title('Calculator')
root.configure(bg="#d6bdff")


class nums():
    def __init__(self, master):
        self.num1 = 0
        self.num2 = 0
        self.tmp = ''

        self.e = Entry(master, width=55, borderwidth=5, fg='#34558b', bg='#ffdce2')
        self.e.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        self.bu0 = Button(master, text='0', padx=50, pady=20, fg='#34558b', bg='#ffd6d6', command=lambda: self.Show_num('0'))
        self.bu1 = Button(master, text='1', padx=50, pady=20, fg='#34558b', bg='#ffd6d6', command=lambda: self.Show_num('1'))
        self.bu2 = Button(master, text='2', padx=50, pady=20, fg='#34558b', bg='#ffd6d6', command=lambda: self.Show_num('2'))
        self.bu3 = Button(master, text='3', padx=50, pady=20, fg='#34558b', bg='#ffd6d6', command=lambda: self.Show_num('3'))
        self.bu4 = Button(master, text='4', padx=50, pady=20, fg='#34558b', bg='#ffd6d6', command=lambda: self.Show_num('4'))
        self.bu5 = Button(master, text='5', padx=50, pady=20, fg='#34558b', bg='#ffd6d6', command=lambda: self.Show_num('5'))
        self.bu6 = Button(master, text='6', padx=50, pady=20, fg='#34558b', bg='#ffd6d6', command=lambda: self.Show_num('6'))
        self.bu7 = Button(master, text='7', padx=50, pady=20, fg='#34558b', bg='#ffd6d6', command=lambda: self.Show_num('7'))
        self.bu8 = Button(master, text='8', padx=50, pady=20, fg='#34558b', bg='#ffd6d6', command=lambda: self.Show_num('8'))
        self.bu9 = Button(master, text='9', padx=50, pady=20, fg='#34558b', bg='#ffd6d6', command=lambda: self.Show_num('9'))
        self.buplus = Button(master, text='+', padx=50, pady=20, fg='#34558b', bg='#ffd6d6', command=lambda: self.Add())
        self.buminus = Button(master, text='-', padx=50, pady=20, fg='#34558b', bg='#ffd6d6', command=lambda: self.Minus())
        self.bumulti = Button(master, text='x', padx=50, pady=20, fg='#34558b', bg='#ffd6d6', command=lambda: self.Multi())
        self.busub = Button(master, text='/', padx=50, pady=20, fg='#34558b', bg='#ffd6d6', command=lambda: self.Sub())
        self.bueq = Button(master, text='=', padx=50, pady=20, fg='#34558b', bg='#ffd6d6', command=lambda: self.Equalres())
        self.buclr = Button(master, text='C', padx=50, pady=20, fg='#34558b', bg='#ffd6d6', command=lambda: self.Clear())

        self.bu0.grid(row=4, column=0)
        self.bu1.grid(row=3, column=0)
        self.bu2.grid(row=3, column=1)
        self.bu3.grid(row=3, column=2)
        self.bu4.grid(row=2, column=0)
        self.bu5.grid(row=2, column=1)
        self.bu6.grid(row=2, column=2)
        self.bu7.grid(row=1, column=0)
        self.bu8.grid(row=1, column=1)
        self.bu9.grid(row=1, column=2)
        self.buplus.grid(row=1, column=3)
        self.buminus.grid(row=2, column=3)
        self.bumulti.grid(row=3, column=3)
        self.busub.grid(row=4, column=3)
        self.bueq.grid(row=4, column=2)
        self.buclr.grid(row=4, column=1)

    def Clear(self):
        self.e.delete(0, END)

    def Show_num(self, strnum):
        curr = self.e.get()
        self.Clear()
        self.e.insert(0, curr + strnum)

    def Add(self):
        self.num1 = float(self.e.get())
        self.tmp = '+'
        self.Clear()

    def Sub(self):
        self.num1 = float(self.e.get())
        self.tmp = '/'
        self.Clear()

    def Minus(self):
        self.num1 = float(self.e.get())
        self.tmp = '-'
        self.Clear()

    def Multi(self):
        self.num1 = float(self.e.get())
        self.tmp = '*'
        self.Clear()


    def Equalres(self):
        self.num2 = float(self.e.get())
        self.Clear()
        if self.tmp == '+':
            self.e.insert(0, str(self.num1 + self.num2))
        elif self.tmp == '-':
            self.e.insert(0, str(self.num1 - self.num2))
        elif self.tmp == '*':
            self.e.insert(0, str(self.num1 * self.num2))
        else:
            self.e.insert(0, str(self.num1 / self.num2))


obj = nums(root)
root.resizable(0, 0)

root.mainloop()
#keepruning
