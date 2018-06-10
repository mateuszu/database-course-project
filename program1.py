import psycopg2
import json
import sys

class Function:
    
    def __init__(self):
        self.open = open()

    @staticmethod
    def open(json_line):

        globals().update(json_line)

        conn = psycopg2.connect("dbname=%s user=%s password=%s"% (database, login, password))
        conn.autocommit = True

        print "Connected!\n" #debug

        cursor = conn.cursor()
        cursor.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto;")
        f = open('queries.sql', 'r').read()

        queries_list = f.split(';')
  
        for c in queries_list[:-1]:
            cursor.execute(c)
        
        print json.dumps({"status" : "OK"})

        return cursor
    
    @staticmethod
    def root(json_line, cursor):
        globals().update(json_line)
        query = """insert into Employee(data, newpasswd,emp) VALUES(%s, crypt(%s, gen_salt('bf',8)), %s)"""

        if secret == "qwerty":
            try:
                cursor.execute(query, (data,newpasswd,emp))
                print json.dumps({"status" : "OK"})
            except Exception as e:
                print json.dumps({"status" : "ERROR"})
                print e #debug
        else:
            print json.dumps({"status" : "ERROR"})
            print "BAD PASSWORD" #debug

    @staticmethod
    def new(json_line, cursor):
        globals().update(json_line)
        query = """INSERT INTO EMPLOYEE(admin,passwd,data,newpasswd,emp1,emp) VALUES(%s, crypt(%s, gen_salt('bf',8)), %s, crypt(%s, gen_salt('bf',8)), %s, %s);
        """

        if ((emp or emp1) > 0):
            try:
                cursor.execute(query, (admin,passwd,data,newpasswd,emp1,emp))
                print json.dumps({"status" : "OK"}) 
            except Exception as e:
                print json.dumps({"status" : "ERROR"})
                print e #debug
        else:
            print json.dumps({"status" : "ERROR"})
            print "EMP OR EMP1 < 0" #debug



def main():
   
    for line in sys.stdin:

        function_name = json.loads(line).keys()[0]
        print line #debug

        if function_name == 'open':
            try:
                cursor = getattr(Function, function_name)(json.loads(line)[function_name])
            except Exception as e:
                print {"status" : "NOT IMPLEMENTED"}
                print e #debug
        else:
                getattr(Function, function_name)(json.loads(line)[function_name], cursor)
                try:
                    pass#getattr(Function, function_name)(json.loads(line)[function_name], cursor)
                except Exception as e:
                    print {"status" : "NOT IMPLEMENTED"}
                    print e #debug

if __name__ == "__main__":
    main()
