#!python3.6
import os, sys
import datetime
import requests, json
import discord

info = {
    "anna" : {
        "ch" : "",
        "url" : ""
    },
    "yuriko" : {
        "ch" : "",
        "url" : ""
    }
}

TOKEN = ""

report_ch_id = ""

class Bot():
    def __init__(self, client:discord.Client):
        self.client = client
        self.set_ch_url()

    def set_ch_url(self):
        self.ch_url = {info["anna"]["ch"] : info["yuriko"]["url"], info["yuriko"]["ch"] : info["anna"]["url"]}

    async def boot_action(self):
        self.set_channel()
        await self.check_permissions()

    def set_channel(self):
        self.anna_ch = self.client.get_channel(info["anna"]["ch"])
        self.yuriko_ch = self.client.get_channel(info["yuriko"]["ch"])
        self.report_ch = self.client.get_channel(report_ch_id)

    async def check_permissions(self) -> bool:
        if not self.anna_ch.permissions_for(member).read_messages:
            await self.permission_error("杏奈")
        if not self.yuriko_ch.permissions_for(member).read_messages:
            await self.permission_error("百合子")
    
    async def permission_error(self, idol:str):
        await self.client.send_message(self.report_ch, idol + "サーバーでのメッセージを読む権限がありません。")

    async def launch_report(self):
        content = "{0} has started. \nStartup time: {1}".format(self.client.user.name, datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
        await self.client.send_message(self.report_ch, content)

    def action(self, msg:discord.message):
        url = self.ch_url.get(msg.channel.id)
        if url is None:
            return None
        content = self.create_content(msg)
        self.send(url, send)
        
    def create_content(self, msg:discord.message):
        return {
            "username" : msg.author.name,
            "avatar_url" : msg.author.avatar_url,
            "content" : msg.content
        }
    
    def send(self, url:str, content:dict):
        content = json.dumps(content)
        requests.post(url, content, headers={'Content-Type': 'application/json'})         

client = discord.Client()
bot = Bot(client)

@bot.event
async def on_ready():
    print("start")
    await bot.boot_action()

@client.event
async def on_message(message):
    bot.action(message)

bot.run(TOKEN)
