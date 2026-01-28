# kagemori-config-manager

Wrapper for reading and writing configuration files.

## Usage

### Direct usage

You can use the wrapper directly to manage configuration files like so

```python
import kagemori_config_manager
conf = kagemori_config_manager.KagemoriConfigManager("./myconfig.yaml")
print(conf["user"])

'Me!'
```

The wrapper will automatically write changes to the file by default. However, there are other (better) ways that you can use the wrapper

### Custom classes

The config manager supports setting default values and asserting variable types, like this

```python
import kagemori_config_manager

class MyConfig(kagemori_config_manager.KagemoriConfigManager):
    def defaults(self):
        return {
            "user": "me"
        }

    def mandatory(self):
        return {
            "user": str
        }

test_config = MyConfig("./myconfig.yaml")
```

In this instance, the wrapper will attempt to load `myconfig.yaml`. If this file does not exist, it will be created. Then, any unset default values will be set. Following, all mandatory values will be asserted. By default, mandatory and default assertions will be checked whenever changes are made.

## To-do

- [ ] Add support for file inclusions (#1)
- [ ] Add support for different file formats (#2)
- [ ] Add tests (#3) 
- [ ] Deploy to Pypi (#4)
- [ ] Improve documentation (#5)
