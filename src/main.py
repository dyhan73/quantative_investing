import os
import field_map as fmap

print(os.getcwd())
print("kakarott")
print(os.listdir(os.getcwd()))
cwd = os.getcwd()
print(cwd)

print(fmap.dic_companies)

y = 2020
m = 5000

for i in range(1, 20):
    print(y + i, m)
    m = m * 1.15

import sys
print(sys.path)

import pandas as pd
import numpy as np

dir(pd)
dir(np)

y = 2020
m = 5000

for i in range(1, 20):
    print(y + i, m)
    m = m * 1.15

import sys
print(sys.path)

import pandas as pd
import numpy as np

dir(pd)
dir(np)
