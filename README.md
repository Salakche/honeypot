# LLM based honeypot

My LLM honeypot project is an advanced cybersecurity tool designed to simulate a realistic SSH server environment using a Large Language Model (LLM). It leverages Python libraries such as Paramiko, threading, and YAML to handle connections, simulate system responses, and log interactions for analysis. This project aims to study attacker behavior by creating an interactive and believable environment, making it an invaluable resource for researchers and cybersecurity enthusiasts looking to analyze malicious tactics and improve system defenses.

## Workflow Summary

### 1. Opening the SSH Port
The honeypot opens a non-standard SSH port using Python's `socket` library, serving as the entry point for connections. The system is secured and isolated to prevent unauthorized access to the underlying network.

### 2. Establishing the SSH Connection
Incoming SSH connection attempts are managed using the `Paramiko` library, which simulates a functional SSH server. Authentication is configured to accept any credentials, leading attackers into a controlled session.

### 3. Capturing and Redirecting Inputs
Attacker commands are intercepted via the SSH session and processed by the LLaMA3 model via Groq Cloud API. Using advanced chat-completion, the model generates realistic and contextually appropriate system responses.

### 4. Logging Inputs and Outputs
All interactions, including commands and generated responses, are logged into files for analysis. These logs are essential for understanding attack patterns and improving cybersecurity measures.

## Features
- **Realistic SSH Environment:** Simulates an authentic command-line interface.
- **Interactive LLM Responses:** Processes attacker commands and generates contextual responses.
- **Secure and Isolated Setup:** Prevents unauthorized access to the underlying system.
- **Comprehensive Logging:** Captures all interactions for post-attack analysis.

## Requirements
- Python 3.8+
- Libraries: `Paramiko`, `socket`, `threading`, `os`, `argparse`, `yaml`

## Setup 
Setup your libraries and API key, Please visit [here](https://console.groq.com/keys) to create an API Key:
```
~$ # Install requirements
~$ pip install -r requirements.txt
~$ # Configure your API key as an environment variable
~$ export GROQ_API_KEY=<your-api-key-here>
```

## Usage
Clone the repository and follow the instructions in the `README` to deploy the honeypot. Ensure you configure the SSH port and security settings as needed.
