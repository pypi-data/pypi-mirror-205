class Config:
    def __init__(self, config_dict):
        for k, v in config_dict.items():
            setattr(self, k, v)

    @classmethod
    def fromfile(cls, filepath):
        file_globals = {}
        with open(filepath) as f:
            exec(f.read(), file_globals)
        config_dict = {k: v for k, v in file_globals.items() if not k.startswith("__")}
        
        return cls(config_dict)