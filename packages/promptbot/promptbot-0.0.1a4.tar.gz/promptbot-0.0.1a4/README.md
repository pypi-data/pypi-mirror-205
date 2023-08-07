# promptbot
A Novel way of creating ChatGTP bots.

## What is promptbot?

`promptbot` is a python package that allows you to quickly create bots using OpenAI's GPT models. 
It bootstraps a prompt for you and allows you to add rules and commands to the prompt.

## Why use promptbot?

`promptbot` is a great way to quickly create bots using OpenAI's GPT models to use in your cli applications. 
It also allows you to build very specific bots that can be used to automate tasks for yourself. 

## Building a basic bot

Here's a simple example that shows how to build a greeting bot using `promptbot`:

```python
from promptbot import PromptBot

bot = PromptBot()
bot.add_cmd("I am greeter bot. I come up with funny greetings for people.")
bot.add_rule("I can only output a JSON object.")
bot.add_rule("I must remember that my output will be consumed by python")
bot.set_example_output('{"greeting": "Hello, Johny! Awesome to meet a fellow dancer!"}')

bot.set_goal("Greet Bobby Jones")
print(bot.run_ai())
# example output : 
# {"greeting": "Hey there, Bobby Jones! How's it going, big guy?"}
```

This will output a response from the bot based on the commands, rules and the input data. 
You can experiment with different inputs to get different responses. 

## What makes up a bot?
1. `Commands` - you add them using .add_cmd(); They define the behaviour of the bot.
2. `Rules` - you add them using .add_rule(); They define the constraints of the bot.
3. `Example Output` - you set it using .set_example_output(); It defines the output structure of the bot.
4. `Goal` - you set it using .set_goal(); It defines what the bot should do.

That's it! With just a few lines of code, you can create your own bots using OpenAI's powerful GPT models.

## Installation

You can install `promptbot` using pip:

```
pip install promptbot
```

## Configuration

To use `promptbot`, you need to create a `promptbot.toml` file in the root of your project directory with your OpenAI API key. 

```toml
[openai]
organization="org-YoUrOrGaNiZaTiOn"
api_key="sk-YourApiKeyHeRe"
model="gpt-3.5-turbo"
[promptbot]
verbose=false
```

There is an example `promptbot.toml` file in the root of this repository that you can use as a template.

## Instantiation as a class

To create a bot as a class, you can do the following:

```python
from promptbot import PromptBot

class BreakdownBot(PromptBot):
    def __init__(self):
        super().__init__("BreakdownBot")
        self.add_cmd("I can breakdown any complex task into smaller tasks.")
        self.add_rule("I must output only a data structure in JSON format")
        self.add_rule("I cannot provide any dialog or request additional info")
        self.add_rule("I must output only in the example format.")
        self.set_example_output(f'[{{ "step": "1", "task": "The 1st task I create"}},'
                            f'{{ "step": "2", "task": "The 2nd task I create"}}]')

    def start(self, text):
        self.set_goal(text)
        return self.run_ai()
```