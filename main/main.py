import os
import random
import openpyxl

# getting the brain storage
brain_name = os.getcwd() + '\\' + "brain_spreadsheet.xlsx"
brain_wb = openpyxl.load_workbook(brain_name)
brain_sheet = brain_wb.active

# other variables
bot_turn = True  # random.choice([True, False])
game_done = False
board = "_"*9
cell_letters = ["B", "C", "D", "E", "F", "G", "K", "I", "J"]
ai_letter = "X"

# clear the spreadsheet (i will forget about this and start crying later)
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
def check_for_board():
    # copy the current board
    layout = board

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
    brain_wb.save(brain_name)


# make a choice and place a marker on the selected space
def make_choice(current_row):
    global board
    accepted = False

    # until a valid move is played
    while not accepted:
        # create a list with the amount of opportunity to play per confidence
        # like 3 confidence in spot 8 means that 8 would be in the list 3 times
        choices = []
        for cell in cell_letters:
            choices += [brain_sheet[cell+"1"].value] * brain_sheet[cell+str(current_row)].value

        # break up the board into a list
        b = list(board)
        selected_cell = random.choice(choices)  # select the cell

        # don't let the AI play on occupied spots
        if b[selected_cell] == "_":
            # if the selected cell is unoccupied
            b[selected_cell] = ai_letter
            board = "".join(b)
            render_board()
            accepted = True
        else:
            # if the selected cell is occupied
            print("did the thing")
            brain_sheet[cell_letters[selected_cell]+str(current_row)] = 0  # set confidence to 0
            brain_wb.save(brain_name)


# main
def main():
    global bot_turn
    while not game_done:
        # if it is the computer's turn
        if bot_turn:
            # the bot plays
            layout_row = check_for_board()
            if layout_row:
                # the bot has seen the current board before
                make_choice(layout_row)

                # the bot has made a move
                bot_turn = False
                continue
            else:
                # the bot has never seen the board before
                add_layout()
                continue  # restart play without switching players
        else:
            # the player plays
            pass

        break


main()
