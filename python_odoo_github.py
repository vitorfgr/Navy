import xmlrpc.client
import sys
import mysql.connector




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
maquina = {'Torneamento':'TR10', 'Montagem':'MT10', 'Teste':'ET10', 'Usinagem':'CU10'}


running = True
while running:

# Search MO - Odoo
# *********
    model_name = 'mrp.production'
    domain = [[ ['state', '=', 'confirmed'] ]]
    parameters = {'fields': ['name', 'product_id', 'product_qty', 'state', 'components_availability', 'workorder_ids']}
    records = models.execute_kw(db, uid, password, model_name, 'search_read', domain, parameters)
    

    if not records:
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


if WO_key and WO_Status == 0:
    WO_Start(WO_key[id])


if WO_Status == 1:
    WO_WriteProduction(WO_key['id'], qty_produced)





        




