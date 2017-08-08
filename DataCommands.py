import discord
from discord.ext import commands
import logging
import asyncio
from espnff import League
import requests
import json
import os
import time
from operator import attrgetter


class Stats():
    def __init__(self, bot):
        self.bot = bot

    'Team Data Commands'
    @bot.command()
    async def teams():
        for team in league.teams:
            await bot.say(team.team_name + ": Owned by " + team.owner)


    @bot.command()
    async def east():
        await bot.say("East Division:")
        await bot.say("==================")
        for team in league.teams:
            if team.division_id == 0:
                await bot.say(team.team_name)


    @bot.command()
    # @commands.has_permissions(manage_messages=True)
    async def west():
        await bot.say("West Division:")
        await bot.say("==================")
        for team in league.teams:
            if team.division_id == 1:
                await bot.say(team.team_name)


    @bot.command(pass_context=True)
    async def won(ctx, *, name: str):
        for team in league.teams:
            if team.team_name.lower() == name.lower():
                await bot.say(team.team_name + " has won " + str(team.wins) + " games!")
                return
            elif name.lower() in team.owner.lower():
                await bot.say(team.owner + "'s team has won " + str(team.wins) + " games!")
                return
        await bot.say("Hmm...I couldn't find a team or owner named \"" + name + "\".")


    @bot.command(pass_context=True)
    async def lost(ctx, *, name: str):
        for team in league.teams:
            if team.team_name.lower() == name.lower():
                await bot.say(team.team_name + " has lost " + str(team.losses) + " games!")
                return
            elif name.lower() in team.owner.lower():
                await bot.say(team.owner + "'s team has lost " + str(team.losses) + " games!")
                return
        await bot.say("Hmm...I couldn't find a team or owner named \"" + name + "\".")


    @bot.command(pass_context=True)
    async def schedule(ctx, *, name: str):
        for team in league.teams:
            if team.team_name.lower() == name.lower():
                await bot.say(team.owner + "'s Schedule")
                await bot.say("==========================")
                await bot.say('\n'.join('Week {}:\t{}'.format(*k) for k in enumerate(ctx.message.author.roles, 1)))
                return
            elif name.lower() in team.owner.lower():
                await bot.say(team.owner + "'s Schedule")
                await bot.say("==========================")
                await bot.say('\n'.join('Week {}:\t{}'.format(*k) for k in enumerate(map(attrgetter('owner'), team.schedule), 1)))
                return
        await bot.say("Hmm...I couldn't find a team or owner named \"" + name + "\".")


    @bot.command(pass_context=True)
    async def points_for(ctx, *, name: str):
        for team in league.teams:
            if team.team_name.lower() == name.lower():
                await bot.say(team.owner + " has scored " + str(team.points_for) + " total points")
                return
            elif name.lower() in team.owner.lower():
                await bot.say(team.owner + " has scored " + str(team.points_for) + " total points")
                return
        await bot.say("Hmm...I couldn't find a team or owner named \"" + name + "\".")


    @bot.command(pass_context=True)
    async def points_against(ctx, *, name: str):
        for team in league.teams:
            if team.team_name.lower() == name.lower():
                await bot.say(team.owner + " has had " + str(team.points_for) + " total points scored against them.")
                return
            elif name.lower() in team.owner.lower():
                await bot.say(team.owner + " has had " + str(team.points_for) + " total points scored against them.")
                return
        await bot.say("Hmm...I couldn't find a team or owner named \"" + name + "\".")


    @bot.command(pass_context=True)
    async def scores(ctx, *, name: str):
        for team in league.teams:
            if team.team_name.lower() == name.lower():
                await bot.say(team.owner + "'s Scores")
                await bot.say("==========================")
                await bot.say('\n'.join('Week {}:\t{}'.format(*k) for k in enumerate(team.scores, 1)))
                return
            elif name.lower() in team.owner.lower():
                await bot.say(team.owner + "'s Scores")
                await bot.say("==========================")
                await bot.say('\n'.join('Week {}:\t{}'.format(*k) for k in enumerate(team.scores, 1)))
                return
        await bot.say("Hmm...I couldn't find a team or owner named \"" + name + "\".")


    @bot.command(pass_context=True)
    async def ranking(ctx, *, week_num):
        'Need to fix the ranking output'
        await bot.say('\n'.join('{}:\t{}'.format(*k) for k in enumerate(league.power_rankings(week=int(week_num)), 1)))


    @bot.command()
    async def scoreboard():
        scoreboard = league.scoreboard()
        counter = 0
        await bot.say("Current Week Matchups\n==========================")
        for score in scoreboard:
            matchup = scoreboard[counter]
            await bot.say(matchup.home_team.owner + ":\t" + str(matchup.home_score) + " pts\tvs.\t" + matchup.away_team.owner + ":\t" + str(matchup.away_score) + "pts ")
            counter = counter + 1


    @bot.command(pass_context=True)
    async def ping(ctx):
        pingtime = time.time()
        pingms = await bot.say("Pinging... `{}'s` location".format(ctx.message.author.mention))
        ping = time.time() - pingtime
        await bot.edit_message(pingms, "The ping time is `%.01f seconds`" % ping)

def setup(bot):
    bot.add_cog(Stats(bot))
