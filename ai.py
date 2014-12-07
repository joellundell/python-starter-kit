import random
score = None
inventory = None
current_level_layout = None
picked_up_music_items = None
current_position_of_monkey = None
remaining_turns = None

def move(current_game_state):
    global current_position_of_monkey
    global current_level_layout
    global inventory_is_full
    global remaining_turns
    global inventory_size
    global inventory
    global score
    current_position_of_monkey = tuple(current_game_state['position'])
    remaining_turns = current_game_state['remainingTurns']
    inventory_size = current_game_state['inventorySize']
    current_level_layout = current_game_state['layout']
    inventory = current_game_state['inventory']
    score = current_game_state['score']

    inventory_is_full =len(inventory) >= inventory_size

    # Map the game board and get the distance to everything on the map
    game_board_map = create_map_from(current_position_of_monkey, None)
    # print 'game_board_map: ' + str(game_board_map)

    ## Decide what to do, wheter it is to go to the user och collect something
    # Strategy:
    # If no points - get a point then spank the monkey till inventory is full
    # when inventory is full, get more points
    # When number of moves left is ecual to distance to closest user, go to hen

    if inventory_is_full: # Inventory full, go to closest user
        destination = find_destination(["user"], game_board_map)
    elif score <= 0: # if score is less than 1, get some!
        if len(inventory) <= 0: # Go pick up something
            destination = find_destination(["song", "album", "playlist"], 
                game_board_map)
        else: # then return it to user
            destination = find_destination(["user"], game_board_map)
    else: #TODO: Spank the monkey 
        destination = find_destination(["monkey"], game_board_map)

    # Create the path to the destination
    if destination is not None:
        astar_array = create_map_from(destination, current_position_of_monkey)
    else:
        print 'Error: destination is: ' + str(destination)
        print '       returning: idle'
        return {'command': 'idle'} 
   # import pdb; pdb.set_trace()
    move = get_move(astar_array)

    ## Print interestion stuff here
    print 'destination: ' + str(destination)
    print 'current_position_of_monkey: ' + str(current_position_of_monkey)
    # print 'inventory: ' + str(inventory)
    # print 'inventory_size: ' + str(inventory_size)
    # print_game_board()
    print ("Moving: [" + move + "] towards [" +
        get_value_from_coordinate(astar_array[0][0:2]) +
        "] using: " + str(astar_array))


    # import pdb; pdb.set_trace()
    # Return next command
    if move == 'idle':
        return {'command': 'idle'}
    else:
        return {'command': 'move',
            'direction': move}


def find_destination(search_for, game_board_map):
    possible_destinations = []
    for element in game_board_map:
        #print "element:" + str(element) + " looking for: " + str(search_for)
        for destination in search_for:
                if element[3] == destination:
                    possible_destinations.append(element)
    if len(possible_destinations) > 0:

        if search_for[0] == 'monkey':
            destination = max(possible_destinations,
                key=lambda destination: destination[2])
        else:
            destination = min(possible_destinations,
                key=lambda destination: destination[2])
    else:
        return None
    return destination


def print_game_board():
    print current_position_of_monkey
    print inventory
    for row in current_level_layout:
        print row


#def map_game_board(monkey_position):
#    #create and add moneky to game_board_map
#    game_board_map = []
#    game_board_map.append(monkey_position + (0,
#        get_value_from_coordinate(monkey_position)))
#    
#    # iterateing through game_board_map and add new elements in end
#    # makes the loop end when there is no new elements to add
#    for element in game_board_map:
#        coordinates_around = get_coordinates_around((element[0], element[1]), 
#            ['wall', 'closed-door'])
#        # coordinates_around have +1 in dictance
#        counter = element[2] + 1   
#        for c in coordinates_around:
#            game_board_map = append_element_to_astar_array(c,
#                counter, game_board_map)
#    return game_board_map
#
#
#def create_astar_array(destination):
#    astar_array = []
#    destination_coordinates = (destination[0], destination[1])
#    astar_array.append(destination_coordinates + (0,
#        get_value_from_coordinate(destination_coordinates)))
#    for element in astar_array:
#        coordinates_around = get_coordinates_around((element[0], element[1]), 
#            ['wall', 'closed-door'])
#
#        # coordinates_around have +1 in dictance
#        counter = element[2] + 1
#        for c in coordinates_around:
#            if (c[0] == current_position_of_monkey[0] and
#                c[1] == current_position_of_monkey[1]):
#                print "found monkey"
#            else:
#                astar_array = append_element_to_astar_array(c, counter,
#                 astar_array)
#    return astar_array

def create_map_from(coordinate, stop_at):
    print "create map from and stop at" + str(stop_at)
    astar_array = []
    destination_coordinates = (coordinate[0], coordinate[1])
    astar_array.append(destination_coordinates + (0,
                       get_value_from_coordinate(destination_coordinates)))
    for element in astar_array:
        astar_array = add_coordinate(element, stop_at, element[2], astar_array)

        # if it's tunnel, find other entrance and
        # add coordinates around there with counter +1

#        value = get_value_from_coordinate([element[0], element[1]])
#        if (value.startswith("tunnel")):
#            print "isTunnel"
#            # find other entrance
#            #import pdb; pdb.set_trace()
#            tunnels = find_elements_on_map(current_level_layout,
#                                           value)
#            print "tunnel coordinates: " + str(tunnels)
#            for tunnel in tunnels:
#                if not is_coordinates_equal(tunnel, element):
#        #            astar_array = add_coordinate(tunnel, stop_at, element[2], astar_array)
#                    # add tunnel coordinate
#                    append_element_to_astar_array(tunnel, element[2] + 
    return astar_array


def add_coordinate(coordinate, stop_at, current_counter, astar_array):
    coordinates_around = get_coordinates_around((coordinate[0], coordinate[1]),
                                                ['wall', 'closed-door'])
    # coordinates_around have +1 in dictance
    counter = current_counter + 1
    for c in coordinates_around:
        #Check if c is a tunnel, if so set c to the tunnel exit
        value = get_value_from_coordinate(c)
        if (value.startswith("tunnel")):
            print "isTunnel"
            # find other entrance
            tunnels = find_elements_on_map(current_level_layout,
                                           value)
            print "tunnel coordinates: " + str(tunnels)
            for tunnel in tunnels:
                if not is_coordinates_equal(tunnel, c):
                    print "old c: " + str(c)
                    c = tunnel
                    print "new  c: " + str(c)
                    break
        if stop_at is not None:
            if (c[0] == current_position_of_monkey[0] and
                    c[1] == current_position_of_monkey[1]):
                print "found the coordinate where it should stop at"
            else:
                astar_array = append_element_to_astar_array(c, counter,
                                                            astar_array)
        else:
            astar_array = append_element_to_astar_array(c, counter,
                                                        astar_array)
    return astar_array


# careful when changing, map_game_board() and create_astar_array() use this
def append_element_to_astar_array(coordinate, counter, current_astar_array):
    existingElements = [element for element in current_astar_array if
                        element[0] == coordinate[0] and element[1] ==
                        coordinate[1]]
    # print str(existingElements)
    if len(existingElements) > 0:
        for element in existingElements:
            if element[2] >= counter:
                #substitute for the new one
                current_astar_array.remove(element)
                current_astar_array.append(coordinate + (counter,
                    get_value_from_coordinate(coordinate)))
    else:
        current_astar_array.append(coordinate + (counter,
                                   get_value_from_coordinate(coordinate)))
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
    # print 'astar_array: ' + str(astar_array)
    goalcoordinate = astar_array[0][0:2]
    print 'goalcoordinate: ' + str(goalcoordinate)
    going_to_user = get_value_from_coordinate(goalcoordinate) == "user"
    if inventory_is_full:
        avoid = ['wall', 'closed-door', 'song', 'album', 'playlist', 'banana', 'trap']
    else:
        avoid = ['wall', 'closed-door', 'user']
        if going_to_user:
            avoid.remove('user')
    possible_moves = [move for move in astar_array if move_is_possible(move, avoid)]
    print "possible_moves: " + str(possible_moves)
    return possible_moves


def move_is_possible(move, avoid):
    coordinates_around = get_coordinates_around(current_position_of_monkey, avoid)
    for c in coordinates_around:
        if c[0] == move[0] and c[1] == move[1]:
            return True
    return False


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
    return filtered_list


def find_elements_on_map(game_board, looking_for):
    coordinates = []
    for i in range(len(game_board)):
        for j in range(len(game_board[0])):
            value = get_value_from_coordinate([i, j])
            if value == looking_for:
                coordinates.append((i, j))
    return coordinates


def get_value_from_coordinate(coordinate):
    return current_level_layout[coordinate[0]][coordinate[1]]


def is_coordinates_equal(coordinate1, coordinate2):
    return coordinate1[0] == coordinate2[0] and coordinate1[1] == coordinate2[1]
