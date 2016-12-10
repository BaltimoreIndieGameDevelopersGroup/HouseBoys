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
        self._x = x
        self._y = y

    def distance(self, other):
        segment = Point(other.x - self._x, other.y - self._y)
        return math.sqrt(math.pow(segment.x, 2) + math.pow(segment.y, 2))

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
        new_origin = Point(self._origin.x + position.x, self._origin.y + position.y)
        return Rectangle(new_origin, self._size)

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
        self._width = width
        self._height = height

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
# Class: RoomDimensions
########################################
class RoomDimensions(object):
    def __init__(self, bounding_boxes, vertices, max_scale=-1):
        self._max_scale = max_scale
        self._bounding_boxes = bounding_boxes[:]
        self._vertices = vertices[:]
        self._walls = []
        self._room_constructors = (SquareRoom, ThreeToTwoRoom, TwoToOneRoom)
        self.generate_walls()

    def generate_walls(self):
        pass

    @staticmethod
    def create_random_room():
        scale = random.randint(1, 4)

    @property
    def bounding_boxes(self):
        return self._bounding_boxes

    @property
    def max_scale(self):
        return self._max_scale

    @property
    def walls(self):
        return self._walls


class RectangleRoom(RoomDimensions):
    def __init__(self, width, height, max_scale):
        bounding_boxes = [Rectangle(Point(0, 0), Size(width, height))]
        vertices = [Point(0, 0), Point(0, height), Point(width, height), Point(width, 0)]
        RoomDimensions.__init__(self, bounding_boxes, vertices, max_scale)


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
    def __init__(self, position=None, dimensions=None):
        self._dimensions = dimensions
        self._position = position
        self._total_wall_length = 0

    def calculate_total_wall_length(self):
        self._total_wall_length = 0

        if self._dimensions is not None:
            for index in range(1, len(self._dimensions.vertices)):
                v1 = self._dimensions.vertices[index - 1]
                v2 = self._dimensions.vertices[index]
                self._total_wall_length += v1.distance(v2)

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
        return [rect.clone_at_position(self._position) for rect in self._dimensions.bounding_boxes]

    @property
    def dimensions(self):
        return self._dimensions

    @dimensions.setter
    def dimensions(self, dimensions):
        self._dimensions = dimensions
        self.calculate_total_wall_length()

    @property
    def position(self):
        return self._position


########################################
# Class: Level
########################################
class Level(object):
    def __init__(self):
        self._size = Size(60, 40)
        self._rooms = []
        self._tiles = [["*" for x in range(self._size.width)] for y in range(self._size.height)]

    def add_room(self, room):
        self._rooms.append(room)

    def output(self):
        for column in self._tiles:
            tile_row = ""
            for tile in column:
                tile_row += tile
            print tile_row

    def size(self):
        return self._size

    @property
    def room(self):
        return self._rooms


########################################
# Function: generate_level
########################################
def generate_level(difficulty=1):
    level = Level()
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
