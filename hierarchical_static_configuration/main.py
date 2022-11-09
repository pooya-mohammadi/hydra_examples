from dataclasses import dataclass
import hydra
from hydra.core.config_store import ConfigStore
from omegaconf import OmegaConf


@dataclass
class MySQLConfig:
    host: str = "localhost"
    port: int = 3306


@dataclass
class UserInterface:
    title: str = "My app"
    width: int = 1024
    height: int = 768


@dataclass
class MyConfig:
    db: MySQLConfig = MySQLConfig()
    ui: UserInterface = UserInterface()


cs = ConfigStore.instance()
cs.store(name="config", node=MyConfig)


@hydra.main(version_base=None, config_name="config")
def my_app(cfg: MyConfig) -> None:
    print(OmegaConf.to_yaml(cfg))


if __name__ == "__main__":
    my_app()
