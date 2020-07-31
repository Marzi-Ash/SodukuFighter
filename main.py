import math
import copy
import time
from tabulate import tabulate
import sys
#Functions
def update_neighbors(domain,I,J,value):
    #update row
    for y in range (0, k*k):
        if (value in domain[I][y] and (y != J)):
            domain[I][y].remove(value)

    #update column
    for x in range (0, k*k):
        if (value in domain[x][J] and (x != I)):
            domain[x][J].remove(value)

    #update square
    for i in range (math.floor(I/k)*k, math.floor(I/k)*k+k):
        for j in range (math.floor(J/k)*k, math.floor(J/k)*k+k):
            if (value in domain[i][j] and (i!=I or j!=J)):
                domain[i][j].remove(value)

    return domain

def check_domain (domain):
    checking = 1
    error=0
    while (checking):
        #count_element(domain)
        domain_s = copy.deepcopy(domain)
        for i in range(0,k*k):
            for j in range (0, k*k):
                if (len(domain[i][j]) < 1):
                    #print("No Answer")
                    error=1
                    return domain,error
                if (len(domain[i][j]) == 1):
                    domain = update_neighbors(domain,i,j,domain[i][j][0])

        if (domain == domain_s):
            checking = 0
    return domain,error

def count_element(domain):
    count = 0
    assigned = 0
    for i in domain:
        for j in i:
            count = count + len(j)
            if (len(j) == 1):
                assigned = assigned + 1
    #print(assigned)
    #print (count)
    return count,assigned

def Update_2_Equal(list):
    N = len(list)
    n = int(math.sqrt(N))

    arr=[]
    # find all units with |domain|=2
    for r in range(0,N):
        for c in range(0,N):
            if len(list[r][c])==2:
                arr.append([r,c,list[r][c]])
    for i in range(0, len(arr)-1):
        for j in range(i+1, len(arr)):
            if (arr[i][2] == arr[j][2]) and (arr[i][0]==arr[j][0]): # check if in the same row
                # remove elements in the row
                for e in range (0,N):
                    # remove domain 1 from all elements except one's with |domain|=2
                    if (len(arr[i][2]) == 2):
                        if arr[i][2][1] in list[arr[i][0]][e]:
                            if (e != arr[i][1]) and (e != arr[j][1]):
                                list[arr[i][0]][e].remove(arr[i][2][1])

                        if arr[i][2][0] in list[arr[i][0]][e]:
                            if (e != arr[i][1]) and (e != arr[j][1]):
                                list[arr[i][0]][e].remove(arr[i][2][0])

            elif (arr[i][2] == arr[j][2]) and (arr[i][1] == arr[j][1]): # check if in the same column
                # remove element in the column
                for e in range (0,N):
                    # remove domain 1 from all elements except one's with |domain|=2
                    if (len(arr[i][2]) == 2):
                        if arr[i][2][0] in list[e][arr[i][1]]:
                            if (e != arr[i][0]) and (e != arr[j][0]):
                                list[e][arr[i][1]].remove(arr[i][2][0])

                        if arr[i][2][1] in list[e][arr[i][1]]:
                            if (e != arr[i][0]) and (e != arr[j][0]):
                                list[e][arr[i][1]].remove(arr[i][2][1])

            if  (arr[i][2] == arr[j][2]) and (int(arr[i][0]/n) == int(arr[j][0]/n)) and (int(arr[i][1]/n) == int(arr[j][1]/n)):
                # check if in the same square
                # remove elements in the square
                start_row = arr[i][0] - arr[i][0]%n
                start_col = arr[i][1] - arr[i][1]%n
                for r in range (0,n):
                    for c in range (0,n):

                        if (len(arr[i][2]) == 2):
                            if arr[i][2][0] in list[start_row+r][start_col+c]:
                                if ((start_row+r == arr[i][0]) and (start_col+c == arr[i][1])) or\
                                    ((start_row+r == arr[j][0]) and (start_col+c == arr[j][1])) :
                                    pass
                                else:
                                    list[start_row+r][start_col+c].remove(arr[i][2][0])

                            if arr[i][2][1] in list[start_row+r][start_col+c]:
                                if ((start_row+r == arr[i][0]) and (start_col+c == arr[i][1])) or\
                                    ((start_row+r == arr[j][0]) and (start_col+c == arr[j][1])) :
                                    pass
                                else:
                                    list[start_row+r][start_col+c].remove(arr[i][2][1])
    return list

def search(domain):
    stack =[]
    stack.append([domain,None,None])
    poped_variable = [None]*2
    while(True):

        ready = final_result(stack[-1][0])
        if (ready):
            return stack[-1][0]
        domain_current = copy.deepcopy(stack[-1][0])
        if (poped_variable == [None,None]):
            variable = mrv(domain_current)
        else:
            variable = poped_variable
            poped_variable = [None]*2
            while (len(domain_current[variable[0]][variable[1]]) < 1):
                # pop
                [_,variable,value] = stack.pop()
                [domain_current,_,_] = stack[-1]
                domain_current[variable[0]][variable[1]].remove(value)
                stack[-1][0]= copy.deepcopy(domain_current)

        value = lcv(domain_current,variable)
        domain_current[variable[0]][variable[1]]=[value]
        domain_current,error = check_domain(domain_current)
        err = 0
        if (error == 0):
            domain_current = pruning(domain_current)
            domain_current,err = check_domain(domain_current)
            if (err == 0):
                stack.append([domain_current, variable, value])

        if (error == 1 or err == 1):
            domain_temp = copy.deepcopy(stack[-1][0])
            domain_temp[variable[0]][variable[1]].remove(value)
            stack[-1][0]= copy.deepcopy(domain_temp)

            while(len(domain_temp[variable[0]][variable[1]])>0):
                domain_for_variable = (stack[-1][0])
                new_value = lcv(domain_for_variable,variable)
                domain_for_variable[variable[0]][variable[1]]=[new_value]
                domain_for_variable,error = check_domain(domain_for_variable)
                err = 0
                if(error == 0):
                    domain_for_variable = pruning(domain_for_variable)
                    domain_for_variable,err = check_domain(domain_for_variable)
                    if (err == 0):
                        stack.append([domain_for_variable, variable, new_value])
                    break
                if (error == 1 or err == 1):
                    domain_temp[variable[0]][variable[1]].remove(new_value)
                    stack[-1][0]= copy.deepcopy(domain_temp)

            if(len(domain_temp[variable[0]][variable[1]])==0):
                [_,poped_variable,poped_value]= stack.pop()
                domain_top = copy.deepcopy(stack[-1][0])
                domain_top[poped_variable[0]][poped_variable[1]].remove(poped_value)
                stack[-1][0]= copy.deepcopy(domain_top)

def mrv (P):
    dim = len(P)
    le=dim
    r=0
    c=0
    for i in range (dim):
        for j in range (dim):
            if len(P[i][j]) > 1 and len(P[i][j]) < le :
                le= len(P[i][j])
                r=i
                c=j
    return [r,c]

def lcv2(domain, variable):

    N = len(domain)
    k = int(math.sqrt(N))
    I = variable[0]
    J = variable[1]
    max = -1
    sol = domain[variable[0]][variable[1]][0]

    for value in domain[variable[0]][variable[1]]:
        temp_domain = copy.deepcopy(domain)
        temp_domain[variable[0]][variable[1]] = [value]
        temp_domain,error = check_domain(temp_domain)
        min = N
        if (error != 1):
            #row
            for y in range (0, N):
                if (y!=J and len(temp_domain[I][y])>1):
                    if len(temp_domain[I][y])<min:
                        min = len(temp_domain[I][y])

            #update column
            for x in range (0, N):
                if (x!=I and len(temp_domain[x][J])>1):
                    if len(temp_domain[x][J])<min:
                        min = len(temp_domain[x][J])


            #update square
            for i in range (math.floor(I/k)*k, math.floor(I/k)*k+k):
                for j in range (math.floor(J/k)*k, math.floor(J/k)*k+k):
                    if ((i!=I or j!=J) and len(temp_domain[i][j])>1):
                        if len(temp_domain[i][j])<min:
                            min = len(temp_domain[i][j])

            if min>max:
                sol = value
    return sol

def lcv (P,var):
    dim = len(P)
    r= var[0]
    c= var[1]
    d= P[r][c]
    maxi=-1
    sr= int(math.sqrt(dim))
    rr= (int(r/sr))*sr
    cc= (int(c/sr))*sr
    sol = 0
    for v in range (len(d)):
        val= P[r][c][v]
        mini=dim
        le1=dim
        le2=dim
        le3=dim
        for i in range (dim):
            for z in (P[r][i]):
                if i!=c:
                    if z==val:
                        le1= len(P[r][i])-1
                        #break
            if le1 < mini:
                mini=le1

            for h in (P[i][c]):
                if i !=r:
                    if h==val:
                        le2= len(P[i][c])-1
                        #break
            if le2 <mini:
                mini=le2

        for w in range (sr):
            for o in range (sr):
                if w+rr ==r and o+cc==c :
                    pass
                else:
                    for q in (P[w+rr][o+cc]):
                        if q==val:
                            le3= len(P[w+rr][o+cc])-1
                            #break
                if le3<mini:
                    mini=le3

        if maxi<mini:
            maxi=mini
            sol= val
    return (sol)

def dh (P):
    dim = len(P)
    sr= int(math.sqrt(dim))
    r = 0
    c = 0
    cons=0
    for i in range(dim):
        for j in range(dim):
            rr= (int(i/sr))*sr
            cc= (int(j/sr))*sr
            if len(P[i][j])>1 :
                k=0
                for m in range (dim):
                    if len(P[i][m])>1 and m!=i:
                        k=k+1
                    if len(P[m][j])>1 and j!=m:
                        k=k+1
                for a in range (sr):
                    for b in range (sr):
                        if a+rr ==i or b+cc==j:
                            pass
                        else:
                            if len(P[a+rr][b+cc])>1:
                                k=k+1

                if k>cons:
                    cons= k
                    r=i
                    c=j
    return [r,c]

def mrv_dh (P):
    dim=len(P)
    le=dim
    r=0
    c=0
    list=[]
    for i in range (dim):
        for j in range (dim):
            if len(P[i][j]) > 1 and len(P[i][j]) <= le :
                if len(P[i][j])< le:
                    list=[]
                list.append([P[i][j],i,j])
                le= len(P[i][j])
    sr= int(math.sqrt(dim))
    cons=0
    for i in range(len(list)):
            row=list[i][1]
            col=list[i][2]
            rr= (int(row/sr))*sr
            cc= (int(col/sr))*sr
            k=0
            for m in range (dim):
                if len(P[row][m])>1:
                    k=k+1
                if len(P[m][col])>1:
                    k=k+1
            for a in range (sr):
                for b in range (sr):
                    if a+rr ==row or b+cc==col:
                        pass
                    else:
                        if len(P[a+rr][b+cc])>1:
                            k=k+1

            if k-2>cons:
                cons= k-2
                r=row
                c=col
    return [r,c]

def Update_by_Single_Value(list):
    N = len(list)
    n = int(math.sqrt(N))

    # check one existing element in the domain of all variables in a row
    for i in range(0,N):
        arr_row=[0]*N
        for j in range(0,N):
            for k in (list[i][j]):
                arr_row[k] = arr_row[k]+1

        for j in range(0,N):
            if arr_row[j] == 1:
                for k in range(0,N):
                    if j in list[i][k]:
                        list[i][k] = [j]
        # call update
        list,error = check_domain(list)

    # check one existing element in the domain of all variables in a column
    for i in range(0,N):
        arr_col=[0]*N
        for j in range(0,N):
            for k in (list[j][i]):
                arr_col[k] = arr_col[k]+1
        for j in range(0,N):
            if arr_col[j] == 1:
                for k in range(0,N):
                    if j in list[k][i]:
                        list[k][i] = [j]
        # call update
        list,error = check_domain(list)

    # check one existing element in the domain of all variables in a square
    for i in range(0,N):
        arr=[0]*N
        start_row = int(i/n)*n
        start_col = int(i%n)*n
        for r in range(0,n):
            for c in range(0,n):
                for k in list[start_row+r][start_col+c]:
                    arr[k] = arr[k]+1

        for j in range(0,N):
            if arr[j] == 1:
                for r in range(0,n):
                    for c in range(0,n):
                        if j in list[start_row+r][start_col+c]:
                            list[start_row+r][start_col+c] = [j]
        # call update
        list,error = check_domain(list)

    return list

def final_result (domain):
    for i in domain:
        for j in i:
            if (len(j) != 1):
                    return 0
    return 1

def pruning(domain):
    start=10000
    end=0
    while ((start-end)>0):
        start,_= count_element(domain)
        domain = Update_2_Equal(domain)
        domain = Update_by_Single_Value(domain)
        end,_ = count_element(domain)
    return domain

def Update_3(list):
    N = len(list)
    n = int(math.sqrt(N))

    arr=[]
    # find all units with 2<=|domain|<=3
    for r in range(0,N):
        for c in range(0,N):
            if len(list[r][c])>=2 and len(list[r][c])<=3:
                arr.append([r,c,list[r][c]])

    if len(arr)< 3:
        return (list)

    dom3=[]  #list of triples with same domain
    dom=[0]*N
    dom0=copy.deepcopy(dom)
    for i in range(len(arr)):
        for a in arr[i][2]:
            dom[a]=1
        dom11=copy.deepcopy(dom)
        for j in range(i+1, len(arr)):
            for b in arr[j][2]:
                dom[b]=1
            dom12=copy.deepcopy(dom)
            for k in range(j+1, len(arr)):
                for c in arr[k][2]:
                    dom[c]=1
                e=0
                for d in range(N):
                    e = e + dom[d]
                if e==3:
                    dom3.append ([arr[i],arr[j],arr[k]])
                dom = []
                dom = copy.deepcopy(dom12)
            dom = []
            dom = copy.deepcopy(dom11)
        dom = []
        dom = copy.deepcopy(dom0)

    for i in range (len(dom3)):
        d=[]
        for j in range (N):
            if (j in dom3[i][0][2]) or (j in dom3[i][1][2]) or (j in dom3[i][2][2]):
                d.append(j)
        dom3[i].append(d)

    for q in range (len(dom3)):
        if dom3[q][0][0]== dom3[q][1][0] == dom3[q][2][0] :  #same row
            row= dom3[q][0][0]
            for i in range(N):
                # remove elements in the row

                if dom3[q][3][0] in list[dom3[q][0][0]][i]:
                    if (i!= dom3[q][0][1]) and (i!=dom3[q][1][1]) and (i!=dom3[q][2][1]):
                        list[row][i].remove(dom3[q][3][0])
                if dom3[q][3][1] in list[dom3[q][0][0]][i]:
                    if (i!= dom3[q][0][1]) and (i!=dom3[q][1][1]) and (i!=dom3[q][2][1]):
                        list[row][i].remove(dom3[q][3][1])
                if dom3[q][3][2] in list[dom3[q][0][0]][i]:
                    if (i!= dom3[q][0][1]) and (i!=dom3[q][1][1]) and (i!=dom3[q][2][1]):
                        list[row][i].remove(dom3[q][3][2])

        #call update
        if dom3[q][0][1]== dom3[q][1][1] == dom3[q][2][1] : #same column
            col= dom3[q][0][1]
            for i in range(N):
                # remove elements in the column

                if dom3[q][3][0] in list[i][col]:
                    if (i!= dom3[q][0][0]) and (i!=dom3[q][1][0]) and (i!=dom3[q][2][0]):
                        list[i][col].remove(dom3[q][3][0])
                if dom3[q][3][1] in list[i][col]:
                    if (i!= dom3[q][0][0]) and (i!=dom3[q][1][0]) and (i!=dom3[q][2][0]):
                        list[i][col].remove(dom3[q][3][1])
                if dom3[q][3][2] in list[i][col]:
                    if (i!= dom3[q][0][0]) and (i!=dom3[q][1][0]) and (i!=dom3[q][2][0]):
                        list[i][col].remove(dom3[q][3][2])

        #call update
        if  (int(dom3[q][0][0]/n) == int(dom3[q][1][0]/n)== int(dom3[q][2][0]/n)) and (int(dom3[q][0][1]/n) == int(dom3[q][1][1]/n)== int(dom3[q][2][1]/n)):
                # check if in the same square
                # remove elements in the square
                start_row = dom3[q][0][0] - dom3[q][0][0]%n
                start_col = dom3[q][0][1] - dom3[q][0][1]%n
                for r in range (0,n):
                    for c in range (0,n):
                        if dom3[q][3][0] in list[start_row+r][start_col+c]:
                            if ((start_row+r == dom3[q][0][0]) and (start_col+c == dom3[q][0][1])) or\
                                ((start_row+r == dom3[q][1][0]) and (start_col+c == dom3[q][1][1])) or\
                                ((start_row+r == dom3[q][2][0]) and (start_col+c == dom3[q][2][1])):
                                pass
                            else:
                                list[start_row+r][start_col+c].remove(dom3[q][3][0])

                        if dom3[q][3][1] in list[start_row+r][start_col+c]:
                            if ((start_row+r == dom3[q][0][0]) and (start_col+c == dom3[q][0][1])) or\
                                ((start_row+r == dom3[q][1][0]) and (start_col+c == dom3[q][1][1])) or\
                                ((start_row+r == dom3[q][2][0]) and (start_col+c == dom3[q][2][1])):
                                pass
                            else:
                                list[start_row+r][start_col+c].remove(dom3[q][3][1])

                        if dom3[q][3][2] in list[start_row+r][start_col+c]:
                            if ((start_row+r == dom3[q][0][0]) and (start_col+c == dom3[q][0][1])) or\
                                ((start_row+r == dom3[q][1][0]) and (start_col+c == dom3[q][1][1])) or\
                                ((start_row+r == dom3[q][2][0]) and (start_col+c == dom3[q][2][1])):
                                pass
                            else:
                                list[start_row+r][start_col+c].remove(dom3[q][3][2])

        #call update
    return(list)


#Define Parameter
k = 5
table = [[0 for i in range(k*k)] for j in range(k*k)]
domain = [[[v for v in range(k*k)] for i in range(k*k)] for j in range(k*k)]

#read from file and creat table
start_time = time.time()
data = open('./'+sys.argv[1]).read().split()
for i in range(0,k*k):
    for j in range (0, k*k):
        table [i][j] = int(data[i*k*k+j])
        if (table[i][j] != -1):
            domain [i][j] = [table[i][j]]

count_element(domain)
domain,error = check_domain(domain)
count_element(domain)
domain = pruning(domain)
count_element(domain)
print ("searching!!!!!")
domain = search(domain)
domain,error = check_domain(domain)

for i in range (0,k*k):
    for j in range (0,k*k):
        table[i][j] = domain[i][j][0]

print (tabulate (table,tablefmt='grid'))

if (error==1):
    print ('No Answer')

print (time.time()-start_time)
