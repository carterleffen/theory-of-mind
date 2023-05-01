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
            {"role": "system", "content": "You are an expert in problem solving and critical thinking. Use your skills, thinking step by step to answer the last question, taking inspiration from the previous scenarios."},
            {"role": "user", "content": f"Given the scenario \"{self.user_scenario}\" and \"{self.user_question}\", generate a completely random, unrelated scenario with its corresponding question and answer in iteration {self.iteration}."}
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

def split_input(input_text):
    """
    Split the user input into a scenario and a question.

    Args:
        input_text (str): The user input.

    Returns:
        tuple: The scenario and question, or (None, None) if an error occurs.
    """
    scenario, question = input_text.split('\n', 1)
    return scenario.strip(), question.strip()

def generate_answer(prompt, model_name, temperature):
    messages = [
        {"role": "system", "content": "You are an expert in problem solving and critical thinking. Use your skills, thinking step by step to answer the last question, taking inspiration from the previous scenarios."},
        {"role": "user", "content": prompt}
    ]

    response = openai.ChatCompletion.create(
        model=model_name,
        messages=messages,
        temperature=temperature,
        max_tokens=500,
    )

    answer = response['choices'][0]['message']['content'].strip()
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

        user_scenario, user_question = split_input(input_text)

        scenarios = []
        for i in range(1, 3):
            scenario_generator = ScenarioGenerator(user_scenario, user_question, i, model_name, temperature)
            scenario = scenario_generator.generate()
            scenarios.append(scenario)

        prompt = f"Scenario: {user_scenario}\nQuestion: {user_question}\n...\nAnswer: "
        final_answer = generate_answer(prompt, model_name, temperature)

        output_data.append({
            'id': id,
            'model_name': model_name,
            'temperature': temperature,
            'input_text': input_text,
            'input_scenario': user_scenario,
            'input_question': user_question,
            'generated_scenario1': scenarios[0]['scenario'],
            'generated_question1': scenarios[0]['question'],
            'generated_answer1': scenarios[0]['answer'],
            'generated_scenario2': scenarios[1]['scenario'],
            'generated_question2': scenarios[1]['question'],
            'generated_answer2': scenarios[1]['answer'],
            'final_answer': final_answer
        })

    fieldnames = ['id', 'model_name', 'temperature', 'input_text', 'input_scenario', 'input_question', 'generated_scenario1', 'generated_question1', 'generated_answer1', 'generated_scenario2', 'generated_question2', 'generated_answer2', 'final_answer']

    with open('output.csv', 'w', newline='') as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=fieldnames, delimiter='|')
        writer.writeheader()
        writer.writerows(output_data)

if __name__ == "__main__":
    main()

