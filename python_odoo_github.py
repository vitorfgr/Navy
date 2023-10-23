import xmlrpc.client
import sys
import mysql.connector
import time





#Connection ODOO
url = "https://edu-smarters-navy.odoo.com"
db = 'edu-smarters-navy'
username = 'gustavorp3@al.insper.edu.br'
password = 'P@ssword79'


#verify if the connection information is correct
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})
print("User ID = ", uid)
if uid == False:
    print("erro na autenticacao de usuario")
    sys.exit()

models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))


# Operaçoes
def WO_Start(WO_id):
    model_name = 'mrp.workorder'
    WO_start = models.execute_kw(db,uid,password, model_name,'button_start',[WO_id])
    return WO_start

def WO_WriteProduction(WO_id, qty_produced):
    model_name = 'mrp.workorder'
    wo_write = models.execute_kw(db, uid, password, model_name, 'write', [[WO_id], {'qty_produced': qty_produced}] )
    wo_write = models.execute_kw(db, uid, password, model_name, 'write', [[WO_id], {'qty_producing': qty_produced}] )
    return wo_write

def WO_Done(WO_id):
    model_name = 'mrp.workorder'
    WO_done = models.execute_kw(db,uid,password, model_name,'button_done',[WO_id])
    return WO_done

def MO_MarkAsDone(MO_id):
    model_name = 'mrp.production'
    MO_done = models.execute_kw(db, uid, password, model_name, 'button_mark_done', [[MO_id]] )
    return MO_done

# Dicionario 
maquina = {'Torno Centur':'TR10', 'Torno': 'TR10', 'Estação Montagem':'MT10', 'Estação Teste':'ET10', 'Centro Usinagem Robodrill':'CU10'}

def nome(dic):
    for i in dic:
        palavra = WO_key["workcenter_id"][1]
        if palavra == i:
            maq = maquina[i]
    return maq

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
            print("MySQL connection is closed")
    return "MySQL connection is closed"

def WO_Status(WO_id):
    WO_Status = None
    try:
        #Abrir a conexao com o BD
        mydb = mysql.connector.connect(
        host="smarters-db.c50q6rz9ggrg.us-east-1.rds.amazonaws.com",
        user="navy", password="navy", database="smarters-db-navy" )

        #Executar consulta SQL a partir do cursor
        mycursor = mydb.cursor()
        sql = "SELECT WO_Status FROM wo_to_factory WHERE WO_id = %s"
        args = (WO_id)
        mycursor.execute(sql, args)

        #Ler resultado
        print("Resultados do Select")
        myresults = mycursor.fetchall()
        for res in myresults:
            WO_Status = res[0]
            print(res[0])


    except mysql.connector.Error as error:
        print("Failed to run SQL {}".format(error))
    
    finally:
        if mydb.is_connected():
            mycursor.close()
            mydb.close()
            print("MySQL connection is closed")

    return WO_Status

def workID(x):
    lista = []
    for item in x:
        lista.append(item['workorder_ids'])
    
    for i in lista:
        r = i

    return r

def ManuID(x):
    lista = []
    for item in x:
        lista.append(item['id'])

    for i in lista:
        r = i

    return r





running = True
while running:

# Search MO - Odoo
# *********
    model_name = 'mrp.production'
    domain = [[['state', '=', 'confirmed']]]
    parameters = {'fields': ['name', 'product_id', 'product_qty', 'state', 'components_availability', 'workorder_ids']}
    records_p = models.execute_kw(db, uid, password, model_name, 'search_read', domain, parameters)
    print(records_p)

    if not records_p:
        time.sleep(20)
        pass

    else:
        running = False
        key = workID(records_p)
        model_name = 'mrp.workorder'
        for Key in key:
            domain = [Key]
            parameters = {'fields':['name', 'workcenter_id', 'qty_production', 'qty_producing', 'qty_produced', 'working_state', 'production_state', 'state', 'is_produced']}
            records_w = models.execute_kw(db, uid, password, model_name, 'read', domain, parameters)
            WO_key = records_w[0]

            print(WO_key['id'])
            print(ManuID(records_p))

            #Enviar 
            input_sql(WO_key['id'], ManuID(records_p), nome(maquina), 'CURDATE()', WO_key['qty_production'])


        if WO_Status([WO_key['id']]) == 0:
            print('fabrica')
            time.sleep(10)
        if WO_Status([WO_key['id']]) == 1:
            print('inicio')
            time.sleep(10)
        elif WO_Status([WO_key['id']]) == 3:
            print('pronto')
            running = True







        




