
f=open(input("Enter The File Name:"),'r')
L=f.readlines()
pc=0
h=int((L[pc].split("="))[-1])
pc=1
v=int((L[pc].split("="))[-1])
H=[]
V=[]
pc=3
for i in range(h):
    H.append(L[pc].split(","))
    pc=pc+1
pc=pc+1
for i in range(h):
    V.append(L[pc].split(","))
    pc=pc+1


# def rm_Inconsistent_values(x,y):
#     removed=False
#     for i in domain(x):
#         if  no value p in domain of x allow (i,p) to satisfy the constraint x<->y:
#             delete i from domain of x 
#             removed=True
#     return removed

# def ac3(csp):
#     while len(queue)!=0:
#         (x,y)<-remove first(queue)
#         if rm_Inconsistent_values(x,y):
#             for eack p in neighbors(x):
#                 add(p,x) to queue