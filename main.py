import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from model import Model
from kivy.clock import Clock


class CrudApp(App):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.layout_atual = self.build() 
        Window.size = (300, 600)

        
    

    def build(self):
        # Cria o layout da tela principal.
        self.layoutLogin = BoxLayout(orientation='vertical', spacing=10, padding=20)


        label_login = Label(text='LOGIN', size_hint=(1, 0.1), height=50)
        label_login.font_size = '24sp'  # Aumenta o tamanho da fonte

        # Cria um rótulo para o campo de e-mail.
        label_email = Label(text='E-mail:', size_hint=(1, 0.05), height=10)
        label_email.font_size = '20sp'

        # Cria um widget TextInput para o campo de e-mail.
        self.input_email = TextInput(font_size='18sp', size_hint=(1, None), height=30, multiline=False)

        # Cria um rótulo para o campo de senha.
        label_senha = Label(text='Senha:', size_hint=(1, 0.05), height=10)
        label_senha.font_size = '20sp'

        # Cria um widget TextInput para o campo de senha.
        self.input_senha = TextInput(size_hint=(1, None), height=30, multiline=False, password=True)

        # Cria um botão para fazer login.
        button_login = Button(text='Login', size_hint=(1, None), height=50)
        button_login.bind(on_press=self.login)
        self.message_label = Label(text="", size_hint=(1, 0.1), height=30, color=(1, 0, 0, 1), font_size='16sp')

        # Adiciona os widgets ao layout interno.
        self.layoutLogin.add_widget(label_login)
        self.layoutLogin.add_widget(label_email)
        self.layoutLogin.add_widget(self.input_email)
        self.layoutLogin.add_widget(label_senha)
        self.layoutLogin.add_widget(self.input_senha)
        self.layoutLogin.add_widget(button_login)
        self.layoutLogin.add_widget(self.message_label)

        # Define a imagem de fundo do layout.
        return self.layoutLogin




    def build2(self):
        # Define o tamanho da tela

        self.layout = BoxLayout(orientation='vertical')

        size = (1, 0.1)


        # Cria os rótulos
        label_titulo = Label(text='CRUD', size_hint=size)
        label_pid = Label(text='Nome do Processo (PID)', size_hint=size)
        label_uid = Label(text='Nome do Usuário (UID)', size_hint=size)
        label_prioridade = Label(text='Prioridade', size_hint=size)
        label_cpu = Label(text='Uso da CPU (%)', size_hint=size)
        label_estado = Label(text='Estado', size_hint=size)
        label_memoria = Label(text='Espaço de Memória (mb)', size_hint=size)
        self.message_label = Label(text="", size_hint=size, color=(1, 0, 0, 1))

        # Cria os campos de entrada
        self.pid_entry = TextInput(size_hint=size)
        self.uid_entry = TextInput(size_hint=size)
        self.prioridade_entry = TextInput(size_hint=size)
        self.cpu_entry = TextInput(size_hint=size)
        self.estado_entry = TextInput(size_hint=size)
        self.memoria_entry = TextInput(size_hint=size)  # Instancia um novo objeto TextInput

        # Cria os botões
        salvar_button = Button(text='Salvar', size_hint=size)
        #cancelar_button = Button(text='Cancelar', size_hint=size)
        consultar_button = Button(text='Consultar', size_hint=size)
        atualizar_button = Button(text='Atualizar', size_hint=size)
        deletar_button = Button(text='Deletar', size_hint=size)

        #Adiciona a função aos botões
        salvar_button.on_press = self.salvar

        consultar_button.on_press = self.consultar
        atualizar_button.on_press = self.atualizar
        deletar_button.on_press = self.deletar

        # Adiciona os rótulos e campos de entrada ao layout
        self.layout.add_widget(label_titulo)
        self.layout.add_widget(label_pid)
        self.layout.add_widget(self.pid_entry)
        self.layout.add_widget(label_uid)
        self.layout.add_widget(self.uid_entry)
        self.layout.add_widget(label_prioridade)
        self.layout.add_widget(self.prioridade_entry)
        self.layout.add_widget(label_cpu)
        self.layout.add_widget(self.cpu_entry)
        self.layout.add_widget(label_estado)
        self.layout.add_widget(self.estado_entry)
        self.layout.add_widget(label_memoria)
        self.layout.add_widget(self.memoria_entry)


        # Adiciona os botões ao layout
        self.layout.add_widget(salvar_button)
        self.layout.add_widget(consultar_button)
        self.layout.add_widget(atualizar_button)
        self.layout.add_widget(deletar_button)
        #self.layout.add_widget(cancelar_button)
        self.layout.add_widget(self.message_label)

        return self.layout

    def salvar(self):
        # Obtém os dados do usuário
        pid = self.pid_entry.text
        uid = self.uid_entry.text
        prioridade = self.prioridade_entry.text
        cpu = self.cpu_entry.text
        estado = self.estado_entry.text
        memoria = self.memoria_entry.text

        # Verifica se algum dos campos está vazio
        if not pid or not uid or not prioridade or not cpu or not estado or not memoria:
            self.mostrar_mensagem("Preencha todos os campos.")
            return
        
        # Cria um documento para salvar no banco de dados
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
            # Obtém o PID do processo a ser consultado
            pid = self.pid_entry.text

            # Verifica se o campo PID não está vazio
            if not pid:
                raise ValueError("Digite um PID para consultar.")

            # Consulta o documento no banco de dados
            documents = list(self.model.find_documents({"pid": pid}))

            if not documents:
                raise ValueError("Processo não encontrado.")

            # Atualiza os campos de entrada com os dados do primeiro documento encontrado
            document = documents[0]
            self.pid_entry.text = document["pid"]
            self.uid_entry.text = document["uid"]
            self.prioridade_entry.text = document["prioridade"]
            self.cpu_entry.text = document["cpu"]
            self.estado_entry.text = document["estado"]
            self.memoria_entry.text = document["memoria"]

        except ValueError as e:
            self.mostrar_mensagem(str(e))


    def atualizar(self):
        # Obtém os dados do usuário
        pid = self.pid_entry.text
        uid = self.uid_entry.text
        prioridade = self.prioridade_entry.text
        cpu = self.cpu_entry.text
        estado = self.estado_entry.text
        memoria = self.memoria_entry.text

        # Verifica se algum dos campos está vazio
        if not pid or not uid or not prioridade or not cpu or not estado or not memoria:
            self.mostrar_mensagem("Preencha todos os campos.")
            return

        # Cria um objeto query para atualizar o documento
        query = {"pid": pid}

        # Cria um objeto update para definir os novos valores do documento
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
        # Obtém o PID do processo a ser deletado
        pid = self.pid_entry.text

        # Verifica se o campo PID não está vazio
        if not pid:
            self.mostrar_mensagem("Digite um PID para deletar.")
            return

        # Deleta o documento no banco de dados
        self.model.delete_document({"pid": pid})

        self.limpar_campos()

        self.mostrar_mensagem("Processo deletado com sucesso!")

    def limpar_campos(self):
        self.pid_entry.text = ""
        self.uid_entry.text = ""
        self.prioridade_entry.text = ""
        self.cpu_entry.text = ""
        self.estado_entry.text = ""
        self.memoria_entry.text = ""


    def mostrar_mensagem(self, mensagem):
        # Atualiza o texto do widget Label para exibir a nova mensagem
        self.message_label.text = mensagem

        # Define um temporizador para limpar a mensagem após alguns segundos
        Clock.schedule_once(self.limpar_mensagem, 3)  # Limpa a mensagem após 3 segundos
    
    def limpar_mensagem(self, dt):
        # Limpa o texto do widget Label
        self.message_label.text = ""
    
    def login(self, button):
        # Obtém os valores dos campos de e-mail e senha.
        email = self.input_email.text
        senha = self.input_senha.text

        # Valida os valores dos campos.
        if email == '' or senha == '':
            self.mostrar_mensagem('Preencha todos os campos.')
            return

        # Faz a autenticação do usuário.
        # (Esse código é apenas um exemplo, você deve implementar seu próprio código de autenticação.)
        if email == 'admin' and senha == '123456':
            self.mostrar_mensagem('Login efetuado com sucesso!')
            self.layoutLogin.clear_widgets()

            # Defina o layout atual como o layout principal
            self.layout_atual = self.build2()

            # Adicione o layout atual ao aplicativo
            self.root.add_widget(self.layout_atual)
        else:
            self.mostrar_mensagem('E-mail ou senha inválidos.')
        

    def run(self):
        self.build()
        super().run()

if __name__ == '__main__':

    model = Model(db_name="my_database", collection_name="my_collection")
    crud_app = CrudApp(model)
    crud_app.run()
