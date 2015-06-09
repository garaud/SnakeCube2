# coding: utf-8

import numpy as np
import pandas as pd

from timeit import default_timer as timer

from snakecube.snakecube import SnakeCube
from snakecube.utils import (letter_to_seq,
                             lexicographical_version,
                             array_to_string,
                             string_to_letter,
                             string_to_path,
                             sol_to_string)
from snakecube.draw import (draw_sequence,
                            draw_path_series)



StandardCubes = {'KevsKubes': 'ESCCCSCSCCCCCCCCCCCCCSCSCCE',
                 'CubraGreen': 'ESCSCSCCSCSCSCCCCSCCSCCSCSE',
                 'CubraBlue': 'ESCSCSCSCCCCSCSCCCSCCSCCCSE',
                 'CubraRed': 'ESCCCCCCCCCSCCCCCCCSCSCCCCE',
                 'CubraOrange': 'ESCSCCCCSCCCCCCCCSCCCSCCCSE',
                 'CubraPurple': 'ECCCCSCSCCCCCCCCCCCSCSCCCCE'}

ColStandardCubes = {'KevsKubes': 'LightGray',
                    'CubraGreen': 'LightGreen',
                    'CubraBlue': 'LightBlue',
                    'CubraRed': 'Tomato',
                    'CubraOrange': 'LightSalmon',
                    'CubraPurple': 'Plum'}

N = 3
snake_cube = {}

for key in StandardCubes:
    name = key
    cube = StandardCubes[key]
    print '\n', name
    t0 = timer()
    seq = letter_to_seq(cube)
    snake_cube[name] = SnakeCube(seq, N)
    snake_cube[name].solve()
    t1 = timer()
    print '\nrun time = {:.3f}s'.format(t1-t0)
    print 'nb solutions = {}'.format(len(snake_cube[name].all_solution))


df_solution = {}
for key in StandardCubes:
    name = key
    seq = [lexicographical_version(array_to_string(s[0], ''))
            for s in snake_cube[name].all_solution][0]
    flat_sol = [sol_to_string(s[1])
            for s in snake_cube[name].all_solution]
    first_pos = [array_to_string(s[2], ',')
            for s in snake_cube[name].all_solution]
    direct = [array_to_string(s[3], ',')
            for s in snake_cube[name].all_solution]
    df_solution[name] = pd.DataFrame(data=np.array([flat_sol, first_pos, direct]).T,
                                index = range(1, len(flat_sol)+1),
                                columns=['flat solution', 'first position', 'direction'])
    df_solution[name].index.name = seq

# drawing
for key in StandardCubes:
    name = key
    df = df_solution[name].copy()
    print '\n{} sequence=\n\t{}\n\t{}'.format(name, df.index.name, string_to_letter(df.index.name))
    draw_sequence(df.index.name, ColStandardCubes[name])
    ps = map(string_to_path, df.ix[1:15, 'flat solution'])
    draw_path_series(ps)
    #sleep(2)
