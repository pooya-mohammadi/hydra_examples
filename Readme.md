# Hydra examples

Here I present the examples that I have tested so far.

## Highlights:
1) Override config parameters from command line(ex_01)
2) Config files are `yaml` files with `.yaml` extension(ex_01)
2) saves the modified config in `output` directory(ex_01)
3) @hydra.main(version_base=None, config_path=".", config_name="config")
   4) `config` is the name of the `config.yaml`. It must be in `config_path` dir.
5) Using `++` to override and existing item(ex_01)
3) switch between config files(ex_02)
4) multi-run. Running multiple (ex_02, config_store_example)
5) `???` must field in the future object type(ex_03)
6) different access types to features within code is given in ex_03


## Instructions

### Example_00
```commandline
cd example_00
python my_app.py +db.driver=mysql +db.user=omry +db.password=secret
```
Output:
```commandline
db:
  driver: mysql
  user: omry
  password: secret
```

**Notes:** 
1) The `+` indicates that the field is new.
2) DictConfig is an empty object!

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

using `++`:
```commandline
python my_app.py ++db.user=pooya_mohammadi
```
Output:
```commandline
db:
  driver: mysql
  user: pooya_mohammadi
  pass: secret
```

**Note:** No need for `+` because the params are already defined in `config.yaml`
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

### ConfigStore
ConfigStore is a singleton storing configs in memory. Instead of creating yaml files, one can create a dataclass and pass it to a `ConfigStore`
 It covers every aspect that is possible with `yaml` files configurations.
```commandline
class ConfigStore(metaclass=Singleton):
    def store(
        self,
        name: str,
        node: Any,
        group: Optional[str] = None,
        package: Optional[str] = "_group_",
        provider: Optional[str] = None,
    ) -> None:
        """
        Stores a config node into the repository
        :param name: config name
        :param node: config node, can be DictConfig, ListConfig,
            Structured configs and even dict and list
        :param group: config group, subgroup separator is '/',
            for example hydra/launcher
        :param package: Config node parent hierarchy.
            Child separator is '.', for example foo.bar.baz
        :param provider: the name of the module/app providing this config.
            Helps debugging.
        """
    ...
```

tests:
```commandline
python my_app.py +db=mysql db.user=pooya
```
output:
```commandline
db:
  driver: mysql
  user: pooya
  password: secret
```
#### Why do we use `+` before `db`?
Because we didn't define any default list for this example like the others. Therefore, the + will add this option to default list itself.

The `+` indicates that the field is new!

**Note:** default list for other examples are in `config.yaml`!

#### Run with parameter
```commandline
python my_app.py --multirun +db=mysql,postgresql ++db.user=Ali,Hassan
```
Output
```commandline
[2022-11-08 17:18:44,168][HYDRA] Launching 4 jobs locally
[2022-11-08 17:18:44,168][HYDRA]        #0 : +db=mysql ++db.user=Ali
db:
  driver: mysql
  user: Ali
  password: secret

[2022-11-08 17:18:44,209][HYDRA]        #1 : +db=mysql ++db.user=Hassan
db:
  driver: mysql
  user: Hassan
  password: secret

[2022-11-08 17:18:44,253][HYDRA]        #2 : +db=postgresql ++db.user=Ali
db:
  driver: postgresql
  user: Ali
  password: '*****'

[2022-11-08 17:18:44,294][HYDRA]        #3 : +db=postgresql ++db.user=Hassan
db:
  driver: postgresql
  user: Hassan
  password: '*****'
```

### Example_3 -> config-object types
```commandline
cd example_03
python main.py
```
Output:
```commandline
Traceback (most recent call last):
  File "my_app.py", line 32, in my_app
    cfg.node.waldo
omegaconf.errors.MissingMandatoryValue: Missing mandatory value: node.waldo
    full_key: node.waldo
    object_type=dict
```

### conf_group
```commandline
cd config_group
python my_app.py
```
output:
```commandline
{}
```
It's empty because config_name is not defined in the `my_app` file.

```commandline
python my_app.py +db=postgresql
```

output:
```commandline
db:
  driver: postgresql
  user: postgres_user
  password: drowssap
  timeout: 10
```

Overwrite:
```commandline
python my_app.py +db=postgresql db.timeout=20
```
Output:
```commandline
$ python my_app.py +db=postgresql db.timeout=20
db:
  driver: postgresql
  pass: drowssap
  timeout: 20
  user: postgres_user
```

# References:
1) https://github.com/facebookresearch/hydra
2) https://hydra.cc/docs/intro/