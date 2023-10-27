import pymongo
import random
import threading
import time

class Model:
    def __init__(self, db_name, collection_name):
        # Conecta-se ao banco de dados MongoDB
        self.client = pymongo.MongoClient("mongodb://localhost:27017")
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
        self.lock = threading.Lock()  
        self.collection.delete_many({}) 
        self.max_active_processes = 10

    def insert_document(self, document):
        self.collection.insert_one(document)

    def find_documents(self, query=None):
        return self.collection.find(query)

    def update_document(self, query, update):
        with self.lock:
            self.collection.update_one(query, update)

    def delete_document(self, query):
        self.collection.delete_one(query)

    def cria_registros(self):
        # Conta o número de processos ativos
        active_count = self.collection.count_documents({"estado": {"$ne": "Término"}})

        if active_count < self.max_active_processes:
            pid = random.randint(1, 100)
            uid = random.randint(1, 100)
            prioridade = random.choice(['Alta', 'Média', 'Baixa'])
            cpu = random.randint(1, 100)
            estado = 'Início'  # Certifique-se de que o estado inicial seja 'Início'
            memoria = random.randint(1, 100)

            registro = {
                'pid': pid,
                'uid': uid,
                'prioridade': prioridade,
                'cpu': cpu,
                'estado': estado,
                'memoria': memoria,
            }

            self.insert_document(registro)


    def mudar_estado(self, num_processos_alterados=2):
    
        processos_execucao = list(self.collection.find({"estado": "Execução"}))
        processos_pronto = list(self.collection.find({"estado": "Pronto"}))
        processos_espera = list(self.collection.find({"estado": "Espera"}))
        processos_inicio = list(self.collection.find({"estado": "Início"}))

        if not processos_execucao and processos_pronto:
            # Se não houver processos em execução e houver processos prontos, inicie um em execução.
            processo_execucao = random.choice(processos_pronto)
            processo_execucao['estado'] = 'Execução'
            self.update_document({'pid': processo_execucao['pid']}, {'$set': {'estado': 'Execução'}})

        for processo in processos_execucao:
            proximo_estado = random.choice(["Pronto", "Espera", "Término"])
            processo['estado'] = proximo_estado
            self.update_document({'pid': processo['pid']}, {'$set': {'estado': proximo_estado}})

        if processos_inicio:
            for processo in processos_inicio:
                proximo_estado = 'Pronto'
                processo['estado'] = proximo_estado
                self.update_document({'pid': processo['pid']}, {'$set': {'estado': proximo_estado}})
        else:
            # Se não houver processos em Início, você pode fazer outra ação apropriada aqui.
            pass

        for processo in processos_espera:
            proximo_estado = "Pronto"
            processo['estado'] = proximo_estado
            self.update_document({'pid': processo['pid']}, {'$set': {'estado': proximo_estado}})


    def show_records(self):
    
        records = self.collection.find()
        return records