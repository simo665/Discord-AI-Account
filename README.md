# Discord AI-SELF-BOT


___



## Introduction 
Hello, this repository files will make you able to make your a human (not a discord bot) discord account to respond to users automatically using llm (Large language models) through Groq API. 

## Futures

- **AI-Powered Chat:** Uses the Groq AI model to generate human-like responses.
- **Short-Term Memory:** Remembers recent user interactions within a channel.
- **Custom Instructions:** Behavior can be tailored using instructions loaded from a configuration file.
- **Multi-API Support:** Automatically switches to backup APIs in case of errors.
- **Asynchronous Message Handling:** Processes multiple messages in a queue to avoid spamming.
- **Public and Private Interactions:** Responds in both direct messages and public channels when mentioned.

---

## **Setup Instructions**

### **1. Prerequisites**
- Python 3.8 or higher installed.
- A Discord bot token.
- A Groq API key (or multiple keys for failover).
- `pip` for installing dependencies.

---

### **2. Installation**

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Edit the .env file and fill up the following requirements:**
```
TOKEN_lora=<Your Discord Bot Token>
API1=<Groq API Key 1>
API2=<Groq API Key 2>  # Optional
API3=<Groq API Key 3>  # Optional
```

3. **Edit instructions (optional):**
   got to file at `configs/instructions_lora.txt` to specify the bot’s behavior.

 
#### 4. **Running the Bot**
To start the bot, follow these steps:
0. **Open a Terminal or Command Prompt**
  Use your system's terminal or command prompt to navigate to the project folder.
1. **Install requirements**
   install bot requirements using this command:
```bash
pip install requirements.txt
```
2. **Navigate to the Project Director.**
   Use the cd command to move to the directory where your bot's code is located. For example:
```bash
cd path/to/your/project
```
3. **Run the Bot**
   Use the following command to start the bot:
```bash
python Main.py
```
4. **Verify the Bot is Running**
   If everything is set up correctly, you should see the bot log in and print a message in the terminal:
```bash
Logged in as <Bot's Username>
```


## Contributing
Feel free to submit issues or pull requests for improvements and bug fixes.

## Note:
Note that the bot will take a brief delay before starting to type, mimicking human behavior. The delay is randomized between 5–10 seconds before it starts typing, and an additional 3–8 seconds during typing. and ofc you can change that
