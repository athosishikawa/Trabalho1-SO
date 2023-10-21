import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from model import Model
from kivy.clock import Clock
from kivy.uix.spinner import Spinner
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
import threading



class App(App):
    def __init__(self):
        super().__init__()
        self.model = None
        self.layout_atual = self.build() 
        Window.size = (300, 600)
        self.process_update_event = None
    

    def build(self):
        self.model = Model(db_name="my_database", collection_name="my_collection")

        self.layoutLogin = BoxLayout(orientation='vertical', spacing=10, padding=20)


        label_login = Label(text='LOGIN', size_hint=(1, 0.1), height=50)
        label_login.font_size = '24sp'  

        label_email = Label(text='E-mail:', size_hint=(1, 0.05), height=10)
        label_email.font_size = '20sp'
        self.input_email = TextInput(font_size='18sp', size_hint=(1, None), height=30, multiline=False)

        label_senha = Label(text='Senha:', size_hint=(1, 0.05), height=10)
        label_senha.font_size = '20sp'
        self.input_senha = TextInput(size_hint=(1, None), height=30, multiline=False, password=True)

        button_login = Button(text='Login', size_hint=(1, None), height=50)
        button_login.bind(on_press=self.login)
        self.message_label = Label(text="", size_hint=(1, 0.1), height=30, color=(1, 0, 0, 1), font_size='16sp')

        self.layoutLogin.add_widget(label_login)
        self.layoutLogin.add_widget(label_email)
        self.layoutLogin.add_widget(self.input_email)
        self.layoutLogin.add_widget(label_senha)
        self.layoutLogin.add_widget(self.input_senha)
        self.layoutLogin.add_widget(button_login)
        self.layoutLogin.add_widget(self.message_label)

        return self.layoutLogin



    def build2(self):
        self.layout = BoxLayout(orientation='vertical')

        size = (1, 0.1)


        label_titulo = Label(text='CRUD', size_hint=size)
        label_pid = Label(text='Nome do Processo (PID)', size_hint=size)
        label_uid = Label(text='Nome do Usuário (UID)', size_hint=size)
        label_prioridade = Label(text='Prioridade', size_hint=size)
        label_cpu = Label(text='Uso da CPU (%)', size_hint=size)
        label_estado = Label(text='Estado', size_hint=size)
        label_memoria = Label(text='Espaço de Memória (mb)', size_hint=size)
        self.message_label = Label(text="", size_hint=size, color=(1, 0, 0, 1))

        self.pid_entry = TextInput(size_hint=size)
        self.uid_entry = TextInput(size_hint=size)
        self.prioridade_spinner = Spinner(
            text='Selecione a prioridade',
            size_hint=size,
            values=('Alta', 'Média', 'Baixa')
        )
        self.cpu_entry = TextInput(size_hint=size)
        self.estado_spinner = Spinner(
            text='Selecione o estado',
            size_hint=size,
            values=('Pronto', 'Execução', 'Espera')
        )
        self.memoria_entry = TextInput(size_hint=size)  

        # Botões
        salvar_button = Button(text='Salvar', size_hint=size)
        consultar_button = Button(text='Consultar', size_hint=size)
        atualizar_button = Button(text='Atualizar', size_hint=size)
        deletar_button = Button(text='Deletar', size_hint=size)
        processos_button = Button(text='Processos', size_hint=size)

        salvar_button.on_press = self.salvar

        consultar_button.on_press = self.consultar
        atualizar_button.on_press = self.atualizar
        deletar_button.on_press = self.deletar
        processos_button.on_press = self.build3

        self.layout.add_widget(label_titulo)
        self.layout.add_widget(label_pid)
        self.layout.add_widget(self.pid_entry)
        self.layout.add_widget(label_uid)
        self.layout.add_widget(self.uid_entry)
        self.layout.add_widget(label_prioridade)
        self.layout.add_widget(self.prioridade_spinner)
        self.layout.add_widget(label_cpu)
        self.layout.add_widget(self.cpu_entry)
        self.layout.add_widget(label_estado)
        self.layout.add_widget(self.estado_spinner)
        self.layout.add_widget(label_memoria)
        self.layout.add_widget(self.memoria_entry)


        self.layout.add_widget(salvar_button)
        self.layout.add_widget(consultar_button)
        self.layout.add_widget(atualizar_button)
        self.layout.add_widget(deletar_button)
        self.layout.add_widget(processos_button)
        self.layout.add_widget(self.message_label)

        return self.layout

    def salvar(self):
        pid = self.pid_entry.text
        uid = self.uid_entry.text
        prioridade = self.prioridade_spinner.text
        cpu = self.cpu_entry.text
        estado = self.estado_spinner.text
        memoria = self.memoria_entry.text

        if not pid or not uid or not prioridade or not cpu or not estado or not memoria:
            self.mostrar_mensagem("Preencha todos os campos.")
            return
        
        document = {
            "pid": pid,
            "uid": uid,
            "prioridade": prioridade,
            "cpu": cpu,
            "estado": estado,
            "memoria": memoria,
        }

        # Salva o documento no banco de dados
        self.model.insert_document(document)

        self.limpar_campos()

        self.mostrar_mensagem("Processo salvo com sucesso!")


    def consultar(self):
        try:
            pid = self.pid_entry.text

            if not pid:
                raise ValueError("Digite um PID para consultar.")

            documents = list(self.model.find_documents({"pid": pid}))

            if not documents:
                raise ValueError("Processo não encontrado.")

            document = documents[0]
            self.pid_entry.text = document["pid"]
            self.uid_entry.text = document["uid"]
            self.prioridade_spinner.text = document["prioridade"]
            self.cpu_entry.text = document["cpu"]
            self.estado_spinner.text = document["estado"]
            self.memoria_entry.text = document["memoria"]

        except ValueError as e:
            self.mostrar_mensagem(str(e))


    def atualizar(self):
        #Ddados do usuário
        pid = self.pid_entry.text
        uid = self.uid_entry.text
        prioridade = self.prioridade_spinner.text
        cpu = self.cpu_entry.text
        estado = self.estado_spinner.text
        memoria = self.memoria_entry.text

        if not pid or not uid or not prioridade or not cpu or not estado or not memoria:
            self.mostrar_mensagem("Preencha todos os campos.")
            return

        query = {"pid": pid}

        update = {
            "$set": {
                "pid": pid,
                "uid": uid,
                "prioridade": prioridade,
                "cpu": cpu,
                "estado": estado,
                "memoria": memoria,
            }
        }

        # Atualiza o documento no banco de dados
        self.model.update_document(query, update)

        self.limpar_campos()

        self.mostrar_mensagem("Processo atualizado com sucesso!")


    def deletar(self):
        pid = self.pid_entry.text

        if not pid:
            self.mostrar_mensagem("Digite um PID para deletar.")
            return

        self.model.delete_document({"pid": pid})

        self.limpar_campos()

        self.mostrar_mensagem("Processo deletado com sucesso!")

    def limpar_campos(self):
        self.pid_entry.text = ""
        self.uid_entry.text = ""
        self.prioridade_spinner.text = ""
        self.cpu_entry.text = ""
        self.estado_spinner.text = ""
        self.memoria_entry.text = ""


    def mostrar_mensagem(self, mensagem):
        self.message_label.text = mensagem
        Clock.schedule_once(self.limpar_mensagem, 3)  
    
    def limpar_mensagem(self, dt):
        self.message_label.text = ""
    
    def login(self, button):
        email = self.input_email.text
        senha = self.input_senha.text

        if email == '' or senha == '':
            self.mostrar_mensagem('Preencha todos os campos.')
            return

        # Faz a autenticação do usuário.
        if email == 'admin' and senha == '123456':
            self.mostrar_mensagem('Login efetuado com sucesso!')
            self.layoutLogin.clear_widgets()

            self.layout_atual = self.build2()
            self.root.add_widget(self.layout_atual)
        else:
            self.mostrar_mensagem('E-mail ou senha inválidos.')

    def show_records(self):


        self.layout.clear_widgets()
        self.layout_atual = self.buildProcessos()
        self.root.add_widget(self.layout_atual)

    def build3(self):
        self.model.cria_registros()
        Window.size = (1200, 700)

        self.layoutProcessos2 = BoxLayout(orientation='vertical')

        # Recupere os registros do banco de dados
        records = self.model.show_records()
        
        # Crie uma lista de Labels para exibir os registros
        processo_labels = []
            
        for record in records:
            processo_label = Label(text=f'PID: {record["pid"]}, UID: {record["uid"]}, Prioridade: {record["prioridade"]}, '
                                        f'CPU: {record["cpu"]}, Estado: {record["estado"]}, Memória: {record["memoria"]}')
            processo_labels.append(processo_label)  # Adicione o Label do processo à lista

        for processo_label in processo_labels:
            self.layoutProcessos2.add_widget(processo_label)  # Adicione os Labels ao layout vertical

        if not self.process_update_event:
            self.process_update_event = Clock.schedule_interval(self.update_process_states, 2)




        self.layout.clear_widgets()
        self.layout_atual = self.layoutProcessos2
        self.root.add_widget(self.layout_atual)

        return self.layoutProcessos2
    
    def update_process_states(self, dt):
        # Verifica se a execução anterior da função ainda está em andamento
        if not getattr(self, 'updating_process_states', False):
            # Inicia a atualização em um thread separado
            self.updating_process_states = True
            threading.Thread(target=self.update_process_states_thread).start()

    def update_process_states_thread(self):
        try:
            self.model.mudar_estado()
            # Após atualizar o estado dos processos, atualize os textos dos Labels
            records = self.model.show_records()
            for i, processo_label in enumerate(self.layoutProcessos2.children):
                processo_label.text = f'PID: {records[i]["pid"]}, UID: {records[i]["uid"]}, ' \
                                    f'Prioridade: {records[i]["prioridade"]}, ' \
                                    f'CPU: {records[i]["cpu"]}, ' \
                                    f'Estado: {records[i]["estado"]}, ' \
                                    f'Memória: {records[i]["memoria"]}'
        finally:
            # Marca que a atualização terminou
            self.updating_process_states = False
    
    def atualizar_labels(self):
        records = self.model.show_records()
        for label in self.layoutProcessos2.children:
            if label.text == 'Estado':
                try:
                    pid = int(label.id)
                    if pid <= len(records):
                        label.text = records[pid - 1]['estado']
                except ValueError:
                    pass
                except IndexError:
                    pass    


    # def buildProcessos(self):
    #     self.layoutProcessos = BoxLayout(orientation='horizontal')
    #     Window.size = (1200, 700)

    #     records = self.model.show_records()
    #     column_titles = ["ID", "PID", "UID", "PRIORIDADE", "CPU", "ESTADO", "MEMÓRIA"]  

    #     grid_layout = GridLayout(cols=len(column_titles), spacing=(0, 5))  

    #     for title in column_titles:
    #         grid_layout.add_widget(Label(text=title, bold=True))

    #     for record in records:
    #         for field in record.keys():
    #             grid_layout.add_widget(Label(text=str(record[field])))

    #     scroll_view = ScrollView()
    #     scroll_view.add_widget(grid_layout)

    #     self.layoutProcessos.add_widget(scroll_view)

    #     return self.layoutProcessos

    def run(self):
        self.build()
        super().run()

    def on_stop(self):
        if self.process_update_event:
            self.process_update_event.cancel()

        if self.model:
            # Certifique-se de liberar a conexão do MongoDB
            self.model.client.close()

if __name__ == '__main__':

    crud_app = App()
    crud_app.run()