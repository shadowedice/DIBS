import asyncio
import discord

async def playEffect(client, channel, file):
    try:
        voice = await client.join_voice_channel(channel)
    except:
        return
    
    player = voice.create_ffmpeg_player('./Audio/' + file)
    player.start()
    timer=0
    while player.is_playing():
        await asyncio.sleep(1)
        timer+=1
        if(timer > 30):
            break
    await voice.disconnect() 