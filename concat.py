#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""#########################################################
############################################################
### Concatenate routines.                                ###
###                                                      ###
### Author: Mayara Santos Nascimento                     ###
### Last edited: Sep 2022                                ###
############################################################
#########################################################"""

import pandas as pd
from pandas import DataFrame
from random import sample
import pandas as pd
import os
import numpy as np
from numpy import genfromtxt

def random_img(path_img, filename):
  #Lista os arquivos da pasta especificada
  files = os.listdir(path_img)

  #Embaralha os arquivos da lista files
  aleat_num = sample(files, len(files))
  #print(aleat_num)

  #Transforma a lista aleat_num em uma tabela (data frame)
  df = pd.DataFrame(aleat_num)
  tabela_img = df.to_numpy()
  if not os.path.exists(filename):
    df.to_csv(filename, sep = ';', index=False, mode = "w", header = False)
  return tabela_img

def strip_list(list_of_lists):
  for i in range(len(list_of_lists)):
    l = list_of_lists[i]
    for j in range(len(l)):
      s = list_of_lists[i][j]
      list_of_lists[i][j] = s.strip()
      print("(%d, %d) = %s" % (i, j, list_of_lists[i][j]))
  return list_of_lists



## \brief Merges slide and pause routines
#  Read the slide and pause routine files. Replace path instructions with image instructions
#  adding a randomized image name.
#  Repeats the slide block as many times as defined by blocks and nreps. Between blocks is
#  placed a pause routine.
#  Starting time of each repetition is added to the times of each instruction.
#
#  @param filename_random Output file that stores the randomized image list.
#  @param filename_routine Output file that stores the merged routine.
#  @param path_img Path containing images that will be randomized.
#  @param path_slide Input routine file containing slide exibition routine.
#  @param path_pause Input routine file containing pause routine.
#  @param blocks Number of blocks of slide routines. There is a pause between two blocks.
#  @param repetitions Number of repetitions of slide routine.
def generate_routine(filename_random, filename_routine, path_img, path_slide, path_pause, blocks, repetitions):
  if os.path.exists(filename_random):
    os.remove(filename_random)
  if os.path.exists(filename_routine):
    os.remove(filename_routine)

  tabela = random_img(path_img, filename_random)
  tamanho = len(tabela)

  lf_slide = list(open(path_slide,'r'))
  lfl_slide = [_str.split(';') for _str in lf_slide]
  lfl_slide = strip_list(lfl_slide)
  print(lfl_slide)
  df1 = pd.DataFrame(lfl_slide)
  df_slide = df1[df1[0].str.contains( '#' )==False ]
  maximo_slide = df_slide[0].astype(float).max()

  lf_pause = list(open(path_pause,'r'))
  lfl_pause = [_str.split(';') for _str in lf_pause]
  lfl_pause = strip_list(lfl_pause)
  df2 = pd.DataFrame(lfl_pause)
  df_pause = df2[df2[0].str.contains( '#' )==False ]
  maximo_pause = df_pause[0].astype(float).max()

  maxs = 0
  cont = 0
  tab_final = []

  for i in range(blocks):
    for j in range(repetitions):
      if j == 0 and i == 0:
        valor = ('%s' %df_slide.iloc[0,3])
      else:
        cont += 1
      valor1 = ('%s' %(tabela[cont,0]))
      df_slide.loc[df_slide[1] == "path", 3] = valor + "/" + valor1

      if j==0 and i==0:
        maxs = 0
      else:
        maxs = maxs + maximo_slide
      df_slide = df_slide.assign(Time = df_slide[0].astype(float) + maxs)

      df_slide[3] = df_slide[3].str.replace('"', '')
      df_slide[3] = df_slide[3].str.replace('”\n', '')
      df_slide[3] = df_slide[3].str.replace('\n', '')
      df_slide[1] = df_slide[1].str.replace('\n', '')

      df = DataFrame(df_slide, columns = ['Time', 1, 2, 3])
      df[1] = df[1].str.replace('path', 'image')

      if not os.path.exists(filename_routine):
        df.to_csv(filename_routine, sep = ';', index=False, mode = "w", header = False)
      else:
        df.to_csv(filename_routine, sep = ';', index=False, mode = "a", header = False)

    if i != blocks-1:
      df_pause[3] = df_pause[3].str.replace('"', '')
      df_pause[3] = df_pause[3].str.replace('”\n', '')
      df_pause[3] = df_pause[3].str.replace('\n', '')
      df_pause[1] = df_pause[1].str.replace('\n', '')

      df_pause = df_pause.assign(Time = df_pause[0].astype(float) + maxs + maximo_slide)
      maxs = maxs + maximo_pause

      df1 = DataFrame(df_pause, columns = ['Time', 1, 2, 3])

      if not os.path.exists(filename_routine):
        df1.to_csv(filename_routine, sep = ';', index=False, mode = "w", header = False)
      else:
        df1.to_csv(filename_routine, sep = ';', index=False, mode = "a", header = False)


"""#########################################################
############################################################
### Main function                                        ###
############################################################
#########################################################"""

if __name__ == "__main__":

  #path_img = '/home/ddantas/script/python_venv/img_hrv_lan/images/slides/'
  #slide_routine = '/home/ddantas/script/python_venv/img_hrv_lan/routines/slides.txt'
  #pause_routine = '/home/ddantas/script/python_venv/img_hrv_lan/routines/slides_pause.txt'
  #filename_random = '/home/ddantas/script/python_venv/img_hrv_lan/random.txt'
  #filename_routine = '/home/ddantas/script/python_venv/img_hrv_lan/concate.txt'
  path_img         = 'images/slides/'
  slide_routine    = 'routines/slides.txt'
  pause_routine    = 'routines/slides_pause.txt'
  filename_random  = '/tmp/random.txt'
  filename_routine = '/tmp/concate.txt'

  blocks = 9
  repetitions = 5

  #random_img(path_img, filename_random)
  generate_routine(filename_random, filename_routine, path_img, slide_routine, pause_routine, blocks, repetitions)

