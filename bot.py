import discord
import asyncio
import os

client = discord.Client()

# create server and channel info's dict
server_dict = dict()
server_dict["anna"] = {
    "ch_id" : "494526720402128899",
    "server_id" : "494526720402128897"
}
server_dict["yuriko"] = {
    "ch_id" : "494526830968307724",
    "server_id" : "494526830968307722"
}

class AnYuriBot:    
    def check_idol(self, id):
        if id == server_dict["anna"]["ch_id"]:
            return "yuriko"
        elif id == server_dict["yuriko"]["ch_id"]:
            return "anna"
        else:
            return False

    def get_embed(self, message):
        em = discord.Embed(type = "rich", timestamp = message.timestamp, description = message.content)
        if message.author.nick == None:
            name = message.author.name
        else:
            name = message.author.nick
        em.set_author(name = name, icon_url=message.author.avatar_url)
        del name
        return em
    
    @asyncio.coroutine
    def send_msg(self, idol, content=None, tts=False, embed=None):
        content = str(content) if content is not None else None
        if embed is not None:
            embed = embed.to_dict()
        data = yield from client.http.send_message(server_dict[idol]["ch_id"], content, guild_id=server_dict[idol]["server_id"], tts=tts, embed=embed)
        client.connection._create_message(channel=client.get_channel(data.get('channel_id')), **data)
        del data

@client.event
async def on_ready():
    print("+---------------------------+")
    print("|         login_info        |")
    print("+---------------------------+")
    print("|          BOT_info         |")
    print("| name: " + client.user.name + "        |")
    print("| ID: " + client.user.id + "    |")
    print("+---------------------------+")
    print("|      joined_server        |")
    for s in client.servers:
        print("| " + s.name)
    print("+---------------------------+")

@client.event
async def on_message(message):
    ayb = AnYuriBot()
    if message.author == client.user:
    else:
        idol_name = ayb.check_idol(message.channel.id)
        await ayb.send_msg(idol=idol_name, embed=ayb.get_embed(message))
        del idol_name

client.run("Token")
