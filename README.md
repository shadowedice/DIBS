# DIBS
Discord Interactive Butler/Bot Service

#DIBS List Of Commands

### Magic The Gathering
Command | Description | Usage
--------|--------------|-------
`$mtg` |  Retrieves the card information, picture, and price | $mtg snap
`$mtgtext` | Retrieves the card information | $mtgtext snap
`$mtgimage` | Retrieves the card image | $mtgimage snap
`$mtglegaity` | Retrieves the card legality | $mtglegality snap
`$mtgrulings` | Retrieves the card rulings | $mtgrulings snap

### Stocks
Command | Description | Usage
--------|--------------|-------
`$stock` |  Retrieves the stock's current price and graph | $stock amd

### Sound Effects
Command | Description | Usage
--------|--------------|-------
`$sb` | Plays a sound effect, with possible text and a counter | $sb myman

### Tic Tac Toe
Command | Description | Usage
--------|--------------|-------
`$tictactoe` |  Challenges another player to a game of tic tac toe | $tictactoe @ShadowedIce
`$ttt` | If currently your turn and spot is free, places your mark | $ttt 1 1
`$ttt board` | Prints the current board | $ttt board
`$ttt turn` | Displays the current users turn | $ttt turn
`$ttt quit` | Ends the current game if you are playing | $ttt quit

### Admin
Command | Description | Usage
--------|--------------|-------
`$admin add` | Adds an admin, sb, holidayChannel, twitchChannel (Creates admin if one doesnt exist) | $admin add sb test test.mp3
`$admin remove` | Removes an admin, sb, holidayChannel, twitchChannel | $admin remove sb test
`$admin mute` | Mutes a user or sb | $admin mute sb test
`$admin unmute` | Unmutes a user or sb | $admin unmute sb test
`$admin update` | updates a whois | $admin update whois @name name

### Who is
Command | Description | Usage
--------|--------------|-------
`$iam` |  Sets the stored name for a user | $iam John Doe
`$whois` |  Retrieves the stored name for a user | $whois @JohnDoe

### Holidays
Command | Description | Usage
--------|--------------|-------
`$turkey` | Grabs a turkey if in the channel  | $turkey
`$bags` | Grabs bags if in the channel | $bags 3
`$gifts` | Grabs gifts if in the channel | $gifts 2
`$coal` | Grabs coal if in the channel | $coal 10
`$openBags` | Opens bags to get gifts or coal | $openBags 2
`$convertBags` | Changes bags to gifts | $convertBags 4
`$convertCoal` | Changes coal to gifts | $convertCoal 10
`$coalMagic` | Checks how much coal would make 1 gift | $coalMagic
`$stealGifts` | Steals gifts from another user...or does it? | $stealGifts @ShadowedIce
`$giveGifts` | Gives gifts to another user | $giveGifts @ShadowedIce 2
`$christmasScore` | Checks the score board for the christmas game | $christmasScore

## Twitch
Command | Description | Usage
--------|--------------|-------
`$addTwitch` | Adds your name to the list of twitch streamers. Will periodically check if live. | $addTwitch shadowedice
`$removeTwitch` | Removes your name from the list of twitch streamers.  | $removeTwitch