import xmlrpc.client
import sys
import mysql.connector
import time





# Conexão com o sistema ODOO
url = "https://edu-smarters-navy.odoo.com"
db = 'edu-smarters-navy'
username = 'gustavorp3@al.insper.edu.br'
password = 'P@ssword79'


# Verifica se as informações de conexão estão corretas
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})
print("User ID = ", uid)
if uid == False:
    print("erro na autenticacao de usuario")
    sys.exit()

models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))



# Funções para interagir com o sistema ODOO
def WO_Start(WO_id):
    # Inicia uma ordem de trabalho no ODOO
    model_name = 'mrp.workorder'
    WO_start = models.execute_kw(db, uid, password, model_name, 'button_start', [WO_id])
    return WO_start

def WO_WriteProduction(WO_id, qty_produced):
    # Atualiza a produção em uma ordem de trabalho no ODOO
    model_name = 'mrp.workorder'
    wo_write = models.execute_kw(db, uid, password, model_name, 'write', [[WO_id], {'qty_produced': qty_produced}])
    wo_write = models.execute_kw(db, uid, password, model_name, 'write', [[WO_id], {'qty_producing': qty_produced}])
    return wo_write

def WO_Done(WO_id):
    # Conclui uma ordem de trabalho no ODOO
    model_name = 'mrp.workorder'
    WO_done = models.execute_kw(db, uid, password, model_name, 'button_done', [WO_id])
    return WO_done

def MO_MarkAsDone(MO_id):
    # Marca uma ordem de produção como concluída no ODOO
    model_name = 'mrp.production'
    MO_done = models.execute_kw(db, uid, password, model_name, 'button_mark_done', [[MO_id]])
    return MO_done

# Dicionário para mapear nomes de máquinas
maquina = {'Torno Centur': 'TR10', 'Torno': 'TR10', 'Estação Montagem': 'MT10', 'Estação Teste': 'ET10', 'Centro Usinagem Robodrill': 'CU10'}

# Função para mapear nomes de máquinas
def nome(dic):
    for i in dic:
        #WO_key = WO_Odoo(records[i])
        palavra = WO_key["workcenter_id"][1]
        if palavra == i:
            maq = maquina[i]
    return maq

# Função para inserir dados no banco de dados SQL
def input_sql(WO_id, MO_id, Cod_Maq, Date_ToDo, Qtd_Prod):

    try:

        #Abrir a conexao com o BD
        mydb = mysql.connector.connect(
        host="smarters-db.c50q6rz9ggrg.us-east-1.rds.amazonaws.com",
        user="navy", password="navy", database="smarters-db-navy" )

        #Executar consulta SQL a partir do cursor
        mycursor = mydb.cursor()
        sql = "INSERT INTO wo_to_factory (WO_id, MO_id, Cod_Maq, Date_ToDo, Qtd_Prod, Nome_Prod, Nome_MP, NC_Prog, WO_Status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s )"
        val = (WO_id, MO_id, Cod_Maq, Date_ToDo, Qtd_Prod, '','','',0)
    
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "was inserted.")

    except mysql.connector.Error as error:
        mydb.rollback
        print("Failed to run SQL {}".format(error))
        
    finally:
        if mydb.is_connected():
            mycursor.close()
            mydb.close()
            

    return "MySQL connection is closed"

# Função para obter o status de uma ordem de trabalho no banco de dados SQL
def WO_Status(WO_id):

    Wo_id = []

    try:
        #Abrir a conexao com o BD
        mydb = mysql.connector.connect(
        host="smarters-db.c50q6rz9ggrg.us-east-1.rds.amazonaws.com",
        user="navy", password="navy", database="smarters-db-navy" )

        #Executar consulta SQL a partir do cursor
        mycursor = mydb.cursor()
        sql = "SELECT WO_Status FROM wo_to_factory WHERE WO_id = %s"
        args = (WO_id,)
        mycursor.execute(sql, args)

        #Ler resultado
        myresults = mycursor.fetchall()

        for res in myresults:
            Wo_id.append(int(res[0]))

    except mysql.connector.Error as error:
        print("Failed to run SQL {}".format(error))
    
    finally:
        if mydb.is_connected():
            mycursor.close()
            mydb.close()

    return Wo_id

def finalizando():

    final = []

    try:
        #Abrir a conexao com o BD
        mydb = mysql.connector.connect(
        host="smarters-db.c50q6rz9ggrg.us-east-1.rds.amazonaws.com",
        user="navy", password="navy", database="smarters-db-navy" )

        #Executar consulta SQL a partir do cursor
        mycursor = mydb.cursor()
        sql = "SELECT WO_id FROM wo_to_factory WHERE WO_Status = 3"
        mycursor.execute(sql)

        #Ler resultado
        myresults = mycursor.fetchall()
        for res in myresults:
            final.append(int(res[0]))

    except mysql.connector.Error as error:
        print("Failed to run SQL {}".format(error))
    
    finally:
        if mydb.is_connected():
            mycursor.close()
            mydb.close()

    return final

def sendoFab():
    lista_fab = []

    try:
        #Abrir a conexao com o BD
        mydb = mysql.connector.connect(
        host="smarters-db.c50q6rz9ggrg.us-east-1.rds.amazonaws.com",
        user="navy", password="navy", database="smarters-db-navy" )

        #Executar consulta SQL a partir do cursor
        mycursor = mydb.cursor()
        sql = "SELECT MO_id FROM wo_to_factory;"
        mycursor.execute(sql)

        #Ler resultado
        myresults = mycursor.fetchall()

        for res in myresults:
            lista_fab.append(int(res[0]))

    except mysql.connector.Error as error:
        print("Failed to run SQL {}".format(error))
    
    finally:
        if mydb.is_connected():
            mycursor.close()
            mydb.close()

    return lista_fab

def concluido(WO_id):

    try:
        #Abrir a conexao com o BD
        mydb = mysql.connector.connect(
        host="smarters-db.c50q6rz9ggrg.us-east-1.rds.amazonaws.com",
        user="navy", password="navy", database="smarters-db-navy" )

        #Executar consulta SQL a partir do cursor
        mycursor = mydb.cursor()
        sql = "UPDATE wo_to_factory SET WO_Status = 4 WHERE WO_id = %s"
        args = (WO_id,)
        mycursor.execute(sql,args)
        mydb.commit()


    except mysql.connector.Error as error:
        print("Failed to run SQL {}".format(error))
    
    finally:
        if mydb.is_connected():
            mycursor.close()
            mydb.close()

    return 

def maquina_em_uso():

    maquina = []

    try:
        #Abrir a conexao com o BD
        mydb = mysql.connector.connect(
        host="smarters-db.c50q6rz9ggrg.us-east-1.rds.amazonaws.com",
        user="navy", password="navy", database="smarters-db-navy" )

        #Executar consulta SQL a partir do cursor
        mycursor = mydb.cursor()
        sql = "SELECT Cod_Maq FROM wo_to_factory WHERE WO_Status <= 3"
        mycursor.execute(sql)

        #Ler resultado
        myresults = mycursor.fetchall()

        for res in myresults:
            maquina.append(res[0])

    except mysql.connector.Error as error:
        print("Failed to run SQL {}".format(error))
    
    finally:
        if mydb.is_connected():
            mycursor.close()
            mydb.close()

    return maquina

# Função para obter a chave de trabalho
def workID(x):
    lista = []
    for item in x:
        lista.append(item['workorder_ids'])
    
    for i in lista:
        r = i

    return r

# Função para obter o ID da ordem de produção
def ManuID(x):
    print(x)
    for i in x:
        r = i

    return r

def MO_Odoo():
    # Pesquisar MO no ODOO
    model_name = 'mrp.production'
    domain = [[['state', '=', 'confirmed']]]
    parameters = {'fields': ['name', 'product_id', 'product_qty', 'state', 'components_availability', 'workorder_ids']}
    records = models.execute_kw(db, uid, password, model_name, 'search_read', domain, parameters)
    return records

def WO_Odoo(x):
    keys = workID([x])
    model_name = 'mrp.workorder'
    #for Key in keys:
    domain = [keys[0]]
    parameters = {'fields':['name', 'workcenter_id', 'qty_production', 'qty_producing', 'qty_produced', 'working_state', 'production_state', 'state', 'is_produced']}
    records_w = models.execute_kw(db, uid, password, model_name, 'read', domain, parameters)
    WO_key = records_w[0]
    #input_sql(WO_key['id'], ManuID(x), nome(maquina), 'CURDATE()', WO_key['qty_production'])
    
    return WO_key

def search_MO(WO_id):
    
    Mo_id = []

    try:
        #Abrir a conexao com o BD
        mydb = mysql.connector.connect(
        host="smarters-db.c50q6rz9ggrg.us-east-1.rds.amazonaws.com",
        user="navy", password="navy", database="smarters-db-navy" )

        #Executar consulta SQL a partir do cursor
        mycursor = mydb.cursor()
        sql = "SELECT MO_id FROM wo_to_factory WHERE WO_Status = %s"
        args = (WO_id,)
        mycursor.execute(sql,args)

        #Ler resultado
        myresults = mycursor.fetchall()

        for res in myresults:
            Mo_id.append(int(res[0]))

    except mysql.connector.Error as error:
        print("Failed to run SQL {}".format(error))
    
    finally:
        if mydb.is_connected():
            mycursor.close()
            mydb.close()

    return Mo_id





running = True
while running:

    records = MO_Odoo()



    # Olha se há algm coisa para implementar no sql
    if len(records) != 0:
        print(records[0])
        for i in range(len(records)):

            #ver se não está sendo fabricada
            if records[i]['id'] not in sendoFab():
                WO_key = WO_Odoo(records[i])
                # Ver se tem alguma maquina disponivel 
                if WO_key["workcenter_id"] not in maquina_em_uso():
                    input_sql(WO_key['id'], records[i]['id'], nome(maquina), 'CURDATE()', WO_key['qty_production'])
                
                else: 
                    pass

            else:
                pass
        
    for i in finalizando():

        if WO_Status(i)[0] == 3:
            print(i)
            #WO_WriteProduction(WO_key['id'], WO_key['qty_produced'])
            WO_WriteProduction(i, 1)
            WO_Done(i)
            MO_MarkAsDone(ManuID(search_MO(i)))
            concluido(i)


        else:
            break



    else:
        time.sleep(20)
        pass
        


