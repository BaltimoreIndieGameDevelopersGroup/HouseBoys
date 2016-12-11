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
# Class: Sprite
########################################
class Sprite(object):
    def __init__(self, bounds):
        self._bounds = bounds

    @property
    def bounds(self):
        return self._bounds

    @property
    def position(self):
        return self._bounds.origin

    @position.setter
    def position(self, new_pos):
        self._bounds = Rectangle(new_pos.clone(), self._bounds.size.clone())

    @property
    def size(self):
        return self._bounds.size


########################################
# Class: Sofa
########################################
class Sofa(Sprite):
    def __init__(self):
        Sprite.__init__(self, Rectangle(Point(0, 0), Size(12, 8)))


########################################
# Class: Bed
########################################
class Bed(Sprite):
    def __init__(self):
        Sprite.__init__(self, Rectangle(Point(0, 0), Size(12, 8)))


########################################
# Class: Stove
########################################
class Stove(Sprite):
    def __init__(self):
        Sprite.__init__(self, Rectangle(Point(0, 0), Size(8, 8)))


########################################
# Class: Room
########################################
class Room(Sprite):
    BATHROOM = 1
    BEDROOM = 2
    KITCHEN = 3
    TYPES = (BATHROOM, BEDROOM, KITCHEN)

    def __init__(self, room_type, bounds):
        Sprite.__init__(self, bounds)
        self._type = room_type
        self._furniture = []
        self.insert_room_object()

    def insert_room_object(self):
        furniture = None
        if Room.BATHROOM == self._type:
            furniture = Sofa()
        elif Room.BEDROOM == self._type:
            furniture = Bed()
        elif Room.KITCHEN == self._type:
            furniture = Stove()

        if furniture is not None:
            min_object_x = 0
            max_object_x = int(self.size.width - furniture.size.width)
            min_object_y = 0
            max_object_y = int(self.size.height - furniture.size.height)
            x = random.randint(min_object_x, max_object_x)
            y = random.randint(min_object_y, max_object_y)
            furniture.position = Point(x, y)
            self._furniture.append(furniture)

    # NOTE: This is not the same as a bounding box,
    #       the width and height are decremented by one to fit within the 0-based coords of the map
    @property
    def corners(self):
        origin = self._bounds.origin
        size = self._bounds.size
        return [origin.clone(),
                Point(origin.x, origin.y + size.height - 1),
                Point(origin.x + size.width - 1, origin.y + size.height - 1),
                Point(origin.x + size.width - 1, origin.y)]

    @property
    def furniture(self):
        return self._furniture

    @property
    def type(self):
        return self._type


########################################
# Class: Level
########################################
class Level(object):
    SIZE = Size(60, 40)
    BOUNDS = Rectangle(Point(0, 0), SIZE)

    def __init__(self):
        self._rooms = []
        self._tiles = [["W" for x in range(Level.SIZE.width)] for y in range(Level.SIZE.height)]

    def conflicts_with(self, room_to_check):
        for room in self._rooms:
            if room.overlaps_with(room_to_check):
                return True
        return False

    def generate_random(self, difficulty=1):
        print "Level::generate_random()"
        self.generate_bottom_rooms()
        self.generate_top_rooms()
        self.update_tiles()

    def generate_bottom_rooms(self):
        print "Level::generate_bottom_rooms()"
        min_horiz_scale = 8
        max_horiz_scale = 15
        max_total_room_width = random.randint(min_horiz_scale, max_horiz_scale) * 4
        min_room_width = 16
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
            room_type = random.choice(Room.TYPES)
            self._rooms.append(Room(room_type, bounds))
            room_pos = Point(room_pos.x + room_width - 1, room_pos.y)
            total_room_width += room_width
            print "    total room width:", total_room_width

    def generate_top_rooms(self):
        print "Level::generate_top_rooms()"
        min_horiz_scale = 8
        max_horiz_scale = 15
        max_total_room_width = random.randint(min_horiz_scale, max_horiz_scale) * 4
        min_room_width = 16
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
            room_type = random.choice(Room.TYPES)
            self._rooms.append(Room(room_type, bounds))
            total_room_width += room_width
            print "    total room width:", total_room_width

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
            room_tile = "W"
            if Room.BATHROOM == room.type or Room.KITCHEN == room.type:
                room_tile = "S"
            elif Room.BEDROOM == room.type:
                room_tile = "C"

            room_end = Point(room_pos.x + room_size.width, room_pos.y + room_size.height)
            for row in range(room_pos.y, room_end.y):
                for col in range(room_pos.x, room_end.x):
                    self._tiles[row][col] = room_tile

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

        for room in self._rooms:
            for corner in room.corners:
                if corner.x == 0 or corner.x >= Level.BOUNDS.size.width - 1:
                    continue
                if corner.y == 0 or corner.y >= Level.BOUNDS.size.height - 1:
                    continue
                self._tiles[corner.y][corner.x] = "X"

            for furniture in room.furniture:
                furniture_sprite = None
                if isinstance(furniture, Bed):
                    furniture_sprite = "B"
                elif isinstance(furniture, Sofa):
                    furniture_sprite = "O"
                elif isinstance(furniture, Stove):
                    furniture_sprite = "R"
                if furniture_sprite is not None:
                    row = room.position.y + furniture.position.y
                    col = room.position.x + furniture.position.x
                    self._tiles[row][col] = furniture_sprite

    @property
    def rooms(self):
        return self._rooms


########################################
# Function: generate_level
########################################
def generate_level(difficulty=1):
    level = Level()
    level.generate_random()
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
    # Uncomment this to write level data to file
    # level.write_level_data()


if __name__ == '__main__':
    main()
