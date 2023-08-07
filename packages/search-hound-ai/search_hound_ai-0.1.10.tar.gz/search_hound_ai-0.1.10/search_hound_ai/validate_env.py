import os

def validate_env():
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    if OPENAI_API_KEY == None or OPENAI_API_KEY == '':
        print("OPENAI_API_KEY Environment Variable is not set.")
        exit(1)
