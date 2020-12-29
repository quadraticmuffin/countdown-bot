"""
Math problem generator for practice and competition.
Inspired by Art of Problem Solving's FTW, which was
deprecated when Adobe Flash was phased out after 2020.
"""

# COMMENT THESE TWO LINES BEFORE PUSHING TO PROD
from dotenv import load_dotenv
load_dotenv()

import discord
from discord.ext import commands

import os

import random
import time
import asyncio
import json
import pymongo

import problem_gen as probs

ANS_TOLERANCE = 0.0001
DEFAULT_TIMER = 45
DEFAULT_POINT_GOAL = 4

TOKEN = os.getenv('DISCORD_TOKEN')
DEFAULT_PREFIX = "&"

def get_prefix(client, ctx):
    return DEFAULT_PREFIX
# TODO store prefix by guild in db

client = commands.Bot(command_prefix = get_prefix)

channels_in_session = set()

def check_in_session(channel_id):
    return channel_id in channels_in_session

def toggle_in_session(channel_id):
    global channels_in_session
    channels_in_session ^= {channel_id} # Set symmetric difference

@client.event
async def on_ready():
    print('Bot ready!')

############
# COMMANDS # 
############

@client.command(name='ping')
async def ping(ctx):
    await ctx.send('pong!')

# TODO 
@client.command(name='cd')
async def cd(ctx, *args):
    f"""
    Starts a countdown round where members race to solve problems.
    Format is first to x points, each question t seconds.
    Default: t={DEFAULT_TIMER}, x={DEFAULT_POINT_GOAL}.
    To customize, call {DEFAULT_PREFIX}cd with both arguments specified.
    """
    if len(args) == 2:
        t, x = args
    elif len(args) == 0:
        t, x = 45, 4
    else:
        await ctx.send(f'Improper arguments to {get_prefix(client, ctx)}cd')


@client.command(name='p')
async def problem(ctx):
    """
    Serves a randomized problem.
    """
    if check_in_session(ctx.channel.id):
        await ctx.send('There\'s already an active question in this channel!')
        return

    toggle_in_session(ctx.channel.id)

    print('Generating problem...')

    prob = random.choice(probs.all_probs)()
    question, answer = prob['q'], prob['a']

    await ctx.send(question)
    __in_problem = True
    start_time = time.time_ns()

    def check(m):
        try:
            return round(float(m.content), 3) == round(answer,3) and m.channel == ctx.channel
        except ValueError:
            return
    
    try:
        ans = await client.wait_for('message', timeout=DEFAULT_TIMER, check=check)
    except asyncio.TimeoutError:
        await ctx.send(f'Time out! The answer is {round(answer,3)}.')
        time_spent = DEFAULT_TIMER
    else:
        time_spent = (time.time_ns() - start_time)/1e9
        await ctx.send(f'Correct, {ans.author.name}! You spent {round(time_spent,3)} seconds.')
        author_id = f'{ans.author.name}#{ans.author.discriminator}'
    finally:
        toggle_in_session(ctx.channel.id)
    
# TODO helper function to serve problems
# TODO helper function to check answer forms
# TODO update stats; connect to mongodb for that


@client.command(name='stats')
async def stats(ctx):
    pass

def update(user,time_spent):
    pass


if __name__ == '__main__':
    client.run(TOKEN)
