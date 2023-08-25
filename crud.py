import sys
import tkinter as tk
import mysql.connector
from banco import Banco


class Crud():
    # Constantes para as prioridades
    PRIORIDADE_ALTA = "Alta"
    PRIORIDADE_MÉDIA = "Média"
    PRIORIDADE_COMUM = "Comum"

    # Constantes para os estados
    ESTADO_PRONTO = "Pronto"
    ESTADO_EXECUÇÃO = "Execução"
    ESTADO_ESPERA = "Espera"
    
    def __init__(self, banco):
        
        self.banco = banco

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
    
        # LABELS
        labelTitulo = tk.Label(self.frame1, 
                          text='CRUD', 
                          font=('Arial', 26), 
                          foreground="#359830",
                          background="white",
                          anchor='center')
        labelProcesso = tk.Label(self.frame1, 
                          text='Nome do Processo (PID):', 
                          font=('Arial', 12), 
                          foreground="#359830",
                          background="white",
                          anchor='center')
        labelUsuario = tk.Label(self.frame1, 
                          text='Nome do Usuário(UID):', 
                          font=('Arial', 12), 
                          foreground="#359830",
                          background="white",
                          anchor='center')
        labelPrioridade = tk.Label(self.frame1, 
                          text='Prioridade:', 
                          font=('Arial', 12), 
                          foreground="#359830",
                          background="white",
                          anchor='center')
        labelCPU = tk.Label(self.frame1, 
                          text='Uso da CPU (%):', 
                          font=('Arial', 12), 
                          foreground="#359830",
                          background="white",
                          anchor='center')
        labelEstado = tk.Label(self.frame1, 
                          text='Estado:', 
                          font=('Arial', 12), 
                          foreground="#359830",
                          background="white",
                          anchor='center')
        labelMemoria = tk.Label(self.frame1, 
                          text='Espaço de Memória (mb):', 
                          font=('Arial', 12), 
                          foreground="#359830",
                          background="white",
                          anchor='center')

        #Posiciona as Labels
        labelTitulo.grid(row=0, column=0, sticky='nsew', pady=5)
        labelProcesso.grid(row=1, column=0, sticky='nsew', pady=5)
        labelUsuario.grid(row=3, column=0, sticky='nsew', pady=5)
        labelPrioridade.grid(row=5, column=0, sticky='nsew', pady=5)
        labelCPU.grid(row=7, column=0, sticky='nsew', pady=5)
        labelEstado.grid(row=9, column=0, sticky='nsew', pady=5)
        labelMemoria.grid(row=11, column=0, sticky='nsew', pady=5)

        self.prioridade_var = tk.StringVar(self.frame1)
        self.prioridade_var.set("Prioridade")  # Define a opção padrão
        self.estado_var = tk.StringVar(self.frame1)
        self.estado_var.set("Estado")  # Define a opção padrão

        # Cria os campos de entrada
        self.pid_entry = tk.Entry(self.frame1)
        self.uid_entry = tk.Entry(self.frame1)
        self.prioridade_entry = tk.OptionMenu(self.frame1, self.prioridade_var, self.PRIORIDADE_ALTA, self.PRIORIDADE_MÉDIA, self.PRIORIDADE_COMUM)
        self.cpu_entry = tk.Entry(self.frame1)
        self.estado_entry = tk.OptionMenu(self.frame1, self.estado_var, self.ESTADO_PRONTO, self.ESTADO_EXECUÇÃO, self.ESTADO_ESPERA)
        self.memoria_entry = tk.Entry(self.frame1)


        #Posiciona as entrys
        self.pid_entry.grid(row=2, column=0, sticky='nsew', pady=5)
        self.uid_entry.grid(row=4, column=0, sticky='nsew', pady=5)
        self.prioridade_entry.grid(row=6, column=0, sticky='nsew', pady=5)
        self.cpu_entry.grid(row=8, column=0, sticky='nsew', pady=5)
        self.estado_entry.grid(row=10, column=0, sticky='nsew', pady=5)
        self.memoria_entry.grid(row=12, column=0, sticky='nsew', pady=5)

        # Cria os botões
        salvar_button = tk.Button(self.frame1, text="Salvar")
        cancelar_button = tk.Button(self.frame1, text="Cancelar")
        consultar_button = tk.Button(self.frame1, text="Consultar")
        atualizar_button = tk.Button(self.frame1, text="Atualizar")
        deletar_button = tk.Button(self.frame1, text="Deletar")

        # Adiciona os botões à janela principal
        salvar_button.grid(row=13, column=0, sticky='nsew',
                        pady=5)
        consultar_button.grid(row=14, column=0, sticky='nsew',
                        pady=5)
        atualizar_button.grid(row=15, column=0, sticky='nsew',
                        pady=5)
        deletar_button.grid(row=16, column=0, sticky='nsew',
                        pady=5)
        cancelar_button.grid(row=17, column=0, sticky='nsew',
                        pady=5)


        # Associa as funções aos botões
        salvar_button.config(command= lambda: self.banco.salvar(self.pid_entry.get(), self.uid_entry.get(), self.prioridade_var, self.cpu_entry.get(), self.estado_var, self.memoria_entry.get()))
        consultar_button.config(command= lambda: self.consultar())
        atualizar_button.config(command= lambda: self.atualizar())
        deletar_button.config(command= lambda: self.deletar())

        
        cancelar_button.config(command= self.cancelar)




    def consultar(self):
        # Obtém o PID do processo a ser consultado
        pid = self.pid_entry.get()

        # Consulta o processo no banco de dados
        processo = self.banco.consultar(pid)

        
        # Exibe os dados do processo
        print("PID:", str(processo[0][0]))
        print("UID:", str(processo[0][1]))
        print("Prioridade:", str(processo[0][2]))
        print("CPU:", str(processo[0][3]))
        print("Estado:", str(processo[0][4]))
        print("Memória:", str(processo[0][5]))

        # Cria um Listbox para exibir os dados do processo
        listbox = tk.Listbox(self.frame1, height=5, width=20)

        # Adiciona os dados do processo ao Listbox
        for item in processo:
            listbox.insert(tk.END, item)

        # Posiciona o Listbox na tela
        listbox.grid(row=18, column=0, sticky='nsew', pady=5)

    def atualizar(self):
        processo = self.banco.atualizar(self.pid_entry.get(), self.uid_entry.get(), self.prioridade_var, self.cpu_entry.get(), self.estado_var, self.memoria_entry.get())

        if processo:
                # Cria um Label para exibir os dados do processo
            label = tk.Label(self.frame1, text="Atualizado com Sucesso")
        else:
            label = tk.Label(self.frame1, text="Não Atualizado")
        # Posiciona o Label na tela
        label.grid(row=19, column=0, sticky='nsew', pady=5)

    def deletar(self):

        pid = self.pid_entry.get()
        processo = self.banco.deletar(pid)

        if processo:
                # Cria um Label para exibir os dados do processo
            label = tk.Label(self.frame1, text="Deletado com Sucesso")
        else:
            label = tk.Label(self.frame1, text="Não Deletado")
        # Posiciona o Label na tela
        label.grid(row=19, column=0, sticky='nsew', pady=5)




    def cancelar(self):
        self.root.destroy()


banco = Banco()
Crud(banco)