import discord 
import asyncio
from discord.ext import commands
from main import accepted_channels


class Ai_Inter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="add_channel", description="Add a channel where the self-bot will interact with users.")
    async def a(self, ctx, channel_id: int = None):
        # if a channel id provided 
        if channel_id:
             # Check if it's already in the list
            if str(channel_id) in accepted_channels:
                print(" • Channel id is already in the accepted channels list")
                await ctx.message.delete()
                return 
            # Append channel id
            accepted_channels.append(str(channel_id))
            print(" • Channel id is added successfully!")
            await ctx.message.delete()
            return
        # If no channel is provided 
        # Check if it's already in the list
        if str(ctx.channel.id) in accepted_channels:
            print(" • Channel id is already in the accepted channels list")
            await ctx.message.delete()
            return 
        # Append channel id
        accepted_channels.append(str(ctx.channel.id))
        print(" • Channel id is added successfully!")
        await ctx.message.delete()
        
async def setup(bot):
    await bot.add_cog(Ai_Inter(bot))