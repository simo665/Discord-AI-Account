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



## Note:
Note that the bot will take a brief delay before starting to type, mimicking human behavior. The delay is randomized between 5–10 seconds before it starts typing, and an additional 3–8 seconds during typing. and ofc you can change that
