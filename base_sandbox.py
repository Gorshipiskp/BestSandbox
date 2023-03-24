import random
import time
import config
from pygame import Color


vertical_vector = 1
horizontal_vector = 1

subs = {
    "liquid": {
        "physics": True,
        'loose': True,
        'liquid_like': True,
        'diffusion': False,
        'gas': False,
    },
    "bulk": {
        "physics": True,
        'loose': True,
        'liquid_like': False,
        'diffusion': False,
        'gas': False,
    },
    "solid": {
        "physics": False,
        'loose': False,
        'liquid_like': False,
        'diffusion': False,
        'gas': False,
    },
    "gas": {
        "physics": True,
        'loose': True,
        'liquid_like': False,
        'diffusion': True,
        'gas': True,
    },
}

mats = {
    "brick": {
        'name': 'Кирпич',
        "subs": subs["solid"],
        'temperature': config.base_temperature,
        'density': 9000,
        "color": Color(180, 10, 10),
    },
    "sand": {
        'name': 'Песок',
        "subs": subs["bulk"],
        'temperature': config.base_temperature,
        'density': 1500,
        "color": Color(200, 150, 10),
    },
    "dirt": {
        'name': 'Земля',
        "subs": subs["bulk"],
        'temperature': config.base_temperature,
        'density': 1200,
        "color": Color(162, 101, 62),
    },
    "water": {
        'name': 'Вода',
        "subs": subs["liquid"],
        'temperature': config.base_temperature,
        'density': 1000,
        "color": Color(25, 75, 200),
    },
    "air": {
        'name': 'Воздух',
        "subs": subs["gas"],
        'temperature': config.base_temperature,
        'density': 1.3,
        "color": Color(15, 15, 15),
    },
    "helium": {
        'name': 'Гелий',
        "subs": subs["gas"],
        'temperature': config.base_temperature,
        'density': 0.17,
        "color": Color(190, 190, 190),
    },
    "lava": {
        'name': 'Лава',
        "subs": subs["liquid"],
        'temperature': 1000,
        'density': 2610,
        "color": Color(255, 60, 60),
    },
    "sodium": {
        'name': 'Натрий',
        "subs": subs["bulk"],
        'temperature': config.base_temperature,
        'density': 910,
        "color": Color(235, 230, 235),
        "reactions": [
            [['water'], 'hydroxide_sodium']
        ]
    },
    "hydroxide_sodium": {
        'name': 'Гидроксид натрия',
        "subs": subs["bulk"],
        'temperature': config.base_temperature,
        'density': 1110,
        "color": Color(235, 20, 145),
    },
    "magnesium": {
        'name': 'Магний',
        "subs": subs["bulk"],
        'temperature': config.base_temperature,
        'density': 780,
        "color": Color(135, 130, 135),
        "reactions": [
            [['water'], 'hydroxide_magnesium']
        ]
    },
    "hydroxide_magnesium": {
        'name': 'Гидроксид магния',
        "subs": subs["bulk"],
        'temperature': config.base_temperature,
        'density': 1010,
        "color": Color(35, 180, 95),
    },
    "sulfuric_acid": {
        'name': 'Серная кислота',
        "subs": subs["liquid"],
        'temperature': config.base_temperature,
        'density': 950,
        "color": Color(235, 190, 25),
        "reactions": [
            [['hydroxide_sodium'], 'sodium_sulfate'],
            [['hydroxide_magnesium'], 'magnesium_sulfate']
        ]
    },
    "sodium_sulfate": {
        'name': 'Сульфат натрия',
        "subs": subs["bulk"],
        'temperature': config.base_temperature,
        'density': 1050,
        "color": Color(35, 190, 235),
    },
    "magnesium_sulfate": {
        'name': 'Сульфат магния',
        "subs": subs["bulk"],
        'temperature': config.base_temperature,
        'density': 1150,
        "color": Color(255, 190, 235),
    },
    # "test1": {
    #     'name': 'ТЕСТ1',
    #     "subs": subs["liquid"],
    #     'temperature': config.base_temperature,
    #     'density': 3150,
    #     "color": Color(25, 190, 25),
    #     "reactions": [
    #         [['test2'], 'test1'],
    #     ]
    # },
    # "test2": {
    #     'name': 'ТЕСТ2',
    #     "subs": subs["liquid"],
    #     'temperature': config.base_temperature,
    #     'density': 3150,
    #     "color": Color(25, 25, 190),
    #     "reactions": [
    #         [['test1'], 'test2'],
    #     ]
    # },
}


def do_pos(orig_w: int, orig_h: int, hei: int, wid: int):
    if not ((0 > wid or wid >= orig_w) or (0 > hei or hei >= orig_h)):
        return hei, wid


def get_neighbours(orig_w, orig_h, hei, wid):
    neighs = []

    if hei + 1 < orig_h:
        neighs.append((hei + 1, wid))
    if hei - 1 >= 0:
        neighs.append((hei - 1, wid))
    if wid + 1 < orig_w:
        neighs.append((hei, wid + 1))
    if wid - 1 >= 0:
        neighs.append((hei, wid - 1))
    return neighs


def timer(func):
    def func_f(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)

        try:
            print(f'{func.__name__} = {f"{round(time.time() - start, 4)}s": ^7} {round(1 / (time.time() - start), 2)}μ')
        except ZeroDivisionError:
            print(f'{func.__name__} = {"0s": ^7} inf μ')
        return res

    return func_f


class Pixel:
    def __init__(self, material):
        self.name = material
        self.info = mats[material]
        self.temperature = mats[material]['temperature']

    def __repr__(self):
        return self.name[0]


def diffuse_substance(density_orig, density_down_left, density_down_right, density_right, density_left,
                      down_left, down_right, left, right):
    to_add = []

    if down_left:
        if density_down_left < density_orig:
            to_add.append(down_left)
    if down_right:
        if density_down_right < density_orig:
            to_add.append(down_right)
    if left:
        if density_left < density_orig:
            to_add.append(left)
    if right:
        if density_right < density_orig:
            to_add.append(right)
    return to_add


def loose_substance(density_orig, density_down_left, density_down_right, down_left, down_right):
    to_add = []

    if down_left:
        if density_down_left < density_orig:
            to_add.append(down_left)
    if down_right:
        if density_down_right < density_orig:
            to_add.append(down_right)
    return to_add


def liquid_substance(density_orig, density_left, density_right, left, right):
    to_add = []

    if left and density_left < density_orig:
        to_add.append(left)
    if right and density_right < density_orig:
        to_add.append(right)
    return to_add


def gas_substance(density_orig, density_up, density_up_left, density_up_right, density_left, density_right, up, up_left,
                  up_right, left, right):
    to_add = []

    if up and density_up > density_orig:
        to_add.append(up)
    if up_left and density_up_left > density_orig:
        to_add.append(up_left)
    if up_right and density_up_right > density_orig:
        to_add.append(up_right)
    if right and density_right > density_orig:
        to_add.append(right)
    if left and density_left > density_orig:
        to_add.append(left)
    return to_add


class Matrix:
    def __init__(self, size):
        if isinstance(size, int):
            size = (size, size)

        self.size = size
        self.matrix = list(list(Pixel('air') for _ in range(size[1])) for _ in range(size[0]))
        self.iter_num = 0

    def __repr__(self):
        return '\n'.join(''.join(str(pix) for pix in row) for row in self.matrix)

    def __getitem__(self, item):
        if len(item) == 1:
            return self.matrix[item[0]]
        elif len(item) > 1:
            return self.matrix[item[0]][item[1]].info['color']

    def __setitem__(self, key, value):
        if len(key) == 1:
            self.matrix[key[0]] = value
        elif len(key) > 1:
            self.matrix[key[0]][key[1]] = value

    def moving(self, pos1: tuple[int, int], pos2: tuple[int, int]):
        self.matrix[pos1[0]][pos1[1]], self.matrix[pos2[0]][pos2[1]] = self.matrix[pos2[0]][pos2[1]], \
                                                                       self.matrix[pos1[0]][pos1[1]]
        return pos1, pos2

    def iteration(self):
        cop_matrix = []
        edited = []

        for i_id, i in enumerate(self.matrix):
            cop_matrix.append([])
            for u in i:
                cop_matrix[i_id].append(u)

        for h_id, h in enumerate(cop_matrix):
            for w_id, w in enumerate(h):
                if w.name != 'air' and w.info['subs']['physics']:
                    down = do_pos(self.size[1], self.size[0], h_id, w_id + 1)
                    if w.info['subs']['physics'] and down:
                        moves = []

                        is_loose = w.info['subs']['loose']
                        is_liquid_like = w.info['subs']['liquid_like']
                        is_diffusion = w.info['subs']['diffusion']
                        is_gas = w.info['subs']['gas']

                        if down and not cop_matrix[down[0]][down[1]].info['density'] < w.info['density']:
                            if is_diffusion:
                                down_left = do_pos(self.size[1], self.size[0], h_id - 1, w_id + 1)
                                down_right = do_pos(self.size[1], self.size[0], h_id + 1, w_id + 1)
                                left = do_pos(self.size[1], self.size[0], h_id - 1, w_id)
                                right = do_pos(self.size[1], self.size[0], h_id + 1, w_id)

                                down_left_density = False
                                down_right_density = False
                                left_density = False
                                right_density = False

                                if down_left:
                                    down_left_density = cop_matrix[down_left[0]][down_left[1]].info['density']
                                if down_right:
                                    down_right_density = cop_matrix[down_right[0]][down_right[1]].info['density']
                                if left:
                                    left_density = cop_matrix[left[0]][left[1]].info['density']
                                if right:
                                    right_density = cop_matrix[right[0]][right[1]].info['density']

                                moves.extend(diffuse_substance(w.info['density'], down_left_density, down_right_density,
                                                               right_density, left_density, down_left, down_right, left,
                                                               right))
                            else:
                                if is_loose:
                                    down_left = do_pos(self.size[1], self.size[0], h_id - 1, w_id + 1)
                                    down_right = do_pos(self.size[1], self.size[0], h_id + 1, w_id + 1)

                                    down_left_density = False
                                    down_right_density = False

                                    if down_left:
                                        down_left_density = cop_matrix[down_left[0]][down_left[1]].info['density']
                                    if down_right:
                                        down_right_density = cop_matrix[down_right[0]][down_right[1]].info['density']

                                    moves.extend(loose_substance(w.info['density'], down_left_density,
                                                                 down_right_density, down_left, down_right))
                                if is_liquid_like:
                                    left = do_pos(self.size[1], self.size[0], h_id - 1, w_id)
                                    right = do_pos(self.size[1], self.size[0], h_id + 1, w_id)

                                    left_density = False
                                    right_density = False

                                    if left:
                                        left_density = cop_matrix[left[0]][left[1]].info['density']
                                    if right:
                                        right_density = cop_matrix[right[0]][right[1]].info['density']

                                    moves.extend(liquid_substance(w.info['density'], left_density, right_density,
                                                                  left, right))
                            if is_gas:
                                up = do_pos(self.size[1], self.size[0], h_id, w_id - 1)
                                up_left = do_pos(self.size[1], self.size[0], h_id - 1, w_id - 1)
                                up_right = do_pos(self.size[1], self.size[0], h_id + 1, w_id - 1)
                                left = do_pos(self.size[1], self.size[0], h_id - 1, w_id)
                                right = do_pos(self.size[1], self.size[0], h_id + 1, w_id)

                                up_left_density = False
                                up_right_density = False
                                up_density = False
                                left_density = False
                                right_density = False

                                if up:
                                    up_density = cop_matrix[up[0]][up[1]].info['density']
                                if up_left:
                                    up_left_density = cop_matrix[up_left[0]][up_left[1]].info['density']
                                if up_right:
                                    up_right_density = cop_matrix[up_right[0]][up_right[1]].info['density']
                                if left:
                                    left_density = cop_matrix[left[0]][left[1]].info['density']
                                if right:
                                    right_density = cop_matrix[right[0]][right[1]].info['density']

                                to_move = gas_substance(w.info['density'], up_density, up_left_density,
                                                        up_right_density, left_density, right_density, up, up_left,
                                                        up_right, left, right)

                                if to_move:
                                    moves.extend(to_move)
                                else:
                                    moves.append(down)
                        else:
                            moves.append(down)

                        if w.info.get('reactions'):
                            neighs = []

                            for i in get_neighbours(self.size[1], self.size[0], h_id, w_id):
                                neighs.append(cop_matrix[i[0]][i[1]].name)

                            for react in w.info.get('reactions'):
                                all_in = True
                                for component in react[0]:
                                    if component not in neighs:
                                        all_in = False
                                    if all_in:
                                        self.matrix[h_id][w_id] = Pixel(react[-1])

                        if moves:
                            edited.append(self.moving(random.choice(moves), (h_id, w_id)))
        self.iter_num += 1
        return edited
