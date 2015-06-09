# coding: utf-8

import numpy as np
import pandas as pd


def letter_to_seq(s):
  seq = np.zeros(len(s), dtype=np.int)
  for k in range(1, len(seq)-1):
    seq[k] = 1 if s[k]=='C' else 0
  return seq

def string_to_letter(s):
  t = s.replace('0', 'S').replace('1', 'C')
  t = list(t)
  t[0] = 'E'
  t[-1] = 'E'
  return ''.join(t)

def array_to_string(seq, sep):
  return sep.join(map(str, seq))

def sol_to_string (sol):
  # flatten 3x3x3 array solution
  seq = sol.ravel()
  return ','.join(map(str, seq))

def string_to_array(s):
    return np.fromstring(','.join([c for c in s]), dtype=np.int, sep=',')

def string_to_sol(s):
  # reshape flat solution to 3x3x3 array
  v = np.fromstring(s, dtype=np.int, sep=',')
  return v.reshape(3, 3, 3)

def lexicographical_version(seq):
  # convert the sequence into it smaller lexicographical order
  s = seq if seq<seq[::-1] else seq[::-1]
  return s

def seq_to_pos(s):
    direction = np.cumsum(s)%2
    x = np.append(0, np.cumsum(1-direction[:-1]))
    y = np.append(0, np.cumsum(direction[:-1]))
    return x, y

def string_to_path(s):
    return np.argsort(string_to_sol(s).ravel())+1

def create_df_stat(df):
    nbStraight_min = df['nb of straights'].min()
    nbStraight_max = df['nb of straights'].max()
    nbSol_min = df['nb of solutions'].min()
    nbSol_max = df['nb of solutions'].max()

    print 'nbStraight_min, nbStraight_max = {}, {}'.format(nbStraight_min, nbStraight_max)
    print 'nbSol_min, nbSol_max = {}, {}'.format(nbSol_min, nbSol_max)

    stats = np.zeros([nbSol_max-nbSol_min+1, nbStraight_max-nbStraight_min+1], dtype=np.int)
    for nSol in range(nbSol_max-nbSol_min+1):
      for nStr in range(nbStraight_max-nbStraight_min+1):
        stats[nSol, nStr] = np.logical_and(df['nb of solutions']==nbSol_min+nSol, df['nb of straights']==nbStraight_min+nStr).sum()/(nbSol_min+nSol)

    df_stat = pd.DataFrame(data=stats, index=range(nbSol_min, nbSol_max+1), columns=range(nbStraight_min, nbStraight_max+1))
    df_stat = df_stat[df_stat.sum(axis=1)!=0]
    df_stat['sequence total'] = df_stat.sum(axis=1)
    df_stat['solution total'] = df_stat['sequence total']*df_stat.index
    df_stat = df_stat.append(pd.DataFrame(data=pd.DataFrame(df_stat.sum(axis=0)).T.values, index=['total'], columns=df_stat.columns))
    df_stat.columns.name='nb of straights'
    df_stat.index.name='nb of solutions'
    return df_stat
