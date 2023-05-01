"""
This script generates unique scenarios, questions, and answers based on user input. It
uses OpenAI's GPT-3 model to generate text and the dotenv library to manage environment variables.
"""

import os
import re
import json
import openai
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Constants
API_KEY = os.environ.get("OPENAI_API_KEY")
MODEL_NAME = "gpt-3.5-turbo"
temperature: 0.4
openai.api_key = API_KEY

class InputValidator:
    """
    Class to validate user input. Ensures that the input is a string containing a comma.
    """
    def __init__(self, input_text):
        """Initialize InputValidator with the input text."""
        self.input_text = input_text

    def validate(self):
        """
        Validate the input text.
        Returns True if the input is a string containing a comma, False otherwise.
        """
        if not isinstance(self.input_text, str) or "," not in self.input_text:
            print("Invalid input. Please enter a string containing a comma.")
            return False
        return True

class APIKeyHandler:
    """
    Class to handle the OpenAI API key. Checks that the API key is set.
    """
    def __init__(self):
        """Initialize APIKeyHandler."""
        pass

    def validate(self):
        """
        Validate the API key.
        Returns True if the API key is set, False otherwise.
        """
        if not API_KEY:
            print("API Key not found. Please set the OPENAI_API_KEY environment variable.")
            return False
        return True

class ScenarioGenerator:
    """
    Class to generate scenarios, questions, and answers. Uses OpenAI's GPT-3 model to generate text.
    """
    def __init__(self, user_scenario, user_question, iteration):
        """Initialize ScenarioGenerator with a user scenario, user question, and iteration number."""
        self.user_scenario = user_scenario
        self.user_question = user_question
        self.iteration = iteration

    def generate(self):
        """
        Generate a scenario, question, and answer. Returns a dictionary containing the scenario,
        question, and answer. If an error occurs during generation, returns None.
        """
        messages = [
            {"role": "system", "content": "You are an expert in problem solving and critical thinking. Use your skills, thinking step by step to answer the last question, taking inspiration from the previous scenarios. All output you generate is in JSON format."},
            {"role": "user", "content": f"Given the scenario \"{self.user_scenario}\" and \"{self.user_question}\", generate a completely random, unrelated scenario with its corresponding question and answer in iteration {self.iteration}. Please format your response as follows:\n\nScenario: ...\nQuestion: ...\nAnswer: ...\n\nAnd separate the scenario, question, and answer by new lines."}
        ]

        try:
            response = chat_completion(messages)
        except Exception as error:
            print(f"Error while generating scenario: {error}")
            return None

        generated_text = response['choices'][0]['message']['content'].strip()

        # Split the generated text based on different headers
        sections = re.split(r"\n(?:Scenario: |Question: |Answer: )", generated_text)
        sections = [section.strip() for section in sections if section.strip()]

        if len(sections) < 3:
            print("Unexpected response from the model. It did not generate a complete scenario, question, and answer. Please try again.")
            print(f"Generated text: {generated_text}")  # For debugging purposes
            return None

        scenario_data = {
            "scenario": sections[0].replace("Scenario: ", "", 1),
            "question": sections[1].replace("Question: ", "", 1),
            "answer": sections[2].replace("Answer: ", "", 1)
        }

        return scenario_data

def chat_completion(messages):
    """Function to call OpenAI API for a chat completion task."""
    response = openai.ChatCompletion.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=0.4,
        max_tokens=2000,
    )
    return response

def split_input(input_text):
    """
    Split the user input into a scenario and a question.

    Args:
        input_text (str): The user input.

    Returns:
        tuple: The scenario and question, or (None, None) if an error occurs.
    """
    messages = [
        {"role": "system", "content": "You are an expert in text analysis. Split the following text into a scenario and a question in JSON format."},
        {"role": "user", "content": input_text}
    ]

    try:
        response = chat_completion(messages)
    except Exception as error:
        print(f"Error while splitting input: {error}")
        return None, None

    json_text = response['choices'][0]['message']['content'].strip()

    try:
        scenario_data = json.loads(json_text)
    except json.JSONDecodeError:
        print("Error decoding JSON. Please try again.")
        return None, None

    return scenario_data.get("scenario"), scenario_data.get("question")


def process_answer(answer):
    """
    Process the answer by removing unnecessary text.

    Args:
        answer (str): The answer to process.

    Returns:
        str: The processed answer.
    """
    lines = answer.strip().split('\n')
    # Remove JSON-like objects from the answer
    cleaned_lines = []
    for line in lines:
        cleaned_line = re.sub(r"\{.*\}", "", line)
        cleaned_lines.append(cleaned_line.strip())

    return ' '.join(cleaned_lines)

def display_scenarios(scenarios):
    """
    Display the generated scenarios.

    Args:
        scenarios (list): A list of scenarios to display.
    """
    for i, scenario in enumerate(scenarios, start=1):
        print(f"\nScenario {i}:")
        print(f"Scenario: \"{scenario['scenario']}\"")
        print(f"\nQ: {scenario['question']}")
        print(f"\nA: {scenario['answer']}\n")

def generate_answer(prompt):
    """
    Generate an answer based on the given prompt.

    Args:
        prompt (str): The prompt to pass to the API.

    Returns:
        str: The generated answer, or None if an error occurs.
    """
    messages = [
        {"role": "system", "content": "You are an expert in problem solving and critical thinking. Use your skills, thinking step by step to answer the last question, taking inspiration from the previous scenarios. You output everything in JSON format."},
        {"role": "user", "content": prompt}
    ]

    try:
        response = chat_completion(messages)
    except Exception as error:
        print(f"Error while generating answer: {error}")
        return None

    answer = response['choices'][0]['message']['content'].strip()
    return answer

def main():
    """
    Main function to generate and display scenarios based on user input. 
    Handles user input, input validation, scenario generation, and output display.
    """
    user_input = input("\nPlease enter a scenario and a question: ")
    validator = InputValidator(user_input)
    if not validator.validate():
        return

    user_scenario, user_question = split_input(user_input)

    if user_scenario is None or user_question is None:
        print("Could not split input into scenario and question. Please try again.")
        return

    api_key_handler = APIKeyHandler()
    if not api_key_handler.validate():
        return

    scenarios = []
    for i in range(1, 3):  # Generate two scenarios
        scenario_generator = ScenarioGenerator(user_scenario, user_question, i)
        scenario = scenario_generator.generate()
        if scenario is None:
            print("No scenario generated.")
            return
        scenarios.append(scenario)

    display_scenarios(scenarios)

    # Create a new prompt with user_scenario, user_question, and the generated scenarios
    prompt = ""
    for i, scenario in enumerate(scenarios, start=1):
        prompt += f"Scenario {i}:\n\nScenario: \"{scenario['scenario']}\"\nQ: {scenario['question']}\nA: {scenario['answer']}\n\n"

    prompt += f"Scenario: {user_scenario}\nQuestion: {user_question}\n...\nAnswer: "

    answer = generate_answer(prompt)

    if answer is not None:
        processed_answer = process_answer(answer)
        print(f"User Scenario: {user_scenario}\n\nQ: {user_question}\n\nA: {processed_answer}\n")
    else:
        print("No answer generated.")

if __name__ == "__main__":
    main()
