from database import table_name

def readDB(current_outlet, table_name):
    conn=sqlite3.connect(sqlite_file)
    c=conn.cursor()
    c.execute('SELECT ({cn}) FROM {tn}'.\
              format(cn=current_outlet, tn=table_name))
    current_values=c.fetchall()
    conn.commit()
    conn.close()
    return current_values

def writeDB(databaseValues[], table_name):
    conn=sqlite3.connect(sqlite_file)
    c=conn.cursor()
    c.execute("INSERT INTO {tn} ({cn1}, {cn2}, {cn3}, {cn4}) VALUES ("databaseValues[1]", "databaseValues[2]", "databaseValues[3]", "databaseValues[4])\"".\
              format(tn=table_name, cn1='outlet1', cn2='outlet2', cn3='outlet3', cn4='outlet4'))
    conn.commit()
    conn.close
    return
