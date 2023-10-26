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
            estado = 'Início'
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
        processos_termino = list(self.collection.find({"estado": "Término"}))

        if len(processos_termino) == len(list(self.collection.find())):
            return

        processo_execucao = self.collection.find_one({"estado": "Execução"})

        if processo_execucao:
            proximo_estado = random.choice(["Pronto", "Término", "Espera"])
            processo_execucao['estado'] = proximo_estado
            self.update_document({'pid': processo_execucao['pid']}, {'$set': {'estado': proximo_estado}})
        
        processos_inicio = list(self.collection.find({"estado": "Início"}))
        
        if processos_inicio:
            for processo in processos_inicio:
                processo['estado'] = 'Pronto'
                self.update_document({'pid': processo['pid']}, {'$set': {'estado': 'Pronto'}})
        else:
            processo_pronto = self.collection.find_one({"estado": "Pronto"})

            if processo_pronto:
                processo_pronto['estado'] = 'Execução'
                self.update_document({'pid': processo_pronto['pid']}, {'$set': {'estado': 'Execução'}})
            else:
                processo_espera = self.collection.find_one({"estado": "Espera"})

                if processo_espera:
                    processo_espera['estado'] = 'Pronto'
                    self.update_document({'pid': processo_espera['pid']}, {'$set': {'estado': 'Pronto'}})

        processos = list(filter(lambda processo: processo["estado"] != "Término", self.collection.find()))

        num_processos_alterados = min(num_processos_alterados, len(processos))

        random.shuffle(processos)

        processos_para_alterar = processos[:num_processos_alterados]

        for processo in processos_para_alterar:

            if processo["estado"] == "Espera":
                proximo_estado = "Pronto"
            else:
                proximo_estado = random.choice(["Pronto", "Espera"])

            processo['estado'] = proximo_estado
            self.update_document({'pid': processo['pid']}, {'$set': {'estado': proximo_estado}})
        
        processo_execucao = self.collection.find_one({"estado": "Execução"})
        if not processo_execucao:
            processo_pronto = self.collection.find_one({"estado": "Pronto"})

            if processo_pronto:
                processo_pronto['estado'] = 'Execução'
                self.update_document({'pid': processo_pronto['pid']}, {'$set': {'estado': 'Execução'}})


        return


    def show_records(self):
        records = self.collection.find()
        return records