# MountainBot
Discord Bot for managing hiking trips

# Run

Clone the repo
```
git clone https://github.com/belfastkeyboard/MountainBot
cd MountainBot
```

Create a file globals.py with relevant information like your bot token and channel id, for example:


```
token = "discordbottoken"
filepath = "jsonfilesecretsetc"
channel_id = 8888  # discord channel id
```

Run GNU make
```
make
```

# Creating the Bot account and giving it permissions
Follow the guide [here](https://discordpy.readthedocs.io/en/stable/discord.html):

Required permissions:

- view channels
- send messages
- manage messages
- use application commands
- create events (may not be required)
- manage events (may not be required)

Required from OAuth URL Generator:
- tick 'bot'
- tick 'applications.commands'
