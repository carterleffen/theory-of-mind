import os
import re
import openai
from dotenv import load_dotenv
import csv
from io import StringIO

# Load environment variables from the .env file
load_dotenv()

# Constants
API_KEY = os.environ.get("OPENAI_API_KEY")
MODEL_NAME = "gpt-3.5-turbo"
temperature = 0.4
max_tokens = 2000
openai.api_key = API_KEY

def csv_to_dict(csv_string):
    """Convert a CSV string into a dictionary."""
    reader = csv.DictReader(StringIO(csv_string), delimiter='|')
    return next(reader)

def dict_to_csv(data_dict):
    """Convert a dictionary into a CSV string."""
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=data_dict.keys(), delimiter='|')
    writer.writeheader()
    writer.writerow(data_dict)
    return output.getvalue().strip()

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
    def __init__(self, user_scenario, user_question, iteration):
        self.user_scenario = user_scenario
        self.user_question = user_question
        self.iteration = iteration

    def generate(self):
        messages = [
            {"role": "system", "content": "You are an expert in problem solving and critical thinking. Use your skills, thinking step by step to answer the last question, taking inspiration from the previous scenarios. All output you generate is in CSV format."},
            {"role": "user", "content": f"Given the scenario \"{self.user_scenario}\" and \"{self.user_question}\", generate a completely random, unrelated scenario with its corresponding question and answer in iteration {self.iteration}. Please format your response as follows:\n\nScenario: ...\nQuestion: ...\nAnswer: ...\n\nAnd separate the scenario, question, and answer by new lines."}
        ]

        try:
            response = chat_completion(messages)
        except Exception as error:
            print(f"Error while generating scenario: {error}")
            return None

        generated_text = response['choices'][0]['message']['content'].strip()

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
    response = openai.ChatCompletion.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response

def split_input(input_text):
    messages = [
    {
        "role": "system",
        "content": """You are an expert in semantic understanding and analysis. You know exactly where the true question lies. You are an expert in logic and reason. Thinking step by step. 1. Extract [Question] from [Text]. 2. Add [Text] without [Question] to [Scenario]. 3. Output as follows:
        Scenario: [Scenario]
        Question: [Question]""",
    },
    {"role": "user", "content": input_text},
    ]

    try:
        response = chat_completion(messages)
    except Exception as error:
        print(f"Error while splitting input: {error}")
        return None, None

    generated_text = response['choices'][0]['message']['content'].strip()

    # Split the generated text based on different headers
    sections = re.split(r"\n(?:Scenario: |Question: )", generated_text)
    sections = [section.strip() for section in sections if section.strip()]

    if len(sections) < 2:
        print("Unexpected response from the model. It did not generate a complete scenario and question. Please try again.")
        print(f"Generated text: {generated_text}")  # For debugging purposes
        return None, None

    scenario = sections[0].replace("Scenario: ", "", 1)
    question = sections[1].replace("Question: ", "", 1)

    return scenario, question

def process_answer(answer):
    """
    Process the answer by removing unnecessary text.

    Args:
        answer (str): The answer to process.

    Returns:
        str: The processed answer.
    """
    return answer.strip()

def display_scenarios(scenarios):
    """
    Display the generated scenarios.

    Args:
        scenarios (list): A list of scenarios to display.
    """
    for i, scenario in enumerate(scenarios, start=1):
        print(f"\nAuto Generated Scenario {i}:")
        print(f"Scenario: \"{scenario['scenario']}\"")
        print(f"\nQ: {scenario['question']}")
        print(f"\nA: {scenario['answer']}\n")

def generate_answer(prompt):
    messages = [
        {"role": "system", "content": "You are an expert in problem solving and critical thinking. Use your skills, thinking step by step to answer the question, taking inspiration from the previous scenarios."},
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
    print("Theory of Mind + Thinking Step By Step - Proof of Concept\n")
    print("Provide a scenario and question you want answered.\n")
    print("Example: The morning of the high school dance Sarah placed her high heel shoes under her dress and then went shopping. That afternoon, her sister borrowed the shoes and later put them under Sarah's bed. When Sarah gets ready, does she assume her shoes are under her dress?\n")

    user_input = input("\nEnter your Scenario/Question: ")
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

    prompt = ""
    for i, scenario in enumerate(scenarios, start=1):
        prompt += f"Scenario {i}:\n\nScenario: \"{scenario['scenario']}\"\nQ: {scenario['question']}\nA: {scenario['answer']}\n\n"

    prompt += f"Scenario: {user_scenario}\nQuestion: {user_question}\nAnswer: ...\n\n"


    answer = generate_answer(prompt)

    if answer is not None:
        processed_answer = process_answer(answer)
        print(f"\nUser Scenario: {user_scenario}\n\nQ: {user_question}\n\nA: {processed_answer}\n")
    else:
        print("Could not generate an answer. Please try again.")

if __name__ == "__main__":
    main()
