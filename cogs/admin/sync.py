import asyncio
import discord
import traceback
from discord.ext import commands

class Sync(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(
    name = "sync",
    description = "Sync app commands globally or guild-specifically"
  )
  async def sync(self, ctx : commands.Context, *, guild_ids : str = ""):
    if guild_ids != "":
      successful_syncs = []
      for guild_id in guild_ids.split(" "):
        try:
          guild = discord.Object(id = guild_id)
          await ctx.bot.tree.copy_global_to(guild = guild)
          await ctx.bot.tree.sync(guild = guild)
          successful_syncs.append(guild_id)
        except:
          continue
      embed = discord.Embed(
        description = f"Successfully synced app commands to the following guild(s) :\n{"\n".join([f"> ` {guild_id} `" for guild_id in successful_syncs])}",
        color = 0x39ff14
      )
    else:
      await ctx.bot.tree.sync()
      embed = discord.Embed(
        description = f"Successfully synced app commands globally",
        color = 0x39ff14
      )
    embed.set_author(
      name = self.bot.user.name,
      icon_url = self.bot.user.display_avatar
    )
    await ctx.reply(
      embed = embed,
      mention_author = False,
      delete_after = 5
    )
    await asyncio.sleep(5)
    await ctx.message.delete()

  @sync.error
  async def error(self, ctx, error):
    traceback.print_exc()

async def setup(bot):
  await bot.add_cog(Sync(bot))