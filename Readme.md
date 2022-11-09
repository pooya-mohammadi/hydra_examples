# Hydra examples

Here I present the examples that I have tested so far.

## Highlights:
1) Override config parameters from command line(ex_01)
2) Config files are `yaml` files with `.yaml` extension(ex_01)
2) saves the modified config in `output` directory(ex_01)
3) @hydra.main(version_base=None, config_path=".", config_name="config")
   4) `config` is the name of the `config.yaml`. It must be in `config_path` dir.
5) Using `++` to override and existing item(ex_01)
3) switch between config files(default_config)
4) multi-run. Running multiple (default_config, config_store_example)
5) `???` must field in the future object type(ex_03)
6) different access types to features within code is given in ex_03
7) You can remove a default entry from the defaults list by prefixing it with `~`
8) Get the exact command to install the completion from --hydra-help. Currently, Bash, zsh and Fish are supported. We are relying on the community to implement tab completion plugins for additional shells.
9) Structure Configs:
   10) Union types are only partially supported (see OmegaConf docs on unions)
   11) 


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
### default config:
In this case, the config name must be specified, so that the code can read the default values!

The defaults are ordered:

    If multiple configs define the same value, the last one wins.
    If multiple configs contribute to the same dictionary, the result is the combined dictionary.
```gitignore
cd default_config
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
cd default_config
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

At the registration time, the values of the config class can be modified:
```python
from dataclasses import dataclass

from hydra.core.config_store import ConfigStore

@dataclass
class MySQLConfig:
    host: str = "localhost"
    port: int = 3306

cs = ConfigStore.instance()

# Using the type
cs.store(name="config1", node=MySQLConfig)
# Using an instance, overriding some default values
cs.store(name="config2", node=MySQLConfig(host="test.db", port=3307))
# Using a dictionary, forfeiting runtime type safety
cs.store(name="config3", node={"host": "localhost", "port": 3308})
```

### Hierarchical Static Configuration
Hierarchical configuration is possible with `hydra`

Examples:
```commandline
python main.py db.port=10 # tab completion works till the features!
```
```commandline
db:
  host: localhost
  port: 10
ui:
  title: My app
  width: 1024
  height: 768
```

### Config Group:
different group of configs can be created with in config store
```python
@dataclass
class MySQLConfig:
    ...

@dataclass
class PostGreSQLConfig:
    ...

@dataclass
class Config:
    # We will populate db using composition.
    db: Any

# Create config group `db` with options 'mysql' and 'postgreqsl'
cs = ConfigStore.instance()
cs.store(name="config", node=Config)
cs.store(group="db", name="mysql", node=MySQLConfig)
cs.store(group="db", name="postgresql", node=PostGreSQLConfig)

@hydra.main(version_base=None, config_name="config")
def my_app(cfg: Config) -> None:
    print(OmegaConf.to_yaml(cfg))
```
Here `db` has two options which none of them is default!

```commandline
cd config_group_configstore
python main.py
```
Output:
```commandline
db: ???
```
Select a db:
```commandline
python main.py +db=postgresql
```
Output:
```commandline
 python main.py +db=postgresql 
db:
  driver: postgresql
  host: localhost
  port: 5432
  timeout: 10
```
**Note:** The `+` is required because no default value for db is defined.

Using the following code, `db` can be initialized with a value:
```commandline
@dataclass
class DBConfig:
    host: str = "localhost"
    port: int = MISSING
    driver: str = MISSING
    
@dataclass
class Config:
    db: DBConfig
```
**Note:** 
1) Assign MISSING to a field to indicates that it does not have a default value. This is equivalent to the ??? literal we have seen in OmegaConf configs before.
2) Omitting a default value is equivalent to assigning MISSING to it, although it is sometimes convenient to be able to assign MISSING it to a field.


# References:
1) https://github.com/facebookresearch/hydra
2) https://hydra.cc/docs/intro/