
"""
import openai

# 确保设置了你的 OpenAI API key
openai.api_key = 'AIzaSyCPFUpXLI3tbXlOORQKlqsQdAJNusQBoyQ'
openai.api_base = 'http://137.175.94.175:8080/v1'
conversation = [
    {
        "role": "system",
        "content": "You are Open Interpreter, a world-class programmer that can complete any goal by executing code.\nFirst, write a plan. **Always recap the plan between each code block** (you have extreme short-term memory loss, so you need to recap the plan between each message block to retain it)."
    },
    {
        "role": "user",
        "content": "who are you "
    },
    {
        "role": "user",
        "content": "The code above was executed on my machine. It produced no text output. what's next (if anything, or are we done?"
    },
    {
        "role": "user",
        "content": "Code output:   Cell In[7], line 1\n    ```\n    ^\nSyntaxError: invalid syntax\n\n\nWhat does this output mean / what's next (if anything, or are we done?)"
    },
    {
        "role": "assistant",
        "content": "```python\n```\nimport sympy\nx = sympy.Symbol(\"x\")\nresult\n```"
    }
]

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=conversation,
    temperature=0.7
)

print(response)


import json
import requests

url = "http://137.175.94.175:8080/v1/chat/completions"

messages = {
  "system": [
    {
      "role": "system",
      "content": "You are Open Interpreter, a world-class programmer that can complete any goal by executing code.\nFirst, write a plan. **Always recap the plan between each code block** (you have extreme short-term memory loss, so you need to recap the plan between each message block to retain it)."
    }
  ],  
  "user": [
    {
      "role": "user",  
      "content": "solve an equation like 10x + 14 = 12"    
    },
    {
      "role": "user",
      "content": "The code above was executed on my machine. It produced no text output. what's next (if anything, or are we done?"
    },
    {
      "role": "user",
      "content": "Code output:   Cell In[7], line 1\n    ```\n    ^\nSyntaxError: invalid syntax\n\n\nWhat does this output mean / what's next (if anything, or are we done?)"
    }
  ],
  "assistant": [
    {
      "role": "assistant",
      "content": "```python\n```\nimport sympy\nx = sympy.Symbol(\"x\")\nresult\n```"   
    },
    {
      "role": "assistant",
      "content": " The error message `SyntaxError: invalid syntax`  means that there is something wrong with the syntax of your Python code."
    }
  ]
}

data = {
  "model": "gpt-3.5-turbo",
  "messages": messages,
  "temperature": 0.7
}

headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer AIzaSyCPFUpXLI3tbXlOORQKlqsQdAJNusQBoyQ'}

response = requests.post(url, data=json.dumps(data), headers=headers)

print(response.text)
"""

from interpreter import interpreter



interpreter.offline = True # Disables online features like Open Procedures
#interpreter.llm.model = "gpt-3.5-turbo" # Tells OI to send messages in OpenAI's format
interpreter.llm.model =  "gpt-4-32k-0314"  # map to gpt-4-coder 调用 coz 的coder bot
interpreter.llm.api_key = "sk-YdzPwOl5IXHWlq5AB1A4A26fEdA3471bBaE82483Dc0d1c1a" # LiteLLM, which we use to talk to LM Studio, requires this
interpreter.llm.api_base = "http://137.175.19.77:3000/v1" # Point this at any OpenAI compatible server

"""
interpreter.offline = True # Disables online features like Open Procedures
interpreter.llm.model = "gpt-3.5-turbo" # Tells OI to send messages in OpenAI's format
interpreter.llm.api_key = "AIzaSyCPFUpXLI3tbXlOORQKlqsQdAJNusQBoyQ" # LiteLLM, which we use to talk to LM Studio, requires this
interpreter.llm.api_base = "http://137.175.94.175:8080/v1" # Point this at any OpenAI compatible server
"""

interpreter.auto_run = True
#interpreter.auto_run = True
interpreter.verbose = True

def process_chat():
    
    #interpreter.chat("Plot AAPL and META's normalized stock prices") # Executes a single command

    #interpreter.messages = []
    #interpreter.chat("""Go through all the .docx files in my 'documents' folder
    #and replace every occurrence of 'Machine Learning' with 'AI'.""")
    
    """
    use selenium to get the content of https://github.com/KillianLucas/open-interpreter/blob/main/README.md
    """

    message = "search baidu with keyword AI and return the first result"
    
    'What are the last 3 BBC news headlines?'

    interpreter.messages = []
    interpreter.chat(message)

def run_server():
    interpreter.server()
if __name__ == "__main__":
    
    process_chat()
    #run_server()



