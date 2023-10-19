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




running = True
while running:

# Search MO - Odoo
# *********
    model_name = 'mrp.production'
    domain = [[ ['state', '=', 'confirmed'] ]]
    parameters = {'fields': ['name', 'product_id', 'product_qty', 'state', 'components_availability', 'workorder_ids']}
    records = models.execute_kw(db, uid, password, model_name, 'search_read', domain, parameters)
    

    if not records:
        time.sleep(20)
        pass

    else:
        running = False
        key = records[0]
        model_name = 'mrp.workorder'
        domain = [key['id']]
        parameters = {'fields':
                      ['name','workcenter_id','qty_production','qty_producing','qty_produced','working_state','production_state','state','is_produced']}
        records = models.execute_kw(db, uid, password, model_name, 'read', domain, parameters)
        WO_key = records[0]
        print(WO_key)
        print(nome(maquina))


        # Enviar para o MySql
        # connectar com o MySql
        try:
            #Abrir a conexao com o BD
            mydb = mysql.connector.connect(
            host="smarters-db.c50q6rz9ggrg.us-east-1.rds.amazonaws.com",
            user="navy", password="navy", database="smarters-db-navy" )

            #Executar consulta SQL a partir do cursor
            mycursor = mydb.cursor()
            sql = "INSERT INTO wo_to_factory (WO_id, MO_id, Cod_Maq, Date_ToDo, Qtd_Prod, Nome_Prod, Nome_MP, NC_Prog, WO_Status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s )"
            val = (WO_key['id'], key["id"], nome(maquina), 'CURDATE()', WO_key['qty_production'], '','','',0)
        
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
        


#if WO_key and WO_Status == 0:
#    WO_Start(WO_key[id])
#
#
#if WO_Status == 1:
#    WO_WriteProduction(WO_key['id'], qty_produced)





        




