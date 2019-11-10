import discord
from discord.ext import commands


class GameState:
    def __init__(self, player1, player2):
        self.board = []
        self.board.append(['*', '*', '*'])
        self.board.append(['*', '*', '*'])
        self.board.append(['*', '*', '*'])
        self.turn = 0
        self.player1 = player1
        self.player2 = player2


class TicTacToe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.game_states = {}
        
    # this command starts a new game. Only one game per channel
    @commands.command(pass_context=True)    
    async def tictactoe(self, ctx, opponent : discord.Member):
        state = self.game_states.get(ctx.message.channel)
        if state is None:
            state = GameState(ctx.message.author, opponent)
            self.game_states[ctx.message.channel] = state
            await ctx.send(self.printBoard(state.board))
        else:
            busy = state.player1.name + " and " + state.player2.name + " are already playing a game!"
            await ctx.send(busy)
    
    # This command updates the game. Must be the correct players turn to change the board.
    @commands.command(pass_context=True)    
    async def ttt(self, ctx, *args :str):
        numArgs = len(args)
        if numArgs == 1 or numArgs == 2:
            state = self.game_states.get(ctx.message.channel)
            if state is not None:
                # Valid commands are board, turn, quit
                if numArgs == 1:
                    text = args[0]
                    if text == "board":
                        await ctx.send(self.printBoard(state.board))
                    elif text == "turn":
                        playerturn = None
                        if (state.turn % 2) == 0:
                            playerturn = state.player1.name
                        else:
                            playerturn = state.player2.name
                        await ctx.send("It is currently " + playerturn + "'s turn.")
                    elif text == "quit":
                        if ctx.message.author == state.player1 or ctx.message.author == state.player2:
                            await ctx.send("Ending the match.")
                            del self.game_states[ctx.message.channel]
                        else:
                            await ctx.send("Only " + state.player1.name + " or " + state.player2.name +
                                           "can end the game.")
                    else:
                        await ctx.send("Unknown command " + text + ".")
                # Requires valid row(1-3) and col(1-3)
                else:
                    mark = '*'
                    if (state.turn % 2) == 0 and state.player1 == ctx.message.author:
                        mark = 'X'
                    elif (state.turn % 2) == 1 and state.player2 == ctx.message.author:
                        mark = 'O'
                            
                    if mark != '*':
                        try:
                            row = int(args[0])
                            col = int(args[1])
                            if 1 <= row <= 3 and 1 <= col <= 3:
                                if state.board[row-1][col-1] == '*':
                                    state.board[row-1][col-1] = mark
                                    state.turn += 1
                                    await ctx.send(self.printBoard(state.board))
                                    check = self.checkForWinner(state)
                                    if check is not None:
                                        await ctx.send(check)
                                        del self.game_states[ctx.message.channel]
                                else:
                                    await ctx.send("That space is already taken!")
                            else:
                                await ctx.send("Invalid row or column!")
                        except ValueError:
                            await ctx.send("Invalid row or column!")
                            
        else:   
            await ctx.send("Invalid command.")
        
    # Prints out the gameboard
    def printBoard(self, board):
        separator = "---------\n"
        row1 = board[0][0] + " | " + board[0][1] + " | " + board[0][2] + "\n"
        row2 = board[1][0] + " | " + board[1][1] + " | " + board[1][2] + "\n"
        row3 = board[2][0] + " | " + board[2][1] + " | " + board[2][2] + "\n"
        return row1 + separator + row2 + separator + row3
    
    # Checks for a winner or a cat game
    def checkForWinner(self, state):
        if state.turn >= 5:
            wins = []
            # rows
            wins.append(state.board[0][0] + state.board[0][1] + state.board[0][2])
            wins.append(state.board[1][0] + state.board[1][1] + state.board[1][2])
            wins.append(state.board[2][0] + state.board[2][1] + state.board[2][2])
            #cols
            wins.append(state.board[0][0] + state.board[1][0] + state.board[2][0])
            wins.append(state.board[0][1] + state.board[1][1] + state.board[2][1])
            wins.append(state.board[0][2] + state.board[1][2] + state.board[2][2])
            #diag
            wins.append(state.board[0][0] + state.board[1][1] + state.board[2][2])
            wins.append(state.board[0][2] + state.board[1][1] + state.board[2][0])

            for possible in wins:
                if possible == "XXX":
                    return state.player1.mention + " triumphed over " + state.player2.mention + "!"
                elif possible == "OOO":
                    return state.player2.mention + " triumphed over " + state.player1.mention + "!"
            
        if state.turn == 9:
            return "Cat game between " + state.player1.mention + " and " + state.player2.mention + "!"
        
        return None
