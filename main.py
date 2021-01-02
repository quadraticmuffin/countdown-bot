"""
Math problem generator for practice and competition.
Inspired by Art of Problem Solving's FTW, which was
deprecated when Adobe Flash was phased out after 2020.
"""

# COMMENT THESE TWO LINES BEFORE PUSHING TO PROD
# from dotenv import load_dotenv
# load_dotenv()

import discord
from discord.ext import commands

import os

import random
import time
import asyncio
import pymongo

import problem_gen as probs

DB_URL = os.getenv('MONGODB_URL')
db_client = pymongo.MongoClient(DB_URL)
db = db_client.discord
prefixes = db.prefixes
user_stats = db.user_stats

ANS_TOLERANCE = 0.0001
DEFAULT_TIMER = 45
DEFAULT_POINT_GOAL = 4
IDLE_TIMER = 60*10 # seconds
QUIT_STRING = 'quit'

TOKEN = os.getenv('DISCORD_TOKEN')
DEFAULT_PREFIX = '&'

def get_prefix(client, message):
    id_ = message.guild.id
    res = prefixes.find_one({'guild_id': id_})
    if res is None:
        prefixes.insert_one({'guild_id': id_, 'prefix': DEFAULT_PREFIX})
        return DEFAULT_PREFIX
    else:
        return res['prefix']

client = commands.Bot(command_prefix = get_prefix)

channels_in_session = set()

def check_in_session(channel_id):
    return channel_id in channels_in_session

def toggle_in_session(channel_id):
    global channels_in_session
    channels_in_session ^= {channel_id} # Set symmetric difference

@client.event
async def on_guild_join(guild):
    prefixes.insert_one({'guild_id': guild.id, 'prefix': DEFAULT_PREFIX})
    print(f'Joined {guild.name}')
    

@client.event
async def on_ready():
    global channels_in_session
    channels_in_session = set()
    print('Bot ready!')

############
# COMMANDS # 
############

@client.command(name='ping', hidden=True)
async def ping(ctx):
    await ctx.send('pong!')

_prefix_help = f"""Changes the server's prefix.
    Only takes """
@client.command(name='prefix')
async def update_prefix(ctx, new_prefix): 
    # TODO require privileges for this
    prefixes.update_one({'guild_id': ctx.guild.id}, {'$set': {'prefix': new_prefix}}, upsert=True)
    await ctx.send(f"Prefix updated to '{new_prefix}'")

async def _cd(ctx, *args, p=False):
    if len(args) == 2:
        time_limit, win_score = float(args[0]), int(args[1])
    elif len(args) == 0:
        time_limit, win_score = DEFAULT_TIMER, DEFAULT_POINT_GOAL
    else:
        await ctx.send(f'Improper arguments to {get_prefix(client, ctx.message)}cd.')
        await ctx.send(f"See '{get_prefix(client, ctx.message)}help cd' for more help.")
        return
    
    if check_in_session(ctx.channel.id):
        await ctx.send('There\'s already an active round in this channel!')
        return
    else:
        toggle_in_session(ctx.channel.id)
    
    if not p:
        await ctx.send('Starting in 3 seconds...')
        await asyncio.sleep(3)
    print(f"Starting cd in guild '{ctx.guild.name}' with id {ctx.guild.id}...")

    scores = {}
    idle_start = time.time()

    while True:
        prob = random.choice(probs.all_probs)()
        question, answer = prob['q'], prob['a']
        await ctx.send(question)

        start_time = time.time_ns()

        def correct_or_quit(m):
            str_ = m.content.lower().replace(' ', '')
            try:
                return (str_ == QUIT_STRING or round(float(str_), 3) == round(answer,3)) and m.channel == ctx.channel
            except ValueError:
                return

        try:
            msg = await client.wait_for('message', timeout=time_limit, check=correct_or_quit)
            author = msg.author

        except asyncio.TimeoutError:
            msg = None
            author = None
            await ctx.send(f"Time's up! The answer is {round(answer,3)}.")
            time_spent = time_limit

        else:
            if msg.content.lower().replace(' ', '') != QUIT_STRING:
                time_spent = (time.time_ns() - start_time)/1e9
                await ctx.send(f'Correct, {author.name}! You spent {round(time_spent,3)} seconds.')

                author_id = f'{author.name}#{author.discriminator}' # TODO fix unclear variable name author_id vs author.id
                if author_id not in scores:
                    scores[author_id] = 0
                scores[author_id] += 1
                update_stats(author.id, time_spent)

                idle_start = time.time()

        if scores:
            scorestring = '\n'.join([f'{t[0]}: {t[1]}' for t in sorted(list(scores.items()), key=lambda t: t[1])])
        else:
            scorestring = "None. Try and fill up this scoreboard, will ya?"

        # Exit conditions
        if time.time() - idle_start > IDLE_TIMER:
            print (f"Concluded cd in guild '{ctx.guild.name}' with id {ctx.guild.id} (idle for {IDLE_TIMER} seconds)")
            await ctx.send(f'CD aborted due to idle channel.')
            await ctx.send(f'Final scores:\n{scorestring}')
            toggle_in_session(ctx.channel.id)
            return

        if msg and msg.content.lower().replace(' ', '') == QUIT_STRING:
                print (f"Concluded cd in guild '{ctx.guild.name}' with id {ctx.guild.id} (manual quit)")
                await ctx.send(f"CD aborted.")
                await ctx.send(f"Final scores:\n{scorestring}")
                toggle_in_session(ctx.channel.id)
                return

        if max(scores.values(), default=0) >= win_score:
            if not p: 
                await ctx.send(f'Congrats to the winner, {max(scores, key=scores.get)}!')
                await asyncio.sleep(1)
                await ctx.send(f'Final scores:\n{scorestring}')
            print (f"Concluded cd in guild '{ctx.guild.name}' with id {ctx.guild.id} (victory)")
            toggle_in_session(ctx.channel.id)
            return
        
        if p:
            print (f"Concluded cd in guild '{ctx.guild.name}' with id {ctx.guild.id} (cd = p)")
            toggle_in_session(ctx.channel.id)
            return
        
        # Continue round
        await ctx.send(f'Scores:\n{scorestring}')
        await ctx.send(f'Next question in 5 seconds...')
        await asyncio.sleep(5)


_cd_help = f"""Starts a countdown round where members race to solve problems.
    Each question t seconds, first to x points.
    Default: t={DEFAULT_TIMER}, x={DEFAULT_POINT_GOAL}.
    To specify, call cd with both arguments specified, e.g. '<prefix>cd 20 1'.
    Type {QUIT_STRING} at any time to exit the session."""
@client.command(name='cd', help=_cd_help)
async def cd(ctx, *args):
    await _cd(ctx, *args, p=False)


_p_help = f"""Gives a single randomized problem.
"""
@client.command(name='p', help=_p_help)
async def problem(ctx):
    # TODO accept t as argument
    await _cd(ctx, DEFAULT_TIMER, 1, p=True)

# TODO helper function to check answer forms


@client.command(name='stats')
async def stats(ctx, *args):
    """Displays the stats for a Discord user.
    Takes 1 argument: the username + discriminator of a user, e.g. quadraticmuffins#0561.
    If no arguments, displays the stats of whoever called the command.
    """
    if not args:
        user_id = ctx.author.id
    else:
        pass #TODO


    await ctx.send(f'Stats for {ctx.author.name}#{ctx.author.discriminator}:')
    stats = user_stats.find_one({'user_id': user_id})
    if not stats:
        await ctx.send('None. Solve some problems to get your stats!')
    else:
        statstring = '\n'.join(f'{key}: {value}'for key, value in stats.items())
        await ctx.send(statstring)


@client.command(name='clearstats')
async def clear_stats(ctx):
    """Clears your own stats. You cannot modify anyone else's stats."""
    pass #TODO

def update_stats(user_id,time_spent):
    user_stats.update_one({'user_id': user_id}, {'$inc': {'num_solved': 1, 'total_time': time_spent}}, upsert=True)


if __name__ == '__main__':
    client.run(TOKEN)
