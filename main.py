"""
Math problem generator for practice and competition.
Inspired by Art of Problem Solving's FTW, which was
deprecated when Adobe Flash was phased out after 2020.
"""

import discord
from discord.ext import commands

import os

import random
import time
import asyncio
import json

import problem_gen as pg

RECORDS_PATH = 'C:/Users/jettw/Documents/Sophia Tutoring/speed_bot/user_records.json'
ANS_TOLERANCE = 0.0001
DEFAULT_TIMER = 45
DEFAULT_POINT_GOAL = 4
# PROBLEMS = [f for _, f in problem_gen.__all__]

# %%
# question_generators = [*problem_type.problems() for problem_type in questions]


TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = "&"

client = commands.Bot(command_prefix = PREFIX)

@client.event
async def on_ready():
    print('Bot ready!')

__in_problem = False

@client.command(name='ping')
async def ping(ctx):
    await ctx.send('pong!')

@client.command(name='cd')
async def cd(ctx, *args):
    f"""
    Starts a countdown round where members race to solve problems.
    Format is first to x points, each question t seconds.
    Default: t={DEFAULT_TIMER}, x={DEFAULT_POINT_GOAL}.
    To customize, call {PREFIX}cd with both arguments specified.
    """
    if len(args) == 2 and problem_gen.helpers.check_pos_int(args):
        t, x = args
    elif len(args) == 0:
        t, x = 45, 4
    else:
        await ctx.send(f'Improper arguments to {PREFIX}')




@client.command(name='p')
async def problem(ctx):
    """
    Serves a randomized problem.
    """
    global __in_problem
    if __in_problem:
        await ctx.send('There\'s already an active question!')
        return
    print('Generating problem...')

    question, answer = random.choice(question_generators)()
    await ctx.send(question)
    __in_problem = True
    start_time = time.time_ns()

    def check(m):
        try:
            return round(float(m.content), 3) == round(answer,3) and m.channel == ctx.channel
        except ValueError:
            return
    
    try:
        await client.wait_for('message', timeout=DEFAULT_TIMER, check=check)
    except asyncio.TimeoutError:
        await ctx.send(f'Time out! The answer is {round(answer,3)}.')
        time_spent = DEFAULT_TIMER
    else:
        await ctx.send(f'Correct! You spent {round(time_spent,3)} seconds.')
        time_spent = (time.time_ns() - start_time)/1e9
    author_id = f'{ctx.author.name}#{ctx.author.discriminator}'
    update(author_id,time_spent)
    __in_problem = False
    

@client.command(name='stats')
async def stats(ctx):
    author_id = f'{ctx.author.name}#{ctx.author.discriminator}'
    with open(RECORDS_PATH, 'r', encoding='utf-8') as f:
        try:
            record = json.load(f)[author_id]
        except:
            record = None
    await ctx.send(f'Stats for {author_id}:'
        f'{record}')
    #TODO properly format the stats string

def update(user,time_spent):
    with open(RECORDS_PATH, 'r', encoding='utf-8') as f:
        all_records = json.load(f)
    if user not in all_records:
        last_10 = [-1000] * 9
        last_10.append(time_spent)
        all_records[user] = {'problems attempted': 1, 'avg time': time_spent, 
        'last 10 times': last_10}
        with open('user_records.json','w', encoding='utf-8') as f:
            json.dump(all_records, f, indent=2, ensure_ascii=False)
        return
    record = all_records[user]
    record['avg time'] = (record['avg time']*record['problems attempted'] + time_spent)/(record['problems attempted'] + 1)
    record['problems attempted'] += 1
    q = record['last 10 times']
    q.pop(0)
    q.append(time_spent)
    record['last 10 times'] = q
    with open(RECORDS_PATH,'w', encoding='utf-8') as f:
        json.dump(all_records, f, indent=2, ensure_ascii=False)
# %%
client.run(TOKEN)
