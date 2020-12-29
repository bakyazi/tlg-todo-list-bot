# tlg-todo-list-bot
Telegram TODO list bot

## Screenshot
![usage](https://github.com/bakyazi/tlg-todo-list-bot/blob/master/todobot.png?raw=true)


## Usage
  - /start      : it starts your chat with bot
  - /help       : it is empty for now, you may add usage information in this part
  - /todo       : add a task into to-do list
  - /done       : move a task from to-do list to done list
  - /list       : list all to-do task
  - /done_list  : list all tasks in done-list

## Installation

### 1 - ***Create Telegram Bot via @botfather***
  - Open Telegram
  - Search botfather
  - Then type as below
  - ***Take note the bot token***
    
![botfather](https://github.com/bakyazi/tlg-todo-list-bot/blob/master/botfather.png?raw=true)

### 2- Create Heroku App
  - Create Heroku Account (https://signup.heroku.com/dc)
  - Download & Install Git if you have not have already.
  - Download & Install Heroku CLI.
  - Open terminal & navigate to project directory
  - Type
    ```heroku login``` and log in at opening login page.
  - Type ```heroku create```. In this stage you have to set name of your todo app.<br>Then you will have a webapp url such as https://appname.herokuapp.com/. 
  
### 3- MongoDB
  - Create MongoDB account (https://www.mongodb.com/)
  - Create a project
  - In project, create a cluster (***Note:*** you will determin your database, username and password in this stage)
  - After cluster create, click ***Connect*** button <br>
  ![mongo1](https://github.com/bakyazi/tlg-todo-list-bot/blob/master/mongo1.png?raw=true)
  - Then, ***Connect your application*** <br>
  ![mongo2](https://github.com/bakyazi/tlg-todo-list-bot/blob/master/mongo2.png?raw=true)
  - Lastly, it will generate the connection string after you choose python & version. You should replace your password & database name with related parts <br>
  ![mongo3](https://github.com/bakyazi/tlg-todo-list-bot/blob/master/mongo3.png?raw=true)
  
### 4- Code
Replace following variables with values you obtain above
  ```python
  TOKEN = 'YOUR-TELEGRAM-BOT-TOKEN'
  HEROKU_APP_URL = 'HEROKU-APP-URL'

  MONGODB_CLIENT = 'MONGODB-CONNECTION-URL'
  DB_NAME = 'DB-NAME'
  COLLECTION_NAME = 'COLLECTION-NAME'
  ```
  
  ### 5 - Deploy
  In project directory, type
  ```bash
  git init
  git add .
  git commit -m "first commit"
  heroku git:remote -a YourAppName
  git push heroku master
  ```

  
