
import re
import tiktoken
from datetime import datetime, timedelta

encoding = tiktoken.encoding_for_model("gpt-4")

def extract_urls(text):
    """
    Extracts all URLs from text.
    :param: text: The text to scan for all URLs.
    :return: All the URLs in the text body.
    """

    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    return url_pattern.findall(text)


def remove_urls(text):
    """
    Remove all URLs in the text.
    :param: text: The text to scan for URLs.
    :return: The original text without any URLs in the body.
    """
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    return url_pattern.sub(r'', text)


def num_tokens_from_string(string: str) -> int:
    """
    Returns the number of tokens in a text from a GPT-4 perspective.
    :param: string: The string of text to calculate.
    :return: The number of GPT-4 tokens this text will make use of.
    """

    num_tokens = len(encoding.encode(string))
    return num_tokens


def last_monday():
    """
    Only pull emails from the latest Monday.
     (
        last Monday night,
        yea, we danced on table tops
        and we took too many shots
        thnk we kissed but I forgot
        ...
    )
    return: Returns the exact date of last Monday night.
    """
    today = datetime.today()
    last_monday = today - timedelta(days=today.weekday() + 3)
    return last_monday.strftime('%Y/%m/%d')


def find_first_url(text):
    """
    Find the very first URL in a body of text.
    :param: text: The body of text to scan through.
    :return: The very first URL we find.
    """

    url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    urls = re.findall(url_pattern, text)
    return urls[0] if urls else None


def extract_image_urls(text):
    """
    Extracts all URLs that point to images.
    :param: text: The body of text to scan through.
    :return: All image URLs found.
    """
    url_regex = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    
    # Find matches in text
    urls = re.findall(url_regex, text)
    print("IMAGE URL S================================ ", urls)
    # Filter for image URLs
    image_urls = [url for url in urls if url.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'))]
    
    return image_urls
