import hydra
from omegaconf import DictConfig, OmegaConf


# config name must be provided
@hydra.main(version_base=None, config_path="conf", config_name="config")
def my_app(cfg: DictConfig) -> None:
    print("beautiful yaml format:")
    print(OmegaConf.to_yaml(cfg))
    print("dict form:")
    print(cfg)


if __name__ == '__main__':
    my_app()
