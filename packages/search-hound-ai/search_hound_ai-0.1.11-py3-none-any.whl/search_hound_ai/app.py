import search_hound_ai
import typer

from dotenv import load_dotenv
from hound_client_commands import HoundClientCommands

load_dotenv()

def validate_env():
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    if OPENAI_API_KEY == None or OPENAI_API_KEY == '':
        print("OPENAI_API_KEY Environment Variable is not set.")
        exit(1)


def main():
    app = typer.Typer(name=search_hound_ai.__app_name__, add_completion=True)
    app_client = HoundClientCommands(app)
    app_client()


if __name__ == "__main__":    
    validate_env()
    main()


