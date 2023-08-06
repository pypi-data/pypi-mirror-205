# convert decimal to binary

class op(object):

    def __init__(self):
      pass
    def dec2bin(self, number):
      ans = ""
      if ( number == 0 ):
          return 0
      while ( number ):
          ans += str(number&1)
          number = number >> 1
      ans = ans[::-1]
      return ans
