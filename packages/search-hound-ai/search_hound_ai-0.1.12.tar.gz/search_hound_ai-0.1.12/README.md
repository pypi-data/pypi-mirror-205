# SearchHoundAI  🐕 

A CLI for GPT with a focus on simplicity and ease of use. For developer just wanting to use gpt in there command line.

PIP Package: [Search Hound AI](https://pypi.org/project/search-hound-ai/)

## Installation

Install the CLI globally using pip: 

```bash
pip install search-hound-ai
```

## Usage

The CLI provides several commands for different purposes:

### Chat with GPT

Start a conversation with pip:

```bash
hound
```

Need assistance run:

```bash
hound --help
```

To use hound command:

```bash
hound [search string]
```

### Ask GPT

Ask GPT a question about a specific file:

```bash
hound [...your question here]
```

Example:

```bash
hound "How to purge docker container and images?"
```

## Setting Environment Variables

Required Environment Variable:

* OPENAI_API_KEY

I made some scripts to add Environment Variable to your machine easier.

These Bash scripts make it easy for developers to add a new environment variable to their `.bashrc` or `.zshrc` file.

The scripts prompt the user for the name and value of the environment variable they want to add, and then add the variable to the appropriate shell configuration file using the `echo` command.

Once the environment variable has been added to the shell configuration file, the scripts use the `source` command to reload the file and make the changes take effect.

To use the scripts, follow these steps:

1. Open a terminal window.
2. Navigate to the directory where the script is saved.
3. Run the following command to give the script execute permission:
    
    `chmod +x add_bash_env.sh` or `chmod +x add_zshrc_env`
    
    
4. Run the script by typing the following command and pressing Enter:

    ./add_zshrc_env.sh
    

5. Follow the prompts to enter the name and value of the environment variable you want to add to `.bashrc` or `.zshrc`.
6. Once the script has finished running, the environment variable will be added to the appropriate shell configuration file and available for use in your shell sessions.


## Contributions

Contributions to the SearchHoundAI CLI tool are welcome and encouraged. Please refer to the repository's [CONTRIBUTING.md](http://contributing.md/) file for more information on how to contribute.
