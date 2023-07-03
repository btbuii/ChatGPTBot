import openai
import discord
import asyncio
from discord import app_commands

# Set up the OpenAI API client
openai.api_key = "KEY"

"""| INITIALIZATION |"""
MY_GUILD = discord.Object(id = 381609335291379725)
global toggled 
toggled = False

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents = intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild = MY_GUILD)
        await self.tree.sync(guild = MY_GUILD)
    
intents = discord.Intents.all()
client = MyClient(intents = intents)

"""| ON READY |"""
@client.event
async def on_ready():
    await client.change_presence(status = discord.Status.online, activity = discord.Game("AI online!"))
    print("----------")
    print(f'{client.user} has connected to Discord!')

@client.tree.command(name = 'toggle', description = "Toggle use of GPT")
async def toggle(interaction: discord.Interaction):
    global toggled 
    # Allow only authorized users to toggle use of ChatGPT
    if interaction.user.id != 259571192673861632:
        await interaction.response.send_message("You don't have permission to use that!")
    else:
        if toggled == False:
            toggled = True
            await interaction.response.send_message("Use of /gpt has been **Activated**")
        else:
            toggled = False
            await interaction.response.send_message("Use of /gpt has been **Deactivated**") 


@client.tree.command(name = "gpt", description = "Submit a query to the ChatGPT bot!")
async def gpt(interaction: discord.Interaction, message: str):
    global toggled
    if toggled == True:

        response = openai.Completion.create(
            engine = "text-davinci-003",
            prompt = message,
            max_tokens = 1024,
            temperature = 0.5
        )["choices"][0]["text"]

        embed = discord.Embed(
            title = f"ChatGPT-3 OpenAI: {message}",
            description = response,
            colour = 0xeeffee
        )

        embed.set_author(name = interaction.user.display_name, icon_url = interaction.user.avatar.url)
        embed.set_footer(text = "*Note: Use /gpt to submit a query! Keep in mind, this is not the full version of ChatGPT, so some features are limited. Instead, this bot is best for one-liner text-generation requests. (e.g. Asking simple questions, simple text completion, generation, conversation, search requests.) Due to limited APi / Discord capabilities, you won't be able to generate code or essays from this tool. Created within Wumbo using OpenAI ChatGPT-3 API.")

        await interaction.response.send_message(embed = embed)

    else:
        await interaction.response.send_message("Use of this command is currently disabled!")

@client.tree.command(name = "img", description = "Submit an image-generation request!")
async def img(interaction: discord.Interaction, message: str):
    global toggled
    if toggled == True:

        await interaction.response.send_message(f'Submitting image-generation request for: "{message}"...')

        response = openai.Image.create(
            prompt = message,
            n = 1,
            size = "1024x1024"
        )

        image_url = response['data'][0]['url']

        embed = discord.Embed(
            title = f"ChatGPT-3 OpenAI",
            description = message,
            colour = 0xeeffee
        )
        embed.set_image(url = image_url)
        embed.set_author(name = interaction.user.display_name, icon_url = interaction.user.avatar.url)
        embed.set_footer(text = "*Note: Use /img to submit an image-generation request! This command will generate an image by submitting a prompt to OpenAI's Image model. Keep in mind, this is not the full version of ChatGPT, so some features are limited. Created within Wumbo using OpenAI ChatGPT-3 API.")

        await interaction.followup.send(embed = embed)
    
    else:
        await interaction.response.send_message("Use of this command is currently disabled!")

client.run('TOKEN')