# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import

import logging

import numpy as np


logger = logging.getLogger(__name__)


class SnakeCube(object):
    """Snake cube resolver
    """
    def __init__(self, sequence, N):
        self.N = N
        self.s = len(sequence)
        if (self.s==N**3):
            self.sequence = sequence
        else:
            self.sequence = np.zeros(N**3, dtype=np.int)
            self.sequence[:len(sequence)] = sequence
        self.all_solution = []

    def solve(self):
        logger.debug('start solving')
        self.start_search_from_all_positions()

    def start_search_from_all_positions(self):
        for i in range(self.N):
            for j in range(self.N):
                for k in range(self.N):
                    self.start_from_position(i, j, k)

    def start_from_position(self, x, y, z):
        self.direction = np.zeros(self.N**3-1, dtype=np.int)
        self.solution = np.zeros([self.N, self.N, self.N], dtype=np.int)
        self.position = np.array([x, y, z], dtype=np.int)
        self.first_position = [x, y, z]
        self.solution[x, y, z] = 1
        pos = self.position.copy()
        self.step(0, pos, 1, 1)

    def step(self, n, position, direction, explored_dim):
        sign = -1 if (direction<0) else 1
        pos = position.copy()
        pos[abs(direction) - 1] += sign
        if self.is_valid_position(pos):
            self.branch(n+1, pos, direction, explored_dim)

    def branch(self, n, position, direction, explored_dim):
        self.solution[position[0], position[1], position[2]] = n+1
        self.direction[n-1] = direction

        if self.is_solution_complete(n):
            self.sequence[n] = 0
            if self.keep_solution():
                logger.debug('\rsolution no = %d' % (len(self.all_solution)+1))
                self.all_solution.append([self.sequence.copy(), self.solution.copy(), self.first_position, self.direction.copy()])
        else:
            if (self.s<=n or self.sequence[n]==0):
                # go straight
                self.sequence[n] = 0
                pos = position.copy()
                self.step(n, pos, direction, explored_dim)
            if (self.s<=n or self.sequence[n]==1):
                # make a turn
                self.sequence[n] = 1
                pos = position.copy()
                self.turn(n, pos, direction, explored_dim)

        self.solution[position[0], position[1], position[2]] = 0

    def turn(self, n, position, direction, explored_dim):
        for k in range(1, min(explored_dim, 3)+1):
            if (k!=abs(direction)):
                pos = position.copy()
                self.step(n, pos, k, explored_dim)
                pos = position.copy()
                self.step(n, pos, -k, explored_dim)
        if (explored_dim<3):
            self.step(n, position, explored_dim+1, explored_dim+1)

    def is_valid_position(self, position):
        test = self.is_within_cube(position) and self.is_position_vacant(position)
        return test

    def is_within_cube(self, position):
        test = set(position).issubset(set(range(self.N)))
        return test

    def is_position_vacant(self, position):
        test = self.solution[position[0], position[1], position[2]]==0
        return test

    def is_solution_complete(self, n):
        test = (n==self.N**3-1)
        return test

    def keep_solution(self):
        if (self.s<=1):
            # exhaustive search
            test = self.is_lexicographically_smaller_or_equal_than_reverse()
        elif (self.s==self.N**3):
            # search for one given snake
            test = (not(self.is_palendromic()) or self.is_lexicographically_smaller_or_equal_than_reverse())
        else:
            # intermediary case: user decides what to do - provisionally no filter
            test = True
        return test

    def is_palendromic(self):
        seq = self.sequence
        test = (seq==seq[::-1]).all()
        return test

    def is_lexicographically_smaller_or_equal_than_reverse(self):
        # equal is important to avoid filtering out palendromic snakes in the full search
        reverse_direction = self.generate_reverse_direction()
        test = (list(self.direction) <= list(reverse_direction))
        return test

    def generate_reverse_direction(self):
        direction_map = self.create_direction_map()
        reverse_direction = direction_map[3+self.direction[::-1]]
        return reverse_direction

    def create_direction_map(self):
        direction_map = np.zeros(3+1+3, dtype=np.int)
        explored_dim = np.zeros(3, dtype=np.int)
        reverse_direction = self.direction[::-1]
        i = 0
        d = 0
        while (d<3):
            k = abs(reverse_direction[i])
            if (explored_dim[k-1]==0):
                explored_dim[k-1] = 1
                d += 1
                direction_map[3+reverse_direction[i]] = d
                direction_map[3-reverse_direction[i]] = -d
            i += 1
        return direction_map
