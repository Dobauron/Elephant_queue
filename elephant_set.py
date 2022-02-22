from openpyexcel import load_workbook


def excel(row, col):  # Function used to connect with excel file
    wb = load_workbook('Elephant.xlsx')
    sh = wb.active
    return sh.cell(row, col).value


def zoo():  # function contain loop which taking data from excel sheet and
    # transfer them into list of elephant class object's
    list_elephant = []
    for row in range(1, excel(2, 1)+1):
        eleph = Elephant(row, excel(row+1, 2), excel(row+1, 3), excel(row+1, 4))
        list_elephant.append(eleph)
    return list_elephant


class Elephant(object):
    Total_mass = 0  # Attribute of class to summary mass of all elephant effort
    sequence = {}   # Sequence of all necessary move to setup elephant's according boss order

    def __init__(self, number, mass, current_postion, demended_postion):
        self.number = number
        self.mass = mass
        self.current_position = current_postion
        self.demanded_postion = demended_postion

    def __str__(self):  # only added to check how the algorithm is working
        return "Słoń o numerze:{} i masie:{}, obecnej pozycji:{}, żądanej pozycji:{}".format(self.number,
                                                                                             self.mass,
                                                                                             self.current_position,
                                                                                             self.demanded_postion)

    def move(self):  # method to add total mass after elephant move to another position
        Elephant.Total_mass += self.mass


def sequence_setup(elephant1, elephant2):    # Function which geting two elephant objects,
    #  summary their mass and add them into Elephant.sequence - dictionary, wher
    #  key = mass of both object, value = list of both elephant's current postion
    total_move_mass = elephant1.mass + elephant2.mass
    from_to_postion_move = [elephant1.current_position, elephant2.current_position]
    Elephant.sequence[total_move_mass] = from_to_postion_move  # Add to Elephant.sequence - class attribute


def elephant_swap():  # Function which return list of position two elephant with the smallest mass to move
    for key, value in Elephant.sequence.items():
        if key == min(Elephant.sequence):
            return value


def main():

    elephants = zoo()  # list of objects elephant class

    for i in range(len(elephants)):  # Main loop to repeat whole sequence
        for ele in elephants:  # Loop for choose elephant which are not on boss recomended spot
            if ele.current_position == ele.demanded_postion:
                continue
            elif ele.current_position != ele.demanded_postion:
                for ele2 in elephants:  # Loop for choose second elephant, whos current spot is same
                                        # as boss recomended spot for first elephant
                    if ele2.current_position == ele.demanded_postion:
                        sequence_setup(ele, ele2)  # Both objects of class elephant are sended to function - 'queue_setup'


        for el in elephants:  # Loop for exchange position of elephants with the smallest mass value
            if elephant_swap() is not None:
                if el.current_position == elephant_swap()[0]:
                    el.current_position = elephant_swap()[1]

                    el.move()  # add mass of first elephant into the Elephant.Total_mass
                elif el.current_position == elephant_swap()[1]:
                    el.current_position = elephant_swap()[0]

                    el.move()  # add mass of el into the Elephant.Total_mass

        else:
            Elephant.sequence = {}  # After each elephant position exchange, reset Elephant.sequence for
                                    # create new sequence of demanded moves and their mass cost


main()
print(Elephant.Total_mass)