import os
import random
import time
import keyboard
import openpyxl

# getting the brain storage
brain_name = os.getcwd() + '\\' + "brain_spreadsheet.xlsx"
brain_wb = openpyxl.load_workbook(brain_name)
brain_sheet = brain_wb.active

# other variables
move_sequence = []
bot_2_sequence = []
bot_turn = random.choice([True, False])
game_done = False
board = "_"*9
cell_letters = ["B", "C", "D", "E", "F", "G", "K", "I", "J"]
ai_letter = "X"
player_letter = "O"
# 0 1 2
# 3 4 5
# 6 7 8           /       rows       \/      columns     \/  diagonal  \
winning_combos = ["012", "345", "678", "036", "147", "258", "048", "246"]
facing_ai = False


# clear the brain spreadsheet
def reformat_brain():
    brain_sheet.delete_cols(1, brain_sheet.max_column)
    brain_sheet["A1"] = "board_layout"
    for i, letter in enumerate(cell_letters):
        brain_sheet[letter+"1"] = i
    brain_wb.save(brain_name)


# keep prompting the user until int given
def persist_int(message):
    int_val = input(message)
    while not int_val.isnumeric():
        int_val = input("please enter an integer value")

    return int(int_val)


# render the board
def render_board():
    print("{:^3}|{:^3}|{:^3}".format(board[0], board[1], board[2]))
    print("---+---+---")
    print("{:^3}|{:^3}|{:^3}".format(board[3], board[4], board[5]))
    print("---+---+---")
    print("{:^3}|{:^3}|{:^3}".format(board[6], board[7], board[8]))
    print()


# check to see if the input board layout already exists in the table
def check_for_board(main_ai):
    # copy the current board

    if main_ai:
        layout = board
    else:
        layout = ""
        for char in board:
            if char == "X":
                layout += "O"
            elif char == "O":
                layout += "X"
            else:
                layout += "_"

    # cycle through rotated versions of boards
    for flip_ver in range(2):
        for rotate_ver in range(4):
            # return the value if found
            for cell in brain_sheet["A"]:
                if cell.value == layout:
                    return cell.row

            # rotate the board 90 degrees
            layout = layout[6]+layout[3]+layout[0]+layout[7]+layout[4]+layout[1]+layout[8]+layout[5]+layout[2]
        # flip the board horizontally
        layout = layout[2]+layout[1]+layout[0]+layout[5]+layout[4]+layout[3]+layout[8]+layout[7]+layout[6]


# adds the current board to the list of possibilities
def add_layout():
    # create a new reference for the board in the table
    row = len(brain_sheet["A"])+1
    brain_sheet["A"+str(row)] = board

    # fill up the confidence bars to probably 7
    for option in cell_letters:
        brain_sheet[option+str(row)] = 7

    # save the new sheet
    print("test")
    time.sleep(0.5)
    brain_wb.save(brain_name)


# make a choice and place a marker on the selected space
def make_choice(current_row, main_ai):
    global board
    global move_sequence
    accepted = False

    # get the appropriate letter
    if main_ai:
        letter = ai_letter
    else:
        letter = player_letter

    # until a valid move is played
    while not accepted:
        # create a list with the amount of opportunity to play per confidence
        # like 3 confidence in spot 8 means that 8 would be in the list 3 times

        choices = []
        for cell in cell_letters:
            for i in range(brain_sheet[cell+str(current_row)].value+1):
                choices += [[brain_sheet[cell+"1"].value, cell+str(current_row)]]

        # skip if choices empty
        if len(choices) == 0:
            print("skipped:",board)
            time.sleep(1)
            return

        # break up the board into a list
        b = list(board)
        selected_cell = random.choice(choices)  # select the cell

        # don't let the AI play on occupied spots
        if b[selected_cell[0]] == "_":
            # if the selected cell is unoccupied
            b[selected_cell[0]] = letter
            board = "".join(b)
            render_board()

            move_sequence.append(selected_cell[1])

            accepted = True
        else:
            # if the selected cell is occupied
            brain_sheet[cell_letters[selected_cell[0]]+str(current_row)] = 0  # set confidence to 0
            brain_wb.save(brain_name)


# controls what happens when a bot or the player wins
def check_for_winner():
    global game_done

    modifier_1 = 0
    modifier_2 = 0
    for combo in winning_combos:
        # for every combo sequence

        # get the three spaces that could win
        spaces = []
        for tile in list(combo):
            spaces.append(board[int(tile)])

        # compare the spaces to each other
        if spaces[0] == spaces[1] == spaces[2] == ai_letter:
            # if a move combo is achieved by the AI
            print("AI win")
            game_done = True
            modifier_1 = 2
            modifier_2 = -2

        elif spaces[0] == spaces[1] == spaces[2] == player_letter:
            # if a move combo is achieved by bot2 / the player
            print("bot_2 / player win")
            game_done = True
            modifier_1 = -2
            modifier_2 = 2

        elif "_" not in board:
            # if there is a draw
            print("draw")
            game_done = True
            modifier_1 = 1
            modifier_2 = 1

        # if a winner is found
        if modifier_1 != 0:
            for path in move_sequence:
                brain_sheet[path] = int(brain_sheet[path].value) + modifier_1
            for path_2 in bot_2_sequence:
                brain_sheet[path_2] = int(brain_sheet[path_2].value) + modifier_2
            brain_wb.save(brain_name)
            break


# the player picks where to place a piece
def pick_piece():
    global board

    choice = input("pick a spot (1-9)")
    while choice.isnumeric() and not 1 <= int(choice) <= 9 or not board[int(choice)-1] == "_":
        choice = input("pick a valid option")

    b_lis = list(board)
    b_lis[int(choice)-1] = player_letter
    board = "".join(b_lis)


# the AI's turn
def ai_play(main_bot):
    global bot_turn

    layout_row = check_for_board(main_bot)
    if layout_row:
        # the bot has seen the current board before
        make_choice(layout_row, main_bot)

        # the bot has made a move
        bot_turn = not main_bot
    else:
        # the bot has never seen the board before
        # restart play without switching players
        add_layout()


# run one play of tic-tac-toe
def run_game():
    global bot_turn

    while not game_done:
        # if it is the computer's turn
        if bot_turn:
            # the bot plays
            ai_play(True)
        else:
            # the player plays
            if facing_ai:
                # if 2 AI are fighting
                ai_play(False)
            else:
                pick_piece()
                bot_turn = True

        # check to see if anyone won
        check_for_winner()


# train an AI to play tic-tac-toe
def main():
    global move_sequence
    global game_done

    game_done = False
    run_game()

    print(move_sequence)


# reset the game to the default state
def setup_board():
    global move_sequence
    global bot_turn
    global game_done
    global board

    move_sequence = []
    bot_turn = random.choice([True, False])
    game_done = False
    board = "_"*9


# get brain and players set up
if input("refactor brain [y/n]").lower().startswith("y"):
    reformat_brain()
if input("fight 2 AI (training) [y/n]").lower().startswith("y"):
    facing_ai = True

# game loop
while not keyboard.is_pressed("Esc"):
    setup_board()
    if not bot_turn: render_board()
    main()
    time.sleep(1)
