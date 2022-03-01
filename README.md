# Chismosa Bot 🤖


### Disclaimer ⚠️
This is the repo for my Discord bot that I code for fun. The bot is full of internal jokes that my friends and I have, so please do not take this project too seriously.

### About Chismosa ℹ️

<p>Chismosa was created mainly for handling roles for the members of our server, but over time, we decided it would be nice to allow the bot to store and send what we call "chismes" which is Spanish for "Gossip", we tought it was a good idea for keeping the members engaged. We wanted the bot to have a personality, so there are plenty of commands or messages that can be triggered by specific words found in our member's messages.</p>

<p>Chismosa consumes the senquoute API, does a role routine every 24 hours or everytime the server restarts, sends random chismes to the general channel, is able to count the days of each member, and uses a machine learning model for language processing wich allows the bot to reply to messages similar to what a human would say. </p>

---

### Libraries 📚

I mainly use this bot for practice, this is a list of the different libraries I used for coding the bot.

- discord.py
- youtubedl
- neuralintents
- datetime
- json
- request
- tensorflow
- pickle

---

## Commands 💻

| Command     | Arguments   | Description   |
| :---        | :---        | :---          |
|Chismosa I'm depressed | None | Chismosa will send you an inspirational message from the zenquotes API. |
| Chisme | None | Chismosa will send you a random chisme from our chisme database.|
| Days All | None | Chismosa will display a list with all the members' days in descending order |
| Days | Username | Chismosa will send you the days this user has in our server|
| My Days | None | Chismosa will send you the days you have in our server.
| Chismosa play | Song name | Chismosa will join the voice channel you're in, search for the song, and play it for you. |
| Chismosa pause | None | Chismosa will pause the song. |
| Chismosa resume | None | Chismosa will resume the song she was previously playing. |

---

### Authors 🧑‍💻

- [@Juan Camilo](https://github.com/Juansu01)
- [@Jason](https://github.com/jlucero805)
