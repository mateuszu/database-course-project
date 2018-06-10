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
                getattr(Function, function_name)(json.loads(line)[function_name], cursor)
            except Exception as e:
                print {"status" : "NOT IMPLEMENTED"}
                print e

if __name__ == "__main__":
    main()




if __name__ == "__main__":
    main()