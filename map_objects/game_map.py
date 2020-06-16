from random import randint

from map_objects.tile import  Tile
from map_objects.rectangle import Rect


class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialise_tiles()

    def initialise_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

        return tiles

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True

        return False

    def create_room(self, room):
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player):
        rooms = []
        num_rooms = 0

        for r in range(max_rooms):
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)

            x = randint(0, map_width - w - 1)
            y = randint(0, map_height - h - 1)

            newRoom = Rect(x, y, w, h)

            for otherRoom in rooms:
                if newRoom.intersect(otherRoom):
                    break
            else:
                self.create_room(newRoom)

                (newX, newY) = newRoom.centre()

                if num_rooms == 0:
                    player.x = newX
                    player.y = newY
                else:
                    (prevX, prevY) = rooms[num_rooms - 1].centre()

                    if randint(0, 1) == 1:
                        self.create_h_tunnel(prevX, newX, prevY)
                        self.create_v_tunnel(prevY,newY,newX)
                    else:
                        self.create_v_tunnel(prevY, newY, prevX)
                        self.create_h_tunnel(prevX, newX, newY)

            rooms.append(newRoom)
            num_rooms += 1