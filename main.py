from twitchio.ext import commands
from ollama_api import OllamaClient

class Bot(commands.Bot):
    # Change the URL if Ollama is running on a different machine.
    ollama_client = OllamaClient(base_url="http://localhost:11434")

    def __init__(self):
        # Get a token from https://twitchtokengenerator.com/ with scope chat:read and chat:edit
        super().__init__(token='YOUR_TOKEN_HERE', prefix='?', initial_channels=['CHANNEL_NAME'])

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    async def event_message(self, message):
        if message.echo:
            return

        ## Uncomment this if you want it to respond to all messages I guess.
        # response = self.ollama_client.generate_completion(model="llama3.1:latest", stream=False,
        #                                                   prompt=f'Keep responses short. Less than 500 characters. Prompt: {message.content}')
        # await message.channel.send(f'{response["response"][0:500]}')

        await self.handle_commands(message)

    @commands.command()
    async def ollama(self, ctx: commands.Context, *, prompt: str):
        print(f'{ctx.author.display_name} asked {prompt}')
        response = self.ollama_client.generate_completion(model="llama3.1:latest", stream=False, prompt=f'Keep responses short. Less than 500 characters. Prompt: {prompt}')
        await ctx.send(f'{response["response"][0:500]}')


bot = Bot()
bot.run()