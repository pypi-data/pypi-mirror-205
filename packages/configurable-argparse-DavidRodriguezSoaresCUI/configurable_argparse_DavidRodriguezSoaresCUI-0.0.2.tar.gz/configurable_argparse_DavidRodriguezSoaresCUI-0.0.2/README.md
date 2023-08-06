# [configurable_argparse](https://github.com/DavidRodriguezSoaresCUI/configurable_argparse) - Argparse-based way of CLI argument handling boosted by YAML reusable configurations

When writing a command-line Python script that needs to take many arguments, usability issues may arise:

- Tediousness: Especially if used often with mostly the same arguments
- Incompleteness: It's easy to miss arguments
- RTFM fatigue: having to often refer to documentation takes away from actually using the software
- Need to write execution scripts: Writing scripts with arguments is sensible but locks users into static configurations

Configurable argparse aims at offloading the "noise" (often used argument configurations) into "recipes" that can be reused, while retaining the ability to override what needs to be adapted (the "signal"), therefore giving the user an experience that allows to efficiently use the program.

## Example

This simple example is there show how to use configurable argparse and how it makes using

### With argparse

```
def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-t', '--nb_threads',
        type: int, default=4,
        help="Number of threads to use"
    )
    ...
    exclusive_group = parser.add_mutually_exclusive_group()
    exclusive_group.add_argument(
        '--verbose',
        action='store_true',
        help='Show all messages'
    )
    exclusive_group.add_argument(
        '--quiet',
        action='store_true',
        help='Show no messages'
    )
    parser.parse_args()

...

def main():
    args = get_args()
```

Usage example:

- Every time: `python example_program.py -t 4 --use_library=libabc --ignore=E123,E321 --add_src=/homes/user/documents/ --quality=0.65 --no_audio --quiet`

In this example, if the user wants to change an argument from run to run, the difference is lost in the "noise".

### With configurable_argparse

```
ARGPARSE_PARSER_ARGS = {"prog": "Example program"}
ARGPARSE_ARGUMENTS = [
    Argument(
        ('-t', '--nb_threads'),
        {
            'type': int,
            'default': 4,
            'help': "Number of threads to use"
        }
    ),
    ...
    ArgumentExclusiveGroup([
        Argument(
            '--verbose',
            {
                'action': 'store_true',
                'help': 'Show all messages'
            }
        ),
        Argument(
            '--quiet',
            {
                'action': 'store_true',
                'help': 'Show no messages'
            }
        )
    ])
]
...

def main():
    args = get_args(
        parser_args=ARGPARSE_PARSER_ARGS,
        arguments=ARGPARSE_ARGUMENTS,
        yaml_config_base=Path(__file__)
    )
```

Usage example:
- First run: `python example_program.py -t 4 --use_library=libabc --ignore=E123,E321 --add_src=/homes/user/documents/ --quality=0.65 --no_audio --quiet` (save config as `usual`)
- Subsequent runs: `python example_program.py --use_config=usual --quality=0.55`

In this example, if the user wants to change an argument from run to run, the difference is immediately apparent since the "noise" is abstracted away in a `usual` configuration.