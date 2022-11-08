# Hydra examples

Here I present the examples that I have tested so far.

## Highlights:
1) Override config parameters from command line(ex_01)
2) saves the modified config in `output` directory(ex_01)
3) switch between config files(ex_02)
4) multi-run. Running multiple 


## Instructions
### Example_01
#### Without command line:
```gitignore
cd example_01
python my_app.py
```
output:
```gitignore
beautiful yaml format:
db:
  driver: mysql
  user: pooya
  pass: secret

dict form:
{'db': {'driver': 'mysql', 'user': 'pooya', 'pass': 'secret'}}
```
#### With command line:
```
python my_app.py db.user=root db.pass=1234
```
output:
```
beautiful yaml format:
db:
  driver: mysql
  user: root
  pass: 1234

dict form:
{'db': {'driver': 'mysql', 'user': 'root', 'pass': 1234}}
```

### Example_02:
```gitignore
cd example_02
python my_app.py db=postgresql db.timeout=10
```
output:
```
beautiful yaml format:
db:
  driver: postgresql
  pass: drowssap
  timeout: 10
  user: postgres_user

dict form:
{'db': {'driver': 'postgresql', 'pass': 'drowssap', 'timeout': 10, 'user': 'postgres_user'}}
```
#### Multirun
```gitignore
cd example_02
python my_app.py --multirun db=mysql,postgresql
```
output:
```gitignore
[2022-11-08 11:39:59,931][HYDRA] Launching 2 jobs locally
[2022-11-08 11:39:59,931][HYDRA]        #0 : db=mysql
beautiful yaml format:
db:
  driver: mysql
  pass: drowssap
  timeout: 10
  user: mysql_user

dict form:
{'db': {'driver': 'mysql', 'pass': 'drowssap', 'timeout': 10, 'user': 'mysql_user'}}
[2022-11-08 11:39:59,973][HYDRA]        #1 : db=postgresql
beautiful yaml format:
db:
  driver: postgresql
  pass: drowssap
  timeout: 20
  user: postgres_user

dict form:
{'db': {'driver': 'postgresql', 'pass': 'drowssap', 'timeout': 20, 'user': 'postgres_user'}}
```






# References:
1) https://github.com/facebookresearch/hydra
2) https://hydra.cc/docs/intro/