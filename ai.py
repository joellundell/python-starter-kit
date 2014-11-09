import random

astar_array = []

remaining_number_of_turns = None
current_level_layout = None
picked_up_music_items = None
current_position_of_monkey = None

def move(current_game_state):
    '''This is where you put your AI code!

    The AI looks at the current game state and decides
    the monkey's next move.'''

    # Every game has a limited number of turns. Use every turn wisely!
    remaining_number_of_turns = current_game_state['turns']

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
    picked_up_music_items = current_game_state['pickedUp']

    # The position attribute tells you where your monkey is
    global current_position_of_monkey
    current_position_of_monkey = current_game_state['position']

    # Speaking of positions...
    #
    # X and Y coordinates can be confusing.
    # Which way is up and which way is down?
    #
    # Here is an example explaining how coordinates work in
    # Monkey Music Challenge:
    #
    # {
    #   "layout": [["empty", "monkey"]
    #              ["song",  "empty"]]
    #   "position": [0, 1],
    #   ...
    # }
    #
    # The "position" attribute tells you the location of your monkey
    # in the "layout" matrix. In this example, you're at layout[0][1].
    #
    # If you send { "command": "move", "direction": "down", ... }
    # to the server, you'll get back:
    #
    # {
    #   "layout": [["empty", "empty"]
    #              ["song",  "monkey"]]
    #   "position": [1, 1]
    # }
    #
    # If you instead send { "command": "move", "direction": "left", ... }
    # to the server, you'll get back:
    #
    # {
    #   "layout": [["monkey", "empty"]
    #              ["song",   "empty"]]
    #   "position": [0, 0]
    # }
    #
    # So what about picking stuff up then?
    #
    # It's simple!
    #
    # Just stand next to something you want to pick up and move towards it.
    #
    # For example, say our current game state looks like this:
    #
    # {
    #   "layout": [["empty", "empty"]
    #              ["song",  "monkey"]]
    #   "position": [1, 1],
    #   "pickedUp": []
    # }
    #
    # When you send { "command": "move", "direction": "left", ... }
    # to the server, you'll get back:
    #
    #   "layout": [["empty",  "empty"]
    #              ["empty",  "monkey"]]
    #   "position": [1, 1],
    #   "pickedUp": ["song"],
    #   ...
    # }
    #
    # Instead of moving, your monkey successfully picked up the song!
    #
    # Got it? Sweet! This message will self destruct in five seconds...

    print_game_board()
    create_astar_array()
    move = random.choice(['up', 'down', 'left', 'right'])
    print "Moving: " + move
    import pdb; pdb.set_trace()
    return move

def print_game_board():
    print current_position_of_monkey
    print picked_up_music_items
    for row in current_level_layout:
        print row

def create_astar_array():
    user = find_element("user")
    print "User position: " + str(user)
    print "Monkey position: " + str(current_position_of_monkey)
    counter = 0
    global astar_array
    astar_array.append(user + (counter,))
    counter += 1
    astar_array = next_step(astar_array, counter)
    print "main list: " + str(astar_array)

def next_step(astar_array, counter):
    for element in astar_array: 
        coordinates_around = get_coordinates_around((element[0], element[1]))
    for c in coordinates_around:
        print str(c) + " -> " +  get_value_from_coordinate(c)
        astar_array.append(c + (counter,))
    return astar_array


def find_element(element_to_find, ):
    for rIndex, row in enumerate(current_level_layout):
        for cIndex, column in enumerate(row):
            if column == element_to_find:
                return tuple([rIndex, cIndex])
    return "can't find element:" + elementToFind

def get_coordinates_around(coordinate):
    coordinates_around =  [(coordinate[0] - 1,  coordinate[1]),
        (coordinate[0] + 1, coordinate[1]),
        (coordinate[0], coordinate[1] - 1),
        (coordinate[0], coordinate[1] + 1)]
    filtered_list = [c for c in coordinates_around if c[0] >= 0 and c[0] < len(current_level_layout)
            and c[1] >= 0 and c[1] < len(current_level_layout[0]) and get_value_from_coordinate(c) is not "wall"]
    return filtered_list

def get_value_from_coordinate(coordinate):
    return current_level_layout[coordinate[0]][coordinate[1]]
