from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Funções para interagir com o banco de dados
def criar_tabela():
    conn = sqlite3.connect('Objetos.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS tablets (patrimonio int(8) PRIMARY KEY,IMEI int,ordem INTEGER,data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,agencia TEXT,funcional INTEGER,completo INTEGER,falta TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS DMCS_Positivo (patrimonio int(8) PRIMARY KEY,IMEI_1 int,IMEI_2,,ordem INTEGER,data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,agencia TEXT,funcional INTEGER,Completo INTEGER,falta TEXT)''')
    conn.commit()
    conn.close()

def adicionar_tablet(patrimonio,imei,ordem,agencia, funcional,completo,falta):
    conn = sqlite3.connect('Objetos.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO tablets (patrimonio,IMEI, ordem, funcional, agencia,defeito) VALUES (?,?, ?, ?,?,?)''',(patrimonio,imei, ordem,agencia,funcional,completo,falta))
    conn.commit()
    conn.close()

def adicionar_DMCP(patrimonio,imei_1,imei_2,SN,ordem,agencia,funcional,completo,falta)

def obter_tablets():
    conn = sqlite3.connect('Objetos.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM tablets''')
    tablets = cursor.fetchall()
    conn.close()
    return tablets

# Cria a tabela se não existir
criar_tabela()

@app.route('/')
def index():
    tablets = obter_tablets()
    return render_template('index.html', tablets=tablets)

@app.route('/add_objeto', methods=['POST'])
def add_objeto():
    selecionado = request.form['objetos']
    if selecionado == 'tablet':
       return add_tablet()
    elif selecionado == 'DMCP':
        return add_DMCP()


def add_tablet():
    #patrimonio e IMEI
    patrimonio = request.form['patrimonio']
    imei = request.form['imei']
    #ordem
    ordem=1
    conn = sqlite3.connect('Objetos.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM tablets''')
    tablets = cursor.fetchall()
    for tablet in tablets:
        ordem=ordem+1 
    #funcional
    funcional = 1 if request.form['funcional'] == 'Sim' else 0
    #agencia
    agencia = request.form['agencia']
    #defeito
    defeito=request.form['defeito']
    if funcional == 1:
        defeito="Sem defeito"
    elif funcional == 0 and defeito == "":
        defeito = "Defeito não especificado"
    adicionar_tablet(patrimonio,imei,ordem,funcional, agencia,defeito)
    return index()

if __name__ == '__main__':
    app.run(debug=True)
