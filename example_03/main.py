from omegaconf import DictConfig, OmegaConf
import hydra


@hydra.main(version_base=None, config_path=".", config_name="config")
def my_app(cfg: DictConfig):
    assert cfg.node.loompa == 10  # attribute style access
    assert cfg["node"]["loompa"] == 10  # dictionary style access

    assert cfg.node.zippity == 10  # Value interpolation
    assert isinstance(cfg.node.zippity, int)  # Value interpolation type
    assert cfg.node.do == "oompa 10"  # string interpolation

    waldo = cfg.node.waldo  # raises an exception


if __name__ == "__main__":
    my_app()
