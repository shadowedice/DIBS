import discord
import MagicCard
import Token

client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
			
    if message.content.startswith('$alex'):
         await client.send_message(message.channel, 'Alex does suck dick legit.')
         
    elif message.content.startswith('$mtg jamal'):
         await client.send_message(message.channel, 'Fuck you Brian')
    
    elif message.content.startswith('$mtgimage'):
        card_id = MagicCard.card_check(message.content[10:])
        if card_id:
            imgname = MagicCard.card_image(card_id)
            await client.send_file(message.channel, imgname)
        
    elif message.content.startswith('$mtgtext'):
        card_id = MagicCard.card_check(message.content[9:])
        if card_id:
            text = MagicCard.card_text(card_id)
            await client.send_message(message.channel, text)
        
    elif message.content.startswith('$mtgprice'):
        card_id = MagicCard.card_check(message.content[10:])
        if card_id:
            price = MagicCard.card_price(message.content[10:])
            await client.send_message(message.channel, price)
        
    elif message.content.startswith('$mtg'):
        card_id = MagicCard.card_check(message.content[5:])
        if card_id:
            reply = MagicCard.card_text(card_id)
            reply += MagicCard.card_price(message.content[5:])
            imgname = MagicCard.card_image(card_id)
            await client.send_file(message.channel, imgname, content=reply)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
	
client.run(Token.get_token())