# Theory of Mind Scenario Generator

This repository contains a script that generates unique scenarios, questions, and answers based on user input. It uses OpenAI's GPT-3 model to generate text and the dotenv library to manage environment variables.

The primary goal of this project is to improve question-answering performance in large language models (LLMs) by boosting their Theory-of-Mind (ToM) reasoning abilities. ToM refers to the understanding of agents' beliefs, goals, and mental states, which are essential for common-sense reasoning involving humans.

The script is inspired by the work titled "Boosting Theory-of-Mind Performance in Large Language Models via Prompting" by Shima Rahimi Moghaddam and Christopher J. Honey. This research measures the ToM performance of GPT-4 and three GPT-3.5 variants and investigates the effectiveness of in-context learning in improving their ToM comprehension.

## Requirements

- Python 3.6+
- OpenAI Python library (openai)
- dotenv library (python-dotenv)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/carterleffen/theory-of-mind.git
```

2. Install the required libraries:

```bash
pip install openai python-dotenv
```

3. Set your OpenAI API key in the `.env` file:

```ini
OPENAI_API_KEY=your_api_key_here
```

## Usage

Run the script:

```bash
python theory_of_mind.py
```

Enter a scenario and a question when prompted:

```
Please enter a scenario and a question: John believes that Mary stole his sandwich, but it was actually Peter. Is John's belief true or false?
```

The script will generate two random scenarios with their corresponding questions and answers. Then, it will generate an answer for the user's question, taking inspiration from the generated scenarios.

## How It Works

The script utilizes several classes and functions to perform its tasks:

1. **InputValidator**: Validates user input to ensure that it is a string containing a comma.
2. **APIKeyHandler**: Handles the OpenAI API key and checks that the API key is set.
3. **ScenarioGenerator**: Generates scenarios, questions, and answers using OpenAI's GPT-3 model.
4. **split_input**: Splits user input into a scenario and a question.
5. **process_answer**: Processes the generated answer by removing unnecessary text.
6. **display_scenarios**: Displays the generated scenarios.
7. **generate_answer**: Generates an answer based on the given prompt.
8. **main**: Main function that handles user input, input validation, scenario generation, and output display.

## Contributing

We welcome contributions to improve the scenario generator. If you have any suggestions or encounter any issues, please submit a pull request or open an issue on GitHub.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
