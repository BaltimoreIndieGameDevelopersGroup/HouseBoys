# Company: Zanzo Studios - http://zanzostudios.com
# Author: Michael McClenney at 16:34 on 12/10/2016.

import json
import math
import os
import random
import uuid

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

    def __eq__(self, other):
        return self._x == other.x and self._y == other.y

    def __hash__(self):
        return hash("{0}_{1}".format(self._x, self._y))

    def __mult__(self, scale):
        return Point(self._x * scale, self._y * scale)

    def __sub__(self, other):
        return Point(self._x - other.x, self._y - other.y)

    def clone(self):
        return Point(self._x, self._y)

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
    def clone(self):
        return Point(self.origin.clone(), self._size.clone())

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

    def clone(self):
        return Size(self._width, self._height)

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

    def __init__(self, bounding_boxes, vertices, size, max_scale=-1):
        self._max_scale = max_scale
        self._bounding_boxes = list(bounding_boxes)
        self._size = size
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
    def size(self):
        return self._size

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
        size = Size(width, height)
        bounding_boxes = [Rectangle(Point(0, 0), size)]
        vertices = [Point(0, 0), Point(0, height - 1), Point(width - 1, height - 1), Point(width - 1, 0)]
        RoomPrefab.__init__(self, bounding_boxes, vertices, size, max_scale)


class SquareRoom(RectangleRoom):
    def __init__(self, scale):
        RectangleRoom.__init__(self, scale, scale, 8)


class FourToThreeRoom(RectangleRoom):
    def __init__(self, scale):
        RectangleRoom.__init__(self, scale * 4, scale * 3, 40)


class ThreeToTwoRoom(RectangleRoom):
    def __init__(self, scale):
        RectangleRoom.__init__(self, scale * 3, scale * 2, 8)


class TwoToOneRoom(RectangleRoom):
    def __init__(self, scale):
        RectangleRoom.__init__(self, scale * 2, scale, 8)


class RandomRoom(object):
    def __init__(self, bounds):
        self._bounds = bounds

    @property
    def bounds(self):
        return self._bounds


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
    BOUNDS = Rectangle(Point(0, 0), SIZE)
    BOTTOM_LEFT = 0
    TOP_LEFT = 1
    TOP_RIGHT = 2
    BOTTOM_RIGHT = 3
    DECREASE_VERTICAL = 0
    INCREASE_VERTICAL = 1
    DECREASE_HORIZONTAL = 0
    INCREASE_HORIZONTAL = 1
    HORIZONTAL = 0
    VERTICAL = 1
    DIAGONAL = 2
    BUILD_DIRECTIONS = (HORIZONTAL, VERTICAL, DIAGONAL)
    # VERTICES = (BOTTOM_LEFT, TOP_LEFT, TOP_RIGHT, BOTTOM_RIGHT)
    VERTICES = (Point(0, 0), Point(0, SIZE.height), Point(SIZE.width, SIZE.height), Point(SIZE.width, 0))

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

    def conflicts_with(self, room_to_check):
        for room in self._rooms:
            if room.overlaps_with(room_to_check):
                return True
        return False

    def generate_random(self, difficulty=1):
        print "Level::generate_random()"
        # wall_width, wall_height = self.generate_wall(3, 10)
        # start_point = Point(0, 0)
        # end_point = Point(start_point.x + wall_width, start_point.y + wall_height)
        # print "  wall start point: ({0},{1}), end point: ({2},{3})".format(start_point.x, start_point.y, end_point.x, end_point.y)
        # print "  randomly generated wall size: [{0},{1}]".format(wall_width, wall_height)
        # for row in range(start_point.y, wall_height):
        #     self._tiles[row][wall_width - 1] = "W"
        # for col in range(start_point.x, wall_width):
        #     self._tiles[wall_height - 1][col] = "W"
        # room = self.build_next_room()
        # self._rooms.append(room)
        # self.update_tiles()
        self.generate_bottom_rooms()
        self.generate_top_rooms()
        self.update_tiles()

    def generate_bottom_rooms(self):
        print "Level::generate_bottom_rooms()"
        min_horiz_scale = 8
        max_horiz_scale = 15
        min_vert_scale = 3
        max_vert_scale = 6
        max_total_room_width = random.randint(min_horiz_scale, max_horiz_scale) * 4
        min_room_width = 16
        max_room_scale = 6
        total_room_width = 0
        room_pos = Point(0, 0)
        print "  max room width:", max_total_room_width
        while total_room_width + min_room_width < max_total_room_width:
            room_height = random.randint(3, 5) * 3
            room_width = random.randint(4, 6) * 4
            while total_room_width + min_room_width >= max_total_room_width:
                room_width = random.randint(4, 6) * 4
            print "    generating room [{0},{1}] @({2},{3})".format(room_width, room_height, room_pos.x, room_pos.y)
            bounds = Rectangle(room_pos.clone(), Size(room_width, room_height))
            self._rooms.append(RandomRoom(bounds))
            room_pos = Point(room_pos.x + room_width - 1, room_pos.y)
            total_room_width += room_width
            print "    total room width:", total_room_width

    def generate_top_rooms(self):
        print "Level::generate_top_rooms()"
        min_horiz_scale = 8
        max_horiz_scale = 15
        min_vert_scale = 3
        max_vert_scale = 6
        max_total_room_width = random.randint(min_horiz_scale, max_horiz_scale) * 4
        min_room_width = 16
        max_room_scale = 6
        total_room_width = 0
        room_pos = None
        print "  max room width:", max_total_room_width
        while total_room_width + min_room_width < max_total_room_width:
            room_height = random.randint(3, 5) * 3
            room_width = random.randint(4, 6) * 4
            while total_room_width + min_room_width >= max_total_room_width:
                room_width = random.randint(4, 6) * 4
            if room_pos is None:
                print "    room pos is None"
                room_pos_x = Level.BOUNDS.size.width - room_width # - 1
                room_pos_y = Level.BOUNDS.size.height - room_height # - 1
            else:
                print "    room pos: ({0},{1})".format(room_pos.x, room_pos.y)
                room_pos_x = room_pos.x - room_width + 1
                room_pos_y = Level.BOUNDS.size.height - room_height # - 1
            room_pos = Point(room_pos_x, room_pos_y)
            print "    generating room [{0},{1}] @({2},{3})".format(room_width, room_height, room_pos.x, room_pos.y)
            bounds = Rectangle(room_pos.clone(), Size(room_width, room_height))
            self._rooms.append(RandomRoom(bounds))
            # room_pos = Point(room_pos.x + room_width - 1, room_pos.y)
            total_room_width += room_width
            print "    total room width:", total_room_width

    # def build_next_room(self, previous_room=None, direction=DIAGONAL):
    #     # For now just do diagonal
    #     # wall_width, wall_height = self.generate_wall(3, 10)
    #     # room_bounds = Rectangle(position, Size(wall_width, wall_height))
    #     # print "creating room: [{0},{1}] @({2},{3})".format(wall_width, wall_height, position.x, position.y)
    #     # return RandomRoom(room_bounds)
    #     position = Point(0, 0)
    #     if previous_room is not None:
    #         position = previous_room.position
    #     room_size = self.generate_room_size(3, 10)
    #     return RandomRoom(Rectangle(position.clone(), room_size.clone()))

    def generate_room_size(self, min_scale, max_scale):
        return Size(random.randint(min_scale, max_scale) * 4, random.randint(min_scale, max_scale) * 3)

    def write_level_data(self):
        output_dir = "/Users/mmcclenney/Dropbox/Ludum Dare/test_levels/"
        filename = "{0}.json".format(uuid.uuid4())
        output_filespec = os.path.join(output_dir, filename)

        assert os.path.exists(output_dir)
        assert not os.path.exists(output_filespec)

        tiles = []
        for row in self._tiles:
            tiles.extend(row)

        json_props = {
            "number": 1,
            "timer": 60,
            "difficulty": 0,
            "rows": Level.SIZE.height,
            "columns": Level.SIZE.width,
            "tiles": tiles
        }

        print "writing output file to:", output_filespec
        with open(output_filespec, "w") as outfile:
            json.dump(json_props, outfile, sort_keys=True, indent=4)

    def get_room_conflicts(self):
        room_conflicts = {}
        for first_room_index in range(len(self._rooms)):
            room_conflicts[first_room_index] = []
            for second_room_index in range(first_room_index + 1, len(self._rooms)):
                first_room = self._rooms[first_room_index]
                second_room = self._rooms[second_room_index]
                if first_room.overlaps_with(second_room):
                    room_conflicts[first_room_index].append(second_room_index)

        return room_conflicts

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
            # draw first wall - bottom left -> top left
            room_pos = room.bounds.origin
            room_size = room.bounds.size
            if room_pos.x > 0:
                col = room_pos.x
                for row in range(room_pos.y, room_pos.y + room_size.height):
                    self._tiles[row][col] = "V"

            # draw second wall - top left -> top right
            if room_pos.y + room_size.height < (Level.BOUNDS.size.height - 1):
                row = room_pos.y + room_size.height - 1
                for col in range(room_pos.x, room_pos.x + room_size.width):
                    self._tiles[row][col] = "H"

            # draw third wall - top right -> bottom right
            if room_pos.x + room_size.width < (Level.BOUNDS.size.width - 1):
                col = room_pos.x + room_size.width - 1
                for row in range(room_pos.y, room_pos.y + room_size.height):
                    self._tiles[row][col] = "V"

            # draw fourth wall - bottom right -> bottom left
            if room_pos.y > 0:
                row = room_pos.y
                for col in range(room_pos.x, room_pos.x + room_size.width):
                    self._tiles[row][col] = "H"


    @property
    def rooms(self):
        return self._rooms


########################################
# Function: generate_level
########################################
def generate_level(difficulty=1):
    level = Level()
    level.generate_random()

    # total_rooms = random.randint(4, 6)
    # max_iterations = 10000
    # total_iterations = 0
    # # for room_num in range(1, random.randint(4, 6)):
    # while total_iterations < max_iterations and len(level.rooms) < total_rooms:
    #     x = random.randint(0, 50)
    #     y = random.randint(0, 30)
    #     # room_prefab = RoomPrefab.create_random_room()
    #     room_prefab = FourToThreeRoom(random.randint(1, 4))
    #     room = Room(Point(x, y), room_prefab)
    #     if not level.conflicts_with(room):
    #         level.add_room(room)
    #
    # # print "does room have conflicts:", level.has_conflicts()
    # level_conflicts = level.get_room_conflicts()
    # print "room conflicts:"
    # for room_index in sorted(level_conflicts):
    #     room_conflicts = level_conflicts[room_index]
    #     if len(room_conflicts) == 0:
    #         print "[{0}]: None".format(room_index)
    #     else:
    #         room_indexes = ",".join([str(i) for i in level_conflicts[room_index]])
    #         print "[{0}]: {1}".format(room_index, room_indexes)

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
    # level.write_level_data()


if __name__ == '__main__':
    main()
