import xmlrpc.client
import sys

#Connection
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


running = True
while running:

    # Search MO - Odoo
    # *********
    model_name = 'mrp.production'
    domain = [[ ['state', '=', 'confirmed'] ]]
    parameters = {'fields': ['name', 'product_id', 'product_qty', 'state', 'components_availability', 'workorder_ids']}
    records = models.execute_kw(db, uid, password, model_name, 'search_read', domain, parameters)
    print("\nManuf Orders:")
    for key in records:
        print(key)


    # Search WO - Odoo
    # ********
    model_name = 'mrp.workorder'
    domain = ['workorder_ids']
    parameters = {'fields':
                  ['name','workcenter_id','qty_production','qty_producing','qty_produced','working_state','production_state','state','is_produced']}
    records = models.execute_kw(db, uid, password, model_name, 'read', domain, parameters)
    print("\nWork Orders:")
    for key in records:
        print(key)

    if records != 0:
        # START WO
        


# START WO
#*********
"""WO_id = 22
model_name = 'mrp.workorder'
parameters = {}
WO_start = models.execute_kw(db, uid, password, model_name, 'button_start', [WO_id], parameters)
print("Bt WO start:", WO_start)

# WRITE WO (QTY PRODUCED)
# ***********************
WO_id = 22
model_name = 'mrp.workorder'
WO_write = models.execute_kw(db, uid, password, model_name, 'write', [[WO_id], {'qty_produced': 10}] )
print("Write WO production:", WO_write)

# STOP WO
#********
WO_id = 22
model_name = 'mrp.workorder'
parameters = {}
WO_stop = models.execute_kw(db, uid, password, model_name, 'button_done', [WO_id], parameters)
print("Bt WO done:", WO_stop)

# MASK MO AS DONE
#****************
MO_id = 22
model_name = 'mrp.production'
parameters = {}
MO_done = models.execute_kw(db, uid, password, model_name, 'button_mark_done', [MO_id], parameters)
print("Bt MO Mark as Done:", MO_done)"""