# bot.py
import os
import random
import re
import collections
from datetime import date
from discord.ext import commands
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')


@bot.command(name='ejemplo', help='Por si no te enteras')
async def roll(ctx):
    ejemplo = """1. ElPanaMiguel ...... 14578978
2. Yo ...... 787899
3. Katri ...... 457897
4. YoOtraVez ...... 14564
5. MiAbuela(QueEstaMuerta) ...... 4578
1. Yo ...... 14578978
2. Katri ...... 787899
3. MiAbuela(QueEstaMuerta) ...... 457897
4. ElPanaMiguel ...... 14564
5. YoOtraVez ...... 4578"""
    await ctx.message.delete()
    await ctx.send(ejemplo)

def check(ctx):
    return lambda m: m.author == ctx.author and m.channel == ctx.channel

async def get_input_of_type(func, ctx):
	while True:
		try:
			msg = await bot.wait_for('message', check=check(ctx))
			return func(msg.content)
		except ValueError:
			if(func == int):
				await ctx.send("Pásame un número entero, crack")
			else:
				await ctx.send("El formato no está muy fino, usa !ejemplo")

@bot.command(name='mideTulas', help='Mira quien la tiene mas larga')
async def medir(ctx):

	try:
		await ctx.message.delete()
		await ctx.send("¿De cuantos participantes es el ranking?")
		ranking = await get_input_of_type(int, ctx)
		await ctx.send("Pegame los rankings (puedes usar !ejemplo para ver el formato)")
		resultados = await get_input_of_type(str, ctx)

		embed = discord.Embed(title=f"__**Los más facheros:**__", color=0x03f8fc,timestamp= ctx.message.created_at)
		resList = resultados.split("\n")
		pares = {}
		for res in resList:
		    par = re.findall("(.*) .\.\.\.",res)
		    for p in par:
		        pareja = p.split(" ")
		        pareja[0] = pareja[0].replace(" ","").replace(".","")
		        if pareja[1] not in pares:
		            pares[pareja[1]]  = ranking + 1 - int(pareja[0])
		        else:
		            pares[pareja[1]]  = pares[pareja[1]] + ranking + 1 - int(pareja[0])
		pares_ordenados = sorted(pares.items(), key=lambda kv: kv[1], reverse=True)
		await ctx.send('**'+pares_ordenados[0][0] +'**' + ", tremenda tula compañero" ) 
		indice = 1
		mensaje = [
			":warning: Solo cuentan las kills, si no cae el boss no se guarda el daño/heal que estabas haciendo. \n",
			":arrows_counterclockwise: Actualizado " + date.today().strftime("%d/%m/%Y") + "\n \n",
			"Puntuación DPS Ny'Alotha HC \n"]
		for par in pares_ordenados:
			if (indice == 1):
				mensaje.append(":first_place: ")
			if (indice == 2):
				mensaje.append(":second_place: ")
			if (indice == 3):
				mensaje.append(":third_place: ")
			else:
				mensaje.append(str(indice) + ". ")
			mensaje.append(str(str(par[0]) + ": " + str(par[1]) + " :eggplant: \n"))
			indice = indice + 1
		mensaje = ''.join(mensaje)
		await ctx.send(mensaje)
	except ValueError:
		await ctx.send('Así no va esto bro, usa !ejemplo a ver si te aclaras')

bot.run(TOKEN)
