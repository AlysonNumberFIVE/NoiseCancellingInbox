import openai 
import os
import prompts

openai.api_key = os.environ.get("OPENAI_KEY")


def summarise_text(email_objects: list,
        context:str="You are a helpful and cheerful assistant with an edge of sarcasm",
        model:str="gpt-4",
        tokens:int=3500):
    """
    Takes all the emails pulled from your Gmail inbox and begins to summarize them using
    GPT-4 (or whatever model you choose).

    :param: email_objects: The list of all the emails clumped together. Each list item is
        a contiguous collection of emails separated by the MAX_TOKEN_COUNT (see gmail.py)
    :param: context: The context to give the GPT-4 model a "persona" to follow. In this case
        the voice of the A.I journalist typing up the newsletter of your inbox.
    :param: model: The GPT-4 model being used. GPT-4 is recommended as GPT-3.5-turbo is
        unreliable in the formatting it returns.
    :param: tokens: The max number of GPT tokens being requested. A higher number will give
        you a more fleshed out newsletter.
    :return: The newly formatted email summaries for the contents of your inbox.
    """
    email_list = str()

    requesting = prompts.newsletter_prompt + '\n' + email_objects[0]
    for obj in email_objects:
        requesting = prompts.newsletter_prompt + '\n' + obj
        result = openai_call(requesting, model, context, tokens)
        email_list += result
        # hardcoded separator.
        email_list += '----------------\n'
  
    return email_list


def openai_call(prompt:str, model:str, context:str="", tokens=300):
    """
    Makes the call to OpenAI's API.
    
    :param: prompt: The prompt to send to GPT for processing/answering.
    :param: model: The GPT model being used.
    :param: tokens: The max amount of tokens being requested.
    :return: The response content from GPT.
    """
    messages = [
        {"role": "system", "content": context},
        {"role": "user", "content": prompt},
    ]
    response = openai.ChatCompletion.create(
        model=model, messages=messages,
        max_tokens=tokens, n=1, stop=None, temperature=0.8,
    )
    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.text}")
        return ""

    # TODO(FIVE): Return a boolean attached with this for better error handlnig.
    return response.choices[0].message['content']
