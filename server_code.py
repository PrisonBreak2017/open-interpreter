from interpreter import interpreter

#interpreter.llm.api_key = "sk--" #your are key here
interpreter.llm.api_base = "http://137.175.19.77:3000/v1" 
interpreter.llm.model = "gpt-4-32k-0314"
interpreter.auto_run = True
interpreter.verbose = True
interpreter.offline = True

def process_chat():
    
    #interpreter.chat("Plot AAPL and META's normalized stock prices") # Executes a single command

    #interpreter.messages = []
    #interpreter.chat("""Go through all the .docx files in my 'documents' folder
    #and replace every occurrence of 'Machine Learning' with 'AI'.""")
    
    """
    use selenium to get the content of https://github.com/KillianLucas/open-interpreter/blob/main/README.md
    """
    message = """Can you make a folder called documents and put five .docx files in it
and write a sentence about machine learning in each of them?"""


    "Plot AAPL and META's normalized stock prices"
    
    "Selenium is installed under current dir, use it to get the content of https://en.wikipedia.org/wiki/Tesla,_Inc. "
    
    'What are the last 3 BBC news headlines?'

    interpreter.messages = []
    interpreter.chat(message)

def run_server():
    interpreter.server()
if __name__ == "__main__":
    
    #process_chat()
    print("\nVisit http://localhost:8000/test to test the WebSocket endpoint.\n")
    run_server()

