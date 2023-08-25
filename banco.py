import mysql.connector
import tkinter as tk


class Banco():
    pass

    def __init__(self):
        # Conecta com o banco de dados
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="rootAthos,",
            database="crud",
        )

        # Define o comportamento dos botões
    def salvar(self, pid_entry, uid_entry, prioridade_entry, cpu_entry, estado_entry, memoria_entry):
        # Obtém os valores dos campos de entrada

        prioridade = str(prioridade_entry)

        estado = str(estado_entry)

        # Imprime os valores dos campos de entrada
        print("PID:", pid_entry)
        print("UID:", uid_entry)
        print("Prioridade:", prioridade)
        print("CPU:", cpu_entry)
        print("Estado:", estado)
        print("Memória:", memoria_entry)



        # Prepara a instrução SQL
        cursor = self.connection.cursor()
        sql = "INSERT INTO processos (pid, uid, prioridade, cpu, estado, memoria) VALUES (%s, %s, %s, %s, %s, %s)"

        # Insere os dados do processo na tabela
        cursor.execute(sql, (pid_entry, uid_entry, prioridade, cpu_entry, estado, memoria_entry))

        # Fecha a conexão com o banco de dados
        self.connection.commit()
        self.connection.close()

        # Exibe uma mensagem de sucesso
        print("Processo salvo com sucesso!")

    def consultar(self, pid):
        # Prepara a instrução SQL
        cursor = self.connection.cursor()

        try:
            cursor.execute("SELECT * FROM processos WHERE pid = %s", (pid,))
            registros = cursor.fetchall()
            cursor.close()

            return registros
        except:
            return False


    def atualizar(self, pid, uid, prioridade, cpu, estado, memória):
        # Obtém os novos valores do processo

        prioridade = str(prioridade)
        estado = str(estado)

        # Verifica se o PID existe no banco de dados
        cursor = self.connection.cursor()
        sql = "SELECT * FROM processos WHERE pid = %s"
        cursor.execute(sql, (pid,))

        # Se o PID não existir, gera um erro
        if not cursor.fetchone():
            return False

        # Prepara a instrução SQL
        cursor = self.connection.cursor()
        sql = "UPDATE processos SET uid = %s, prioridade = %s, cpu = %s, estado = %s, memoria = %s WHERE pid = %s"

        # Atualiza os dados do processo no banco de dados
        cursor.execute(sql, (uid, prioridade, cpu, estado, memória, pid))

        # Fecha a conexão com o banco de dados
        self.connection.commit()
        self.connection.close()

        print("Processo atualizado com sucesso!")
        return True


    def deletar(self, pid):
        # Obtém o PID do processo a ser excluído

        # Verifica se o PID existe no banco de dados
        cursor = self.connection.cursor()
        sql = "SELECT * FROM processos WHERE pid = %s"
        cursor.execute(sql, (pid,))

        # Se o PID não existir, gera um erro
        if not cursor.fetchone():
            return False

        # Prepara a instrução SQL
        cursor = self.connection.cursor()
        sql = "DELETE FROM processos WHERE pid = %s"

        # Exclui o processo do banco de dados
        cursor.execute(sql, (pid,))

        # Fecha a conexão com o banco de dados
        self.connection.commit()
        self.connection.close()

        print("Processo excluído com sucesso!")
        return True

        
