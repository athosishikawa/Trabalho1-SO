
import sys
import tkinter as tk
from tkinter import ttk


class View():
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("480x820")
        self.root.configure(bg="white")

        self.container = tk.Frame(relief=tk.RAISED, 
                                  borderwidth=1, 
                                  bg="white")
        self.container.pack(fill=tk.BOTH, 
                            expand=True)

        self.createFrame1()
        self.frame1.grid(row=0, column=0, sticky='nsew')
        self.showFrame1()

        self.root.bind('<Escape>', self.close)


        self.root.mainloop()

    def close(self, evento=None):
        sys.exit()

    def showFrame1(self):
        self.frame1.tkraise()

    def createFrame1(self):
        self.frame1 = tk.Frame(self.container, 
                               relief=tk.RAISED, 
                               bg="white",
                               borderwidth=0)
        self.frame1.grid(row=0, 
                         column=0, 
                         padx=20,
                         pady=10,
                         sticky='nsew')
    
        # Título
        label = tk.Label(self.frame1, 
                          text='TELA DE LOGIN', 
                          font=('Arial', 26), 
                          foreground="#359830",
                          background="white",
                          anchor='center')
        label.grid(row=0, 
                   column=0, 
                   sticky='nsew',
                   pady=20)
        
        labelLogin = tk.Label(self.frame1, 
                          text='Login:', 
                          font=('Arial', 12), 
                          foreground="#359830",
                          background="white",
                          anchor='center')
        
        labelLogin.grid(row=1, 
                   column=0, 
                   sticky='nsew',
                   pady=20)
        
        entryLogin = tk.Entry(self.frame1)
        entryLogin.grid(row=2,
                        column=0,
                        sticky='nsew',
                        pady=20)
        
        labelSenha = tk.Label(self.frame1, 
                          text='Senha:', 
                          font=('Arial', 12), 
                          foreground="#359830",
                          background="white",
                          anchor='center')
        
        labelSenha.grid(row=3, 
                   column=0, 
                   sticky='nsew',
                   pady=20)
        
        entrySenha = tk.Entry(self.frame1, show = "*")
        entrySenha.grid(row=4,
                        column=0,
                        sticky='nsew',
                        pady=20)
        
        button = tk.Button(self.frame1, text="Login")
        button.grid(row=5,
                    column=0,
                    sticky='nsew',
                    pady=20)


View()
