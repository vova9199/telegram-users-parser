import requests
import json
from progress.bar import IncrementalBar
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty

api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'

session_file = 'my_account.session'  # Write the name of your session to use without authentication

client = TelegramClient(session_file, api_id, api_hash)
client.start()
client.connect()
print("Session started!")

chats = []
last_date = None
chunk_size = 200
groups = []

result = client(GetDialogsRequest(
    offset_date=last_date,
    offset_id=0,
    offset_peer=InputPeerEmpty(),
    limit=chunk_size,
    hash=0
))
chats.extend(result.chats)

for chat in chats:
    try:
        if chat.megagroup == True:
            groups.append(chat)
    except:
        continue

print('Choose a group to scrape members from:')
i = 0
for g in groups:
    print(str(i) + '- ' + g.title)
    i += 1

g_index = input("Enter the number of group/channel: ")
target_group = groups[int(g_index)]

print(f'Fetching members from "{target_group.title}"')
all_participants = []
all_participants = client.get_participants(target_group, aggressive=True)

users_info = {}
bar = IncrementalBar('Progress of fetching members: ', max=len(all_participants))

for participant in all_participants:
    # Извлекаем информацию о каждом пользователе
    user_id = participant.id
    username = participant.username
    phone = participant.phone
    first_name = participant.first_name
    last_name = participant.last_name

    # Создаем словарь с информацией о пользователе
    user_info = {
        "username": username,
        "phone": phone,
        "name": first_name,
        "last_name": last_name,
    }

    # Добавляем информацию о пользователе в словарь users_info
    users_info[user_id] = user_info

    bar.next()
bar.finish()

file_path = f'users_info_{target_group.title.replace("/", " ")}.json'

# Записываем словарь participants_info в файл JSON
with open(file_path, 'w', encoding='utf-8') as file:
    json.dump(users_info, file, ensure_ascii=False, indent=4)
    print('Members scraped successfully.')


# Функция определения пола через API
def get_gender_from_name(name):
    url = f"https://api.genderize.io/?name={name}"

    response = requests.get(url)
    data = response.json()

    if 'gender' in data:
        return data['gender']
    else:
        return "unknown"


def update_file(filename, new_data):
    with open(filename, 'r+') as file:
        existing_data = file.read().splitlines()
        updated_data = list(set(existing_data + new_data))

        file.seek(0)
        file.truncate()

        file.writelines(item + '\n' for item in updated_data)


# Чтение данных из файла JSON
with open(file_path, 'r', encoding='utf-8') as file:
    users_info = json.load(file)

# Фильтрация пользователей по полу
male_users = set()
female_users = set()

bar = IncrementalBar('Process of gender distribution', max=len(users_info.items()))
for user_id, user_info in users_info.items():
    username = user_info.get('username')
    name = user_info.get('name')

    if username is not None and name is not None:
        gender = get_gender_from_name(name)

        if gender == 'male':
            male_users.add(username)
        elif gender == 'female':
            female_users.add(username)

    bar.next()
bar.finish()

# Обновление файла male.txt
update_file('male.txt', male_users)

# Обновление файла female.txt
update_file('female.txt', female_users)
print('Gender distribution has been done! Check files (male.txt and female.txt)')
