import discord
import asyncio
import os
import sys
import urllib.request
import io
from os.path import split as path_split

client = discord.Client()

home_dir = "C:/Users/cs18087/Documents/ProgramCode/Discord/あんゆり/"

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
        return em
    
    @asyncio.coroutine
    def send_msg(self, idol, content=None, tts=False, embed=None):
        content = str(content) if content is not None else None
        if embed is not None:
            embed = embed.to_dict()
        data = yield from client.http.send_message(server_dict[idol]["ch_id"], content, guild_id=server_dict[idol]["server_id"], tts=tts, embed=embed)
        message = client.connection._create_message(channel=client.get_channel(data.get('channel_id')), **data)
        return message
    
    @asyncio.coroutine
    def edit_msg(self, idol, id, content=None, embed=None):
        content = str(content) if content is not None else None
        embed = embed.to_dict() if embed else None
        data = yield from client.http.edit_message(id, server_dict[idol]["ch_id"], content, guild_id=server_dict[idol]["server_id"], embed=embed)
        client.connection._create_message(channel=client.get_channel(server_dict[idol]["ch_id"]), **data)

    def save_msg(self, idol, reception, send):
        file_name = home_dir + "msg_id_log/" + reception.timestamp.strftime("%Y-%m") + "/" + reception.timestamp.strftime("%d") + "/" + idol + ".txt"
        file_dir = os.path.dirname(file_name)
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        else:
            pass
        with open(file_name, "a", encoding="utf-8") as f:
            f.write(reception.id + "," + send.id + "\n")
    
    def search_msg(self, idol, msg):
        file_name = home_dir + "msg_id_log/" + msg.timestamp.strftime("%Y-%m") + "/" + msg.timestamp.strftime("%d") + "/" + idol + ".txt"
        with open(file_name, "r", encoding="utf-8") as f:
            line = f.readline()
            while line:
                line.strip("\n")
                line_list = line.split(",")
                if msg.id == line_list[0]:
                    id = line_list[1]
                    break
                else:
                    line = f.readline()
                    id = False
        return id

    def file_action(self, message, idol):
        file_list = list()
        opener = urllib.request.build_opener()
        opener.addheaders=[("User-Agent", "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0")]
        urllib.request.install_opener(opener)
        for sent_file in message.attachments:
            url = sent_file["proxy_url"]
            file_name = home_dir + "file_log/" + sent_file["filename"]
            urllib.request.urlretrieve(url=url, filename=file_name)
            file_list.append(file_name)
        return file_list

ayb = AnYuriBot()

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
    if message.author != client.user:
        idol_name = ayb.check_idol(message.channel.id)
        send_message = await ayb.send_msg(idol=idol_name, embed=ayb.get_embed(message))
        if message.attachments != list():
            file_list = ayb.file_action(message=message, idol=idol_name)
            channel = client.get_channel(server_dict[idol_name]["ch_id"])
            for fl in file_list:
                await client.send_file(channel, fl)
        else:
            pass
        ayb.save_msg(idol=idol_name, reception=message, send=send_message)
    else:
        pass

@client.event
async def on_message_edit(befor, after):
    if befor.author != client.user:
        idol_name = ayb.check_idol(befor.channel.id)
        id = ayb.search_msg(idol=idol_name, msg=befor)
        await ayb.edit_msg(idol=idol_name, id=id, embed=ayb.get_embed(after))

client.run("Token")
