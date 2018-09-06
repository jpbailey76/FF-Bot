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
    def __init__(self, bot, league_id, year):
        self.bot = bot
        self.league_id = 1380682
        self.year = 2018
        self.league = League(league_id, year)

    'Pulled the server channel ID to be stored in the database'
    async def on_server_join(self, server):
        print("test")
        print("Joining server: {0.id} ({0.name})".format(server))

    'League Info'
    @commands.has_permissions(administrator=True)
    @commands.command(pass_context=True)
    async def leagueid(self, ctx, *, id: str):
        try:
            try:
                self.league = League(int(id), 2018)
            except:
                await bot.say("Unable to find a league with ID \"" + id +"\".")
            print("New League ID: " + str(self.league.league_id))
            await self.bot.say("The league has been changed to: " + self.league.settings.name)
        except discord.errors.Forbidden:
            await self.bot.say("Missing Permissions.") 


    'Team Data Commands'
    @commands.command()
    async def teams(self):
        teamList = []
        await self.bot.say("Teams:\n==================")
        for team in self.league.teams:
            teamList.append(team.team_name)
        await self.bot.say('\n '.join(teamList))


    @commands.command()
    async def east(self):
        eastList = []
        await self.bot.say("East Division:\n==================")
        for team in self.league.teams:
            if team.division_id == 0:
                eastList.append(team.team_name)
                #await self.bot.say(team.team_name)
        await self.bot.say('\n'.join(eastList))

    @commands.command()
    # @commands.has_permissions(manage_messages=True)
    async def west(self):
        westList = []
        await self.bot.say("West Division:\n==================")
        for team in self.league.teams:
            if team.division_id == 1:
                westList.append(team.team_name)
                #await self.bot.say(team.team_name)
        await self.bot.say('\n'.join(westList))

    @commands.command(pass_context=True)
    async def won(self, ctx, *, name: str):
        for team in self.league.teams:
            if team.team_name.lower() == name.lower():
                await self.bot.say(team.team_name + " has won " + str(team.wins) + " games!")
                return
            elif name.lower() in team.owner.lower():
                await self.bot.say(team.owner + "'s team has won " + str(team.wins) + " games!")
                return
        await self.bot.say("Hmm...I couldn't find a team or owner named \"" + name + "\".")

    @commands.command(pass_context=True)
    async def lost(self, ctx, *, name: str):
        for team in self.league.teams:
            if team.team_name.lower() == name.lower():
                await self.bot.say(team.team_name + " has lost " + str(team.losses) + " games!")
                return
            elif name.lower() in team.owner.lower():
                await self.bot.say(team.owner + "'s team has lost " + str(team.losses) + " games!")
                return
        await self.bot.say("Hmm...I couldn't find a team or owner named \"" + name + "\".")

    @commands.command(pass_context=True)
    async def schedule(self, ctx, *, name: str):
        for team in self.league.teams:
            if team.team_name.lower() == name.lower():
                await self.bot.say(team.owner + "'s Schedule")
                await self.bot.say("==========================")
                await self.bot.say('\n'.join('Week {}:\t{}'.format(*k) for k in enumerate(ctx.message.author.roles, 1)))
                return
            elif name.lower() in team.owner.lower():
                await self.bot.say(team.owner + "'s Schedule")
                await self.bot.say("==========================")
                await self.bot.say('\n'.join('Week {}:\t{}'.format(*k) for k in enumerate(map(attrgetter('owner'), team.schedule), 1)))
                return
        await self.bot.say("Hmm...I couldn't find a team or owner named \"" + name + "\".")

    @commands.command(pass_context=True)
    async def points_for(self, ctx, *, name: str):
        for team in self.league.teams:
            if team.team_name.lower() == name.lower():
                await self.bot.say(team.owner + " has scored " + str(team.points_for) + " total points")
                return
            elif name.lower() in team.owner.lower():
                await self.bot.say(team.owner + " has scored " + str(team.points_for) + " total points")
                return
        await self.bot.say("Hmm...I couldn't find a team or owner named \"" + name + "\".")

    @commands.command(pass_context=True)
    async def points_against(self, ctx, *, name: str):
        for team in self.league.teams:
            if team.team_name.lower() == name.lower():
                await self.bot.say(team.owner + " has had " + str(team.points_for) + " total points scored against them.")
                return
            elif name.lower() in team.owner.lower():
                await self.bot.say(team.owner + " has had " + str(team.points_for) + " total points scored against them.")
                return
        await self.bot.say("Hmm...I couldn't find a team or owner named \"" + name + "\".")

    @commands.command(pass_context=True)
    async def scores(self, ctx, *, name: str):
        for team in self.league.teams:
            if team.team_name.lower() == name.lower():
                await self.bot.say(team.owner + "'s Scores\n==========================")
                await self.bot.say('\n'.join('Week {}:\t{}'.format(*k) for k in enumerate(team.scores, 1)))
                return
            elif name.lower() in team.owner.lower():
                await self.bot.say(team.owner + "'s Scores\n==========================")
                await self.bot.say('\n'.join('Week {}:\t{}'.format(*k) for k in enumerate(team.scores, 1)))
                return
        await self.bot.say("Hmm...I couldn't find a team or owner named \"" + name + "\".")

    @commands.command(pass_context=True)
    async def ranking(self, ctx, *, week_num):
        'Need to fix the ranking output'
        await self.bot.say('\n'.join('{}:\t{}'.format(*k) for k in enumerate(league.power_rankings(week=int(week_num)), 1)))

    @commands.command()
    async def scoreboard(self):
        scoreboard = self.league.scoreboard()
        counter = 0
        await self.bot.say("Current Week Matchups\n==========================")
        for score in scoreboard:
            matchup = scoreboard[counter]
            await self.bot.say(matchup.home_team.owner + ":\t" + str(matchup.home_score) + " pts\tvs.\t" + matchup.away_team.owner + ":\t" + str(matchup.away_score) + "pts ")
            counter = counter + 1

    @commands.command(pass_context=True)
    async def ping(self, ctx):
        pingtime = time.time()
        pingms = await self.bot.say("Pinging... `{}'s` location".format(ctx.message.author.mention))
        ping = time.time() - pingtime
        await self.bot.edit_message(pingms, "The ping time is `%.01f seconds`" % ping)

def setup(bot):
    bot.add_cog(Stats(bot, 1380682, 2018))
