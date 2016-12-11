# Company: Zanzo Studios - http://zanzostudios.com
# Author: Michael McClenney at 16:34 on 12/10/2016.

import math
import random

# Level:
#   1. What % should be walls (destroyable objects)
#   2. Where to put start?
#   3. ???
#
#  Walls:
#   1. Normal
#   2. Electric
#
# Rooms:
#   1. All rooms must have an entryway
#   2. Doors count as entryways, but must be destroyed and not opened
#   3. Rooms can be inside of other rooms
#
# Obstacles:
#   1. Walls
#   2. Furniture
#   3. Plants


########################################
# Class: Point
########################################
class Point(object):
    def __init__(self, x, y):
        self._x = int(x)
        self._y = int(y)

    def __add__(self, other):
        return Point(self._x + other.x, self._y + other.y)

    def __div__(self, scale):
        return Point(self._x / scale, self._y / scale)

    def __mult__(self, scale):
        return Point(self._x * scale, self._y * scale)

    def __sub__(self, other):
        return Point(self._x - other.x, self._y - other.y)

    def segment_distance(self, other):
        return (other - self).distance

    @property
    def distance(self):
        return math.sqrt(math.pow(self.x, 2) + math.pow(self.y, 2))

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y


########################################
# Class: Rectangle
########################################
class Rectangle(object):
    def __init__(self, origin, size):
        self._origin = Point(origin.x, origin.y)
        self._size = Size(size.width, size.height)

    def __repr__(self):
        return "[Rect - [{0},{1}] @({2},{3})]".format(self._size.width, self._size.height,
                                                      self._origin.x, self._origin.y,)

    def overlaps_with(self, other):
        self_top_left = Point(self.origin.x, self.origin.y + self.size.height)
        self_bottom_right = Point(self.origin.x + self.size.width, self.origin.y)
        other_top_left = Point(other.origin.x, other.origin.y + other.size.height)
        other_bottom_right = Point(other.origin.x + other.size.width, other.origin.y)

        if self_top_left.x > other_bottom_right.x or other_top_left.x > self_bottom_right.x:
            return False
        if self_top_left.y < other_bottom_right.y or other_top_left.y < self_bottom_right.y:
            return False

        return True

    def clone_at_position(self, position):
        # new_origin = Point(self._origin.x + position.x, self._origin.y + position.y)
        return Rectangle(self._origin + position, self._size)

    @property
    def origin(self):
        return self._origin

    @property
    def size(self):
        return self._size


########################################
# Class: Size
########################################
class Size(object):
    def __init__(self, width, height):
        self._width = int(width)
        self._height = int(height)

    def __repr__(self):
        return "[Size - {0} x {1}]".format(self._width, self._height)

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height


########################################
# Class: Wall
########################################
class Wall(object):
    NORMAL = 0
    ELECTRIC = 1

    def __init__(self, start=Point(0, 0), end=Point(0, 0), type=NORMAL):
        self._start = start
        self._end = end
        self._type = type


########################################
# Class: RoomPrefab
########################################
class RoomPrefab(object):
    ROOM_CONSTRUCTORS = []

    def __init__(self, bounding_boxes, vertices, max_scale=-1):
        self._max_scale = max_scale
        self._bounding_boxes = list(bounding_boxes)
        self._vertices = list(vertices)
        self._walls = []
        self.generate_walls()

    def generate_walls(self):
        pass

    @staticmethod
    def initialize_room_constructors():
        RoomPrefab.ROOM_CONSTRUCTORS.append(SquareRoom)
        RoomPrefab.ROOM_CONSTRUCTORS.append(ThreeToTwoRoom)
        RoomPrefab.ROOM_CONSTRUCTORS.append(TwoToOneRoom)

    @staticmethod
    def create_random_room():
        if len(RoomPrefab.ROOM_CONSTRUCTORS) == 0:
            RoomPrefab.initialize_room_constructors()
        room_ctor = random.choice(RoomPrefab.ROOM_CONSTRUCTORS)
        print "room_ctor:", room_ctor
        return room_ctor(random.randint(4, 8))

    @property
    def bounding_boxes(self):
        return self._bounding_boxes

    @property
    def max_scale(self):
        return self._max_scale

    @property
    def vertices(self):
        return self._vertices

    @property
    def walls(self):
        return self._walls


# +--------------------------------------
# Class: Pre-Defined Rooms & Base Classes
# +--------------------------------------
class RectangleRoom(RoomPrefab):
    def __init__(self, width, height, max_scale):
        width = min(width, max_scale)
        height = min(height, max_scale)
        bounding_boxes = [Rectangle(Point(0, 0), Size(width, height))]
        vertices = [Point(0, 0), Point(0, height - 1), Point(width - 1, height - 1), Point(width - 1, 0)]
        RoomPrefab.__init__(self, bounding_boxes, vertices, max_scale)


class SquareRoom(RectangleRoom):
    def __init__(self, scale):
        RectangleRoom.__init__(self, scale, scale, 8)


class ThreeToTwoRoom(RectangleRoom):
    def __init__(self, scale):
        RectangleRoom.__init__(self, scale * 3, scale * 2, 8)


class TwoToOneRoom(RectangleRoom):
    def __init__(self, scale):
        RectangleRoom.__init__(self, scale * 2, scale, 8)


########################################
# Class: Room
########################################
class Room(object):
    def __init__(self, position=None, prefab=None):
        self._prefab = prefab
        self._position = position
        self._total_wall_length = 0

    def calculate_total_wall_length(self):
        self._total_wall_length = 0

        if self._prefab is not None:
            for index in range(1, len(self._prefab.vertices)):
                v1 = self._prefab.vertices[index - 1]
                v2 = self._prefab.vertices[index]
                self._total_wall_length += v1.segment_distance(v2)

    def overlaps_with(self, other):
        self_bounding_boxes = self.bounding_boxes
        other_bounding_boxes = other.bounding_boxes
        for self_bb in self_bounding_boxes:
            for other_bb in other_bounding_boxes:
                if self_bb.overlaps_with(other_bb):
                    return True
        return False

    @property
    def bounding_boxes(self):
        return [rect.clone_at_position(self._position) for rect in self._prefab.bounding_boxes]

    @property
    def prefab(self):
        return self._prefab

    @prefab.setter
    def prefab(self, prefab):
        self._prefab = prefab
        self.calculate_total_wall_length()

    @property
    def position(self):
        return self._position

    @property
    def vertices(self):
        return [self._position + vertex for vertex in self._prefab.vertices]


########################################
# Class: Level
########################################
class Level(object):
    SIZE = Size(60, 40)

    def __init__(self):
        self._rooms = []
        self._tiles = [["*" for x in range(Level.SIZE.width)] for y in range(Level.SIZE.height)]
        # print "rows:", len(self._tiles)
        # print "cols:", len(self._tiles[0])

    def add_room(self, room):
        # print "adding room at: (", room.position.x, ",", room.position.y, ")"
        print "adding room at: ({0}, {1})".format(room.position.x, room.position.y)
        print "   room dimensions: [{0}]".format(room.bounding_boxes[0])
        self._rooms.append(room)
        self.update_tiles()

    def output(self):
        print "total columns:", len(self._tiles[0])

        col_markers = " "
        for col in range(len(self._tiles[0])):
            col_markers += str(col % 10)
        print col_markers

        for row in reversed(range(len(self._tiles))):
            tile_row = str(row % 10)
            for col in range(len(self._tiles[row])):
                tile_row += self._tiles[row][col]
            print tile_row

        col_markers = " "
        for col in range(len(self._tiles[0])):
            col_markers += str(col % 10)
        print col_markers

    def update_tiles(self):
        for room in self._rooms:
            # print "updating tiles for room"
            vertices = room.vertices
            for index in range(len(vertices)):
                start_index = index
                end_index = index + 1
                if end_index >= len(vertices):
                    end_index = 0
                start = vertices[start_index]
                end = vertices[end_index]
                wall_segment = end - start
                is_horizontal = True if wall_segment.y == 0 else False
                is_vertical = not is_horizontal
                do_decrement = False
                if is_horizontal:
                    do_decrement = wall_segment.x < 0
                else:
                    do_decrement = wall_segment.y < 0

                col = start.x
                row = start.y
                # print "  processing segment from ({0},{1}) to ({2},{3}) with distance: {4}".format(start.x, start.y, end.x, end.y, wall_segment.distance)
                for step in range(int(wall_segment.distance)):
                    self._tiles[row][col] = "W"
                    # print "    setting tile at: ({0},{1})".format(col, row)
                    if is_horizontal:
                        if do_decrement:
                            col -= 1
                        else:
                            col += 1
                    else:
                        if do_decrement:
                            row -= 1
                        else:
                            row += 1

    @property
    def rooms(self):
        return self._rooms


########################################
# Function: generate_level
########################################
def generate_level(difficulty=1):
    level = Level()

    for room_num in range(1, 5):
        x = random.randint(0, 50)
        y = random.randint(0, 30)
        room_prefab = RoomPrefab.create_random_room()
        room = Room(Point(x, y), room_prefab)
        level.add_room(room)

    return level


########################################
# Function: print_level
########################################
def print_level(difficulty=1):
    pass


########################################
# Function: main
########################################
def main():
    level = generate_level()
    level.output()


if __name__ == '__main__':
    main()
