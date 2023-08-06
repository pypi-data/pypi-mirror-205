from sqlalchemy import create_engine
import pandas as pd

sample_db_path = r'C:\Users\juanf\Dropbox\_PROGRAMMING\JFQ\JFQ\sample_db.sqlite3'

def create_SQLalchemy_connection(dbFile):
    engine = create_engine(r'sqlite:///' + dbFile)
    return engine

def query_unique_records(db,table,field):
    '''
    :param db: string with database location or existing db connection
    :param table:
    :param field:
    :return:
    '''
    if type(db)==str:
        engine = create_SQLalchemy_connection(db)
    else:
        engine = db
    sqlCommand = 'select distinct %s from %s; ' % (field,table)
    distinctFields = engine.execute(sqlCommand)
    for d in distinctFields:
        print(d)

def list_all_tables(db):
    '''
    :param db: string with database location or existing db connection
    :return:
    '''
    #this lists all tables
    if type(db)==str:
        engine = create_SQLalchemy_connection(db)
    else:
        engine = db
    res = engine.execute("SELECT name FROM sqlite_master WHERE type='table';")
    for name in res:
        print (name[0])

def vacuum_connection(db):
    '''
    :param db: string with database location or existing db connection
    :return:
    '''
    #this lists all tables
    if type(db)==str:
        engine = create_SQLalchemy_connection(db)
    else:
        engine = db
    engine.execute('VACUUM')

def save_data_to_database(downloaded_data,db,table_name,unique_fields,keep="first",ask_before_adding=True,replace_table=False):
    '''
    :param downloaded_data: the df with the data we've downloaded from Bloomberg in exactly the same format as that stored in the DB.
            In most cases, this means that the dates will appear as a column and not an index
    :param db: string with database location or existing db connection
    :param table_name:  name of the table within the database that we want to update. Default = BBG database
    :param unique_fields: a list containing the fields that, given a certain combination of the same, will make a record a unique one. eg. ['Date','security','fundamental']
    :param keep: "first" or "last"
    :param ask_before_adding: If False, data is added directly
    :param replace_table:  if True, it will wipe out the existing data. If False (default), it will just append new records
    :return: kept,updated,added,net_set df
    '''

    # retrieve existing data from DB
    if type(db)==str:
        con = create_SQLalchemy_connection(db)
    else:
        con = db

    #if we just want to override the table, go for this
    if replace_table==True:
        downloaded_data.to_sql(name=table_name, con=con, if_exists='replace', index=False)
        return [downloaded_data]*4

    #else, check what's already in the database and look for duplicates
    existing_records = pd.read_sql_table(table_name=table_name,  con=con)
    uniques_existing = existing_records.set_index(unique_fields)
    filter = uniques_existing.index.duplicated(keep="last")
    if filter.max()==True:
        print("warning - duplicate records in source")
        return [uniques_existing[filter]]*4
    uniques_downloaded = downloaded_data.set_index(unique_fields)
    filter = uniques_downloaded.index.duplicated(keep="last")
    if filter.max()==True:
        print("warning - duplicate records in downloaded data")
        return [uniques_downloaded[filter]]*4

    #what is the net, expanded record set:
    net_set = pd.concat([existing_records,downloaded_data],axis=0,ignore_index=True)
    net_set = net_set.drop_duplicates(subset=unique_fields,keep=keep)

    #what are the dropped and added records
    comparison = existing_records.merge(downloaded_data,on=unique_fields,how="outer", indicator=True)
    kept = comparison[comparison["_merge"]=="left_only"].drop("_merge",axis=1)
    updated = comparison[comparison["_merge"]=="both"].drop("_merge",axis=1)
    added = comparison[comparison["_merge"]=="right_only"].drop("_merge",axis=1)

    if keep=="first":
        kept = pd.concat([kept,updated],axis=0)
        updated = []

    #Add records if appropriate
    print(f'{len(updated)} records to be updated and {len(added)} records to be added')

    if (len(added) + len(updated))==0:
        return ['NO new or updated records found']*4
    else:
        if ask_before_adding:
            i = input('Update database? (y/n)').lower()

        else:
            i='y'

        print('***********************************************')
        if i == 'y':
            net_set.to_sql(name=table_name, con = con,if_exists='replace',index=False)
            print('database updated')
        else:
            print('new records found but NOT added')
        print('***********************************************')
        return kept,updated,added,net_set

def load_data_from_database(db, table_name,index_col=''):
    '''
    :param db: string with database location or existing db connection
    :param table_name:
    :param index_col: if specified, it will define the field(s) that become the index. Can be string for single field or list for multiple fields
    :return:
    '''
    if type(db)==str:
        engine = create_SQLalchemy_connection(db)
    else:
        engine = db
    df = pd.read_sql_table(table_name=table_name, con=engine)
    if index_col!='':
        df = df.set_index(index_col)
    return df

def duplicate_database_table(db,original_table_name,new_table_name):
    '''
    :param db: string with database location or existing db connection
    :param original_table_name:
    :param new_table_name:
    :return:
    '''
    if type(db)==str:
        engine = create_SQLalchemy_connection(db)
    else:
        engine = db
    sqlCommand = 'CREATE TABLE {} AS SELECT * FROM {};'.format(new_table_name,original_table_name)
    engine.execute(sqlCommand)



#example
# df0 = pd.DataFrame(index=[1,2],columns=["A","B"],data=[["A1","B1"],["A2","B2"]])
# df1 = pd.DataFrame(index=[1,2,3],columns=["A","B"],data=[["A1","B1"],["A2","B2"],["A2","B3"]])
# df2 = pd.DataFrame(index=[1,2,3,4],columns=["A","B"],data=[["A1","B1"],["A2","B2"],["A2","B4"],["A2","B5"]])
# df3 = pd.DataFrame(index=[1,2,3,4],columns=["A","B"],data=[["A1","B1"],["A2","B2"],["A2","B4"],["A2","B4"]])
# kept,updated,added,net_set = save_data_to_database(downloaded_data=df3,db=sample_db_path,table_name="test_table",unique_fields=["A","B"],keep="first",ask_before_adding=True,replace_table=False)
# load_data_from_database(db=sample_db_path,table_name="test_table")