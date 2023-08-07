class Registry:
    def __init__(self, name):
        self.name = name
        self._module_dict = dict()
    
    def register_module(self, cls):
        name = cls.__name__
        if name in self._module_dict:
            # raise ValueError(f"{name} is already registered in {self.name}")
            return cls
        self._module_dict[name] = cls
        return cls

    def build(self, cfg):
        cls = self._module_dict.get(cfg["type"])
        if cls is None:
            raise KeyError(f"{cfg['type']} is not in the {self.name} registry")
        return cls(**cfg)

def build_from_cfg(cfg, registry):
    return registry.build(cfg)
