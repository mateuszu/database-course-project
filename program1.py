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

        if login == 'init' and password == 'qwerty':
            create_user_app = """
            DO
            $do$
            BEGIN
                IF NOT EXISTS (
                    SELECT                       
                    FROM   pg_catalog.pg_roles
                    WHERE  rolname = 'app') THEN
                CREATE ROLE app LOGIN PASSWORD 'qwerty';
            END IF;
            END
            $do$;         
            """
            
            cursor.execute(create_user_app)


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

    @staticmethod
    def child(json_line, cursor):
        globals().update(json_line)
        query = """ SELECT emp FROM Employee WHERE emp1 = %s"""
        
        try:
            cursor.execute(query,[emp])
            result = cursor.fetchall()

            flattened_result = []

            for sublist in result:
                for val in sublist:
                    flattened_result.append(val)

            flattened_result_no_duplicates = []

            for i in flattened_result:
                if i not in flattened_result_no_duplicates:
                    flattened_result_no_duplicates.append(i)

            result_dict = {
                "status":"OK",
                "data" : flattened_result_no_duplicates
            }

            print json.dumps(result_dict)
        except Exception as e:
            print json.dumps({"status" : "ERROR"})
            print e #debug

        return cursor

    @staticmethod
    def parent(json_line, cursor):
        globals().update(json_line)
        query = """SELECT emp1 FROM Employee WHERE emp = %s """
        try:
            cursor.execute(query,[emp])
            result = cursor.fetchall()

            flattened_result = ""
            for sublist in result:
                for val in sublist:
                    flattened_result += str(val)
        
            result_dict = {
                "status":"OK",
                "data" : flattened_result
            }
            print json.dumps(result_dict)
        except Exception as e:
            print json.dumps({"status" : "ERROR"})
            print e #debug

        return cursor



def main():
   
    for line in sys.stdin:

        function_name = json.loads(line).keys()[0]
        print line #debug

        function_name = json.loads(line).keys()[0]

        if function_name == 'open':
            try:
                cursor = getattr(Function, function_name)(json.loads(line)[function_name])
            except Exception as e:
                print {"status" : "NOT IMPLEMENTED"}
                print e #debug
        else:
            getattr(Function, function_name)(json.loads(line)[function_name], cursor)
            try:
                pass#getattr(Function, function_name)(json.loads(line)[function_name], self.cursor)
            except Exception as e:
                print {"status" : "NOT IMPLEMENTED"}
                print e #debug

if __name__ == "__main__":
    main()
