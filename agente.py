from langchain_ollama import ChatOllama
import csv

llm = ChatOllama(
    model        = "llama3.2:1b",
    temperature  = 0.7
)

csv_file = open("history.csv", "r+")
csv_reader = csv.reader(csv_file)
history = [tuple(row) for row in csv_reader]
csv_file.close()

prompt = ""
while (True):
  prompt = input("Usuário: ")
  prompt = prompt.lower()

  if (prompt == "sair" or prompt == "exit"):
    break

  history.append(("human", prompt.strip("\n").replace(",","")))
  print(history)
  llm_answer = llm.invoke(history)
  edit_content = llm_answer.content.replace("\n\n", "\n").replace("\n", "\n     ")
  edit_content = "\nLLM: " + edit_content + "\n"
  print(edit_content)
  history.append(("assistant", edit_content.replace("\n", " ").replace(",","")))
  if (len(history) > 3):
    history.pop(1)
    history.pop(1)

csv_file = open("history.csv", "w")
for element in history:
  csv_file.write(element[0] + "," + element[1] + "\n")
csv_file.close()
