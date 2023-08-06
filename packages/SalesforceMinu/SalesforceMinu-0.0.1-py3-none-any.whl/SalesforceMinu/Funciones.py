# OBTENEMOS IDs DEL DATAFRAME
def get_dataframe_ids(df, nam_or, title = 'id'):
    ids_df = []
    for i in range(len(nam_or)):
        data = df[df['name'] == nam_or[i]][title]
        ids_df.append(data[data.index[0]])
    return ids_df

# OBTENER NOMBRES DE UN DATAFRAME
def get_names_list(df, title = 'name'):
    if len(df[title]) == 1:
        names = df[title].get(1)
    else:
        names = ",".join(df[title])
    # Convertimos a lista
    names = names.split(',')
    return names

# OBTENER LOS IDS DE ACCOUNT Y EL ORDEN DE SUS NOMBRE
# Si no encuentra el nombre que mande mensaje de error o algo
def get_account_id_names(names):
    # Puede ser un nombre o varios
    case = 0
    if type(names) == str:
        where = f"Name = '{str(names)[1:-1]}'"
    else:
        where = f"Name IN ({str(names)[1:-1]})"
        case = 1
    
    query = f"""SELECT Id, Name, NumberOfEmployees
    FROM Account
    WHERE {where}"""
    
    records = sf.query_all(query)
    # Obtenemos el orden de los nombres y sus IDs
    Names_order = [ row['Name'] for row in records['records']]
    IDs = [ row['Id'] for row in records['records']]
    
    # Ver si no encontro alguno, es decir que el tamaño sea menor que la entrada
    if case == 1 and len(names) != len(Names_order):
        raise ValueError("No se encontro una o más empresas")
    elif case == 0 and Names_order == []:
        raise ValueError("No se encontro el nombre de la empresa")
    return Names_order, IDs

# OBTENER LOS SUSCRIPTORES DE EMPRESAS
def get_subs(account_ids):
    # Puede ser un ID o varios
    razones = [sf.query_all(f"""SELECT Head_count__c
                      FROM Raz_n_Social__c
                      WHERE Cuenta__c = '{row}'""")['records'] for row in account_ids]
    # Puede haber más de una razón por empresa
    subs = []
    for i in range(len(razones)):
        if len(razones[i]) == 1:
            subs.append(razones[i][0]['Head_count__c'])
        else: # Mas de una razon
            lis = []
            for j in range(len(razones[i])):
                lis.append(razones[i][j]['Head_count__c'])
            subs.append(sum(lis))
    
    return subs
    
# OBTENEMOS FECHA CIERRE DE CONTRATO
def get_contract_dates(account_ids):
    contract_dates = [sf.query_all(f"""SELECT Fecha_cierre_en_el_contrato__c
                      FROM Opportunity
                      WHERE AccountId = '{row}'""")['records'][0]['Fecha_cierre_en_el_contrato__c'] for row in account_ids]
    return contract_dates

# OBTENEMOS OPPORTUNITY IDS
def get_opportunity_ids(account_ids):
    opportunity_ids = [sf.query_all(f"""SELECT Id
                      FROM Opportunity
                      WHERE AccountId = '{row}'""")['records'][0]['Id'] for row in account_ids]
    return opportunity_ids

# OBTENEMOS EL PRODUCTID
def get_product_id(opportunity_ids):
    products_ids = [sf.query_all(f"""SELECT Product2Id
                      FROM OpportunityLineItem
                      WHERE OpportunityId = '{row}'""")['records'][0]['Product2Id'] for row in opportunity_ids]
    return products_ids
    

# OBTENEMOS MODELO DE SUSCRIPCIÓN, EL CODIGO Y SU NOMBRE
def get_model(products_ids):
    
    dict_plan = {'005':'starter',
             '009':'starter',
             '011':'starter',
             '013':'starter',
             '006':'total',
             '008':'total',
             '010':'total',
             '012':'total'}
    
    model = [ list(sf.query_all(f"""SELECT Name, ProductCode
                      FROM Product2
                      WHERE Id = '{row}'""")['records'][0].values()) for row in products_ids]
    # Puede haber más de una razón por empresa
    models = []
    plan = []
    if len(model) == 1:
        models.append(dict_plan[model[2]])
        plan.append(model[2])
    else: # Mas de una razon
        for i in range(len(model)):
            models.append(dict_plan[model[i][2]])
            plan.append(model[i][2])
    return models, plan
    