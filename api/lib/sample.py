from mysqlclass import MysqlPython


conn = MysqlPython('localhost', 'root', 'mysql123', 'SCG')

conditional_query='ID = %s'

#result= conn.update('Settings.EmailSetting', conditional_query, 8, ReceiverID='hariharaselvam8@gmail.com', PhoneNumber='8904621882')

#result= conn.insert('Settings.EmailSetting', ReceiverID='hariharaselvam@gmail.com', PhoneNumber='', Device='SCG')

result= conn.delete('Settings.EmailSetting', conditional_query, 11)

print result
