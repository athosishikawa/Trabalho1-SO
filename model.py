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
        self.lock = threading.Lock()  # Semáforo para proteger operações no MongoDB
        # Deleta todos os registros ao inicializar o modelo
        self.collection.delete_many({}) 


    def insert_document(self, document):
        # Insere um documento no banco de dados
        self.collection.insert_one(document)

    def find_documents(self, query=None):
        # Retorna uma lista de documentos do banco de dados
        return self.collection.find(query)

    def update_document(self, query, update):
        # Atualiza um documento no banco de dados
        with self.lock:
            self.collection.update_one(query, update)

    def delete_document(self, query):
        # Exclui um documento do banco de dados
        self.collection.delete_one(query)

    def cria_registros(self):
        for _ in range(5):
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

            # Insira o registro no banco de dados
            self.insert_document(registro)

    def mudar_estado(self):
        # Obtenha todos os processos em estado "Início"
        processos_inicio = list(self.collection.find({"estado": "Início"}))

        if processos_inicio:
            for processo in processos_inicio:
                processo['estado'] = 'Pronto'
                self.update_document({'pid': processo['pid']}, {'$set': {'estado': 'Pronto'}})
        else:
            # Obtenha o processo em estado "Execução"
            processo_execucao = self.collection.find_one({"estado": "Execução"})

            if processo_execucao:
                # Use random.choice para escolher aleatoriamente o próximo estado
                proximo_estado = random.choice(["Pronto", "Término", "Espera"])
                processo_execucao['estado'] = proximo_estado
                self.update_document({'pid': processo_execucao['pid']}, {'$set': {'estado': proximo_estado}})
            else:
                # Obtenha o processo em estado "Pronto"
                processo_pronto = self.collection.find_one({"estado": "Pronto"})

                if processo_pronto:
                    processo_pronto['estado'] = 'Execução'
                    self.update_document({'pid': processo_pronto['pid']}, {'$set': {'estado': 'Execução'}})
                else:
                    # Obtenha o processo em estado "Espera"
                    processo_espera = self.collection.find_one({"estado": "Espera"})

                    if processo_espera:
                        processo_espera['estado'] = 'Pronto'
                        self.update_document({'pid': processo_espera['pid']}, {'$set': {'estado': 'Pronto'}})

        return


    def show_records(self):
        records = self.collection.find()
        return records