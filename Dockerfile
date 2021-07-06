FROM python:3.8.5
WORKDIR /app
COPY . ./
RUN pip install discord.py python-dotenv
ENTRYPOINT [ "python", "main.py" ]