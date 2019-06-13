import numpy as np
from pylab import *
import datetime
import time
from scipy.misc import derivative

class PIDataConverter(object):
  def __init__(self):
    self.method = method

  def partial_derivative(func,var=0,point=[]):
    args = point[:]
    def wraps(x):
      args[var] = x
      return func(*args)
    return derivative(wraps,point[var],dx=1e-6)
  def AccessData(self,address):
    return 0

  def AV_Pos(self,rope_len):
