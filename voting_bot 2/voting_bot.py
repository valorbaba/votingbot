import discord
from discord.ext import commands, tasks
from discord import app_commands
import random
import json
from datetime import datetime, timedelta
from pathlib import Path

# Initialize bot
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Configuration file
CONFIG_FILE = "bot_config.json"
VOTING_DATA_FILE = "voting_data.json"
LEADERBOARD_MSG_FILE = "leaderboard_messages.json"

def load_config():
    """Load bot configuration"""
    if Path(CONFIG_FILE).exists():
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {
        "guild_configs": {}
    }

def save_config(config):
    """Save bot configuration"""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

def get_guild_config(guild_id):
    """Get configuration for a specific guild"""
    config = load_config()
    if str(guild_id) not in config["guild_configs"]:
        config["guild_configs"][str(guild_id)] = {
            "vote_channel_id": None,
            "cooldown_hours": 24,
            "difficulty": "easy",
            "min_number": 1,
            "max_number": 20,
            "operations": ["+", "-", "*"],
            "question_time": 30,
            "setup_complete": False
        }
        save_config(config)
    return config["guild_configs"][str(guild_id)]

def update_guild_config(guild_id, updates):
    """Update configuration for a specific guild"""
    config = load_config()
    guild_config = get_guild_config(guild_id)
    guild_config.update(updates)
    config["guild_configs"][str(guild_id)] = guild_config
    save_config(config)

def load_voting_data():
    """Load voting data"""
    if Path(VOTING_DATA_FILE).exists():
        with open(VOTING_DATA_FILE, 'r') as f:
            return json.load(f)
    return {"votes": {}, "cooldowns": {}}

def save_voting_data(data):
    """Save voting data"""
    with open(VOTING_DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def load_leaderboard_messages():
    """Load leaderboard message IDs"""
    if Path(LEADERBOARD_MSG_FILE).exists():
        with open(LEADERBOARD_MSG_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_leaderboard_messages(data):
    """Save leaderboard message IDs"""
    with open(LEADERBOARD_MSG_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def get_relative_time(timestamp_str):
    """Convert ISO timestamp to relative time like '2 hours ago'"""
    if isinstance(timestamp_str, str):
        timestamp = datetime.fromisoformat(timestamp_str)
    else:
        timestamp = timestamp_str
    
    now = datetime.now()
    diff = now - timestamp
    seconds = diff.total_seconds()
    
    if seconds < 60:
        sec = int(seconds)
        return f"{sec}s ago" if sec != 1 else "1s ago"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        return f"{minutes}m ago" if minutes != 1 else "1m ago"
    elif seconds < 86400:
        hours = int(seconds // 3600)
        return f"{hours}h ago" if hours != 1 else "1h ago"
    else:
        days = int(seconds // 86400)
        return f"{days}d ago" if days != 1 else "1d ago"

class SetupButtons(discord.ui.View):
    def __init__(self, guild_id):
        super().__init__()
        self.guild_id = guild_id

    @discord.ui.button(label="Easy", style=discord.ButtonStyle.green, custom_id="difficulty_easy")
    async def easy_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        config = get_guild_config(self.guild_id)
        config["difficulty"] = "easy"
        config["min_number"] = 1
        config["max_number"] = 20
        update_guild_config(self.guild_id, config)
        
        embed = discord.Embed(
            title="✅ Difficulty Set to Easy",
            description="Questions will use numbers 1-20 with basic operations (+, -, *)",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Medium", style=discord.ButtonStyle.blurple, custom_id="difficulty_medium")
    async def medium_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        config = get_guild_config(self.guild_id)
        config["difficulty"] = "medium"
        config["min_number"] = 10
        config["max_number"] = 50
        update_guild_config(self.guild_id, config)
        
        embed = discord.Embed(
            title="✅ Difficulty Set to Medium",
            description="Questions will use numbers 10-50 with basic operations",
            color=discord.Color.blurple()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Hard", style=discord.ButtonStyle.red, custom_id="difficulty_hard")
    async def hard_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        config = get_guild_config(self.guild_id)
        config["difficulty"] = "hard"
        config["min_number"] = 50
        config["max_number"] = 100
        update_guild_config(self.guild_id, config)
        
        embed = discord.Embed(
            title="✅ Difficulty Set to Hard",
            description="Questions will use numbers 50-100 with all operations",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

class CooldownButtons(discord.ui.View):
    def __init__(self, guild_id):
        super().__init__()
        self.guild_id = guild_id

    @discord.ui.button(label="6 Hours", style=discord.ButtonStyle.blurple, custom_id="cooldown_6")
    async def cooldown_6(self, interaction: discord.Interaction, button: discord.ui.Button):
        update_guild_config(self.guild_id, {"cooldown_hours": 6})
        embed = discord.Embed(
            title="✅ Cooldown Set to 6 Hours",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="12 Hours", style=discord.ButtonStyle.blurple, custom_id="cooldown_12")
    async def cooldown_12(self, interaction: discord.Interaction, button: discord.ui.Button):
        update_guild_config(self.guild_id, {"cooldown_hours": 12})
        embed = discord.Embed(
            title="✅ Cooldown Set to 12 Hours",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="24 Hours", style=discord.ButtonStyle.blurple, custom_id="cooldown_24")
    async def cooldown_24(self, interaction: discord.Interaction, button: discord.ui.Button):
        update_guild_config(self.guild_id, {"cooldown_hours": 24})
        embed = discord.Embed(
            title="��� Cooldown Set to 24 Hours",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="48 Hours", style=discord.ButtonStyle.blurple, custom_id="cooldown_48")
    async def cooldown_48(self, interaction: discord.Interaction, button: discord.ui.Button):
        update_guild_config(self.guild_id, {"cooldown_hours": 48})
        embed = discord.Embed(
            title="✅ Cooldown Set to 48 Hours",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

class AnswerButtons(discord.ui.View):
    def __init__(self, correct_answer, user_id, guild_id, username, cog):
        super().__init__(timeout=30)
        self.correct_answer = correct_answer
        self.user_id = user_id
        self.guild_id = guild_id
        self.username = username
        self.cog = cog
        self.answered = False
        
        # Generate 4 answer options
        answers = [correct_answer]
        while len(answers) < 4:
            wrong = random.randint(correct_answer - 20, correct_answer + 20)
            if wrong != correct_answer and wrong not in answers:
                answers.append(wrong)
        
        random.shuffle(answers)
        
        # Create buttons for each answer
        for answer in answers:
            btn = discord.ui.Button(
                label=str(answer),
                style=discord.ButtonStyle.blurple,
                custom_id=f"answer_{answer}"
            )
            btn.callback = self.create_callback(answer)
            self.add_item(btn)
    
    def create_callback(self, answer):
        async def callback(interaction: discord.Interaction):
            if self.answered:
                await interaction.response.send_message("❌ You already answered!", ephemeral=True)
                return
            
            if interaction.user.id != self.user_id:
                await interaction.response.send_message("❌ This is not your question!", ephemeral=True)
                return
            
            self.answered = True
            
            if answer == self.correct_answer:
                # Correct answer!
                self.cog.count_vote(self.user_id, self.username, self.guild_id)
                self.cog.set_user_cooldown(self.user_id, self.guild_id)
                
                success_embed = discord.Embed(
                    title="✅ Vote Counted!",
                    description=f"{interaction.user.mention} just voted for the server!",
                    color=discord.Color.green()
                )
                success_embed.add_field(name="Your Answer", value=f"```\n{answer}\n```", inline=True)
                success_embed.add_field(name="Status", value="✅ Correct!", inline=True)
                
                # Disable all buttons
                for item in self.children:
                    item.disabled = True
                
                await interaction.response.defer()
                await interaction.message.edit(view=self)
                await interaction.followup.send(embed=success_embed, ephemeral=True)
            else:
                # Wrong answer
                self.cog.set_user_cooldown(self.user_id, self.guild_id)
                
                fail_embed = discord.Embed(
                    title="❌ Wrong Answer",
                    description=f"Your answer was incorrect.",
                    color=discord.Color.red()
                )
                fail_embed.add_field(name="Your Answer", value=f"```\n{answer}\n```", inline=True)
                fail_embed.add_field(name="Correct Answer", value=f"```\n{self.correct_answer}\n```", inline=True)
                
                # Disable all buttons
                for item in self.children:
                    item.disabled = True
                
                await interaction.response.defer()
                await interaction.message.edit(view=self)
                await interaction.followup.send(embed=fail_embed, ephemeral=True)
        
        return callback
    
    async def on_timeout(self):
        """Called when the view times out"""
        for item in self.children:
            item.disabled = True

class LeaderboardButtons(discord.ui.View):
    def __init__(self, cog, guild_id):
        super().__init__(timeout=None)
        self.cog = cog
        self.guild_id = guild_id
    
    @discord.ui.button(label="🗳️ Vote", style=discord.ButtonStyle.green, custom_id="lb_vote")
    async def vote_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Handle vote button from leaderboard"""
        config = get_guild_config(self.guild_id)
        
        # Check if setup is complete
        if not config["setup_complete"]:
            setup_embed = discord.Embed(
                title="❌ Bot Not Configured",
                description="An admin needs to run `/setup` first to configure the voting bot.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=setup_embed, ephemeral=True)
            return
        
        # Check cooldown
        if not self.cog.check_user_cooldown(interaction.user.id):
            voting_data = load_voting_data()
            cooldown_time = datetime.fromisoformat(voting_data["cooldowns"][str(interaction.user.id)])
            await interaction.response.send_message(
                f"❌ You've already voted! Try again <t:{int(cooldown_time.timestamp())}:R>",
                ephemeral=True
            )
            return
        
        # Generate question
        question, correct_answer = self.cog.generate_math_question(self.guild_id)
        
        embed = discord.Embed(
            title="🎯 Math Challenge",
            description=f"Answer this question correctly to vote for the server!\nSelect the correct answer from the buttons below.",
            color=discord.Color.blue()
        )
        embed.add_field(name="Question", value=f"```\n{question}\n```", inline=False)
        embed.set_footer(text=f"You have 30 seconds to answer")
        
        # Create answer buttons view
        view = AnswerButtons(correct_answer, interaction.user.id, self.guild_id, interaction.user.name, self.cog)
        
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
    
    @discord.ui.button(label="⚙️ Settings", style=discord.ButtonStyle.blurple, custom_id="lb_settings")
    async def settings_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Handle settings button from leaderboard"""
        # Check if user is admin
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "❌ Only administrators can access settings!",
                ephemeral=True
            )
            return
        
        config = get_guild_config(self.guild_id)
        
        if not config["setup_complete"]:
            await interaction.response.send_message(
                "❌ Bot hasn't been setup yet. Use `/setup` to configure it.",
                ephemeral=True
            )
            return
        
        vote_channel = interaction.guild.get_channel(config["vote_channel_id"])
        
        settings_embed = discord.Embed(
            title="⚙️ Bot Settings",
            color=discord.Color.blurple()
        )
        settings_embed.add_field(
            name="Vote Channel",
            value=vote_channel.mention if vote_channel else "Channel not found",
            inline=False
        )
        settings_embed.add_field(
            name="Question Difficulty",
            value=f"{config['difficulty'].capitalize()} (Numbers: {config['min_number']}-{config['max_number']})",
            inline=False
        )
        settings_embed.add_field(
            name="Vote Cooldown",
            value=f"{config['cooldown_hours']} hours",
            inline=False
        )
        settings_embed.add_field(
            name="Question Time Limit",
            value=f"{config['question_time']} seconds",
            inline=False
        )
        settings_embed.add_field(
            name="Allowed Operations",
            value=", ".join(config["operations"]),
            inline=False
        )
        
        await interaction.response.send_message(embed=settings_embed, ephemeral=True)

class VotingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_leaderboards.start()
    
    def generate_math_question(self, guild_id):
        """Generate a math question based on guild settings"""
        config = get_guild_config(guild_id)
        
        num1 = random.randint(config["min_number"], config["max_number"])
        num2 = random.randint(config["min_number"], config["max_number"])
        operation = random.choice(config["operations"])
        
        if operation == '+':
            answer = num1 + num2
        elif operation == '-':
            answer = num1 - num2
        else:  # multiplication
            answer = num1 * num2
        
        question = f"{num1} {operation} {num2} = ?"
        return question, answer
    
    def check_user_cooldown(self, user_id):
        """Check if user is on cooldown"""
        voting_data = load_voting_data()
        if str(user_id) not in voting_data["cooldowns"]:
            return True
        
        cooldown_time = datetime.fromisoformat(voting_data["cooldowns"][str(user_id)])
        if datetime.now() > cooldown_time:
            return True
        return False
    
    def set_user_cooldown(self, user_id, guild_id):
        """Set cooldown for user"""
        config = get_guild_config(guild_id)
        voting_data = load_voting_data()
        
        cooldown_time = datetime.now() + timedelta(hours=config["cooldown_hours"])
        voting_data["cooldowns"][str(user_id)] = cooldown_time.isoformat()
        save_voting_data(voting_data)
    
    @app_commands.command(name="setup", description="Setup the voting bot for your server")
    @app_commands.checks.has_permissions(administrator=True)
    async def setup(self, interaction: discord.Interaction):
        """Setup wizard for the voting bot"""
        guild_id = interaction.guild_id
        
        # Step 1: Set voting channel
        embed = discord.Embed(
            title="🎯 Voting Bot Setup",
            description="Let's configure your voting bot!\n\n**Step 1/3: Set Voting Channel**",
            color=discord.Color.blue()
        )
        embed.add_field(
            name="Instructions",
            value="Please mention the channel where voting will be allowed (or type the channel name/ID)",
            inline=False
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        
        # Wait for channel response
        def check_channel(msg):
            return msg.author == interaction.user and msg.channel == interaction.channel
        
        try:
            channel_msg = await self.bot.wait_for('message', check=check_channel, timeout=60.0)
            
            # Parse channel mention or ID
            if channel_msg.channel_mentions:
                vote_channel = channel_msg.channel_mentions[0]
            else:
                try:
                    channel_id = int(channel_msg.content.strip())
                    vote_channel = interaction.guild.get_channel(channel_id)
                    if not vote_channel:
                        await channel_msg.reply("❌ Channel not found!")
                        return
                except ValueError:
                    await channel_msg.reply("❌ Invalid channel! Please mention a channel or provide its ID.")
                    return
            
            update_guild_config(guild_id, {"vote_channel_id": vote_channel.id})
            
            confirm_embed = discord.Embed(
                title="✅ Channel Set",
                description=f"Voting channel set to {vote_channel.mention}",
                color=discord.Color.green()
            )
            await channel_msg.reply(embed=confirm_embed)
            
            # Step 2: Set difficulty
            difficulty_embed = discord.Embed(
                title="🎯 Voting Bot Setup",
                description="**Step 2/3: Select Question Difficulty**",
                color=discord.Color.blue()
            )
            difficulty_embed.add_field(
                name="Easy",
                value="Numbers 1-20, Basic Operations",
                inline=False
            )
            difficulty_embed.add_field(
                name="Medium",
                value="Numbers 10-50, Basic Operations",
                inline=False
            )
            difficulty_embed.add_field(
                name="Hard",
                value="Numbers 50-100, All Operations",
                inline=False
            )
            await interaction.followup.send(embed=difficulty_embed, view=SetupButtons(guild_id), ephemeral=True)
            
            # Step 3: Set cooldown
            await interaction.followup.send(
                embed=discord.Embed(
                    title="🎯 Voting Bot Setup",
                    description="**Step 3/3: Select Vote Cooldown Period**",
                    color=discord.Color.blue()
                ),
                view=CooldownButtons(guild_id),
                ephemeral=True
            )
            
            # Mark setup as complete
            update_guild_config(guild_id, {"setup_complete": True})
            
            final_embed = discord.Embed(
                title="✅ Setup Complete!",
                description="Your voting bot is now ready to use!",
                color=discord.Color.green()
            )
            final_embed.add_field(
                name="Next Steps",
                value="Users can now use the Vote button on the leaderboard! Use `/recent_votes` to see latest voters.",
                inline=False
            )
            await interaction.followup.send(embed=final_embed, ephemeral=True)
            
        except TimeoutError:
            await interaction.followup.send("❌ Setup timed out. Please try again.", ephemeral=True)
    
    @app_commands.command(name="vote", description="Vote for the server by answering a math question!")
    async def vote(self, interaction: discord.Interaction):
        """Main voting command"""
        config = get_guild_config(interaction.guild_id)
        
        # Check if setup is complete
        if not config["setup_complete"]:
            setup_embed = discord.Embed(
                title="❌ Bot Not Configured",
                description="An admin needs to run `/setup` first to configure the voting bot.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=setup_embed, ephemeral=True)
            return
        
        # Check cooldown
        if not self.check_user_cooldown(interaction.user.id):
            voting_data = load_voting_data()
            cooldown_time = datetime.fromisoformat(voting_data["cooldowns"][str(interaction.user.id)])
            await interaction.response.send_message(
                f"❌ You've already voted! Try again <t:{int(cooldown_time.timestamp())}:R>",
                ephemeral=True
            )
            return
        
        # Generate question
        question, correct_answer = self.generate_math_question(interaction.guild_id)
        
        embed = discord.Embed(
            title="🎯 Math Challenge",
            description=f"Answer this question correctly to vote for the server!\nSelect the correct answer from the buttons below.",
            color=discord.Color.blue()
        )
        embed.add_field(name="Question", value=f"```\n{question}\n```", inline=False)
        embed.set_footer(text=f"You have 30 seconds to answer")
        
        # Create answer buttons view
        view = AnswerButtons(correct_answer, interaction.user.id, interaction.guild_id, interaction.user.name, self)
        
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
    
    def count_vote(self, user_id, username, guild_id):
        """Record a vote"""
        voting_data = load_voting_data()
        guild_key = str(guild_id)
        now = datetime.now().isoformat()
        
        if guild_key not in voting_data["votes"]:
            voting_data["votes"][guild_key] = {}
        
        voting_data["votes"][guild_key][str(user_id)] = {
            "username": username,
            "timestamp": now,
            "user_id": user_id
        }
        
        save_voting_data(voting_data)
    
    @app_commands.command(name="recent_votes", description="See who recently voted for the server")
    async def recent_votes(self, interaction: discord.Interaction, limit: int = 10):
        """View recent votes with relative timestamps"""
        voting_data = load_voting_data()
        guild_key = str(interaction.guild_id)
        
        if guild_key not in voting_data["votes"] or not voting_data["votes"][guild_key]:
            no_votes_embed = discord.Embed(
                title="📊 Recent Votes",
                description="No votes yet! Be the first to vote for the server.",
                color=discord.Color.orange()
            )
            await interaction.response.send_message(embed=no_votes_embed, ephemeral=True)
            return
        
        # Get votes sorted by timestamp (newest first)
        votes = voting_data["votes"][guild_key]
        sorted_votes = sorted(
            votes.values(),
            key=lambda x: datetime.fromisoformat(x["timestamp"]),
            reverse=True
        )
        
        # Limit to requested amount
        sorted_votes = sorted_votes[:limit]
        
        recent_embed = discord.Embed(
            title="📊 Recent Votes",
            description=f"Last {len(sorted_votes)} vote(s)",
            color=discord.Color.blue()
        )
        
        for vote in sorted_votes:
            relative_time = get_relative_time(vote["timestamp"])
            recent_embed.add_field(
                name=f"👤 {vote['username']}",
                value=f"Voted **{relative_time}**",
                inline=False
            )
        
        await interaction.response.send_message(embed=recent_embed, ephemeral=True)
    
    @app_commands.command(name="leaderboard", description="Post a live-updating leaderboard of recent voters")
    @app_commands.checks.has_permissions(administrator=True)
    async def leaderboard(self, interaction: discord.Interaction):
        """Post a live updating leaderboard"""
        voting_data = load_voting_data()
        guild_key = str(interaction.guild_id)
        
        if guild_key not in voting_data["votes"] or not voting_data["votes"][guild_key]:
            await interaction.response.send_message("❌ No votes yet!", ephemeral=True)
            return
        
        votes = voting_data["votes"][guild_key]
        sorted_votes = sorted(
            votes.values(),
            key=lambda x: datetime.fromisoformat(x["timestamp"]),
            reverse=True
        )[:20]
        
        # Create leaderboard embed with new style
        leaderboard_embed = discord.Embed(
            color=0x2c2f33
        )
        
        # Build leaderboard text with monospace formatting
        leaderboard_text = ""
        for idx, vote in enumerate(sorted_votes, 1):
            leaderboard_text += f"`{idx:2d}.` `1 OY` **{vote['username']}**\n"
        
        leaderboard_embed.description = leaderboard_text
        leaderboard_embed.title = "🏆 VOTE LEADERBOARD"
        leaderboard_embed.set_footer(text="Updates every 30 seconds | Live voting tracker")
        
        # Create view with buttons
        view = LeaderboardButtons(self, interaction.guild_id)
        
        message = await interaction.response.send_message(embed=leaderboard_embed, view=view)
        
        # Store message ID for updates
        leaderboard_msgs = load_leaderboard_messages()
        leaderboard_msgs[str(interaction.guild_id)] = {
            "message_id": message.id,
            "channel_id": interaction.channel_id
        }
        save_leaderboard_messages(leaderboard_msgs)
    
    @app_commands.command(name="vote_stats", description="View voting statistics")
    @app_commands.checks.has_permissions(administrator=True)
    async def vote_stats(self, interaction: discord.Interaction):
        """View voting statistics"""
        voting_data = load_voting_data()
        guild_key = str(interaction.guild_id)
        
        total_votes = 0
        
        if guild_key in voting_data["votes"]:
            total_votes = len(voting_data["votes"][guild_key])
        
        config = get_guild_config(interaction.guild_id)
        
        stats_embed = discord.Embed(
            title="📊 Voting Statistics",
            color=discord.Color.gold()
        )
        stats_embed.add_field(name="Total Voters", value=f"```\n{total_votes}\n```", inline=True)
        stats_embed.add_field(name="Difficulty Level", value=f"```\n{config['difficulty'].capitalize()}\n```", inline=True)
        stats_embed.add_field(name="Vote Cooldown", value=f"```\n{config['cooldown_hours']} hours\n```", inline=True)
        
        await interaction.response.send_message(embed=stats_embed, ephemeral=True)
    
    @app_commands.command(name="view_settings", description="View current bot settings")
    @app_commands.checks.has_permissions(administrator=True)
    async def view_settings(self, interaction: discord.Interaction):
        """View current settings"""
        config = get_guild_config(interaction.guild_id)
        
        if not config["setup_complete"]:
            await interaction.response.send_message(
                "❌ Bot hasn't been setup yet. Use `/setup` to configure it.",
                ephemeral=True
            )
            return
        
        vote_channel = interaction.guild.get_channel(config["vote_channel_id"])
        
        settings_embed = discord.Embed(
            title="⚙️ Bot Settings",
            color=discord.Color.blurple()
        )
        settings_embed.add_field(
            name="Vote Channel",
            value=vote_channel.mention if vote_channel else "Channel not found",
            inline=False
        )
        settings_embed.add_field(
            name="Question Difficulty",
            value=f"{config['difficulty'].capitalize()} (Numbers: {config['min_number']}-{config['max_number']})",
            inline=False
        )
        settings_embed.add_field(
            name="Vote Cooldown",
            value=f"{config['cooldown_hours']} hours",
            inline=False
        )
        settings_embed.add_field(
            name="Question Time Limit",
            value=f"{config['question_time']} seconds",
            inline=False
        )
        settings_embed.add_field(
            name="Allowed Operations",
            value=", ".join(config["operations"]),
            inline=False
        )
        
        await interaction.response.send_message(embed=settings_embed, ephemeral=True)
    
    @app_commands.command(name="reset_guild_data", description="Reset all voting data for your server")
    @app_commands.checks.has_permissions(administrator=True)
    async def reset_guild_data(self, interaction: discord.Interaction):
        """Reset voting data for the guild"""
        voting_data = load_voting_data()
        guild_key = str(interaction.guild_id)
        
        if guild_key in voting_data["votes"]:
            del voting_data["votes"][guild_key]
        
        save_voting_data(voting_data)
        
        reset_embed = discord.Embed(
            title="🔄 Data Reset",
            description="All voting data for this server has been cleared.",
            color=discord.Color.orange()
        )
        await interaction.response.send_message(embed=reset_embed, ephemeral=True)
    
    @tasks.loop(seconds=30)
    async def update_leaderboards(self):
        """Update all leaderboard messages every 30 seconds"""
        leaderboard_msgs = load_leaderboard_messages()
        voting_data = load_voting_data()
        
        for guild_id, msg_info in leaderboard_msgs.items():
            try:
                channel = self.bot.get_channel(msg_info["channel_id"])
                if not channel:
                    continue
                
                message = await channel.fetch_message(msg_info["message_id"])
                
                if guild_id not in voting_data["votes"]:
                    continue
                
                votes = voting_data["votes"][guild_id]
                sorted_votes = sorted(
                    votes.values(),
                    key=lambda x: datetime.fromisoformat(x["timestamp"]),
                    reverse=True
                )[:20]
                
                # Build leaderboard text
                leaderboard_text = ""
                for idx, vote in enumerate(sorted_votes, 1):
                    leaderboard_text += f"`{idx:2d}.` `1 OY` **{vote['username']}**\n"
                
                leaderboard_embed = discord.Embed(
                    color=0x2c2f33
                )
                leaderboard_embed.description = leaderboard_text
                leaderboard_embed.title = "🏆 VOTE LEADERBOARD"
                leaderboard_embed.set_footer(text="Updates every 30 seconds | Live voting tracker")
                
                # Recreate view to ensure buttons still work
                view = LeaderboardButtons(self, int(guild_id))
                
                await message.edit(embed=leaderboard_embed, view=view)
            except Exception as e:
                print(f"Error updating leaderboard: {e}")
    
    @update_leaderboards.before_loop
    async def before_update_leaderboards(self):
        await self.bot.wait_until_ready()

@bot.event
async def on_ready():
    print(f"✅ {bot.user} has connected to Discord!")
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"❌ Error syncing commands: {e}")

async def setup_cog():
    await bot.add_cog(VotingCog(bot))

async def main():
    async with bot:
        await setup_cog()
        await bot.start("YOUR_BOT_TOKEN_HERE")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())