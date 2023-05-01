import os
import csv
import re
import openai
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Constants
API_KEY = os.environ.get("OPENAI_API_KEY")
openai.api_key = API_KEY

class ScenarioGenerator:
    def __init__(self, user_scenario, user_question, iteration, model_name, temperature):
        self.user_scenario = user_scenario
        self.user_question = user_question
        self.iteration = iteration
        self.model_name = model_name
        self.temperature = temperature

    def generate(self):
        messages = [
            {"role": "system", "content": "You are an creative story telling expert and problem solver. You follow instructions precisely. You always think step by step"},
            {"role": "user", "content": f"Given the scenario \"{self.user_scenario}\" and \"{self.user_question}\", generate a completely random, unrelated scenario with its corresponding question and answer in iteration {self.iteration}. For example, Scenario: 'A person is trying to decide which car to buy.' Question: 'What factors should they consider when choosing a car?' Answer: 'Some factors to consider when choosing a car include price, fuel efficiency, safety ratings, and personal preferences such as color and style.'"}
        ]

        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=messages,
            temperature=self.temperature,
            max_tokens=2000,
        )

        generated_text = response['choices'][0]['message']['content'].strip()
        sections = re.split(r"\n(?:Scenario: |Question: |Answer: )", generated_text)
        sections = [section.strip() for section in sections if section.strip()]

        scenario_data = {
            "scenario": sections[0].replace("Scenario: ", "", 1),
            "question": sections[1].replace("Question: ", "", 1),
            "answer": sections[2].replace("Answer: ", "", 1)
        }

        return scenario_data

def split_input_with_model(input_text, model_name, temperature):
    """
    Split the user input into a scenario and a question using the AI model.

    Args:
        input_text (str): The user input.
        model_name (str): The name of the AI model.
        temperature (float): The temperature for the AI model.

    Returns:
        tuple: The scenario and question, or (None, None) if an error occurs.
    """
    messages = [
        {"role": "system", "content": "You are an expert in text analysis. Split the following text into a scenario and a question."},
        {"role": "user", "content": input_text}
    ]

    try:
        response = openai.ChatCompletion.create(
            model=model_name,
            messages=messages,
            temperature=temperature,
            max_tokens=2000,
        )
    except Exception as error:
        print(f"Error while splitting input: {error}")
        return None, None

    text = response['choices'][0]['message']['content'].strip()
    split_text = text.split('\n', 1)

    if len(split_text) != 2:
        print("Error: AI model did not return a valid response. Please try again.")
        return None, None

    scenario, question = split_text
    return scenario.replace('\n', ' ').strip(), question.replace('\n', ' ').strip()

def generate_answer(generated_scenarios, user_scenario, user_question, model_name, temperature):
    # Build the initial messages with the system role
    messages = [{"role": "system", "content": "You are an expert in problem solving. You find solutions to problems by breaking them down and thinking about them logically."}]

    # Add each generated scenario, question, and answer to the messages
    for i, scenario in enumerate(generated_scenarios, start=1):
        messages.append({
            "role": "user",
            "content": f"Scenario {i}\nScenario: {scenario['scenario']}\nQuestion: {scenario['question']}\nAnswer: {scenario['answer']}"
        })

    # Add the user's scenario and question
    messages.append({
        "role": "user",
        "content": f"User Scenario:\nScenario: {user_scenario}\nQuestion: {user_question}"
    })

    # Request the chat completion
    response = openai.ChatCompletion.create(
        model=model_name,
        messages=messages,
        temperature=temperature,
        max_tokens=2000,
    )

    # Extract and return the answer
    answer = response.choices[0].message.get('content', '').strip()
    return answer

def main():
    with open('input.csv', 'r') as input_csv:
        reader = csv.DictReader(input_csv, delimiter='|')
        input_data = list(reader)

    output_data = []

    for data in input_data:
        id = data['Id']
        model_name = data['model_name']
        temperature = float(data['temperature'])
        input_text = data['input_text']

        user_scenario, user_question = split_input_with_model(input_text, model_name, temperature)

        scenarios = []
        for i in range(1, 3):
            scenario_generator = ScenarioGenerator(user_scenario, user_question, i, model_name, temperature)
            scenario = scenario_generator.generate()
            scenarios.append(scenario)

        final_answer = generate_answer(scenarios, user_scenario, user_question, model_name, temperature)

        output_data.append({
            'id': id,
            'model_name': model_name,
            'temperature': temperature,
            'input_text': input_text,
            'input_scenario': user_scenario,
            'input_question': user_question,
            'final_answer': final_answer,
            'generated_scenario1': scenarios[0]['scenario'],
            'generated_question1': scenarios[0]['question'],
            'generated_answer1': scenarios[0]['answer'],
            'generated_scenario2': scenarios[1]['scenario'],
            'generated_question2': scenarios[1]['question'],
            'generated_answer2': scenarios[1]['answer']
        })

    fieldnames = ['id', 'model_name', 'temperature', 'input_text', 'input_scenario', 'input_question', 'generated_scenario1', 'generated_question1', 'generated_answer1', 'generated_scenario2', 'generated_question2', 'generated_answer2', 'final_answer']

    with open('output6.csv', 'w', newline='') as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=fieldnames, delimiter='|')
        writer.writeheader()
        writer.writerows(output_data)

if __name__ == "__main__":
    main()
