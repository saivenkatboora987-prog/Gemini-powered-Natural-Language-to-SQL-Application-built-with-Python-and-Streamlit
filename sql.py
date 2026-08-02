import sqlite3

#Connectt to SQlite
#Our database name: Naresh_it_student
connection=sqlite3.connect("Naresh_it_employee.db")

# Create a cursor object to insert record,create table

cursor=connection.cursor()

#create the table
#Our table name student
#Columns names are: name, course
table_info="""
Create table Naresh_it_employee(employee_name varchar(30),
                    employee_role varchar(30),
                    employee_salary FLOAT);
"""
cursor.execute(table_info)

#Insert the records

cursor.execute('''Insert Into Naresh_it_employee values('Omkar Nallagoni','Data Science',75000)''')
cursor.execute('''Insert Into Naresh_it_employee values('Naresh','Data Science',90000)''')
cursor.execute('''Insert Into Naresh_it_employee values('Phani','Data Science',88000)''')
cursor.execute('''Insert Into Naresh_it_employee values('Naga babu','Data Engineer',50000)''')
cursor.execute('''Insert Into Naresh_it_employee values('Ajay','Data Engineer',35000)''')
cursor.execute('''Insert Into Naresh_it_employee values('Pawan','Data Engineer',60000)''')

#Disspaly ALl the records

print("The isnerted records are")
data=cursor.execute('''Select * from Naresh_it_employee''')
for row in data:
    print(row)

#Commit your changes int he databse
connection.commit()
connection.close()