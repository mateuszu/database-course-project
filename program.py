import psycopg2
import json
import sys

def remove_none_elements_from_list(list):
    return [e for e in list if e != None]

def pass_auth(admin, pwd, cursor):

    query1 = "SELECT * FROM employee WHERE id = %s AND password = crypt(%s, password)"
    
    cursor.execute(query1, (admin, pwd,))
    if cursor.fetchone():
        return True
    else:
        return False

def admin_auth(admin, employee_id, pwd, cursor):

    query = "SELECT superior FROM Employee WHERE id = %s "


    if pass_auth(admin, pwd, cursor):
        cursor.execute(query,[employee_id])
        result_parent = cursor.fetchone()
        result = []
        result.append(result_parent)

        while(result_parent != None):
            cursor.execute(query,[result_parent])
            result_parent = cursor.fetchone()
            result.append(result_parent)

        result = remove_none_elements_from_list(result)

        flattened_result = []
        for sublist in result:
            for val in sublist:
                flattened_result.append(val)
        if admin in flattened_result:
            return True
        else:
            return False
    else:
        print json.dumps({"status" : "ERROR", "debug" : "Authentication Error"})
        return False


class Function:
    
    def __init__(self):
        self.open = open()

    @staticmethod
    def open(json_line):

        globals().update(json_line)

        conn = psycopg2.connect("dbname=%s user=%s password=%s"% (database, login, password))
        conn.autocommit = True

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
        
        print {"status" : "OK", "debug" : "Connected"}

        return cursor
    
    @staticmethod
    def root(json_line, cursor):
        globals().update(json_line)
        query = """insert into Employee(id, data, password) VALUES(%s, %s, crypt(%s, gen_salt('bf',8)))"""

        if secret == "qwerty":
            try:
                cursor.execute(query, (emp,data,newpassword))
                print json.dumps({"status" : "OK"})
            except Exception as e:
                print json.dumps({"status" : "ERROR"})
                print e #debug
        else:
            print json.dumps({"status" : "ERROR" , "debug" : "Bad Secret"})

    @staticmethod
    def new(json_line, cursor):
        globals().update(json_line)
        query = """INSERT INTO EMPLOYEE(id,superior, data,admin,password) VALUES(%s, %s,  %s, %s, crypt(%s, gen_salt('bf',8)));
        """

        if pass_auth(admin, passwd, cursor) or admin_auth(admin, emp, passwd, cursor):
            try:
                cursor.execute(query, (emp, emp1, data, admin, newpasswd,))
                print {"status" : "OK", "debug" : "new user id %d" %emp}
            except Exception as e:
                print json.dumps({"status" : "ERROR"})
                print e #debug
        else:
            print json.dumps({"status" : "ERROR", "debug": "Authentication Error"})

        return cursor


    @staticmethod
    def child(json_line, cursor):
        globals().update(json_line)
        query = """ SELECT id FROM Employee WHERE superior = %s"""
        
        if pass_auth(admin, passwd, cursor):
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
                    "debug": "child for id %d" %emp,
                    "data" : flattened_result_no_duplicates
                }

                print json.dumps(result_dict)
            except Exception as e:
                print json.dumps({"status" : "ERROR"})
                print e #debug
        else:
            print json.dumps({"status" : "ERROR", "debug": "Authentication Error"})

            return cursor

    @staticmethod
    def parent(json_line, cursor):
        globals().update(json_line)

        query = """SELECT superior FROM Employee WHERE id = %s """

        if pass_auth(admin, passwd, cursor):
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
                    "debug": "parent for id %d" %emp,
                    "data" : flattened_result_no_duplicates
                }

                print json.dumps(result_dict)
            except Exception as e:
                print json.dumps({"status" : "ERROR"})
                print e #debug
        else:
            print json.dumps({"status" : "ERROR", "debug": "Authentication Error"})

        return cursor

    @staticmethod
    def ancestors(json_line, cursor):
        globals().update(json_line)
    
        query = """SELECT superior FROM Employee WHERE id = %s """

        if pass_auth(admin, passwd, cursor):
            try:
                cursor.execute(query,[emp])
        
                result_parent = cursor.fetchone()
                result = []
                result.append(result_parent)

                while(result_parent != None): 
                    cursor.execute(query,[result_parent])
                    result_parent = cursor.fetchone()
                    result.append(result_parent)

                result = remove_none_elements_from_list(result)

                flattened_result = []
                for sublist in result:
                    for val in sublist:
                        flattened_result.append(val)

                flattened_result.sort()

                result_dict = {
                    "status":"OK",
                    "debug" : "ancestors",
                    "data" : flattened_result
                    }
                print json.dumps(result_dict)

            except Exception as e:
                print json.dumps({"status" : "ERROR"})
                print e #debug
        else:
            print json.dumps({"status" : "ERROR", "debug": "Authentication Error"})

        return cursor

    @staticmethod
    def ancestor(json_line, cursor):
        globals().update(json_line)
 
        query = "SELECT superior FROM Employee WHERE id = %s"

        if pass_auth(admin, passwd, cursor):
            
            try:
                cursor.execute(query,[emp1])
        
                result_parent = cursor.fetchone()
                result = []
                result.append(result_parent)

                while(result_parent != None):
                    cursor.execute(query,[result_parent])
                    result_parent = cursor.fetchone()
                    result.append(result_parent)

                result = remove_none_elements_from_list(result)

                flattened_result = []
                for sublist in result:
                    for val in sublist:
                        flattened_result.append(val)

                result_flag = False

                for x in range(0, len(flattened_result)):
                    if flattened_result[x] == emp2:
                        result_flag = True
                        break

                result_dict = {
                    "status":"OK",
                    "debug" : "ancestor",
                    "data" : result_flag
                    }

                print json.dumps(result_dict)

            except Exception as e:
                print json.dumps({"status" : "ERROR"})
                print e #debug
        else:
            print json.dumps({"status" : "ERROR", "debug": "Authentication Error"})

        return cursor

    @staticmethod
    def update(json_line, cursor):
        
        globals().update(json_line)

        query = "UPDATE Employee SET data = %s"
        
        if pass_auth(admin, passwd, cursor) or admin_auth(admin, emp, passwd, cursor): 
                
            try:
                cursor.execute(query, [newdata])
                print {"status" : "OK",
                "debug" : "update for id %d" %emp
                }
            except Exception as e:
                json.dumps({"status" : "ERROR"})
                print e
        else:
            print json.dumps({"status" : "ERROR", "debug": "Authentication Error"})

        return cursor

    @staticmethod
    def read(json_line, cursor):
        globals().update(json_line)

        query = "SELECT data FROM Employee WHERE id = %s"

        if pass_auth(admin, passwd, cursor) or admin_auth(admin. emp, passwd, cursor):
                
            try:
                cursor.execute(query, [emp])
                result = cursor.fetchall()

                flattened_result = ""
                for sublist in result:
                    for val in sublist:
                        flattened_result += str(val)

                result_dict = {
                    "status":"OK",
                    "debug" : "read for id %d" %emp,
                    "data" : flattened_result
                }
                print json.dumps(result_dict)
            except Exception as e:
                json.dumps({"status" : "ERROR"})
                print e #debug
        else:
            print json.dumps({"status" : "ERROR", "debug": "Authentication Error"})

        return cursor

    @staticmethod
    def descendants(json_line, cursor):
        globals().update(json_line)

        query = """
        with recursive cte
        as (select id FROM employee as e
        where superior = %s
        UNION ALL
        select e.id
        from employee as e
        join cte
        on e.superior = cte.id
        ) select * from cte;
        """
        if pass_auth(admin, passwd, cursor):
                
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
                    "debug" : "descendants for id %d" %emp,
                    "data" : flattened_result_no_duplicates
                }

                print json.dumps(result_dict)
            except Exception as e:
                print json.dumps({"status" : "ERROR"})
                print e #debug
        else:
            print json.dumps({"status" : "ERROR", "debug": "Authentication Error"})

        return cursor

    @staticmethod
    def remove(json_line, cursor):
        globals().update(json_line)

        query1 = """
        with recursive cte
        as (select id FROM employee as e
        where superior = %s
        UNION ALL
        select e.id
        from employee as e
        join cte
        on e.superior = cte.id
        ) DELETE FROM employee WHERE id IN (SELECT id FROM cte);
        """
        query2 =  "DELETE FROM employee WHERE id = %s"

        if pass_auth(admin, passwd, cursor) or admin_auth(admin, emp, passwd, cursor):
            try:
                cursor.execute(query1,[emp])
                cursor.execute(query2,[emp])
                
                print json.dumps({"status" : "OK"})
            
            except Exception as e:
                print json.dumps({"status" : "ERROR"})
                print e #debug
        else:
            print json.dumps({"status" : "ERROR", "debug": "Authentication Error"})



def main():
   
    for line in sys.stdin:

        function_name = json.loads(line).keys()[0]
        #print line #debug

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
