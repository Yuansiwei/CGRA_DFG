class A:
    a=0
    str='a'
from queue import Queue 
A_obj=A()
A_obj.index=1
q=Queue()
q.put(A_obj)

out=q.get()
out.index=2;
print(A_obj.index)