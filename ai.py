import random
score = None
buffs = None
inventory = None
current_level_layout = None
picked_up_music_items = None
current_position_of_monkey = None
remaining_turns = None
inventory_is_full = False

def move(current_game_state):
    global current_position_of_monkey
    global current_level_layout
    global inventory_is_full
    global remaining_turns
    global inventory_size
    global inventory
    global buffs
    global score
    current_position_of_monkey = tuple(current_game_state['position'])
    remaining_turns = current_game_state['remainingTurns']
    inventory_size = current_game_state['inventorySize']
    current_level_layout = current_game_state['layout']
    inventory = current_game_state['inventory']
    buffs = current_game_state['buffs']
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
    
    ## Dictande to user:
    closest_user = find_destination(["user"], game_board_map)
    print 'closest_user: ' + str(closest_user)
    if closest_user:
        dictance_to_user = closest_user[2]
    else:
        dictance_to_user = 1000

    if "banana" in inventory and "speedy" not in buffs:
        return {"command": "use", "item": "banana"}

    # Real game strategy here:
    if not inventory_is_full:
        close_item = get_destination_if_less_than([("playlist", 2), ("banana", 1), ("album", 1)], game_board_map)
        destination = close_item
    if destination is None:
        if (inventory_is_full or (dictance_to_user < 3 and len(inventory) >= 1)
                or (remaining_turns + 2 >= dictance_to_user and len(inventory) >= 1)):
            #inventory full, close to user or soon end of game
            destination = find_destination(["user"], game_board_map)
        elif score <= 0: # if score is less than 1, get some!
            if len(inventory) <= 0: # Go pick up something
                destination = find_destination(["song", "album", "playlist", "banana", "trap"], 
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
    
    if ("trap" in inventory and dictance_to_user <= 1):
        return {"command": "use", "item": "trap"}

    move = get_move(astar_array, current_position_of_monkey)
    print "get move returned: " + str(move)
    print 'destination: ' + str(destination)
    print 'current_position_of_monkey: ' + str(current_position_of_monkey)
    #if move is not None evaluate else return idle
    #if speedy and move_2 is not None return Directions command
    #else return direction with move
    if move is not None:
        direction = get_one_direction(move, current_position_of_monkey)
        if 'speedy' in buffs:
            move_2 = get_move(astar_array, move)
            if move_2 is not None:
                direction_2 = get_one_direction(move_2, move)
                print 'Directions: ' + str(direction) + ' and ' + str(direction_2)
                return {'command': 'move',
                    'directions': [direction, direction_2]}
            else:
                return {'command': 'move',
                    'direction': direction}
        else:
            return {'command': 'move',
                    'direction': direction}
    else:
        return {'command': 'idle'}

def get_destination_if_less_than(search_for, game_board_map):
    # element of type (item, max distance)
    for element in search_for:
        print "looking for smart stuff... in:  "
        close_item = find_destination([element[0]], game_board_map)
        print "looking for: " + str(element) + " found: " + str(close_item)
        if close_item is not None and close_item [2] <= element[1]:
            print "going for: " + str(close_item)
            return close_item

def find_destination(search_for, game_board_map):
    possible_destinations = []
    for element in game_board_map:
        #print "element:" + str(element) + " looking for: " + str(search_for)
        for destination in search_for:
                if element[3] == destination:
                    possible_destinations.append(element)
    print "possible destinations for: " + str(search_for) + " are: " + str(possible_destinations)
    print
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


def create_map_from(coordinate, stop_at):
    astar_array = []
    destination_coordinates = (coordinate[0], coordinate[1])
    astar_array.append(destination_coordinates + (0,
                       get_value_from_coordinate(destination_coordinates)))
    for element in astar_array:
        astar_array = add_coordinate(element, stop_at, element[2], astar_array)

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
            # find other entrance
            tunnels = find_elements_on_map(current_level_layout,
                                           value)
            for tunnel in tunnels:
                if not is_coordinates_equal(tunnel, c):
                    c = tunnel
                    break
        if stop_at is not None:
            if (c[0] == current_position_of_monkey[0] and
                    c[1] == current_position_of_monkey[1]):
                1 + 1
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


def get_move(astar_array, from_coordinate):
    possible_moves_list = possible_moves(astar_array, from_coordinate)
    if len(possible_moves_list) > 0:
        move = min(possible_moves_list, key=lambda move: move[2])
        return move
    else:
        return None


def get_one_direction(move, from_coordinate):
    if move[0] == from_coordinate[0]:
        if from_coordinate[1] - move[1] > 0:
            return "left"
        else:
            return "right"
    elif from_coordinate[0] - move[0] > 0:
        return "up"
    else:
        return "down"


def possible_moves(astar_array, from_coordinate):
    # print 'astar_array: ' + str(astar_array)
    goalcoordinate = astar_array[0][0:2]
    print 'goalcoordinate: ' + str(goalcoordinate) + " value: " + get_value_from_coordinate(goalcoordinate)
    going_to_user = get_value_from_coordinate(goalcoordinate) == "user"
    if inventory_is_full:
        avoid = ['wall', 'closed-door', 'song', 'album', 'playlist', 'banana', 'trap']
    else:
        avoid = ['wall', 'closed-door', 'user']
        if going_to_user:
            avoid.remove('user')
    possible_moves = [move for move in astar_array if move_is_possible(move, avoid, from_coordinate)]
    print "possible_moves: " + str(possible_moves)
    return possible_moves


def move_is_possible(move, avoid, from_coordinate):
    coordinates_around = get_coordinates_around(from_coordinate, avoid)
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
