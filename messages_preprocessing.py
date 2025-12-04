import json

with open('chats/conversation_data.json', 'r') as file:
    data = json.load(file)

# print(json.dumps(data, indent=4))

# Extracting messages
Tylers_chats = []
Olivers_chats = []
for convo in data:
    if convo['sender_id'] == "Tyler":
        Tylers_chats.append(convo)
    if convo['sender_id'] == 'Oliver':
        Olivers_chats.append(convo)

with open('chats/Tylers_chats.json', 'w') as file:
    json.dump(Tylers_chats, file)
print("Extracted Tyler's chat messsages")
with open('chats/Olivers_chats.json', 'w') as file:
    json.dump(Olivers_chats, file)
print("Extracted Tyler's chat messsages")