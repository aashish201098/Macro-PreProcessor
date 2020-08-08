import string
src= open("src2.txt","r")
output= open("op2.txt","w")
deftab= open("deftab2.txt","r+")
count= -1
expanding=False
lines=[]
namtab=[]
argtab=[]
proto=[]
e=[]
d=[]  # default 
data= list(src.readlines())
for line in data:
	if(line=='\n' or line=='\n\t' or line=='\t\n'):
		pass
	else:
		lines.append(line)
	
def getline():
	if expanding:
		global i
		i+=1
		#print(p)
		#print(d1)
		for j in range(0,len(p)):
			st= "?"+str(j)
			#print(e[i])
			if st in e[i]:
				if p[j]!='':
					e[i]= str.replace(e[i],st,p[j])
				else:
					e[i]= str.replace(e[i],st,d1[j])
				
		return e[i]
	else:
		global count
		count+=1
		return lines[count]
	
def define(line):
	#print("in define")
	l= line.split()
	#print(l)
	for j in range(0,len(namtab)):
		if l[1]==namtab[j]:
			return
	if len(l)>2:
		p= l[2].split(',')
	else:
		p=[]
	#print(p)
	global d1
	d1=[]
	for i in range(0,len(p)):
		p1= p[i].split('=')
		if len(p1)>1:
			d1.append(p1[1])
			p[i]=p1[0]
		else:
			d1.append('')
	#print(p)
	global d
	d.append(d1)		
	global argtab
	argtab.append(p);
	namtab.append(l[1])
	deftab.write(line)
	level=1
	while level>0:
		line= getline()
		#print(line)
		if line.strip().startswith("!!"):
			continue
		if expanding and line.strip()!="MEND" and "MBEGIN" not in line:
			output.write(line)
		for w in p:
			if w in line and not line.strip().startswith("MBEGIN") and not line.strip().startswith("DEFINE"):
				line = str.replace(line,w,"?"+str(p.index(w)))
		#print(line)
		deftab.write(line)
		if line.strip().startswith("MBEGIN"):
			level=level+1
		elif line.strip()=="MEND":
			level= level-1
	#deftab.close()
	
			
	
def definesingle(line):
	l= line.split()
	# l[1]= name of macro
	# l[2]= parameter list
	# l[3] and ahead = macro body
	for j in range(0,len(namtab)):
		if l[1]== namtab[j]:
			return
	if l[2].startswith("&"):
		p= l[2].split(',')
		global d1
		d1=[]
		for i in range(0,len(p)):
			p1= p[i].split('=')
			if len(p1)>1:
				d1.append(p1[1])
				p[i]=p1[0]
			else:
				d1.append('')
		global d
		d.append(d1)		
		global argtab
		argtab.append(p);
		for w in p:
			if w in l[4]:
				l[4] = str.replace(l[4],w,"?"+str(p.index(w)))
		line= ' '.join(l)
		
	namtab.append(l[1])
	deftab.write(line)
		

def expand(line):
	#print("in expand")
	
	global expanding
	expanding=True
	l= line.split()
	global e
	deftab.seek(0)
	e= list(deftab.readlines())
	global i
	i=0
	for i in range(0,len(e)):
		if l[0] in e[i]:
			break;
	proto= e[i].strip()
	pro= proto.split()
	#print(pro)
	#index= namtab.index(pro[1])
	global p
	p= line.split()
	if len(p)>1:
		p= p[1].split(',')
	else:
		p=[]
	if len(pro)>2:
		pro= pro[2].split(',')
	else:
		pro=[]
	global d1
	d1=[]
	for k in range(0,len(pro)):
		t= pro[k].split('=')
		if len(t)>1:
			d1.append(t[1])
		else:
			d1.append('')
	while True:	
		line=getline()
		#print(line)
		if line.strip()=="MEND":
			break
		processline(line)
	#deftab.close()
	expanding=False
	
def expandsingle(line):
	l= line.split()
	deftab.seek(0)
	global e
	e= list(deftab.readlines())
	j=0
	for j in range(0,len(e)):
		if l[0] in e[j]:
			break
	e[j]= e[j].split()
	if e[j][2].startswith("&"):
		p= e[j][2].split(',')
	else:
		p=[]
	if len(l)>1:
		l= l[1].split(',')
	for i in range(0,len(p)):
		st= "?"+str(i)
		if st in e[j][4]:
			if l[i]!='':
				e[j][4]= str.replace(e[j][4],st,l[i])
	if e[j][2].startswith("&"):
		line= e[j][3]+" "+e[j][4]+'\n'
	else:
		line= e[j][2]+" "+e[j][3]+'\n'
	output.write(line)
				
def condition(line):
	#print("IN condition")
	l= line.split()
	flag= False
	if l[3]=="EQ":
		if l[2]==l[4]:
			flag= True
	elif l[3]=="NE":
		if l[2]!= l[4]:
			flag= True
	elif l[3]=="GT":
		if int(l[2])> int(l[4]):
			flag= True
	elif l[3]=="LT":
		if int(l[2])< int(l[4]):
			flag= True
	elif l[3]== "GE":
		if int(l[2])>= int(l[4]):
			flag= True
	elif l[3]=="LE":
		if int(l[2])<= int(l[4]):
			flag= True
	if flag:
		line= getline()
		while not line.strip().startswith("ELSE") and not line.strip().startswith("ENDIF"):
			output.write(line)
			line= getline()
		while not line.strip().startswith("ENDIF"):
			line= getline()
	else:
		line= getline()
		while not line.strip().startswith("ELSE") and not line.strip().startswith("ENDIF"):
			line= getline()
		line= getline()
		while not line.strip().startswith("ENDIF"):
			output.write(line)
			line= getline()
	
def loop(line):
	l= line.split()
	x= int(l[2])
	y= int(l[4])
	j=-1
	while(True):	
		flag= False
		if l[3]=="EQ":
			if x==y:
				flag= True
		elif l[3]=="NE":
			if x!= y:
				flag= True
		elif l[3]=="GT":
			if x> y:
				flag= True
		elif l[3]=="LT":
			if x< y:
				flag= True
		elif l[3]== "GE":
			if x>= y:
				flag= True
		elif l[3]=="LE":
			if x<= y:
				flag= True
		if flag:
			j=j+1
			global i
			i= i-j
			print(j)
			j=0
			line= getline()
			while not line.strip().startswith("ENDW"):
				j=j+1
				print("loop body "+ line)
				if line.strip().startswith("INR"):
					x=x+1
				elif line.strip().startswith("DCR"):
					x=x-1
				else:
					output.write(line)
				line= getline()
		else:
			while not line.strip().startswith("ENDW"):
				line= getline()
			break
			
	
	
def processline(line):
	flag=0
	l= line.split()
	if len(l)==0:
		return
	#print(l)
	for i in range(0,len(namtab)):
		if l[0]==namtab[i]:
			flag=1
			break;
			
	if flag==1:
		if line.strip().startswith("@@"):
			expandsingle(line)
		else:
			expand(line)
	elif l[0]=="MBEGIN":
		define(line)
	elif l[0]=="DEFINE":
		definesingle(line)
	elif l[0]=="IF":
		condition(line)
	elif l[0]=="WHILE":
		loop(line)
	else:
		output.write(line)
		

while count<len(lines)-1:
	line=getline()
	#print(line)
	processline(line)
	
	
#deftab.truncate(0)	
print(namtab)
print(argtab)
print(d)
src.close()
output.close()

