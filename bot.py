# bot.py
import os
import re
from datetime import date
from discord.ext import commands

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


def calcula_ranking(resultados, tipo,ranking,raid):
    resList = resultados.split("\n")
    pares = {}
    for res in resList:
        par = re.findall("(.*) .\.\.\.", res)
        for p in par:
            pareja = p.split(" ")
            pareja[0] = pareja[0].replace(" ", "").replace(".", "")
            if pareja[1] not in pares:
                pares[pareja[1]] = ranking + 1 - int(pareja[0])
            else:
                pares[pareja[1]] = pares[pareja[1]] + ranking + 1 - int(pareja[0])
    pares_ordenados = sorted(pares.items(), key=lambda kv: kv[1], reverse=True)
    indice = 1
    mensaje = ["Puntuación " + tipo + " " + raid + "\n"]
    for par in pares_ordenados:
        if (indice == 1):
            mensaje.append(":first_place: ")
        elif (indice == 2):
            mensaje.append(":second_place: ")
        elif (indice == 3):
            mensaje.append(":third_place: ")
        else:
            mensaje.append(str(indice) + ". ")
        mensaje.append(str(str(par[0]) + ": " + str(par[1]) + " :eggplant: \n"))
        indice = indice + 1
    mensaje = ''.join(mensaje)
    return mensaje


@bot.command(name='mideTulas', help='Mira quien la tiene mas larga')
async def medir(ctx):
    try:
        await ctx.message.delete()
        await ctx.send("¿De cuantos participantes es el ranking?")
        ranking = await get_input_of_type(int, ctx)
        await ctx.send("Pásame el nombre de la raid")
        raid = await get_input_of_type(str, ctx)

        await ctx.send("Pegame los rankings de DPS (puedes usar !ejemplo para ver el formato)")
        resultados = await get_input_of_type(str, ctx)

        await ctx.send("Pegame los rankings de HPS (puedes usar !ejemplo para ver el formato)")
        resultadosHeal = await get_input_of_type(str, ctx)

        mensaje = [
        ":warning: Solo cuentan las kills, si no cae el boss no se guarda el daño/heal que estabas haciendo. \n",
        ":arrows_counterclockwise: Actualizado " + date.today().strftime("%d/%m/%Y") + "\n \n"]

        mensaje.append(calcula_ranking(resultados, "DPS", ranking, raid) + "\n")
        mensaje.append(calcula_ranking(resultados, "HPS", ranking, raid))

        mensaje.append("""\n\n:beginner:Las puntuaciones se basan en el HISTORICO de recounts de cada boss. 
            :beginner:El top 1 es el que más DPS ha metido al boss en todos los trys que han caido. 
            :beginner:Si el top DPS actual tiene 50k en un boss, tienes que hacer más de 50k para adelantarle. 
            :beginner:Quedar top 1 un día no significa salir top 1 en las tablas, si alguien ha hecho más dps en el mismo boss otro día también queda guardado.
            :beginner:El top 1 recibe 5 puntos, el top 2 recibe 4 puntos...etc \n""")
	mensaje = ''.join(mensaje)
        await ctx.send(mensaje)

    except ValueError:
        await ctx.send('Así no va esto bro, usa !ejemplo a ver si te aclaras')

bot.run(TOKEN)
