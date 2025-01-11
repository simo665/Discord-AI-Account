import discord 
import asyncio
from discord.ext import commands
from main import load_accepted_channels, load_blocked_users, owner_id
import json



class Ai_Inter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.accepted_channels = []
        self.blocked_users = []
        
    def save_accepted_channels(self):
        with open("configs/accepted_channels.json", "w") as file:
            json.dump(self.accepted_channels, file)
            
    def save_blocked_users(self):
        with open("configs/blocked_users.json", "w") as file:
            json.dump(self.blocked_users, file)


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        prefix = self.bot.command_prefix
        if isinstance(error, commands.CommandNotFound):
            print(f"Oops! That command doesn't exist. Please check the available commands using `{prefix}help`.")
        else:
            # For other errors, you can log them or handle them differently
            raise error

    @commands.command(description="Add a channel where the self-bot will interact with users.")
    async def a(self, ctx, channel_id: int = None):
        try:
            self.accepted_channels = load_accepted_channels()
            # if a channel id provided 
            if channel_id:
                 # Check if it's already in the list
                if str(channel_id) in self.accepted_channels:
                    print(" • Channel id is already in the accepted channels list")
                    return 
                # Append channel id
                self.accepted_channels.append(str(channel_id))
                self.save_accepted_channels()
                print(" • Channel id is added successfully!")
                return
            # If no channel is provided 
            # Check if it's already in the list
            if str(ctx.channel.id) in self.accepted_channels:
                print(" • Channel id is already in the accepted channels list")
                return 
            # Append channel id
            self.accepted_channels.append(str(ctx.channel.id))
            self.save_accepted_channels()
            print(" • Channel id is added successfully!")
        except Exception as e:
            print("Error in 'Add channel' command", e)
            
    @commands.command(description="Remove a channel where the self-bot will interact with users.")
    async def r(self, ctx, channel_id: int = None):
        try:
            self.accepted_channels = load_accepted_channels()
            # if a channel id provided 
            if channel_id:
                 # Check if it's already in the list
                if not str(channel_id) in self.accepted_channels:
                    print(" • Channel id is not in the accepted channels list to be removed.")
                    return 
                # Append channel id
                self.accepted_channels.remove(str(channel_id))
                self.save_accepted_channels()
                print(" • Channel was removed successfully!")
                return
            # If no channel is provided 
            # Check if it's already in the list
            if not str(ctx.channel.id) in self.accepted_channels:
                print(" • Channel id is not in the accepted channels list to be removed")
                return 
            # Append channel id
            self.accepted_channels.remove(str(ctx.channel.id))
            self.save_accepted_channels()
            print(" • Channel id was removed successfully!")
        except Exception as e:
            print("Error in 'removing channel' command", e)
            
    @commands.command(description="Block a user from interacting with the bot.")
    async def block(self, ctx, user_id: int):
        self.blocked_users = load_blocked_users()
        # check if it's not the bot owner 
        if not str(ctx.author.id) == str(owner_id):
            return
        # check if the user already blocked 
        if str(user_id) in self.blocked_users:
            print("User already blocked.")
            return 
        # Add the id to the self.blocked_users list.
        self.blocked_users.append(str(user_id))
        self.save_blocked_users()
        print("User blocked successfully!")
        
    @commands.command(description="UnBlock a user from interacting with the bot.")
    async def unblock(self, ctx, user_id: int):
        self.blocked_users = load_blocked_users()
        # check if it's not the bot owner 
        if not str(ctx.author.id) == str(owner_id):
            return
        # check if the user already blocked 
        if not str(user_id) in self.blocked_users:
            print("User is not blocked.")
            return 
        # remove the id from the self.blocked_users list.
        self.blocked_users.remove(str(user_id))
        self.save_blocked_users()
        print("User unblocked successfully!")
        
        
async def setup(bot):
    await bot.add_cog(Ai_Inter(bot))