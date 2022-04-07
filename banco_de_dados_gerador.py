import sqlite3


banco_de_dados = sqlite3.connect('nome_pontuacao.db') #Criando banco de dados
cursor = banco_de_dados.cursor() #Objeto que vai permitir modificar o banco de dados

#Criando a tabela "NOME_PONTOS" e colocando as colunas "Score" e "Name"
#cursor.execute("CREATE TABLE nomes_pontos(Score integer, Name text)")

#Exibir dados de acordo com o score:
cursor.execute("SELECT rowid, * FROM nomes_pontos ORDER BY Score LIMIT 10")
itens2 = cursor.fetchmany(10)
#print(itens2[0][0])


#2 linhas para visualizar o banco
""" cursor.execute("SELECT * FROM nomes_pontos") 
print(cursor.fetchall()) 
 """
