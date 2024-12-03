import os
from groq import Groq
import yaml
import argparse
from datetime import datetime
from time import sleep
import random
import subprocess
import os
import subprocess
import tempfile

def initialize_llm():
    global client, identity, prompt, messages

    client = Groq(api_key="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",)
    
    with open('personalitySSH.yml', 'r', encoding="utf-8") as file:
        identity = yaml.safe_load(file)
    
    identity = identity['personality']
    prompt = identity['prompt']
    parser = argparse.ArgumentParser(description = "Simple command line with llama3-70b")
    parser.add_argument("--personality", type=str, help="A brief summary of chatbot's personality", default= prompt)
    
    args = parser.parse_args()
    
    initial_prompt = f"You are a Linux OS terminal. Your personality is: {args.personality}."
    messages = [{"role": "system", "content": initial_prompt}]
    
    chat_completion0 = client.chat.completions.create(
    		    messages=messages,
    		    model="llama3-70b-8192",
    		)
    		
    data = chat_completion0.choices[0].message.content
    print(data,end="")
    return data

def llm(message):
    logs = ""
    if message != "":
        messages.append({
	    "role": "user",
		    "content": message,
               })
        chat_completion = client.chat.completions.create(
                            messages=messages,
                            model="llama3-70b-8192",
                        )

        data = chat_completion.choices[0].message.content
        line = []
        lines = data.split('\n')
        if "will be reported" in data:
            print(data,end="")
            raise KeyboardInterrupt 
        for i in range(0, len(lines)-1):
            print(lines[i])
            logs = logs + lines[i]+"\n"
        print(lines[len(lines)-1],end="")
        messages.append({
             "role": "assistant",
             "content": data,
            })
    else:
        lines = data.split('\n')
        print(lines[len(lines)-1],end="")
    return lines[len(lines)-1], logs  


def add_chat(cmd,output):
    messages.append({
              "role": "user",
              "content": cmd,
              })
    messages.append({
              "role": "assistant",
              "content": output,
                       })
    
    
    
	
	
	
