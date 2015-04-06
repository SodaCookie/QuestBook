import text_game
import traceback
import imp

game = text_game.Game()
quitting = False
while not quitting:
    i = input("Command << ")
    command = "1234 " + i
    if i == "quit":
        quitting = True
    elif i == "reset":
        imp.reload(text_game)
        del game
        game = text_game.Game()
    elif len(i) > 1 and i[0] == "$":
        try:
            exec(i[1:])
        except:
            traceback.print_exc()
    else:
        try:
            print(game.inputCommand(command.split(" ")))
        except:
            traceback.print_exc()