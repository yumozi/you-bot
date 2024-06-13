# You Bot

Deploying a simple bot of yourself on Discord

## Installation

```bash
git clone https://github.com/yumozi/you-bot.git
cd you-bot
pip install -r requirements.txt
```

## Getting Started
First, run construct_dataset.py to create a dataset of your messages.
```bash
python construct_dataset.py -n <number of messages>
```
Usually, 50 messages are enough to train the model that mimics your messaging style, but more messages can be used for better results.

Next, use OpenAI's API to finetune a GPT3.5 model on your dataset. The easiest way is to use their online UI, but you can also use the OpenAI API directly for this. After finetuning, replace the OPENAI_KEY variable in bot.py with your API key and the MODEL variable with your finetuned model ID.

Signup for MongoDB Atlas and create a database to store your messages. Create a new project and cluster, then create a database called "db1" in the cluster. Paste the MongoDB uri into the MONGO_URI variable in bot.py.

Finally, create an app on Discord and copy the token. Select the "send message" scope under Bot, and add the "bot" scope under Guild Install. Paste the token into the DISCORD_TOKEN variable in bot.py.

Now, simply run the bot and you're good to go!
```bash
python bot.py
```
