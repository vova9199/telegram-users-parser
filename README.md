<h1 align="center">Telegram Users Parser</h1>

<p align="left">
  Telegram User Parser is a project that allows you to gather information about users from a selected group or channel in Telegram and determine the gender of each user based on their name. The results are saved in the male.txt and female.txt files, which contain a list of usernames of the corresponding gender.

# Installation
1. Clone the repository to your local machine:
```shell
git clone https://github.com/vova9199/telegram-user-parser.git
```

2. Navigate to the project directory:
```shell
cd telegram-user-parser
```

3. Install the required dependencies:
```shell
pip install -r requirements.txt
```

# Configuration
1. Obtain your **'API_ID'** and **'API_Hash'** by registering an application at [Telegram API](https://my.telegram.org/auth).
2. Replace the **'YOUR_API_ID'** and **'YOUR_API_HASH'** values with your API ID and API Hash respectively in the **'main.py'** file.
```shell
api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'
```

# Usage
1. Run the main.py script:
```shell
python main.py
```
2. Follow the instructions in the terminal to log in to your Telegram account and select a group or channel to gather user information from.

    Infomation will be saved in JSON file **'users_GROUP_NAME.json'** this way:
```shell
 "user_id": {
        "username": "username",
        "phone": "phone",
        "name": "name",
        "last_name": "last name"
    },
  "user_id": {
        "username": "username",
        "phone": "phone",
        "name": "name",
        "last_name": "last name"
    },
  ...
```
3. The parsing results will be saved in the **'male.txt'** and **'female.txt'** files, which contain a list of usernames of the corresponding gender.
# Notes
- If the username or name is missing in the user information, the gender will not be determined.
- A third-party service or API based on the name is used to determine the gender of the user. Also you have limit 1000 requests a day.
