from .singleton import Singleton


class Generator(Singleton):

    def __init__(self):
        self._id = 0

    @staticmethod
    def generate_player_id():
        import itertools
        str_list = ("".join(x) for x in
                  itertools.product("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", repeat=16))
        return next(str_list)

    def new_id(self):
        self._id += 1
        return self._id


generator = Generator()
