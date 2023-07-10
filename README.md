# python-crossword
A repository that contains all the examples that go with a [Medium article called How to Craft Crosswords with Code - A Python, Pygame, and OpenAI API approach](https://medium.com/itnext/how-to-craft-crosswords-with-code-a-python-pygame-and-openai-api-approach-14406396eacc)

![crossword](/crossword.jpg "Crossword")

# Setting up Poetry

1. **Install Poetry**: Poetry is a Python dependency management tool. It handles setting up virtual environments and managing dependencies in Python projects. To install Poetry, you can use the following command in your terminal:

   ```bash
   curl -sSL https://install.python-poetry.org | python -

For Windows users, you can use PowerShell to install Poetry:

  ```bash
  (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
  ```
## Project Setup

### Clone the repository:
First, clone this repository to your local machine using git clone.

### Navigate to the project directory:
Change your current working directory to the cloned repository's location.

### Install Dependencies:
Now you can install the dependencies for this project using Poetry. In the project's root directory, run:

```
poetry install
```
This command reads the pyproject.toml file included in the project, which contains all the dependencies that the project needs. Poetry will set up a new virtual environment and install everything automatically.

### Running the Application
Activate the Poetry Shell: Once the dependencies are installed, activate the virtual environment that Poetry has created for your project:

```
poetry shell
```

Your prompt should change to indicate that you are in a new shell that Poetry has set up with the correct Python version and all the dependencies.

### Running a Python Script
You're now ready to run one of the Python scripts in the app directory. As an example, let's execute the main.py script which generates the crossword:

```
cd app
python main.py
```

This will generate a crossword puzzle, show the backtracking running and finalize with generating a PDF with the crossword puzzle.


