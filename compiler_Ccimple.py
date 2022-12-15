#KONSTANTINOS MOUROUSIDIS 4114 cs04114
#ALEXANDROS NIKOLAOU 4126 cs04126

import sys
import string

f=open(sys.argv[1],"r")
code=open("test.int","w")

lineNo=1
x=f.read(1)

class Token:
	def __init__(self,tokenType,tokenString,lineNo):
		self.tokenType=tokenType
		self.tokenString=tokenString
		self.lineNo=lineNo

alphabet_string_lower=string.ascii_lowercase
alphabet_list_lower=list(alphabet_string_lower)
alphabet_string_upper=string.ascii_uppercase
alphabet_list_upper=list(alphabet_string_upper)
keyword_list=["program","declare","if","else","while","switchcase","forcase","incase","case","default","not","and","or","function","procedure","call","return","in","inout","input","print"]
number_list=["0","1","2","3","4","5","6","7","8","9"]
addOperator_list=["+","-"]
mulOperator_list=["*","/"]
groupSymbol_list=["{","}","[","]","(",")"]
delimeter_list=[",",";"]
rel_op = ["=","<=",">=","<",">","<>"]
id_function=""
function1=False
start=True
code_c=True
name=""
i=0
t=0
array=[]
variables=[]
list_x=[]



def lex():
	global x
	global lineNo
	while(x):
		while((x==" " or x=="\t" or x=="\n") and x):
			if(x=="\n"):
				lineNo+=1
			x=f.read(1)
		y=""

		if(x in alphabet_list_upper or x in alphabet_list_lower):
			while(x!=" " and x!="\t" and x!="\n" and x):
				if(x in alphabet_list_upper or x in alphabet_list_lower or x in number_list):
					y=y+x
					x=f.read(1)
					if(x=="\n"):
						lineNo+=1
				else:
					break
			if(len(y)>30):
				print("too many characters in identifier in line ",lineNo)
				t=Token("error",y,lineNo)
				if(x=="\n"):
					lineNo+=1	
				y=""
				return(t)
			elif(y in keyword_list):
				t=Token("keyword",y,lineNo)
				if(x=="\n"):
					lineNo+=1	
				y=""
				return(t)
			else:
				t=Token("identifier",y,lineNo)	
				if(x=="\n"):
					lineNo+=1	
				y=""
				return(t)
		
		if(x in number_list):
			validNo=True
			while(x!=" " and x!="\t" and x!="\n" and x):
				if(x in alphabet_list_upper or x in alphabet_list_lower or x in number_list):
					y=y+x
					x=f.read(1)
					if(x=="\n"):
						lineNo+=1
				else:
					break
			for c in y:
				if(c in alphabet_list_upper or c in alphabet_list_lower):
					validNo=False
			if(validNo):	
				t=Token("number",y,lineNo)
			elif(x=="\n"):
				lineNo+=1
			else:
				print("identifier must begin with letter in line ",lineNo)
				t=Token("error",y,lineNo)	
			return(t)

		if(x in addOperator_list):
			y=y+x
			t=Token("addOperator",y,lineNo)
			x=f.read(1)
			return(t)

		if(x in mulOperator_list):
			t=Token("mulOperator",x,lineNo)
			x=f.read(1)
			return(t)

		if(x in groupSymbol_list):
			t=Token("groupSymbol_list",x,lineNo)
			x=f.read(1)
			if(x=="\n"):
					lineNo+=1
			return(t)

		if(x in delimeter_list):
			t=Token("delimeter_list",x,lineNo)
			x=f.read(1)
			return(t)

		if(x=="."):
			t=Token("EndOfProgram",".",lineNo)
			return(t)

		if(x==":"):
			y=y+x
			x=f.read(1)
			if(x=="="):
				y=y+x
				t=Token("assignment",y,lineNo)
				x=f.read(1)
			else:
				print("after ':' you must write '=' in line ",lineNo)
			if(x=="\n"):
				lineNo+=1
			return(t)
		#smaller
		if(x=="<"):
			y=y+x
			x=f.read(1)
			if(x==">" or x=="="):
				y=y+x
				t=Token("relOperator",y,lineNo)
				x=f.read(1)
				return(t)
			elif(x in alphabet_list_upper or x in alphabet_list_lower or x in number_list or x==" "):
				t=Token("relOperator",y,lineNo)
				return(t)
			else:
				print("after '<' we must have >,=,number,letter in line ",lineNo)
			
		#equals
		if(x=="="):
			t=Token("relOperator",x,lineNo)
			x=f.read(1)
			return(t)
		#larger
		if(x==">"):
			y=y+x
			x=f.read(1)
			if(x=="="):
				y=y+x
				t=Token("relOperator",y,lineNo)
				x=f.read(1)
				return(t)
			elif(x in alphabet_list_upper or x in alphabet_list_lower or x in number_list or x==" "):
				t=Token("relOperator",y,lineNo)
				return(t)
			else:
				print("after '>' we must have =,number,letter in line ",lineNo)

		#comments
		if(x=="#"):
			x=f.read(1)
			while(x!="#"):
				if(x=="\n"):
					lineNo+=1
				elif(x is None):
					print("# was expected")
					break
				x=f.read(1)
			x=f.read(1)
			return lex()


def program():
	global token
	global name
	token=lex()
	if(token.tokenString=="program"):
		ID()
		name = token.tokenString
		block(name)
		genquad("halt","_","_","_")
		genquad("end_block",name,"_","_")
		if(token.tokenString!="."):
			print("The keyword '.' was expected in line ",token.lineNo,token.tokenString)
	else:
		print("The keyword 'program' was expected in line ",token.lineNo)

def block(name):
	global token
	global function1
	global start
	global code_c
	token=lex()
	if(token.tokenString=="declare"):
		declarations() 
	elif(token.tokenString=="function" or token.tokenString=="procedure"):
		if(function1==True):
			genquad("end_block",id_function,"_","_")
		function1=True
		code_c=False
		subprograms()
	else:
		if(function1==True):
			genquad("end_block",id_function,"_","_")
			function1=False
		if(start==True):
			genquad("begin_block",name,"_","_")
			start=False
		statements()


def declarations():
	global token
	varlist()
	if(token.tokenString!=";"):
		print("The keyword ';' was expected in line ",token.lineNo)
	else:
		block(name)

def subprograms():
	global token 
	subprogram()

def varlist():
	ID()
	global token
	token=lex()
	if(token.tokenString==","):
		varlist()

def subprogram():
	global token
	if(token.tokenString=="function"):
		function()
	elif(token.tokenString=="procedure"):
		procedure()

def procedure():
		ID()
		global token 
		global function
		global id_function
		id_function = token.tokenString
		genquad("begin_block",id_function,"_","_")
		token=lex()
		if(token.tokenString=="("):
			formalparlist()
			if(token.tokenString==")"):
				token=lex()
				statements()
			else:
				print("After in or inout we must have only identifier in line ",token.lineNo)

def function():
		ID()
		global function
		global token
		global id_function
		id_function = token.tokenString
		genquad("begin_block",id_function,"_","_") 
		token=lex()
		if(token.tokenString=="("):
			formalparlist()
			if(token.tokenString==")"):
				token=lex()
				statements()
			else:
				print("After in or inout we must have only identifier in line ",token.lineNo)

def formalparlist():
	formalparitem()
	global token 
	token=lex()
	while(token.tokenString==","):
		formalparitem()
		token=lex()


def formalparitem():
	token=lex()
	if(token.tokenString=="in"):
		ID()
	elif(token.tokenString=="inout"):
		ID()
	else:
		print("The keyword 'in' or 'inout' was expected in line ",token.lineNo)

def statements():
	global token 
	if(token.tokenType=="keyword" or token.tokenType=="identifier"):
		statement()
	elif(token.tokenString=="{"):
		while(token.tokenString!="}"):
			statement()
			while(token.tokenString==";"):
				statement()
		block(name)

def statement():
	global token 
	global e
	token=lex()
	if(token.tokenType=="identifier"):
		id2 = token.tokenString
		assignStat()
		genquad(":=",e,"_",id2)
	elif(token.tokenString=="while"):
		whileStat()
	elif(token.tokenString=="if"):
		ifStat()
	elif(token.tokenString=="switchcase"):
		switchcaseStat()
		token=lex()
	elif(token.tokenString=="forcase"):	
		forcaseStat()
		token=lex()
	elif(token.tokenString=="incase"):
		incaseStat()
	elif(token.tokenString=="call"):
		callStat()
		token=lex()
	elif(token.tokenString=="return"):
		returnStat()
		genquad("retv",e,"_","_")
		token=lex()
	elif(token.tokenString=="input"):
		inputStat()
		genquad("inp",id1,"_","_")
		token=lex()
	elif(token.tokenString=="print"):
		printStat()
		genquad("out",e,"_","_")
		token=lex()

def assignStat():
	global token 
	token=lex()
	if(token.tokenString==":="):
		expression()
		if(token.tokenString!=";"):
			print("The keyword ';' was expected in line ",token.lineNo)
	else:
		print("The keyword ':=' was expected in line ",token.lineNo)

def ifStat():
	global token
	global if_list
	token=lex()
	if(token.tokenString=="("):
		condition()
		if(token.tokenString!=")"):
			print("The keyword ')' was expected in line ",token.lineNo)
	else:
		print("error")

	backpatch(b_true,nextquad())

	statement()

	if_list = makelist(nextquad())
	#genquad("jump","_","_","_")
	backpatch(b_false,nextquad())
	k = 0
	for y in array:
		k += 1
		if(b_false[3]+": " in y):
			array.remove(y)
			array.insert(k-1,(b_false[3]+": "+"jump"+" "+"_"+" "+"_"+" "+str(i)))
	elsepart()

def elsepart():
	statements()
	backpatch(if_list,nextquad())

def whileStat():
	global token 
	b_quad = i
	token=lex()
	if(token.tokenString=="("):
		condition()
		if(token.tokenString!=")"):
			print("The keyword ')' was expected in line ",token.lineNo)
	else:
		print("after while we must have '(' in line ",token.lineNo)
	token=lex()
	backpatch(b_true,nextquad())
	statements()
	genquad("jump","_","_",str(b_quad))
	backpatch(b_false,nextquad())
	k = 0
	for y in array:
		k += 1
		if(b_false[3]+": " in y):
			array.remove(y)
			array.insert(k-1,(b_false[3]+": "+"jump"+" "+"_"+" "+"_"+" "+str(i)))

def switchcaseStat():
	global token
	global b_true
	global b_false
	exitlist = emptylist()
	while(1):
		token=lex()
		if(token.tokenString=="("):
			token=lex()
			if(token.tokenString=="case"):
				token=lex()
				if(token.tokenString=="("):
					condition()
					if(token.tokenString!=")"):
						print("The keyword ')' was expected in line ",token.lineNo)
						break
					backpatch(b_true,nextquad())
					statement()
					sw = makelist(nextquad())
					genquad("jump","_","_","_")
					mergelist(exitlist,sw)
					backpatch(b_false,nextquad())
					k = 0
					for y in array:
						k += 1
						if(b_false[3]+": " in y):
							array.remove(y)
							array.insert(k-1,(b_false[3]+": "+"jump"+" "+"_"+" "+"_"+" "+str(i)))
				else:
					print("The keyword '(' was expected in line ",token.lineNo)
					break
		elif(token.tokenString=="default"):
			break

	statements()
	exitlist = makelist(i)
	backpatch(exitlist,nextquad())
	k = 0
	for y in array:
		k += 1
		if(sw[3]+": " in y):
			array.remove(y)
			array.insert(k-1,(sw[3]+": "+"jump"+" "+"_"+" "+"_"+" "+exitlist[3]))

def forcaseStat():
	global token
	global b_true
	global b_false
	
	while(1):
		p_quad = i
		token=lex()
		if(token.tokenString=="("):
			token=lex()
			if(token.tokenString=="case"):
				token=lex()
				if(token.tokenString=="("):
					condition()
					if(token.tokenString!=")"):
						print("The keyword ')' was expected in line ",token.lineNo)
						break
					backpatch(b_true,nextquad())
					statement()
					genquad("jump","_","_",str(p_quad))
					backpatch(b_false,nextquad())
					k = 0
					for y in array:
						k += 1
						if(b_false[3]+": " in y):
							array.remove(y)
							array.insert(k-1,(b_false[3]+": "+"jump"+" "+"_"+" "+"_"+" "+str(i)))
				else:
					print("The keyword '(' was expected in line ",token.lineNo)
					break
		elif(token.tokenString=="default"):
			break

	statements()

def incaseStat():
	global token 
	w = newtemp()
	in_quad = i
	genquad(":=",1,"_",w) 
	while(1):
		token=lex()
		if(token.tokenString=="("):
			token=lex()
		elif(token.tokenString=="case"):
			token=lex()
			if(token.tokenString=="("):
				condition()
				if(token.tokenString!=")"):
					print("The keyword ')' was expected in line ",token.lineNo)
					break
				backpatch(r_true,nextquad())
				genquad(":=",0,"_",w)
				statements()
				backpatch(r_false,nextquad())
			else:
				print("The keyword '(' was expected in line ",token.lineNo)
				break
	genquad("=",w,0,in_quad)

def returnStat():
	global token 
	token=lex()
	if(token.tokenString=="("):
		expression()
		if(token.tokenString!=")"):
			print("The keyword ')' was expected in line ",token.lineNo)
	else:
		print("The keyword '(' was expected in line ",token.lineNo)

def callStat():
	global token
	ID()
	id_call = id1
	token=lex()
	if(token.tokenString=="("):
		actualparlist()
		if(token.tokenString!=")"):
			print("The keyword ')' was expected in line ",token.lineNo)
	else:
		print("The keyword '(' was expected in line ",token.lineNo)
	genquad("call",id_call,"_","_")

def printStat():
	global token
	token=lex()
	if(token.tokenString=="("):
		expression()
		if(token.tokenString!=")"):
			print("The keyword ')' was expected in line ",token.lineNo)
	else:
		print("The keyword '(' was expected in line ",token.lineNo)

def inputStat():
	token=lex()
	if(token.tokenString=="("):
		ID()
		token=lex()
		if(token.tokenString!=")"):
			print("The keyword ')' was expected in line ",token.lineNo)
	else:
		print("The keyword '(' was expected in line ",token.lineNo)

def actualparlist():
	actualparitem()
	global token 
	while(token.tokenString==","):
		actualparitem()
		token=lex()

def actualparitem():
	global token 
	global e
	token=lex()
	if(token.tokenString=="in"):
		expression()
		genquad("par",e,"CV","_")
	elif(token.tokenString=="inout"):
		ID()
		genquad("par",id1,"REF","_")
		token=lex()
		if(token.tokenString!=")"):
			print("After inout we must have only identifier in line ",token.lineNo)
	else:
		print("The keyword 'in' or 'inout' was expected in line ",token.lineNo)

def condition():
	global token
	global b_true
	global b_false 
	boolterm()
	b_true = q_true
	b_false = q_false
	while(token.tokenString=="or"):
		backpatch(b_false,nextquad())
		boolterm()
		b_true = mergelist(b_true,q_true)
		b_false = q_false

def boolterm():
	global token
	global q_true
	global q_false
	boolfactor()
	q_true = r_true
	q_false = r_false
	while(token.tokenString=="and"):
		backpatch(q_true,nextquad())
		boolfactor()
		q_false = mergelist(q_false,r_false)
		q_true = r_true

def boolfactor():
	global token
	global r_true
	global r_false
	expression()
	e1 = e
	if(token.tokenString in rel_op):
		rel = token.tokenString
		expression()
		e2 = e 
		genquad(rel,e1,e2,str(i+2))
		r_true = makelist(nextquad())
		r_false = makelist(i)
		genquad("jump","_","_","_")
	elif(token.tokenString=="not"):
		token=lex()
		if(token.tokenString=="["):
			condition()
			r_true = b_true
			r_false = b_false
			if(token.tokenString!="]"):
				print("The keyword ']' was expected in line ",token.lineNo)
		else:
			print("The keyword '[' was expected in line ",token.lineNo)
	elif(token.tokenString=="["):
		condition()
		r_true = b_true
		r_false = b_false
		if(token.tokenString!="]"):
			print("The keyword ']' was expected in line ",token.lineNo)
		
def expression():
	global token
	global t1
	global e
	global t2
	token=lex()
	if (token.tokenString not in groupSymbol_list and token.tokenString not in delimeter_list):
		t1 = token.tokenString
	term()
	while(token.tokenString in addOperator_list):
		addOperator = token.tokenString
		token=lex()
		t2 = token.tokenString
		if(t2==id_function):
			function_id()
		w = newtemp()
		genquad(addOperator,t1,t2,w)
		t1 = w
		term()
	e = t1


def term():
	global t1
	global f1
	global f2
	f1 = t1 
	factor()
	global token 
	while(token.tokenString in mulOperator_list):
		mulOperator = token.tokenString
		token=lex()
		f2 = token.tokenString
		if(f2==id_function):
			function_id()
		w = newtemp()
		genquad(mulOperator,f1,f2,w)
		f1 = w
		t1 = w
		factor()
	t1 = f1


def factor():
	global token
	global e 
	global f1
	global t1
	if(token.tokenType=="number"):
		e = t1
		expression()
	elif(token.tokenString=="("):
		expression()
		if(token.tokenString!=")"):
			print("The keyword ')' was expected in line ",token.lineNo)
	elif(token.tokenType=="identifier"):
		if(token.tokenString==id_function):
			function_id()
		else:	
			idtail()

def function_id():
	global token
	global f1
	global t2
	global f2
	token=lex()
	if(token.tokenString=="("):
		actualparlist()
		w = newtemp()
		genquad("par",w,"RET","_")
		genquad("call",id_function,"_","_")
		f1 = w
		t2 = w
		f2 = w
		if(token.tokenString!=")"):
			print("The keyword ')' was expected in line ",token.lineNo)
		token=lex()

def idtail():
	global token
	global id1
	global f1
	id1 = token.tokenString
	token=lex()
	if(token.tokenString=="("):
		actualparlist()
		w = newtemp()
		genquad("par",w,"RET","_")
		genquad("call",id1,"_","_")
		f1 = w
		if(token.tokenString!=")"):
			print("The keyword ')' was expected in line ",token.lineNo)
		else:
			expression()

def ID():
	global token
	global id1
	token=lex()
	id1 = token.tokenString
	if(token.tokenType!="identifier"):
		print("An identifier was expected in line ",token.lineNo)



def genquad(op,x,y,z):
	global i
	array.append(str(i)+": "+op+" "+x+" "+y+" "+z)
	i += 1

def nextquad():
	global i
	line=i
	line += 1
	return(line)

def newtemp():
	global t
	T_i="T_"+str(t)
	t += 1
	return(T_i)

def emptylist():
	global array1 
	array1=[]
	return(array1)

def makelist(x):
	list_x = ["_","_","_",str(x)]
	return(list_x)

def mergelist(list1,list2):
	global list_12
	list_12 = list1+list2

def backpatch(list1,z):
	list1 = ["_","_","_",str(z)] 

def printArray():
	for i in array:
		print(i+"\n")

def transfer():
	for i in array:
		code.write(i+"\n")

def convert_c():
	global variables
	global code_c
	var_str = ""
	if(code_c==True):
		c=open("test.c","w")
		c.write("int main()"+"\n")
		c.write("{"+"\n")
		for l in array:
			num = l.split(": ",1)
			opxyz = num[1].split(" ")
			if not opxyz[1].isdigit() and opxyz[1]!=name and opxyz[1]!="_":
				variables.append(opxyz[1])
			elif not opxyz[2].isdigit() and opxyz[2]!=name and opxyz[2]!="_":
				variables.append(opxyz[2])
			elif not opxyz[3].isdigit() and opxyz[3]!=name and opxyz[3]!="_":
				variables.append(opxyz[3])

		variables = set(variables)
		for l in variables:
			var_str=var_str+l+","
		var_str = var_str[:-1]

		c.write("\t"+"int "+var_str+";"+"\n")

		for l in array:
			num = l.split(": ",1)
			opxyz = num[1].split(" ")
			if(opxyz[0]==":="):
				c.write("\t"+"L_"+num[0]+": "+opxyz[3]+"="+opxyz[1]+"; //("+opxyz[0]+","+opxyz[1]+","+opxyz[2]+","+opxyz[3]+")"+"\n")
			elif(opxyz[0]=="+"):
				c.write("\t"+"L_"+num[0]+": "+opxyz[3]+"="+opxyz[1]+"+"+opxyz[2]+"; //("+opxyz[0]+","+opxyz[1]+","+opxyz[2]+","+opxyz[3]+")"+"\n")
			elif(opxyz[0]=="-"):
				c.write("\t"+"L_"+num[0]+": "+opxyz[3]+"="+opxyz[1]+"-"+opxyz[2]+"; //("+opxyz[0]+","+opxyz[1]+","+opxyz[2]+","+opxyz[3]+")"+"\n")
			elif(opxyz[0]=="*"):
				c.write("\t"+"L_"+num[0]+": "+opxyz[3]+"="+opxyz[1]+"*"+opxyz[2]+"; //("+opxyz[0]+","+opxyz[1]+","+opxyz[2]+","+opxyz[3]+")"+"\n")
			elif(opxyz[0]=="/"):
				c.write("\t"+"L_"+num[0]+": "+opxyz[3]+"="+opxyz[1]+"/"+opxyz[2]+"; //("+opxyz[0]+","+opxyz[1]+","+opxyz[2]+","+opxyz[3]+")"+"\n")
			elif(opxyz[0] in rel_op):
				c.write("\t"+"L_"+num[0]+": if ("+opxyz[1]+opxyz[0]+opxyz[2]+") goto L_"+opxyz[3]+"; //("+opxyz[0]+","+opxyz[1]+","+opxyz[2]+","+opxyz[3]+")"+"\n")
			elif(opxyz[0]=="jump"):
				c.write("\t"+"L_"+num[0]+": goto L_"+opxyz[3]+"; //("+opxyz[0]+","+opxyz[1]+","+opxyz[2]+","+opxyz[3]+")"+"\n")
			elif(opxyz[0]=="inp"):
				c.write("\t"+"L_"+num[0]+": scanf(\"%d\", &"+opxyz[1]+")"+"; //("+opxyz[0]+","+opxyz[1]+","+opxyz[2]+","+opxyz[3]+")"+"\n")				
			elif(opxyz[0]=="out"):
				c.write("\t"+"L_"+num[0]+": printf(\"%d\", "+opxyz[1]+")"+"; //("+opxyz[0]+","+opxyz[1]+","+opxyz[2]+","+opxyz[3]+")"+"\n")								
		c.write("}"+"\n")

def telikos():
	global code_c

	if(code_c==True):
		c=open("test.c","r")
		ass=open("test.asm","w")
		jumps=""
		op=""
		num_fp=0
		num_i=0

		for l in array:
			num = l.split(": ",1)
			opxyz = num[1].split(" ")
			if(opxyz[0]=="jump"):
				ass.write("L"+num[0]+"\t"+"b "+opxyz[3]+"\n")
			elif(opxyz[0] in rel_op):
				if(opxyz[0]=="="):
					jumps="beq"
				elif(opxyz[0]=="<"):
					jumps="blt"
				elif(opxyz[0]==">"):
					jumps="bgt"
				elif(opxyz[0]=="<="):
					jumps="ble"
				elif(opxyz[0]==">="):
					jumps="bge"
				elif(opxyz[0]=="<>"):
					jumps="bne"
				ass.write("L"+num[0]+"\t"+"loadvr("+opxyz[1]+",$t1)"+"\n")
				ass.write("\t"+"loadvr("+opxyz[2]+",$t2)"+"\n")
				ass.write("\t"+jumps+" $t1,$t2,"+opxyz[3]+"\n")
			elif(opxyz[0]==":="):
				ass.write("L"+num[0]+"\t"+"loadvr("+opxyz[1]+",$t1)"+"\n")
				ass.write("\t"+"storerv($t1,"+opxyz[3]+")"+"\n")
			elif(opxyz[0] in addOperator_list or opxyz[0] in mulOperator_list):
				if(opxyz[0]=="+"):
					op="add"
				elif(opxyz[0]=="-"):
					op="sub"
				elif(opxyz[0]=="*"):
					op="mul"
				elif(opxyz[0]=="/"):
					op="div"
				ass.write("L"+num[0]+"\t"+"loadvr("+opxyz[1]+",$t1)"+"\n")
				ass.write("\t"+"loadvr("+opxyz[2]+",$t2)"+"\n")
				ass.write("\t"+op+" $t1,$t1,$t2"+"\n")
				ass.write("\t"+"storerv($t1,"+opxyz[3]+")"+"\n")
			elif(opxyz[0]=="out"):
				ass.write("L"+num[0]+"\t"+"li $v0,1"+"\n")
				ass.write("\t"+"loadvr("+opxyz[1]+",$a0)"+"\n")
				ass.write("\t"+"syscall"+"\n")
			elif(opxyz[0]=="in"):
				ass.write("L"+num[0]+"\t"+"li $v0,5"+"\n")				
				ass.write("\t"+"syscall"+"\n")
				ass.write("\t"+"store($v0,"+opxyz[1]+")"+"\n")
			elif(opxyz[0]=="retv"):
				ass.write("L"+num[0]+"\t"+"loadvr("+opxyz[1]+",$t1)"+"\n")
				ass.write("\t"+"lw $t0,-8($sp)"+"\n")
				ass.write("\t"+"sw $t1,($t0)"+"\n")
			elif(opxyz[0]=="begin_block"):
				if(opxyz[1]!=name):
					ass.write("L"+num[0]+"\t"+"sw $ra,-0($sp)"+"\n")
				else:
					ass.write("L"+num[0]+"\t"+"j "+name+"\n")
					ass.write("\t"+"addi $sp,$sp,"+str(num_fp)+"\n")
					ass.write("\t"+"move $s0,$sp"+"\n")
			elif(opxyz[0]=="end_block"):
				if(opxyz[1]!=name):
					ass.write("L"+num[0]+"\t"+"lw $ra,-0($sp)"+"\n")
					ass.write("\t"+"jr $ra"+"\n")
				else:
					ass.write("L"+num[0]+"\t"+"addi $sp,$sp,"+str(num_fp)+"\n")
					ass.write("\t"+"move $s0,$sp"+"\n")				
			elif(opxyz[0]=="par"):
				if(opxyz[2]=="CV"):
					ass.write("L"+num[0]+"\t"+"loadvr("+opxyz[1]+",$t0)"+"\n")
					ass.write("\t"+"sw $t0,-"+str(12+4*num_i)+"($fp)"+"\n")
					num_i = num_i + 1
				elif(opxyz[2]=="REF"):
					ass.write("L"+num[0]+"\t"+"addi $t0,$sp,-"+str(12+4*num_i)+"\n")
					ass.write("\t"+"sw $t0,"+str(-(12+4*num_i))+"($fp)"+"\n")
					num_i = num_i + 1
				elif(opxyz[2]=="RET"):
					ass.write("L"+num[0]+"\t"+"addi $t0,$sp,-"+str(12+4*num_i)+"\n")
					ass.write("\t"+"sw $t0,-8($fp)"+"\n")
					num_i = num_i + 1
			elif(opxyz[0]=="call"):
				ass.write("L"+num[0]+"\t"+"lw $t0,-4($fp)"+"\n")
				ass.write("\t"+"sw $t0,-4($fp)"+"\n")
				ass.write("\t"+"addi $sp,$sp,"+str(12+4*num_i)+"\n")
				ass.write("\t"+"jal "+opxyz[2]+"\n")
				ass.write("\t"+"addi $sp,$sp,-"+str(12+4*num_i)+"\n")



program()
#printArray()
transfer()
convert_c()
telikos()
