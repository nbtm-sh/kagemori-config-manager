import yaml, os

class KagemoriConfigManager:
    INCLUDE_KEYWORD = "include-config"
    MAPPING = {
        "str": str,
        "bool": bool,
        "int": int,
        "float": float
    }
    def __init__(self, config_file_path=None, write_on_change=True, validate_mandatory_on_change=True, create_if_not_exists=True, allow_file_inclusions=True):
        self.data = {}
        self.config_file_path = config_file_path
        self.write_on_change = write_on_change
        self.validate_mandatory_on_change = validate_mandatory_on_change
        self.create_if_not_exists = create_if_not_exists
        self.allow_file_inclusions = allow_file_inclusions

        if config_file_path is not None:
            self.load_full()

    def defaults(self):
        return {}

    def mandatory(self):
        return {}

    def __delitem__(self, attr):
        old_state = self.data.copy()

        del self.data[attr]
        self.assert_me(old_state)
        del old_state
            
        if self.write_on_change:
            self.write()

    def __getitem__(self, key):
        return self.data[key]
    
    def __setitem__(self, key, value):
        old_state = self.data.copy()

        self.data[key] = value
        self.assert_me(old_state)
        del old_state
            
        if self.write_on_change:
            self.write()

    def write(self):
        with open(self.config_file_path, "w") as config_fp:
            yaml.dump(self.data, config_fp, default_flow_style=False)

    def load_full(self):
        if not os.path.exists(self.config_file_path):
            self.write()

        self.data = KagemoriConfigManager._load_config(self.config_file_path)
        self.data = KagemoriConfigManager.assert_defaults(self.defaults(), self.data)
        mandatory_data = KagemoriConfigManager.assert_mandatory_values(self.mandatory(), self.data)

        if len(mandatory_data) > 0:
            print(mandatory_data)

        self.write()

    def assert_me(self, old_state):
        if self.validate_mandatory_on_change:
            self.data = KagemoriConfigManager.assert_defaults(self.defaults(), self.data)
            mandatory = KagemoriConfigManager.assert_mandatory_values(self.mandatory(), self.data)
            if (mandatory):
                self.data = old_state
                raise KagemoriConfigManager.MandatoryAssertionFailed(f"Failed to assert the following values: {mandatory}")
            del mandatory

    @staticmethod
    def _load_config(path, allow_file_inclusions=False):
        with open(path, "r") as config_fp:
            return yaml.safe_load(config_fp)

    @staticmethod
    def _find_inclusions_paths(values):
        result = {}
        for key in values.keys():
            if key == KagemoriConfigManager.INCLUDE_KEYWORD:
                result[key] = values[key]
            elif isinstance(values[key], dict):
                result[key] = KagemoriConfigManager._find_inclusion_paths(values[key])
        return result

    @staticmethod
    def assert_defaults(defaults, data):
        result = data
        for key in defaults.keys():
            if key not in data:
                result[key] = defaults[key]
            elif isinstance(defaults[key], dict):
                result[key] = KagemoriConfigManager.assert_defaults(defaults[key], data[key])
            else:
                result[key] = data[key]
        return result


    @staticmethod
    def assert_mandatory_values(values, data, path="."):
        result = []
        
        for key in values.keys():
            if key not in data:
                result.append(f"{path}{key}")
            elif isinstance(values[key], dict):
                result.extend(KagemoriConfigManager.assert_mandatory_values(values[key], data[key], path=f"{path}{key}."))
            elif not isinstance(data[key], values[key]):
                result.append(f"{path}{key}")
        return result
    
    class MandatoryAssertionFailed(Exception):
        pass
