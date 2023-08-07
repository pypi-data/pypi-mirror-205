import search_hound_ai
import typer

from dotenv import load_dotenv
from validate_env import validate_env

from hound_client_commands import HoundClientCommands

load_dotenv()

def main():
    app = typer.Typer(name=search_hound_ai.__app_name__, add_completion=True)
    app_client = HoundClientCommands(app)
    app_client()


if __name__ == "__main__":    
    validate_env()
    main()

