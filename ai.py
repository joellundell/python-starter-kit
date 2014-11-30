import random

remaining_number_of_turns = None
current_level_layout = None
picked_up_music_items = None
current_position_of_monkey = None


def move(current_game_state):
    '''This is where you put your AI code!

    The AI looks at the current game state and decides
    the monkey's next move.'''

    # Every game has a limited number of turns. Use every turn wisely!
    remaining_number_of_turns = current_game_state['remainingTurns']

    # The level layout is a 2D-matrix (an array of arrays).
    #
    # Every element in the matrix is a string. The string tells you what
    # s located at the corresponding position on the level.
    #
    # In the warmup challenge, your objective is to find all music items
    # and deliver them to the eagerly waiting Spotify user.
    #
    # "empty": an empty tile, you can move here
    # "monkey": your monkey, this is where you're currently at
    # "song" / "album" / "playlist": a music item, go get them!
    # "user": go here once you've picked up all music items
    #
    # Too easy for you? Good...
    #
    # The real fun begins when the warmup is over and the competition begins!
    global current_level_layout
    current_level_layout = current_game_state['layout']

    # This is an array of all music items you've currently picked up
    global picked_up_music_items
    picked_up_music_items = current_game_state['inventory']

    # The position attribute tells you where your monkey is
    global current_position_of_monkey
    current_position_of_monkey = tuple(current_game_state['position'])

    # The inventory
    global inventory
    inventory = current_game_state['inventory']

        # The inventory
    global inventory_size
    inventory_size = current_game_state['inventorySize']


    # The inventory
    global score
    score = current_game_state['score']


    game_board_map = map_game_board(current_position_of_monkey)

    if len(inventory) >= inventory_size: # Inventory full, go to closest user
        destination = find_elements(["user"], game_board_map)
    elif True: # go pick up something
        destination = find_elements(["song", "album", "playlist"], game_board_map)
    else: #TODO: Spank the monkey 
        destination = find_elements(["monkey"], game_board_map)
    
    print 'destination: ' + str(destination)
    if destination:
        astar_array = create_astar_array(destination)
    else:
        return {'command': 'idle'} 
    # astar_array = getAstarArrayToGoTo(astar_arrays_list)
    move = get_move(astar_array)

    print "Moving: [" + move + "] towards [" + get_value_from_coordinate(astar_array[0][0:2]) + "] using: " + str(astar_array)
    # import pdb; pdb.set_trace()
    if move == 'idle':
        return {'command': 'idle'} 
    else:
        return {'command': 'move',
            'direction': move}

    # changes:
    # 1. Setting weight 10000 for user when deciding what element to go to
    # 2. get_coordinates_around takes a boolean that tells it whether it should consider
    #   the user something it can go to or not. So when there's still items left it 
    #   considers the user a "wall", something it has to go around


def getAstarArrayToGoTo(astar_arrays_list):
    if len(astar_arrays_list) == 1:
        return astar_arrays_list[0][0]
    else:
        distances = []
        for element in astar_arrays_list:
            coordinate = element[0][0][0:2]
            # if get_value_from_coordinate(coordinate) == "user":
            #     distances.append(10000)
            #     # if len(inventory) >= inventory_size: 
            #     #     distances.append(-10000)
            #     # else:
            #     #     distances.append(10000)
            # else:
            #     distances.append(element[1])
            distances.append(element[1])

            #print element
    print distances
    index = distances.index(min(distances))
    return  astar_arrays_list[index][0]
    
def print_game_board():
    print current_position_of_monkey
    print picked_up_music_items
    for row in current_level_layout:
        print row


def map_game_board(monkey_position):
    monkey_not_found = True
    counter = 0
    astar_array = []

    astar_array.append(monkey_position + (counter, get_value_from_coordinate(monkey_position)))
    current_astar_array = []
    done = False
    while not done:
        counter += 1
        current_astar_array = list(astar_array)
        result = next_step(current_astar_array, counter)
        monkey_not_found = result[0]
        astar_array = result[1]
        if len(astar_array) == len(current_astar_array) or counter >= 20:
            done = True
    return astar_array


def create_astar_array(destination):
    print_game_board()
    monkey_not_found = True
    # print "User position: " + str(destination)
    # print "Monkey position: " + str(current_position_of_monkey)
    counter = 0
    astar_array = []
    destination_coordinates = (destination[0], destination[1])
    astar_array.append(destination_coordinates + \
            (counter, get_value_from_coordinate(destination_coordinates)))
    while monkey_not_found:
        counter += 1

        result = next_step2(astar_array, counter)
        monkey_not_found = result[0]
        astar_array = result[1]
        # print 'a: ' + str(len(astar_array))
        # print 'c: ' + str(len(current_astar_array))
        
        #if len(astar_array) == len(current_astar_array) and monkey_not_found:
         #   return (astar_array, 200000)
          ######## MIGHT NEED TO DO SOMETHING HERE TO HANDLE THINGS INSIDE WALLS AND WITH LOCKED DOORS  
    # print "main list: " + str(astar_array)
    return astar_array


def next_step(current_astar_array, counter):
    monkey_not_found = True
    # print current_astar_array
    for element in current_astar_array:
        coordinates_around = get_coordinates_around((element[0], element[1]), ['wall', 'closed-door'])
    #    print current_astar_array
        for c in coordinates_around:
            # if c[0] == current_position_of_monkey[0] and \
            #         c[1] == current_position_of_monkey[1]:
            # monkey_not_found = False
            # else:
            current_astar_array = append_element_to_astar_array(c, counter, current_astar_array)
    return (monkey_not_found, current_astar_array)


def next_step2(current_astar_array, counter):
    monkey_not_found = True
    # print current_astar_array
    existing_elements = list(current_astar_array)
    for element in existing_elements:
        coordinates_around = get_coordinates_around((element[0], element[1]), ['wall', 'closed-door'])
    #    print current_astar_array
        for c in coordinates_around:
            if c[0] == current_position_of_monkey[0] and \
                    c[1] == current_position_of_monkey[1]:
                monkey_not_found = False
            else:
                current_astar_array = append_element_to_astar_array(c, counter, current_astar_array)
    return (monkey_not_found, current_astar_array)


def append_element_to_astar_array(coordinate, counter, current_astar_array):
    existingElements = [element for element in current_astar_array if \
            element[0] == coordinate[0] and element[1] == coordinate[1]]
    # print str(existingElements)
    if len(existingElements) > 0:
        for element in existingElements:
            if element[2] >= counter:
                #substitute for the new one
                current_astar_array.remove(element)
                current_astar_array.append(coordinate + \
                    (counter, get_value_from_coordinate(coordinate)))
    else:
        current_astar_array.append(coordinate + \
            (counter, get_value_from_coordinate(coordinate)))
    return current_astar_array


def get_move(astar_array):

    possible_moves_list = possible_moves(astar_array)
    if len(possible_moves_list) > 0:
        move = min(possible_moves_list, key=lambda move: move[2])
        return get_one_direction(move)
    else:
        return 'idle'

def get_one_direction(move):
    # import pdb; pdb.set_trace()
    if move[0] == current_position_of_monkey[0]:
        if current_position_of_monkey[1] - move[1] > 0:
            return "left"
        else:
            return "right"
    elif current_position_of_monkey[0] - move[0] > 0:
        return "up"
    else:
        return "down"


def possible_moves(astar_array):
    print 'astar_array: ' + str(astar_array)
    print 'game_board_map'
    goalcoordinate = astar_array[0][0:2]
    can_go_to_user = get_value_from_coordinate(goalcoordinate) == "user"
    print 'goalcoordinate: ' + str(goalcoordinate)
    print 'can_go_to_user: ' + str(can_go_to_user)
    if can_go_to_user:
        avoid = ['wall', 'closed-door', 'song', 'album', 'playlist', 'banana', 'trap']
    else:
        avoid = ['wall', 'closed-door', 'user']
    possible_moves = [move for move in astar_array if move_is_possible(move, avoid)]
    print "possible_moves: " + str(possible_moves)
    return possible_moves


def move_is_possible(move, avoid):
    coordinates_around = get_coordinates_around(current_position_of_monkey, avoid)
    for c in coordinates_around:
        if c[0] == move[0] and c[1] == move[1]:
            return True
    return False


def find_elements(search_for, game_board_map):
    print 'search_for: ' + str(search_for)
    for element in game_board_map:
        for destination in search_for:
                if element[3] == destination:
                    return element
    return None
    

def get_coordinates_around(coordinate, avoid):
    # print "get coordinates for: " + str(coordinate)
    coordinates_around =  [(coordinate[0] - 1,  coordinate[1]),
        (coordinate[0] + 1, coordinate[1]),
        (coordinate[0], coordinate[1] - 1),
        (coordinate[0], coordinate[1] + 1)]
   # print "surrounding coordinates: " + str(coordinates_around)
    filtered_list = [c for c in coordinates_around if c[0] >= 0 and 
            c[0] < len(current_level_layout) and c[1] >= 0 and 
            c[1] < len(current_level_layout[0]) and 
            get_value_from_coordinate(c) not in avoid]
   # print filtered_list
    #import pdb; pdb.set_trace()
    return filtered_list


def get_value_from_coordinate(coordinate):
    return current_level_layout[coordinate[0]][coordinate[1]]
