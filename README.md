# Usage

- first run - program called with the --init parameter with following:    
database: "student",  
login: "init",   
password: "qwerty"  

```python
python program.py < test1.init.json
```

Creates table Employee and user "app" with desired privileges.

WARNING: database "student" with password "qwerty" should be created in PostgreSQL before first run!

- next runs - the input contains in the first row the call to the open function with the 
following  
login: "app",  
password: "qwerty",   
and then calling any API functions except open and root.

```python
python program.py < test1.in.json
```

