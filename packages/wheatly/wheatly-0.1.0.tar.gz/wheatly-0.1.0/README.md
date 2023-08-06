# Wheatly
## About
Wheatly is an approach to developing integration tests in a more natural way. While some technical knowledge is still required, this framework aims to allow for tests to be written using more of a natural language approach while still allowing for the flexibility needed to create robust tests.

# Usage
Create some directory you want to store you plugins in (see the `plugins` directory for examples). The only required plugin is a `config.py` file which takes the following form:

```python
lexicon = {
    'model': {
        'class': "Model",
        'tokens': [
            'model',
            'models',
        ],
        'actions': {
            'get': [
                'get',
                'gets',
                'getting',
                'got'
            ],
            'delete': [
                'delete',
                'deleted',
                'deleting',
                'deletes'
            ]
        },
        'modifiers': {}
    }
}
```

Each object in the lexicon variable should correspond to a same name file within the same plugin directory. Each of these files will represent some sort of object you want to work with (or an object to encapsulate various actions). They should take this form (notice that the name of the class matches the lexicon's `class` field):

```python
import config
import wheatly.utils as utils

class Model:
    def __init__(self):
        self.name = 'model'
        self.tokens = config.lexicon[self.name]['tokens']
        self.actions = config.lexicon[self.name]['actions']
        self.modifiers = config.lexicon[self.name]['modifiers']

    def action_get(self, context, logger, args={}, modifiers=[]):
        # perform get actions for this object
        print('get!')
        # return modified context and success or fail
        return context, True

    def action_delete(self, context, logger, args={}, modifiers=[]):
        # perform delete actions for this object 
        print('delete!')
        # return modified context and success or fail
        return context, True

    def __str__(self):
        return f'{self.name}()'

    def __repr__(self):
        return f'{self.name}()'
```

After writing any modules you want to use, create a test file with the following form:

```yaml
tests:
  example:
    # Execute some HTTP request
    - curl:
        host: https://pypi.org
        path: project/calligraphy-scripting
        method: get
        # Set this to a dictionary if you want to send some JSON data alone with the request
        data: ~
        response_type: html
    # Execute a wait with the duration in seconds
    - wait: 5
    # Text of what to do
    - get a model:
        # Optional dictionary for any arguments you want to pass along
        foo: bar
```

Currently you can use `curl` and `wait` to run custom globally available actions. You can also write natural language actions which Wheatly will parse and run via the plugins you wrote.

To run your test, first generate the test JSON via:

```bash
python src/main.py generate -p ./plugins -i examples/example.yaml -o examples/example.json
```

You can then run the generated test JSON via:

```
python src/main.py run -p ./plugins -i examples/example.json
```

# TODO: 

- [ ] Add summary command
