
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


# ============================== MAIN ================================

x_total = 200
y_total = 100
quads = [[90, 60, 90, 40, 110, 40, 110, 60]]
trias = []
elips = [[160, 50, 15, 15]]






















