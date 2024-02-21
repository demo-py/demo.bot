import discord
import traceback
from datetime import datetime, timedelta
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
        custom_activity = f"\n\n> {activity_emoji} {activity.name if activity.name else ''}"
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

async def ban_user(interaction : discord.Interaction, member : discord.Member, reason : str):
  await member.ban(
    delete_message_days = 7,
    reason = reason
  )
  embed = discord.Embed(
    description = f"Successfully banned ` {member.name} `",
    color = 0x39ff14
  ).set_author(
    name = interaction.client.user.name,
    icon_url = interaction.client.user.display_avatar
  ).add_field(
    name = "Reason :",
    value = f"> {reason}",
    inline = False
  )
  await interaction.response.edit_message(
    embed = embed,
    view = None
  )

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
          description = f"View {self.member.name if self.member else ''}'s profile",
          default = True
        ),
        discord.SelectOption(
          label = "Avatar",
          value = "user.avatar",
          description = f"View {self.member.name if self.member else ''}'s avatar"
        )
      ]
    )
    if self.member and self.member.banner:
      self.options.append(
        discord.SelectOption(
          label = "Banner",
          value = "user.banner",
          description = f"View {self.member.name if self.member else ''}'s banner"
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

class BanConfirmationView(ui.View):
  def __init__(self, member : discord.Member, reason : str):
    super().__init__(
      timeout = None
    )
    self.member = member
    self.reason = reason

  @ui.button(
    label = "Confirm",
    style = discord.ButtonStyle.green
  )
  async def confirm_button(self, interaction : discord.Interaction, button : ui.Button):
    await ban_user(interaction, self.member, self.reason)

  @ui.button(
    label = "Cancel",
    style = discord.ButtonStyle.red
  )
  async def cancel_button(self, interaction : discord.Interaction, button : ui.Button):
    embed = discord.Embed(
      description = "Cancelled the action",
      color = 0xff3131
    ).set_author(
      name = interaction.client.user.name,
      icon_url = interaction.client.user.display_avatar
    )
    await interaction.response.edit_message(
      embed = embed,
      view = None
    )

  async def on_error(self, interaction : discord.Interaction, error):
    traceback.print_exc()

class BanReason(ui.Modal):
  def __init__(self, member : discord.Member):
    super().__init__(
      timeout = None,
      title = "User Ban"
    )
    self.member = member
    self.reason = ui.TextInput(
      label = f"Reason for banning {member.name}. Leave blank if None",
      style = discord.TextStyle.long,
      required = False
    )
    self.add_item(self.reason)

  async def on_submit(self, interaction : discord.Interaction):
    reason = str(self.reason) if str(self.reason) != "" else "` No reason provided `"
    embed = discord.Embed(
      description = f"Are you sure you want to **ban** {self.member.mention}",
      color = 0xffff00
    ).set_author(
      name = interaction.client.user.name,
      icon_url = interaction.client.user.display_avatar
    )
    await interaction.response.edit_message(
      embed = embed,
      view = BanConfirmationView(member, reason)
    )

class KickReason(ui.Modal):
  def __init__(self, member : discord.Member):
    super().__init__(
      title = "User Kick",
      timeout = None
    )
    self.member = member
    self.reason = ui.TextInput(
      label = f"Reason for kicking {member.name}. Leave blank if None",
      style = discord.TextStyle.long,
      required = False
    )
    self.add_item(self.reason)

  async def on_submit(self, interaction : discord.Interaction):
    reason = str(sefl.reason) if str(self.reason) != "" else "` No reason provided `"
    await self.member.kick(
      reason = reason
    )
    embed = discord.Embed(
      description = f"Successfully kicked ` {self.member.name} `",
      color = 0x39ff14
    ).set_author(
      name = interaction.client.user.name,
      icon_url = interaction.client.user.display_avatar
    ).add_field(
      name = "Reason :",
      value = f"> {reason}",
      inline = False
    )
    await interaction.response.send_message(
      embed = embed,
      ephemeral = True
    )

class MemberTimeout(ui.Modal):
  def __init__(self, member : discord.Member):
    self.member = member
    super().__init__(
      timoeut = None,
      title = "User Timeout"
    )
    self.seconds = ui.TextInput(
      label = "Seconds : 0 - 60",
      custom_id = "user.timeout.seconds",
      style = discord.TextStyle.short,
      placeholder = "Amount of seconds to append to the duration",
      default = "60",
      required = True,
      min_length = 1,
      max_length = 2
    )
    self.minutes = ui.TextInput(
      label = "Minutes : 0 - 60",
      custom_id = "user.timeout.minutes",
      style = discord.TextStyle.short,
      placeholder = "Amount of seconds to append to the duration",
      default = "0",
      required = True,
      min_length = 1,
      max_length = 2
    )
    self.hours = ui.TextInput(
      label = "Hours : 0 - 24",
      custom_id = "user.timeout.hours",
      style = discord.TexStyle.short,
      placeholder = "Amount of hours to append to the duration",
      default = "0",
      required = True,
      min_length = 1,
      max_length = 2
    )
    self.days = ui.TextInput(
      label = "Days : 0 - 28",
      custom_id = "user.timeout.days",
      style = discord.TextStyle.short,
      placeholder = "Amount of days to append to the duration",
      default = "0",
      required = True,
      min_length = 1,
      max_length = 2
    )
    self.add_item(self.seconds)
    self.add_item(self.minutes)
    self.add_item(self.hours)
    self.add_item(self.days)

class ModerateSelect(ui.Select):
  def __init__(self, member : discord.Member):
    super().__init__(
      placeholder = "Select a moderation action :",
      custom_id = "user.moderate.select",
      min_values = 1,
      max_values = 1,
      options = [
        discord.SelectOption(
          label = "Ban",
          value = "user.ban"
        ),
        discord.SelectOption(
          label = "Kick",
          value = "user.kick"
        ),
        discord.SelectOption(
          label = "Timeout",
          value = "user.timeout"
        )
      ]
    )
    self.member = member

  async def callback(self, interaction : discord.Interaction):
    response = interaction.response
    if self.values[0] == "user.ban":
      await response.send_modal(BanReason(self.member))
    if self.values[0] == "user.kick":
      await response.send_modal(KickReason(self.member))
    if self.values[0] == "user.timeout":
      await response.send_modal(MemberTimeout(self.member))

class User(commands.GroupCog, name = "user", description = "/user"):
  def __init__(self, bot):
    self.bot = bot
    self.bot.add_view(View(None, None))
    self.info_context_menu = app_commands.ContextMenu(
      name = "User Info",
      callback = self.command_callback
    )
    self.bot.tree.add_command(self.info_context_menu)
    self.moderate_context_menu = app_commands.ContextMenu(
      name = "User Moderate",
      callback = self.moderate_callback
    )
    self.bot.tree.add_command(self.moderate_context_menu)

  async def command_callback(self, interaction : discord.Interaction, member : discord.Member):
    response = interaction.response
    await response.defer(
      thinking = True,
      ephemeral = True
    )
    followup = interaction.followup
    member = interaction.guild.get_member(member.id)
    user = await self.bot.fetch_user(member.id)
    embed_profile = await get_profile(interaction, member)
    await followup.send(
      embed = embed_profile,
      view = View(interaction.user, user)
    )

  async def moderate_callback(self, interaction : discord.Interaction, member ; discord.Member):
    response = interaction.response
    if member == interaction.guild.owner:
      err = discord.Embed(
        description = "You cannot ban a Guild Owner",
        color = 0xff3131
      ).set_author(
        name = self.bot.user.name,
        icon_url = self.bot.user.display_avatar
      )
      await response.send_message(
        embed = err,
        ephemeral = True
      )
      return
    if member == interaction.user:
      err = discord.Embed(
        description = "You cannot ban yourself",
        color = 0xff3131
      ).set_author(
        name = self.bot.user.name,
        icon_url = self.bot.user.display_avatar
      )
      await response.send_message(
        embed = err,
        ephemeral = True
      )
      return
    if member == self.bot.user:
      err = discord.Embed(
        description = "I am unable to ban myself",
        color = 0xff3131
      ).set_author(
        name = self.bot.user.name,
        icon_url = self.bot.user.display_avatar
      )
      await response.send_message(
        embed = err,
        ephemeral = True
      )
      return
    if member.bot:
      err = discord.Embed(
        description = "I am unable to ban bots",
        color = 0xff3131
      ).set_author(
        name = self.bot.user.name,
        icon_url = self.bot.user.display_avatar
      )
      await response.send_message(
        embed = err,
        ephemeral = True
      )
      return
    await response.send_message(
      view = ui.View().add_item(ModerateSelect(member)),
      ephemeral = True
    )

  async def ban(self, interaction : discord.Interaction, member : discord.Member, reason : str):
    response = interaction.response
    if member == interaction.guild.owner:
      err = discord.Embed(
        description = "You cannot ban a Guild Owner",
        color = 0xff3131
      ).set_author(
        name = self.bot.user.name,
        icon_url = self.bot.user.display_avatar
      )
      await response.send_message(
        embed = err,
        ephemeral = True
      )
      return
    if member == interaction.user:
      err = discord.Embed(
        description = "You cannot ban yourself",
        color = 0xff3131
      ).set_author(
        name = self.bot.user.name,
        icon_url = self.bot.user.display_avatar
      )
      await response.send_message(
        embed = err,
        ephemeral = True
      )
      return
    if member == self.bot.user:
      err = discord.Embed(
        description = "I am unable to ban myself",
        color = 0xff3131
      ).set_author(
        name = self.bot.user.name,
        icon_url = self.bot.user.display_avatar
      )
      await response.send_message(
        embed = err,
        ephemeral = True
      )
      return
    if member.bot:
      err = discord.Embed(
        description = "I am unable to ban bots",
        color = 0xff3131
      ).set_author(
        name = self.bot.user.name,
        icon_url = self.bot.user.display_avatar
      )
      await response.send_message(
        embed = err,
        ephemeral = True
      )
      return
    embed = discord.Embed(
      description = f"Are you sure you want to **ban** {member.mention}",
      color = 0xffff00
    ).set_author(
      name = self.bot.user.name,
      icon_url = self.bot.user.display_avatar
    )
    await interaction.response.send_message(
      embed = embed,
      view = BanConfirmationView(member, reason),
      ephemeral = True
    )

  @app_commands.command(
    name = "info",
    description = "View a member's info"
  )
  @app_commands.describe(
    member = "Select another member"
  )
  async def user_info(self, interaction : discord.Interaction, member : discord.Member = None):
    await self.command_callback(interaction, member if member else interaction.user)

  @app_commands.command(
    name = "ban",
    description = "Ban a member"
  )
  @app_commands.describe(
    member = "Select a member to ban",
    reason = "Reason for banning the member"
  )
  @app_commands.checks.has_permissions(
    ban_members = True
  )
  @app_commands.default_permissions(
    ban_members = True
  )
  async def user_ban(self, interaction : discord.Interaction, member : discord.Member, reason : str = "No reason provided"):
    await self.ban(interaction, member, reason)

  @app_commands.command(
    name = "kick",
    description = "Kick a member"
  )
  @app_commands.describe(
    member = "Select a member to kick",
    reason = "Reason for kicking the member"
  )
  @app_commands.checks.has_permissions(
    kick_members = True
  )
  @app_commands.default_permissions(
    kick_members = True
  )
  async def user_kick(self, interaction : discord.Interaction, member : discord.Member, reason : str = "No reason provided"):
    response = interaction.response
    if member == interaction.guild.owner:
      err = discord.Embed(
        description = "You cannot kick a Guild Owner",
        color = 0xff3131
      ).set_author(
        name = self.bot.user.name,
        icon_url = self.bot.user.display_avatar
      )
      await response.send_message(
        embed = err,
        ephemeral = True
      )
      return
    if member == interaction.user:
      err = discord.Embed(
        description = "You cannot kick yourself",
        color = 0xff3131
      ).set_author(
        name = self.bot.user.name,
        icon_url = self.bot.user.display_avatar
      )
      await response.send_message(
        embed = err,
        ephemeral = True
      )
      return
    if member == self.bot.user:
      err = discord.Embed(
        description = "I am unable to kick myself",
        color = 0xff3131
      ).set_author(
        name = self.bot.user.name,
        icon_url = self.bot.user.display_avatar
      )
      await response.send_message(
        embed = err,
        ephemeral = True
      )
      return
    if member.bot:
      err = discord.Embed(
        description = "I am unable to kick bots",
        color = 0xff3131
      ).set_author(
        name = self.bot.user.name,
        icon_url = self.bot.user.display_avatar
      )
      await response.send_message(
        embed = err,
        ephemeral = True
      )
      return
    await member.kick(
      reason = reason
    )
    embed = discord.Embed(
      description = f"Successfully kicked ` {member.name} `",
      color = 0x39ff14
    ).set_author(
      name = self.bot.user.name,
      icon_url = self.bot.user.display_avatar
    ).add_field(
      name = "Reason :",
      value = f"> {reason}",
      inline = False
    )
    await response.send_message(
      embed = embed,
      ephemeral = True
    )

  @app_commands.command(
    name = "timeout",
    description = "Timeout a member. Defaults to 60 seconds"
  )
  @app_commands.describe(
    member = "Select a member to timeout",
    days = "Amount of days to timeout the member. Defaults to 0",
    hours = "Amount of hours to timeout the member. Defaults to 0",
    minutes = "Amount of minutes to timeout the member. Defaults to 0",
    seconds = "Amount of seconds to timeout the member. Defaults to 60"
  )
  @app_commands.checks.has_permissions(
    moderate_members = True
  )
  @app_commands.default_permissions(
    moderate_members = True
  )
  async def user_timeout(
    self,
    interaction : discord.Interaction,
    member : discord.Member,
    seconds : app_commands.Range[int, 0, 60] = 60,
    minutes : app_commands.Range[int, 0, 60] = 0,
    hours : app_commands.Range[int, 0, 24] = 24,
    days : app_commands.Range[int, 0, 28] = 0
  ):
    response = interaction.response
    user = interaction.user
    if member == interaction.guild.owner:
      err = discord.Embed(
        description = "Unable to timeout a Guild Owner",
        color = 0xff3131
      ).set_author(
        name = self.bot.user.name,
        icon_url = self.bot.user.display_avatar
      )
      await response.send_message(
        embed = err,
        ephemeral = True
      )
      return
    if member.bot:
      err = discord.Embed(
        description = "Unable to timeout a bot",
        color = 0xff3131
      ).set_author(
        name = self.bot.user.name,
        icon_url = self.bot.user.display_avatar
      )
      await response.send_message(
        embed = err,
        ephemeral = True
      )
      return
    if member == self.bot.user:
      err = discord.Embed(
        description = "Unable to timeout myself",
        color = 0xff3131
      ).set_author(
        name = self.bot.user.name,
        icon_url = self.bot.user.display_avatar
      )
      await response.send_message(
        embed = err,
        ephemeral = True
      )
      return
    if member == user:
      err = discord.Embed(
        description = "Unable to timeout yourself",
        color = 0xff3131
      ).set_author(
        name = self.bot.user.name,
        icon_url = self.bot.user.display_avatar
      )
      await response.send_message(
        embed = err,
        ephemeral = True
      )
      return
    duration = timedelta(
      seconds = seconds,
      minutes = minutes,
      hours = hours,
      days = days
    )
    if int(duration.total_seconds()) == 0:
      embed = discord.Embed(
        description = f"Successfully removed {member.mention}'s timeout",
        color = 0x39ff14
      ).set_author(
        name = self.bot.user.name,
        icon_url = self.bot.user.display_avatar
      )
      await member.timeout(
        None
      )
      await response.send_message(
        embed = embed,
        ephemeral = True
      )
      return
    if duration.days > 28:
      err = discord.Embed(
        description = "You can only timeout a member for 28 days maximum",
        color = 0x39ff14
      ).set_author(
        name = self.bot.user.name,
        icon_url = self.bot.user.display_avatar
      )
      await response.send_message(
        embed = err,
        ephemeral = True
      )
      return
    expires = datetime.now() + duration
    embed = discord.Embed(
      description = f"Successfully timed out {member.mention}. The timeout will expire <t:{int(expires.timestamp())}:R>",
      color = 0x39ff14
    ).set_author(
      name = self.bot.user.name,
      icon_url = self.bot.user.display_avatar
    )
    await member.timeout(
      duration
    )
    await response.send_message(
      embed = embed,
      ephemeral = True
    )

  @user_info.error
  @user_ban.error
  @user_kick.error
  @user_timeout.error
  async def error(self, interaction : discord.Interaction, error):
    if isinstance(error, app_commands.MissingPermissions):
      missing_permissions = "\n".join([f"> ` {permission.title()} `" for permission in error.missing_permissions])
      err = discord.Embed(
        description = f"You are missing the following permissions to execute this command :\n{missing_permissions}",
        color = 0xff3131
      ).set_author(
        name = interaction.client.user.name,
        icon_url = interaction.client.user.display_avatar
      )
      await interaction.response.send_message(
        embed = err,
        ephemeral = True
      )
      return
    traceback.print_exc()

async def setup(bot):
  await bot.add_cog(User(bot))