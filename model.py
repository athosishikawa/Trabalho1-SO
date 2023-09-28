import pymongo


class Model:
    def __init__(self, db_name, collection_name):
        # Conecta-se ao banco de dados MongoDB
        self.client = pymongo.MongoClient("mongodb://localhost:27017")
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def insert_document(self, document):
        # Insere um documento no banco de dados
        self.collection.insert_one(document)

    def find_documents(self, query=None):
        # Retorna uma lista de documentos do banco de dados
        return self.collection.find(query)

    def update_document(self, query, update):
        # Atualiza um documento no banco de dados
        self.collection.update_one(query, update)

    def delete_document(self, query):
        # Exclui um documento do banco de dados
        self.collection.delete_one(query)

