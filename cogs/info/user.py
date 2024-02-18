import discord
import traceback
from discord import app_commands, ui
from discord.ext import commands

async def get_profile(interaction : discord.Interaction, member : discord.Member):
  user = await interaction.client.fetch_user(member.id)
  member = interaction.guild.get_member(member.id)
  custom_activity = ""
  for activity in member.activities:
    if isinstance(activity, discord.CustomActivity):
      if member.bot:
        custom_activity = f"\n\n> {activity.state}"
      else:
        if activity.emoji:
          if activity.emoji.is_custom_emoji():
            activity_emoji = interaction.client.get_emoji(activity.emoji.id)
            if not activity_emoji:
              activity_emoji = activity.emoji
          else:
            activity_emoji = activity.emoji
        else:
          activity_emoji = ""
        custom_activity = f"\n\n> {activity_emoji} {activity.name if activity.name else ""}"
  flags = []
  if member.desktop_status not in [discord.Status.offline, discord.Status.invisible]:
    if member.desktop_status == discord.Status.online:
      emoji = interaction.client.get_emoji(1170180480679821322)
    elif member.desktop_status == discord.Status.idle:
      emoji = interaction.client.get_emoji(1170180477508931605)
    elif member.desktop_status in [discord.Status.dnd, discord.Status.do_not_disturb]:
      emoji = interaction.client.get_emoji(1170180475789254676)
    flags.append(str(emoji))
  if member.mobile_status not in [discord.Status.offline, discord.Status.invisible]:
    if member.mobile_status == discord.Status.online:
      emoji = interaction.client.get_emoji(1170224544057929839)
    elif member.mobile_status == discord.Status.idle:
      emoji = interaction.client.get_emoji(1170224541608443926)
    elif member.mobile_status in [discord.Status.dnd, discord.Status.do_not_disturb]:
      emoji = interaction.client.get_emoji(1170224538718568528)
    flags.append(str(emoji))
  if member.web_status not in [discord.Status.offline, discord.Status.invisible]:
    if member.web_status == discord.Status.online:
      emoji = interaction.client.get_emoji(1170206386009940018)
    elif member.web_status == discord.Status.idle:
      emoji = interaction.client.get_emoji(1170206378703466507)
    elif member.web_status in [discord.Status.dnd, discord.Status.do_not_disturb]:
      emoji = interaction.client.get_emoji(1170206381429764148)
    flags.append(str(emoji))
  if member.bot:
    if member.public_flags.verified_bot:
      emoji_left = interaction.client.get_emoji(1170282122892824656)
      emoji_right = interaction.client.get_emoji(1170282126386679878)
      flags.append(f"{emoji_left}{emoji_right}")
    else:
      emoji = interaction.client.get_emoji(1170282089346781244)
      flags.append(str(emoji))
  if member.public_flags.active_developer:
    emoji = interaction.client.get_emoji(1170279844060332142)
    flags.append(str(emoji))
  if member.public_flags.bug_hunter:
    emoji = interaction.client.get_emoji(1170282093520105532)
    flags.append(str(emoji))
  if member.public_flags.bug_hunter_level_2:
    emoji = interaction.client.get_emoji(1170282096833609728)
    flags.append(str(emoji))
  if member.public_flags.discord_certified_moderator:
    emoji = interaction.client.get_emoji(1170282098620383262)
    flags.append(str(emoji))
  if member.public_flags.early_supporter:
    emoji = interaction.client.get_emoji(1170282102810484736)
    flags.append(str(emoji))
  if member.public_flags.early_verified_bot_developer:
    emoji = interaction.client.get_emoji(1170282107789135892)
    flags.append(str(emoji))
  if member.public_flags.hypesquad:
    emoji = interaction.client.get_emoji(1207595530998255647)
    flags.append(str(emoji))
  if member.public_flags.hypesquad_balance:
    emoji = interaction.client.get_emoji(1170282109663969312)
    flags.append(str(emoji))
  if member.public_flags.hypesquad_bravery:
    emoji = interaction.client.get_emoji(1170285543511302154)
    flags.append(str(emoji))
  if member.public_flags.hypesquad_brilliance:
    emoji = interaction.client.get_emoji(1170282113573072916)
    flags.append(str(emoji))
  if member.public_flags.partner:
    emoji = interaction.client.get_emoji(1170282117293408348)
    flags.append(str(emoji))
  if member.public_flags.staff:
    emoji = interaction.client.get_emoji(1170282121080868914)
    flags.append(str(emoji))
  member_flags = " ".join(flags)
  embed_profile = discord.Embed(
    title = member.name,
    description = f"""
    **Member** : {member.mention} {member_flags}
    **Account Created** : <t:{int(member.created_at.timestamp())}:R>
    **Member Joined** : <t:{int(member.joined_at.timestamp())}:R>
    **Member Roles** : ` {len(member.roles):,} `
    {custom_activity}
    """,
    color = member.color
  ).set_thumbnail(
    url = member.display_avatar
  ).set_footer(
    text = f"User ID : {member.id}"
  )
  if user.banner:
    embed_profile.color = user.accent_color
    embed_profile.set_image(
      url = user.banner.url
    )
  return embed_profile

async def get_avatar(interaction : discord.Interaction, member : discord.Member):
  embed_avatar = discord.Embed(
    title = member.name,
    color = 0x2b2d31
  ).set_image(
    url = member.display_avatar
  ).set_footer(
    text = f"User ID : {member.id}"
  )
  return embed_avatar

async def get_banner(interaction : discord.Interaction, member : discord.Member):
  embed_banner = discord.Embed(
    title = member.name,
    color = 0x2b2d31
  ).set_image(
    url = member.banner.url
  ).set_footer(
    text = f"User ID : {member.id}"
  )
  return embed_banner

class ViewSelect(ui.Select):
  def __init__(self, user : discord.Member, member : discord.Member):
    self.user = user
    self.member = member
    super().__init__(
      custom_id = "view.select",
      placeholder = "Select a property :",
      min_values = 1,
      max_values = 1,
      options = [
        discord.SelectOption(
          label = "Profile",
          value = "user.profile",
          description = f"View {self.member.name if self.member else ""}'s profile",
          default = True
        ),
        discord.SelectOption(
          label = "Avatar",
          value = "user.avatar",
          description = f"View {self.member.name if self.member else ""}'s avatar"
        )
      ]
    )
    if self.member and self.member.banner:
      self.options.append(
        discord.SelectOption(
          label = "Banner",
          value = "user.banner",
          description = f"View {self.member.name if self.member else ""}'s banner"
        )
      )

  async def callback(self, interaction : discord.Interaction):
    try:
      response = interaction.response
      await response.defer(
        thinking = False,
        ephemeral = False
      )
      if interaction.user != self.user:
        err = discord.Embed(
          description = "This is not your menu !",
          color = 0xff3131
        ).set_author(
          name = interaction.client.user.name,
          icon_url = interaction.client.user.display_avatar
        )
        await response.send_message(
          embed = err,
          ephemeral = True
        )
        return
      if self.values[0] == "user.profile":
        embed = await get_profile(interaction, self.member)
        for ind, option in enumerate(self.options):
          if option.value != "user.profile":
            self.options[ind].default = False
          else:
            self.options[ind].default = True
        await interaction.edit_original_response(
          embed = embed,
          view = self.view
        )
        return
      if self.values[0] == "user.avatar":
        embed = await get_avatar(interaction, self.member)
        for ind, option in enumerate(self.options):
          if option.value != "user.avatar":
            self.options[ind].default = False
          else:
            self.options[ind].default = True
        await interaction.edit_original_response(
          embed = embed,
          view = self.view
        )
      if self.values[0] == "user.banner":
        embed = await get_banner(interaction, self.member)
        for ind, option in enumerate(self.options):
          if option.value != "user.banner":
            self.options[ind].default = False
          else:
            self.options[ind].default = True
        await interaction.edit_original_response(
          embed = embed,
          view = self.view
        )
    except:
      traceback.print_exc()

class View(ui.View):
  def __init__(self, user : discord.Member, member : discord.Member):
    super().__init__(
      timeout = None
    )
    self.user = user
    self.member = member
    self.add_item(ViewSelect(user, member))

  async def interaction_check(self, interaction : discord.Interaction):
    response = interaction.response
    if interaction.user != self.user:
      err = discord.Embed(
        description = "This is not your menu !",
        color = 0xff3131
      ).set_author(
        name = interaction.client.user.name,
        icon_url = interaction.client.user.display_avatar
      )
      await response.send_message(
        embed = err,
        ephemeral = True
      )
      return False
    return True

class User(commands.GroupCog, name = "user", description = "/user"):
  def __init__(self, bot):
    self.bot = bot
    self.bot.add_view(View(None, None))

  @app_commands.command(
    name = "profile",
    description = "View a member's profile"
  )
  @app_commands.describe(
    member = "Select another member"
  )
  async def user_profile(self, interaction : discord.Interaction, member : discord.Member = None):
    response = interaction.response
    await response.defer(
      thinking = True,
      ephemeral = True
    )
    followup = interaction.followup
    member_id = interaction.user.id if not member else member.id
    member = interaction.guild.get_member(member_id)
    user = await self.bot.fetch_user(member.id)
    embed_profile = await get_profile(interaction, member)
    await followup.send(
      embed = embed_profile,
      view = View(interaction.user, user)
    )

  @user_profile.error
  async def error(self, interaction : discord.Interaction, error):
    traceback.print_exc()

async def setup(bot):
  await bot.add_cog(User(bot))