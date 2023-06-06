import os
import random
import time

# getting the brain storage
brain = os.getcwd() + '\\' + "brain"
cells = [" ", " ", " ", " ", " ", " ", " ", " ", " "]


# keep prompting the user until int given
def persist_int(message):
    int_val = "3"  # input(message) TODO
    while not int_val.isnumeric():
        int_val = input("please enter an integer value")

    return int(int_val)


def get_brain():
    with open(brain, "r") as brain_read:
        return brain_read.read()


def render_board():
    print("{:^3}|{:^3}|{:^3}".format(cells[0], cells[1], cells[2]))
    print("---+---+---")
    print("{:^3}|{:^3}|{:^3}".format(cells[3], cells[4], cells[5]))
    print("---+---+---")
    print("{:^3}|{:^3}|{:^3}".format(cells[6], cells[7], cells[8]))
    print()


# prompt if the user wants to set up a new brain storage
toSetup = "y"  # input("format brain? [yes/no]").lower() TODO
while not toSetup.startswith("y") and not toSetup.startswith("n"):
    toSetup = input("please enter a valid value").lower()

# if we're formatting the brain
if toSetup.startswith("y"):
    with open(brain, "w") as brain_write:
        for layer in range(persist_int("number of neuron layers")):
            for neuron in range(9):
                for neuron_ref in range(9):
                    brain_write.write(str(neuron_ref)+":10,")
                brain_write.write("\n")
            brain_write.write("\n\n")

bot_turn = random.choice([True, False])

gameDone = True
while not gameDone:
    time.sleep(1)
    render_board()

    if bot_turn:
        pass

# close the files
if brain_write:
    brain_write.close()
