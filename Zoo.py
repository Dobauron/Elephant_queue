from openpyexcel import load_workbook


def excel(row, col):  # Function used to connect with excel file
    wb = load_workbook('Elephant.xlsx')
    sh = wb.active
    return sh.cell(row, col).value


def zoo_elephant():  # function contain loop which taking data from excel sheet and
    # transfer them into list of elephant class object's

    list_elephant = []  # list of elephant class object's
    non_boss_list = []  # list of basic elephant setup

    for row in range(1, excel(2, 1)+1):
        eleph = Elephant(row, excel(row+1, 2))  # object creation, according excel sheet, argument(mass, number)
        list_elephant.append(eleph)  # list of elephant object
        non_boss_list.append(excel(row + 1, 3))  # first elephant queue
        Elephant.boss_queue.append(excel(row + 1, 4))  # elephant queue according boss demands

    for i in non_boss_list:  # loop for create current_queue - list of elephant object set according non_boss_list
        for elephant in list_elephant:
            if i == elephant.number:
                Elephant.current_queue.append(elephant)


class Elephant(object):
    Total_mass = 0  # Attribute of class to summary mass of all elephant effort
    sequence = {}   # Sequence of all necessary move to setup elephant's according boss order
    current_queue = []  # List of actual elephant class objects setup
    boss_queue = []

    def __init__(self, number, mass):
        self.number = number
        self.mass = mass

    def __str__(self):  # only added to check how the algorithm is working
        return "Słoń o numerze:{} i masie:{}".format(self.number,
                                                     self.mass)

    def move(self):  # method for add total mass after elephant move to another position
        Elephant.Total_mass += self.mass


def sequence_setup(elephant1, elephant2):    # Function which geting two elephant objects,
    #  summary their mass and add them into Elephant.sequence - dictionary, wher
    #  key = mass of both object, value = list of both elephant's current postion
    total_move_mass = elephant1.mass + elephant2.mass
    pair_of_elephant = [elephant1.number, elephant2.number]
    Elephant.sequence[total_move_mass] = pair_of_elephant  # Add to Elephant.sequence - class attribute


def min_mass_swap():  # Function which return list of position two elephant with the smallest mass to move
    for key, value in Elephant.sequence.items():
        if key == min(Elephant.sequence):
            return value


def swap_list(el_index1, el_index2, obj1, obj2):  # Function for exchange elephant
    # in current_queue
    Elephant.current_queue.insert(el_index2, obj1)
    del Elephant.current_queue[el_index2 + 1]
    Elephant.current_queue.insert(el_index1, obj2)
    del Elephant.current_queue[el_index1 + 1]
    obj1.move()
    obj2.move()


def main():
    zoo_elephant()  # necessary to create Elephant.current_queue - main list

    for i in range(len(Elephant.current_queue)):  # General loop
        for el in range(len(Elephant.boss_queue)):  # Loop for checking difference between
            # boss_queue and current_queue, if find the difference then
            # call a function sequence_setup with two argument = two objects which need to be exchange
            if Elephant.current_queue[el].number != Elephant.boss_queue[el]:
                for ele in Elephant.current_queue:
                    if ele.number == Elephant.boss_queue[el]:
                        sequence_setup(Elephant.current_queue[el], ele)

        for elephant in Elephant.current_queue:  # Loop to find two elephant with the smallest mass exchange and
            # swap them in the current_queue by index until reach boss_queue setup
            if min_mass_swap() is not None:
                if elephant.number == min_mass_swap()[0]:
                    ele1_index = Elephant.current_queue.index(elephant)
                    for elephant2 in Elephant.current_queue:
                        if min_mass_swap() is not None:
                            if elephant2.number == min_mass_swap()[1]:
                                ele2_index = Elephant.current_queue.index(elephant2)
                                swap_list(ele1_index, ele2_index, elephant, elephant2)
                                Elephant.sequence = {}  # After each elephant position exchange, reset Elephant.sequence


main()

print(Elephant.Total_mass)
