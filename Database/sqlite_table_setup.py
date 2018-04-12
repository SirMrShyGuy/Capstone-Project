import sqlite3

sqlite_file='data_49003.sqlite'
table_name='holder'
new_field1='outlet1'
new_field2='outlet2'
new_field3='outlet3'
new_field4='outlet4'
field_type='INTEGER'

conn=sqlite3.connect(sqlite_file)
c=conn.cursor()

c.execute('CREATE TABLE {tn} ({nf1} {ft})'\
          .format(tn=table_name, nf1=new_field1, ft=field_type))

c.execute("ALTER TABLE {tn} ADD COLUMN '{nf2}' {ft}"\
          .format(tn=table_name, nf2=new_field2, ft=field_type))

c.execute("ALTER TABLE {tn} ADD COLUMN '{nf3}' {ft}"\
          .format(tn=table_name, nf3=new_field3, ft=field_type))

c.execute("ALTER TABLE {tn} ADD COLUMN '{nf4}' {ft}"\
          .format(tn=table_name, nf4=new_field4, ft=field_type))

conn.commit()
conn.close()
