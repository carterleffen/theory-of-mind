# Enhancing Theory of Mind in Large Language Models: A Python Solution - Proof of Concept / Experiment

This repository presents a Python script that enhances Theory of Mind (ToM) performance in Large Language Models (LLMs) by leveraging in-context learning techniques described in the paper: [Boosting Theory-of-Mind Performance in Large Language Models via Prompting](https://arxiv.org/pdf/2304.11490.pdf) by [Shima Rahimi Moghaddam](https://twitter.com/Shima_RM_) and [Christopher J. Honey](https://twitter.com/chrishoney). ToM is a crucial aspect of human-like reasoning that allows understanding of agents' beliefs, goals, and mental states. Improving LLMs' ToM performance is essential for common-sense reasoning and enabling effective interactions with humans.

I've included a sample CSV output of the script running through 20 scenarios.

## Features

- **Automatic Splitting**: Our script accepts paragraphs combining scenario and question, and automatically splits them into separate scenario and question components using the LLM.
- **Scenario Generation**: The Python script generates two example scenarios, with questions and answers, using the LLM and the automatically split scenario and question as inspiration.
- **In-Context Learning**: The script utilizes in-context learning techniques to improve LLMs' ToM comprehension by providing prompts with two-shot chain of thought reasoning and step-by-step thinking instructions. Generated scenarios, questions, and answers are fed into the prompt automatically to assist in answering the user's question.

## Variants

- **theory-of-mind.py**: Accepts your scenario & question as a paragraph and provides two scenarios followed by the answer to your question.
- **theory-of-mind-csv.py**: Processes multiple questions using an input.csv template. Select the model type (gpt-3.5-turbo or gpt-4), temperature, and the questions (with scenario) to be answered. After processing, an output.csv is saved, which can be viewed in Google Sheets, Excel, or your favorite tool.

## How It Works

1. Write your scenario and question combined as a paragraph.
2. The script automatically splits the paragraph into separate scenario and question components.
3. The LLM generates two example scenarios, with questions and answers, inspired by the split scenario and question.
4. Utilizing in-context learning techniques, the script improves LLMs' ToM comprehension.
5. The generated scenarios, questions, and answers are fed into the prompt automatically to assist in answering the user's question.

## Usage

1. Clone the repository.
2. Install the required dependencies.
3. Run `theory-of-mind.py` for single questions or `theory-of-mind-csv.py` for batch processing using input.csv.

## Background

Despite LLMs' success in various tasks, they struggle with complex reasoning tasks such as Theory of Mind. This Python script enhances LLMs' ToM performance by using in-context learning approaches like step-by-step thinking, few-shot learning, and chain-of-thought reasoning. Improving ToM performance in LLMs contributes to the overall reliability of their reasoning in a wide range of everyday applications.

By providing appropriate prompts for in-context learning, all RLHF-trained LLMs exceeded 80% ToM accuracy, with GPT-4 reaching 100%. These results demonstrate the effectiveness of appropriate prompting in enhancing LLM ToM reasoning and highlight the context-dependent nature of LLM cognitive capacities.
