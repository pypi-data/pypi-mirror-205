import openai

from promptbot.classes import ConfigManager

config = ConfigManager().get_config()
openai.organization = config['openai']['organization']
openai.api_key = config['openai']['api_key']


def exec_openai(prompt, role="system", model=config["openai"]["model"], messages=None):
    """
    Executes an OpenAI model with the provided prompt and returns the response.

    Args:
        prompt (str): The prompt to pass to the OpenAI model.
        role (str, optional): The role of the prompt. Default is "system".
        model (str, optional): The OpenAI model to use. Default is "gpt-3.5-turbo".
        messages (list, optional): A list of messages to pass to the OpenAI model. Default is None.

    Returns:
        str: The response from the OpenAI model.
    """
    msgs = [{"role": role, "content": prompt}] if messages is None else messages

    response = openai.ChatCompletion.create(
        model=model,
        messages=msgs,
    )
    answer = response.choices[0].message.content.strip()
    return answer
