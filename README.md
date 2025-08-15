
# Multi-Agent Arxiv Chatbot

This project is a **multi-agent chatbot** designed to process user requests using a system of four specialized agents, providing structured and accurate responses to user queries.

## Description

The chatbot consists of a **multi-agent system** with the following agents:

1. **Coordinator Agent**: Manages user requests and coordinates the interaction between the other agents.
2. **Arxiv Agent**: Searches for information on Arxiv and gathers the most relevant research papers.
3. **Formatting Agent**: Organizes and formats the retrieved information to present it neatly to the user.
4. **Scientific Agent**: Processes the information provided by the Arxiv Agent. When a user asks a question, this agent thinks through the problem multiple times (2-3 iterations) before delivering a final answer.

The chatbot has **two versions**:

- **Terminal-based version** for command-line interaction.
- **Web-based version** running on a localhost server for web interaction.

## Goal

Provide a robust and intelligent chatbot capable of retrieving, processing, and presenting information from Arxiv in a structured and thoughtful manner, allowing users to ask complex questions and receive well-considered answers.

## Features

- Multi-agent system for structured and efficient information processing.
- Intelligent retrieval of research papers from Arxiv.
- Formatting and clean presentation of information.
- Scientific agent capable of multi-step reasoning before answering queries.
- Two user interfaces: terminal and web-based.
- **Flexible AI backend**: Uses Ollama with the Lama 3.1 model by default, but can also connect to **ChatGPT API, Anthropic, or a custom LLM** via Ollama.

## Technologies

- **Python**: Core implementation and agent logic.
- **CamelAI**: Library used to implement and manage the multi-agent system.
- **Ollama (Lama 3.1)**: Default model powering agent intelligence. Supports alternative LLMs via Ollama.
- **HTML, CSS, JavaScript**: For the web interface and localhost server.



