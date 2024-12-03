FROM python:latest

RUN pip install groq pyyaml paramiko && apt-get update && apt-get install net-tools && apt-get install -y iputils-ping
ENV GROQ_API_KEY="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"
COPY . /honeypot
WORKDIR /honeypot
CMD [ "python3","dispatcher.py" ]
