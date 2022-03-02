def convert_data_from_file(line):  # Function which converting data from input and return them as a list of integer's
    list_of_value = []
    var = ''
    for el in line:
        if el != ' ' and el != '\n':
            var += el
        elif el == ' ' or el == '\n':
            list_of_value.append(int(var))
            var = ''
            continue
        elif el == '\\n':
            list_of_value.append(int(var))
            break
    return list_of_value


def get_file_data():  # Function used to connect with .txt file
    file = open('Elephant_reader.txt', 'r')
    quantity = file.readline()
    mass = file.readline()
    basic = file.readline()
    boss = file.readline()
    file.close()
    return [quantity, mass, basic, boss]


def list_boss_and_basic_creator():  # function contain loop which taking data from excel sheet and
    # transfer them into list of elephant class object's

    list_elephant = []  # list of elephant class object's
    non_boss_list = convert_data_from_file(get_file_data()[2])  # list of basic elephant setup

    for row in range(1, convert_data_from_file(get_file_data()[0])[0]+1):
        eleph = Elephant(row, convert_data_from_file(get_file_data()[1])[row-1]) # object creation, according excel sheet, argument(mass, number)

        list_elephant.append(eleph)  # list of elephant object
        Elephant.boss_queue.append(convert_data_from_file(get_file_data()[3])[row-1])  # elephant queue according boss demands

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


def setup_sequence(elephant1, elephant2):    # Function which geting two elephant objects,
    #  summary their mass and add them into Elephant.sequence - dictionary, wher
    #  key = mass of both object, value = list of both elephant's current postion
    total_move_mass = elephant1.mass + elephant2.mass
    pair_of_elephant = [elephant1.number, elephant2.number]
    Elephant.sequence[total_move_mass] = pair_of_elephant  # Add to Elephant.sequence - class attribute


def min_mass_swap():  # Function which return list of position two elephant with the smallest mass to move
    for key, value in Elephant.sequence.items():
        if key == min(Elephant.sequence):
            return value


def swap_elephant_by_index(el_index1, el_index2, obj1, obj2):  # Function for exchange elephant
    # in current_queue
    Elephant.current_queue.insert(el_index2, obj1)
    del Elephant.current_queue[el_index2 + 1]
    Elephant.current_queue.insert(el_index1, obj2)
    del Elephant.current_queue[el_index1 + 1]
    obj1.move()
    obj2.move()


def exchange_elephant_in_current_queue_loop():
    for elephant in Elephant.current_queue:  # Loop to find two elephant with the smallest mass exchange and
        # swap them in the current_queue by index until reach boss_queue setup
        if min_mass_swap() is not None:
            if elephant.number == min_mass_swap()[0]:
                ele1_index = Elephant.current_queue.index(elephant)
                for elephant2 in Elephant.current_queue:
                    if min_mass_swap() is not None:
                        if elephant2.number == min_mass_swap()[1]:
                            ele2_index = Elephant.current_queue.index(elephant2)
                            swap_elephant_by_index(ele1_index, ele2_index, elephant, elephant2)
                            Elephant.sequence = {}  # After each elephant position exchange, reset Elephant.sequence


def send_objects_to_sequence_loop():
    for el in range(len(Elephant.boss_queue)):  # Loop for checking difference between
        # boss_queue and current_queue, if find the difference then
        # call a function sequence_setup with two argument = two objects which need to be exchange
        if Elephant.current_queue[el].number != Elephant.boss_queue[el]:
            for ele in Elephant.current_queue:
                if ele.number == Elephant.boss_queue[el]:
                    setup_sequence(Elephant.current_queue[el], ele)


def main():
    list_boss_and_basic_creator()  # necessary to create Elephant.current_queue - main list

    for i in range(len(Elephant.current_queue)):  # Main loop
        send_objects_to_sequence_loop()
        exchange_elephant_in_current_queue_loop()

    return Elephant.Total_mass


print(main())