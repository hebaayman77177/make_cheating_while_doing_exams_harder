#initialization
import os
os.remove("data.csv")
f=open('data.csv','w')
f.close()
f=open('auto_increment.txt','w')

f.write('0')
f.close()

