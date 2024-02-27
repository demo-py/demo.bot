import discord
import traceback
from discord import app_commands, ui
from discord.ext import commands
from cogs.info.user import get_profile as get_owner

async def get_profile(guild : discord.Guild):
  guild_description = ""
  if guild.description:
    guild_description = f"\n>>> {guild.description}"
  embed = discord.Embed(
    title = guild.name,
    description = f"""
    **Guild Owner** : {guild.owner.mention}
    **Created** : <t:{int(guild.created_at.timestamp())}:R>
    **Bitrate Limit** : ` {int(guild.bitrate_limit // 1_000):,} ` kbps
    **File Size Limit** : ` {int(guild.filesize_limit // 1_000_000):,} ` MB
    **Roles** : ` {len(guild.roles):} `
    **Emojis** : ` {len(guild.emojis):,} ` / ` {guild.emoji_limit:,} `
    **Stickers** : ` {len(guild.stickers):,} ` / ` {guild.sticker_limit:,} `
    {guild_description}
    """,
    color = 0x2b2d31
  ).set_footer(
    text = f"Guild ID : {guild.id}"
  ).add_field(
    name = f"Channels : {len(guild.channels):,}",
    value = f"""
    > **Categories** : ` {len(guild.categories):,} `
    > **Forums** : ` {len(guild.forums):,} `
    > **Stages** : ` {len(guild.stage_channels):,} `
    > **Texts** : ` {len(guild.text_channels):,} `
    > **Voices** : ` {len(guild.voice_channels):,} `
    """,
    inline = True
  ).add_field(
    name = f"Members : {guild.member_count:,}",
    value = f"> **Humans** : ` {len([member for member in guild.members if not member.bot]):,} `\n> **Bots** : ` {len([member for member in guild.members if member.bot]):,} `",
    inline = True
  )
  if guild.banner:
    embed.set_image(
      url = guild.banner.url
    )
  if guild.icon:
    embed.set_thumbnail(
      url = guild.icon.url
    )
  if guild.vanity_url_code:
    embed.add_field(
      name = "Vanity URL Code :",
      value = f"> ` {guild.vanity_url_code} `",
      inline = True
    )
  return embed

async def get_banner(guild : discord.Guild):
  embed = discord.Embed(
    title = guild.name,
    color = 0x2b2d31
  )
  if guild.icon:
    embed.set_humbnail(
      url = guild.icon.url
    )
  if guild.banner:
    embed.set_image(
      url = guild.banner.url
    )
  return embed

async def get_icon(guild : discord.Guild):
  embed = discord.Embed(
    title = guild.name,
    color = 0x2b2d31
  ).set_image(
    url = guild.icon.url
  )
  return embed

class GuildProfileSelect(ui.Select):
  def __init__(self, guild : discord.Guild):
    self.guild = guild
    super().__init__(
      custom_id = "guild.profile.select",
      placeholder = "Select a property :",
      min_values = 1,
      max_values = 1,
      options = [
        discord.SelectOption(
          label = "Guild Profile",
          value = "guild.profile",
          default = True
        ),
        discord.SelectOption(
          label = "Guild Owner",
          value = "guild.owner",
          default = False
        )
      ]
    )
    if guild.banner:
      self.add_option(
        label = "Guild Banner",
        value = "guild.banner",
        default = False
      )
    if guild.icon:
      self.add_option(
        label = "Guild Icon",
        value = "guild.icon",
        default = False
      )

  async def callback(self, interaction : discord.Interaction):
    try:
      await interaction.response.defer(
        thinking = False,
        ephemeral = False
      )
      value = self.values[0]
      for ind, option in enumerate(self.options):
        if option.value != value:
          self.options[ind].default = False
        else:
          self.options[ind].default = True
      if value == "guild.profile":
        embed = await get_profile(self.guild)
        await interaction.edit_original_response(
          embed = embed,
          view = self.view
        )
      elif value == "guild.owner":
        embed = await get_owner(interaction, self.guild.owner)
        await interaction.edit_original_response(
          embed = embed,
          view = self.view
        )
      elif value == "guild.banner":
        embed = await get_banner(self.guild)
        await interaction.edit_original_response(
          embed = embed,
          view = self.view
        )
      elif value == "guild.icon":
        embed = await get_icon(self.guild)
        await interaction.edit_original_response(
          embed = embed,
          view = self.view
        )
    except:
      traceback.print_exc()

class Guild(commands.GroupCog, name = "guild", description = "/guild"):
  def __init__(self, bot):
    self.bot = bot

  @app_commands.command(
    name = "profile",
    description = "View the current guild's profile"
  )
  async def guild_profile(self, interaction : discord.Interaction):
    await interaction.response.defer(
      thinking = True,
      ephemeral = True
    )
    followup = interaction.followup
    guild = interaction.guild
    embed = await get_profile(guild)
    await followup.send(
      embed = embed,
      view = ui.View().add_item(GuildProfileSelect(guild))
    )

  @guild_profile.error
  async def error(self, interaction : discord.Interaction, error):
    traceback.print_exc()

async def setup(bot):
  await bot.add_cog(Guild(bot))