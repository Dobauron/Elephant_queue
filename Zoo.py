from openpyexcel import load_workbook


def excel(row, col):  # Function used to connect with excel file
    wb = load_workbook('Elephant.xlsx')
    sh = wb.active
    return sh.cell(row, col).value

def zoo_elephant():  # function contain loop which taking data from excel sheet and
    # transfer them into list of elephant class object's
    list_elephant = []
    basic_list=[]

    for row in range(1, excel(2, 1)+1):
        eleph = Elephant(row, excel(row+1, 2))
        list_elephant.append(eleph)
        basic_list.append(excel(row + 1, 3))
        Elephant.boss_queue.append(excel(row + 1, 4))

    for i in basic_list:
        for elephant in list_elephant:
            if i == elephant.number:
                Elephant.current_queue.append(elephant)
    return list_elephant


class Elephant(object):
    Total_mass = 0  # Attribute of class to summary mass of all elephant effort
    sequence = {}   # Sequence of all necessary move to setup elephant's according boss order
    current_queue = []
    boss_queue = []

    def __init__(self, number, mass):
        self.number = number
        self.mass = mass


    def __str__(self):  # only added to check how the algorithm is working
        return "Słoń o numerze:{} i masie:{}".format(self.number,
                                                        self.mass)

    def move(self):  # method to add total mass after elephant move to another position
        Elephant.Total_mass += self.mass





def sequence_setup(elephant1, elephant2):    # Function which geting two elephant objects,
    #  summary their mass and add them into Elephant.sequence - dictionary, wher
    #  key = mass of both object, value = list of both elephant's current postion
    total_move_mass = elephant1.mass + elephant2.mass
    pair_of_elephant = [elephant1.number, elephant2.number]
    Elephant.sequence[total_move_mass] = pair_of_elephant  # Add to Elephant.sequence - class attribute


def elephant_swap():  # Function which return list of position two elephant with the smallest mass to move
    for key, value in Elephant.sequence.items():
        if key == min(Elephant.sequence):
            return value


def main():
    elephants = zoo_elephant()  # list of objects elephant class

    for i in range(len(Elephant.current_queue)):
        for el in range(len(Elephant.boss_queue)):
                if Elephant.current_queue[el].number != Elephant.boss_queue[el]:
                    for ele in Elephant.current_queue:
                        if ele.number == Elephant.boss_queue[el]:
                            sequence_setup(Elephant.current_queue[el],ele)

        for elephant in Elephant.current_queue:
            if elephant_swap() is not None:
                if elephant.number == elephant_swap()[0]:
                    ele1_index = Elephant.current_queue.index(elephant)
                    for elephant2 in Elephant.current_queue:
                        if elephant_swap() is not None:
                            if elephant2.number == elephant_swap()[1]:
                                ele2_index = Elephant.current_queue.index(elephant2)
                                Elephant.current_queue.insert(ele2_index, elephant)
                                del Elephant.current_queue[ele2_index+1]
                                Elephant.current_queue.insert(ele1_index, elephant2)
                                del Elephant.current_queue[ele1_index+1]
                                elephant.move()
                                elephant2.move()
                                Elephant.sequence = {} # After each elephant position exchange, reset Elephant.sequence








main()

print(Elephant.Total_mass)
