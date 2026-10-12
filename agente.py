from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

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
message = ""
while (True):
  message = input("Usuário: ")
  message = message.lower()

  if (message == "sair" or message == "exit"):
    break

  llm_prompt = prompt.invoke({"history":history, "message":message})
  llm_answer = llm.invoke(llm_prompt)
  edit_content = llm_answer.content.replace("\n\n", "\n").replace("\n", "\n     ")
  edit_content = "\nLLM: " + edit_content + "\n"
  print(edit_content)
  history.append(("human", message.strip("\n").replace(",","")))
  history.append(("assistant", edit_content.replace("\n", " ").replace(",","").strip("\nLLM: ")))
  if (len(history) > 8):
    history.pop(1)
    history.pop(1)

csv_file = open("history.csv", "w")
csv_file.write(system[0] + "," + system[1] + "\n")
for element in history:
  csv_file.write(element[0] + "," + element[1] + "\n")
csv_file.close()
