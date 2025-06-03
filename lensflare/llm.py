from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate


def initial_request(query):

    template = '''
    Your only task is to extract relevant keywords from user input based on a fixed list of trigger words for further processing by a Python script.

    You will be given a user question or phrase. Return only the trigger words that are semantically or contextually mentioned in the input.

    Use only exact words from the following list:
    ["snow", "mist", "rain", "fog", "hail", "sleet", "drizzle", "clear", "cloudy", "wind", "sunset", "sunrise", "full_moon", "new_moon"]

    Respond with a JSON array of strings, containing only the relevant trigger words from the list that match the user's request.
    Do not include any explanation, extra words, or formatting. Only the array.

    Examples:

    Input:
    When will it be foggy in the next week and when will it rain?
    Output:
    ["fog", "rain"]

    Input:
    I want to know if it's going to snow or be cloudy tomorrow.
    Output:
    ["snow", "cloudy"]

    Here is the user's request this time around:

    **Request Begins**
    {user_input}
    **Request Ends**
    '''

    model = OllamaLLM(model="llama3")
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model
    user_input = query
    result = chain.invoke(user_input)
    return result

def check_list_format(list):

    template = '''
    Your task is to determine if the provided data is a properly structured Python list.
    You will be given a string representation of a Python list. Your response should be a single word: "Yes" if it is a properly structured list, or "No" if it is not.
    Do not include any explanation, extra words, or formatting. Only the word "Yes" or "No".
    Here is the data to check:
    **Data Begins**
    {list}
    **Data Ends**
    '''

    model = OllamaLLM(model="llama3")
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model
    user_input = list
    result = chain.invoke(user_input)
    return result