# Alec lahr - ENPM661 - Project 2

import numpy as np
from cv2 import VideoWriter, VideoWriter_fourcc

# ============================== OBSTACLE CHECKING ================================

def quad_check(x0, y0, quad):
    # extract coords out of quad list
    x1 = quad[0]
    y1 = quad[1]
    x2 = quad[2]
    y2 = quad[3]
    x3 = quad[4]
    y3 = quad[5]
    x4 = quad[6]
    y4 = quad[7]

    # check if the point is within the restricted half-plane side of each line
    chk1 = line_check(x0, y0, x1, y1, x2, y2, False, False)
    chk2 = line_check(x0, y0, x2, y2, x3, y3, False, True)
    chk3 = line_check(x0, y0, x3, y3, x4, y4, True, True)
    chk4 = line_check(x0, y0, x4, y4, x1, y1, True, False)

    # check if point is within resitected half place side of all lines --> in object
    if chk1 and chk2 and chk3 and chk4:
        return False  # point is in obstacle space
    else:
        return True  # point is not in obstacle space


def tria_check(x0, y0, tria):
    # extract coords out of tria list
    x1 = tria[0]
    y1 = tria[1]
    x2 = tria[2]
    y2 = tria[3]
    x3 = tria[4]
    y3 = tria[5]

    # THIS IS BAD CODE AND NOT UNIVERSAL BUT IT WORKS FOR THIS MAP
    # check if the point is within the restricted half-plane side of each line
    chk1 = line_check(x0, y0, x1, y1, x2, y2, False, False)
    chk2 = line_check(x0, y0, x2, y2, x3, y3, False, True)
    chk3 = line_check(x0, y0, x3, y3, x1, y1, True, False)

    # check if point is within resitected half place side of all lines --> in object
    if chk1 and chk2 and chk3:
        return False  # point is in obstacle space
    else:
        return True  # point is not in obstacle space


def line_check(x0, y0, x1, y1, x2, y2, UD, LR):
    # UD = True  if object is bottom side of line
    # UD = False if object is top    side of line
    # LR = True  if object is left   side of line
    # LR = False if object is right  side of line
    if x2 != x1:  # not vertical line
        m = (y2 - y1) / (x2 - x1)  # get the slope
        b = y1 - m * x1  # get the intercept
        # check if point is within the restriced half-plane
        if (y0 >= m * x0 + b and not UD) or (y0 <= m * x0 + b and UD):
            return True  # True means point is within the restriced half-plane
        else:
            return False  # False means point is not within the restriced half-plane

    else:  # x2 == x1 --> vertical line
        if (x0 >= x1 and not LR) or (x0 <= x1 and LR):
            return True  # True means point is within the restriced half-plane
        else:
            return False  # False means point is not within the restriced half-plane


def elip_check(x0, y0, elip):
    # extract dimensions out of elip list
    xc = elip[0]
    yc = elip[1]
    a2 = elip[2]**2  # horizontal dimension
    b2 = elip[3]**2  # vertical dimension

    if (x0 - xc)**2 / a2 + (y0 - yc)**2 / b2 <= 1:  # check if point is within ellipse
        return False  # point is in obstacle space
    else:
        return True  # point is not in obstacle space


def check_all_obstacles(x0, y0):
    for quad in quads:  # check quads
        if not quad_check(x0, y0, quad):  # see if point is in the quad
            return True  # point is in an obstacle

    for tria in trias:  # check trias
        if not tria_check(x0, y0, tria):  # see if point is in the tria
            return True  # point is in an obstacle

    for elip in elips:  # check elips
        if not elip_check(x0, y0, elip):  # see if point is in the elip
            return True  # point is in an obstacle

    return False  # point is not in an obstacle


# ========================= POSSIBLE MOVES ============================

def get_action_options(x, y):
    # takes in node, returns set of acceptable moves
    
    # move is doable if True, not doable if False
    #              R     L     U     D     UR    UL    DR    DL
    okay_moves = [True, True, True, True, True, True, True, True]  # defaults to true, try to prove false
    #                 R       L      U       D     UR      UL     DR      DL
    # action_set = [(1,0), (-1,0), (0,1), (0,-1), (1,1), (-1,1),(1,-1),(-1,-1)]
    
    for i in range(8): # check each of the 8 possible actions
        # get the new x and y after an action has been performed
        xa = x + action_set[i][0]
        ya = y + action_set[i][1]
        
        # check map border
        if xa < 0 or ya < 0 or xa > x_total or ya > y_total:
            okay_moves[i] = False
            continue
    
        # check previous nodes
        for node in nodes:  # check every node that has already been searched
            if xa == node[1] and ya == node[2]:  # if you have already searched this node...
                okay_moves[i] = False
                continue
    
        # check obstacle collison
        if check_all_obstacles(xa, ya):
            okay_moves[i] = False
        
    return okay_moves


# ============================= VIDEO ================================

def create_empty_map():    
    # show the obstacles on the map    
    no_nodes_map = np.zeros((height, width, 3), dtype=np.uint8)
    for y in range(height):
        for x in range(width):
            if check_all_obstacles(x, y):  # point is in an obstacle
                no_nodes_map[height - y - 1][x] = obstacle_color    # set pixel color to reflect obstacle here
            else:
                no_nodes_map[height - y - 1][x] = empty_color    # set pixel color to reflect no obstacle here
           
    # show the start and end points on the map
    no_nodes_map[height - y_init - 1][x_init] = start_color    # set pixel color to reflect start here
    no_nodes_map[height - y_goal - 1][x_goal] = goal_color    # set pixel color to reflect goal here
            
    return no_nodes_map


def add_node_to_frame(x, y, frame):  
    # recolor the node pixel
    frame[height - y - 1][x] = node_color
    return frame


def add_path_to_frame(x, y, frame):   
    # recolor the path pixel
    frame[height - y - 1][x] = path_color
    
    return frame



# ============================== MAIN ================================
# -------- SETUP 1 --------
# test map
# x_total = 200
# y_total = 100
# quads = [[90, 60, 90, 40, 110, 40, 110, 60]]
# trias = []
# elips = [[160, 50, 15, 15]]

# final map
x_total = 400
y_total = 300
quads = [[36.53, 124.38, 48, 108, 170.87, 194.04, 159.40, 210.42],
         [285.57, 105.42, 328, 63, 367.60, 102.60, 325.17, 145.02],
         [319.26, 125.24, 345.13, 117.51, 351.04, 137.3, 325.17, 145.02],
         [340.54, 129.66, 367.60, 102.60, 381.03, 116.03, 351.04, 137.3],
         [200,280,200,230,210,230,210,280],
         [210,280,210,270,230,270,230,280],
         [210,240,210,230,230,230,230,240]]
trias = [[351.04, 137.3, 381.03, 116.03, 381.03, 171.03]]
elips = [[90, 70, 35, 35],
         [246, 145, 60, 30]]

# define colors in RGB
empty_color = [200, 200, 200]
obstacle_color = [0, 0, 0]   
start_color = [255, 255, 0]
goal_color = [255, 0, 0]
node_color = [255, 255, 255]
path_color = [255, 0, 0]    

# convert from RGB to BGR
empty_color.reverse()
obstacle_color.reverse()
start_color.reverse()
goal_color.reverse()
node_color.reverse()
path_color.reverse()

# -------- INPUTS --------
# x_init = 50
# y_init = 35
# x_goal = 180
# y_goal = 60

# x_init = 5
# y_init = 5
# x_goal = 15
# y_goal = 15

# get initial and goal points
while(True):  # get the start point
    x_init = int(input("Where is the starting X coordinate? "))
    y_init = int(input("Where is the starting Y coordinate? "))
    if x_init > x_total or x_init < 0 or y_init > y_total or y_init < 0:  # see if point is within bounds
        print("\nPoint must be within map area. Try again.")
    # see if init point is in an obstacle
    elif not check_all_obstacles(x_init, y_init):
        break  # if it isnt, then
    else:
        print("\nThere is an obstacle in the way of that starting point. Try again.")

while(True):  # get the goal point
    x_goal = int(input("Where is the goal X coordinate? "))
    y_goal = int(input("Where is the goal Y coordinate? "))
    if x_goal > x_total or x_goal < 0 or y_goal > y_total or y_goal < 0:  # see if point is within bounds
        print("\nPoint must be within map area. Try again.")
    elif x_goal == x_init and y_goal == y_init:  # check that goal isnt init
        print("\nGoal point cannot be initial point. Try again.")
    # see if goal point is in an obstacle
    elif not check_all_obstacles(x_goal, y_goal):
        break  # if it isnt, then
    else:
        print("\nThere is an obstacle in the way of that goal point. Try again.")
        
print("\nSearching...")


# -------- SETUP 2 --------
# define nodes lists
# format: [index of parent node, node x coord, node y coord]
nodes = [['N/A', x_init, y_init]]  # add start point to the nodes list

# stores the index within nodes of the start and end of last search layer
start_of_last_layer = 0
end_of_last_layer = 0

# potential action changes x and y
#               R       L      U       D     UR      UL     DR      DL
action_set = [(1,0), (-1,0), (0,1), (0,-1), (1,1), (-1,1),(1,-1),(-1,-1)]

# video information
width = x_total
height = y_total
FPS = 120

# create video 
# https://medium.com/@enriqueav/how-to-create-video-animations-using-python-and-opencv-881b18e41397
fourcc = VideoWriter_fourcc(*'MP42')
video = VideoWriter('./final_map.mp4', fourcc, float(FPS), (width, height))

# create the first frame of only obstacles and start/end points
frame = create_empty_map()
# make buffer frames
for i in range(int(FPS)):
    video.write(frame)

# -------- GOAL SEARCH --------
# loop until goal point is found (loop is terminated with a break later)
while True:
    for i in range(start_of_last_layer, end_of_last_layer + 1):  # loop through all nodes in last search layer
        parent = nodes[i]
        x = parent[1]
        y = parent[2]
        okay_moves = get_action_options(x, y)  # get which moves to make
        
        for action in range(8):  # for each of the 8 actions
            if okay_moves[action]:
                # create new node
                # includes index of parent, new x coord, new y coord
                new_node = [i, x + action_set[action][0], y + action_set[action][1]]
                nodes.append(new_node)
                frame = add_node_to_frame(x + action_set[action][0], y + action_set[action][1], frame)
            
            if new_node[1] == x_goal and new_node[2] == y_goal:  # check if new node is goal node
                video.write(frame)
                break
        else:
            if i % 20 == 0:  # value changes the speed of the video
                video.write(frame)
            continue
        break
    else:
        if i == end_of_last_layer:  # finished the layer loop
            # set the new start and end
            start_of_last_layer = end_of_last_layer + 1
            end_of_last_layer = len(nodes) - 1
        continue
    break

# -------- BACKTRACK --------  
path_indexes = [len(nodes) - 1]  # create array to hold indexes. start with last elem in nodes
path_nodes = []  # create array to hold nodes on the path

# get indices and moves list of parents of solution
while nodes[path_indexes[-1]][0] != 'N/A':  # go until you get back to start node
    path_nodes.append(nodes[path_indexes[-1]])  # add the node to the path
    path_indexes.append(nodes[path_indexes[-1]][0])  # add the index of the parent
    
path_nodes.append(nodes[0])  # add the start node
path_nodes.pop(0)  # remove the end node


for node in path_nodes:
    x = node[1]
    y = node[2]
    frame = add_path_to_frame(x, y, frame)
    video.write(frame)
        
video.release()

print("\nGoal Found -- Video Saved")









