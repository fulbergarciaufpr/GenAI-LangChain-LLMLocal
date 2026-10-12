from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

import csv

llm = ChatOllama(
    model        = "llama3.2:1b",
    temperature  = 0.7
)

csv_file = open("history.csv", "r+")
csv_reader = csv.reader(csv_file)
system = tuple(next(csv_reader))
history = [tuple(row) for row in csv_reader]
csv_file.close()

prompt = ChatPromptTemplate([system,\
                            ("placeholder", "{history}"),\
                            ("human", "{message}")])
output_parser = StrOutputParser()

chain = prompt | llm | output_parser

message = ""
while (True):
  message = input("Usuário: ")
  message = message.lower()

  if (message == "sair" or message == "exit"):
    break

  edit_content = chain.invoke({"history":history, "message":message}).replace("\n\n", "\n").replace("\n", "\n     ")
  print("\nLLM: " + edit_content + "\n")
  history.append(("human", message.strip("\n").replace(",","")))
  history.append(("assistant", edit_content.replace("\n", " ").replace(",","")))
  if (len(history) > 8):
    history.pop(1)
    history.pop(1)

csv_file = open("history.csv", "w")
csv_file.write(system[0] + "," + system[1] + "\n")
for element in history:
  csv_file.write(element[0] + "," + element[1] + "\n")
csv_file.close()
