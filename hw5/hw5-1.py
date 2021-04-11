import pandas as pd
import numpy as np

data=pd.read_excel('HW5-1.xls')
output=data.loc[:,['Output']]
a=data.loc[:,['Input 1','Input 2']]
A=np.array(a)
Output=np.array(output)


inverse = np.linalg.inv(A.transpose().dot(A))
result=inverse.dot(A.transpose()).dot(Output)