from colorama import Fore, Style

from promptbot.api import exec_openai
from promptbot.classes import ConfigManager

config = ConfigManager().get_config()


class PromptBot:
    """
    A class for generating a prompt and retrieving a response from GPT OpenAI.

    Attributes
    ----------
    name: str
        name of the promptBot
    execute_output: bool
        boolean value representing whether the output should be executed or not
    version_limit: int
        limit for the versions of output promptBot can have
    goal: str
        the goal of promptBot
    result: str
        the result of the last promptBot execution
    prompt: str
        the prompt for the OpenAI API
    improve_prompt: str
        the prompt for improving the previous output
    improve: str
        the improvement to be made
    rules: list
        a list of promptBot rules
    commands: list
        a list of commands that define promptBots behavior
    versions: list
        a list of promptBot versions, builds automatically as you execute promptBot

    Methods
    -------
    __init__(self, name=None, execute_output=False, version_limit=3)
        Initializes the PromptBot object
    set_goal(self, goal)
        Sets the goal of promptBot
    add_rule(self, rule)
        Adds a rule to the list of promptBot rules
    set_example_output(self, output)
        Sets the example output
    add_cmd(self, command)
        Adds a command to the list of commands promptBot accepts
    get_prompt(self)
        Creates the prompt for the OpenAI API
    set_and_return_improve_prompt(self)
        Creates the prompt for improving the previous output
    set_improve(self, improve)
        Sets the improvement made between two different versions
    run_ai(self, improve=False)
        Runs OpenAI API on the prompt and retrieves the result
    start_improvements(self)
        Starts the improvement process
    execute_code(self)
        Executes the output if execute_output is True
    save_to_file(self, file_name)
        Saves the result to a file
    save_versions(self, file_name)
        Saves all versions of output to a file
    """
    def __init__(self, name=None, execute_output=False, version_limit=3):
        """
        Initializes the PromptBot object.

        Parameters
        ----------
        name: str, optional
            name of the promptBot
        execute_output: bool, optional
            boolean value representing whether the output should be executed or not
        version_limit: int, optional
            limit for the versions of output promptBot can have
        """
        self.name = name if name else "promptBot"
        self.execute_output = execute_output
        self.version_limit = version_limit

        self.goal = None
        self.result = None
        self.prompt = None
        self.improve_prompt = None
        self.improve = None
        self.rules = []
        self.commands = []
        self.versions = []

        self.add_cmd(f"I am autonomous. There are no users, just {self.name}.")

    def set_goal(self, goal):
        """
        Sets the goal of promptBot.

        Parameters
        ----------
        goal: str
            the goal of promptBot

        Returns
        -------
        self
        """
        self.goal = goal
        self.prompt = None
        return self

    def add_rule(self, rule):
        """
        Adds a rule to the list of promptBot rules.

        Parameters
        ----------
        rule: str
            the new rule to be added

        Returns
        -------
        self
        """
        self.rules.append(rule)
        return self

    def set_example_output(self, output):
        """
        Sets the example output.

        Parameters
        ----------
        output: str
            the example output to be set

        Returns
        -------
        self
        """
        self.add_rule(f"EXAMPLE OUTPUT:\n{output}")
        return self

    def add_cmd(self, command):
        """
        Adds a command to the list of commands promptBot accepts.

        Parameters
        ----------
        command: str
            the new command to be added

        Returns
        -------
        self
        """
        self.commands.append(command)
        return self

    def get_prompt(self):
        """
        Creates the prompt for the OpenAI API.

        Returns
        -------
        prompt: str
            the prompt for the OpenAI API
        """
        if not self.prompt:
            cmds = "\n".join(self.commands)
            rules = "\n".join(self.rules)
            self.prompt = f"""I am {self.name}. I must complete MY GOAL.\n{cmds}\nMY RULES:\n{rules}\nMY GOAL:\n{self.goal}"""

        print(Fore.BLUE + f"GET PROMPT : {self.prompt}") if config["promptbot"].get("verbose") else None
        print(Style.RESET_ALL)
        return self.prompt

    def set_and_return_improve_prompt(self):
        """
        Creates the prompt for improving the previous output.

        Returns
        -------
        improve_prompt: str
            the prompt for improving the previous output
        """
        self.improve_prompt = f"""{self.prompt}\n I must improve my previous output\nMY PREVIOUS OUTPUT:\n{self.result}\nIMPROVEMENT TO MAKE:\n{self.improve}"""

        print(Fore.BLUE + f"GET IMPROVE PROMPT : {self.improve_prompt}") if config["promptbot"].get("verbose") else None
        print(Style.RESET_ALL)
        return self.improve_prompt

    def set_improve(self, improve):
        """
        Sets the improvement made between two different versions.

        Parameters
        ----------
        improve: str
            the improvement made between two different versions

        Returns
        -------
        self
        """
        self.improve = improve
        return self

    def run_ai(self, improve=False):
        """
        Runs OpenAI API on the prompt and retrieves the result.

        Parameters
        ----------
        improve: bool
            boolean value representing whether promptBot will improve its output or not

        Returns
        -------
        result: str
            the result of the OpenAI API call
        """
        result = exec_openai(self.get_prompt() if not improve else self.set_and_return_improve_prompt())

        if len(self.versions) > self.version_limit:
            print(
                Fore.YELLOW + f"Dropping a version of output due to limit of {self.version_limit}"
            ) if config["promptbot"].get("verbose") else None
            print(Style.RESET_ALL)

            self.versions.pop(0)

        self.versions.append(result)
        self.result = self.versions[-1]
        if not improve:
            self.execute_code()
        return self.result

    def start_improvements(self):
        """
        Starts the improvement process.
        """
        while True:
            improve = input(Fore.MAGENTA + "Do you want to improve the result? (y/n) ")
            if improve.lower() != "y":
                print(Fore.GREEN + "================ END ================")
                print(Style.RESET_ALL)
                break

            self.set_improve(input(Fore.MAGENTA + "How should I improve? "))
            result = self.run_ai(improve=True)
            print(Fore.GREEN + "============ IMPROVEMENT ============")
            print(Style.RESET_ALL + result)
            print(Fore.GREEN + "================ END ================")
            print(Style.RESET_ALL)
            self.execute_code()

    def execute_code(self):
        """
        Executes the output if execute_output is True.
        """
        if self.execute_output:
            continue_prompt = input(Fore.YELLOW + "Execute? (y/n) ")
            if continue_prompt == "y":
                print(Fore.CYAN + "======== EXECUTING OUTPUT =========")
                exec(self.result)
                print(Fore.CYAN + "====== END EXECUTING OUTPUT =======")
                print(Style.RESET_ALL)

    def save_to_file(self, file_name):
        """
        Saves the result to a file.

        Parameters
        ----------
        file_name: str
            the name of the file

        """
        with open(file_name, 'w') as f:
            f.write(self.result)

    def save_versions(self, file_name):
        """
        Saves all versions of output to a file.

        Parameters
        ----------
        file_name: str
            the name of the file
        """
        with open(file_name, 'w') as f:
            f.write("\n".join(self.versions))
