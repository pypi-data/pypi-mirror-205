def yacc():
    s="""
    %{
    #include<math.h>
    #include<stdio.h>
    #include<ctype.h>
    #define YYSTYPE double
%}

%%

input:|input line ;

line: '\n' | expr'\n' {printf("Result is %g", $1);} ;

expr: expr '+' term {$$ = $1 + $3;}
    | expr '-' term {$$ = $1 - $3;}
    | term {$$ = $1;} ;

term: term '*' factor {$$ = $1*$3;}
    | term '/' factor {$$ = $1/$3;}
    | factor {$$ = $1;} ;

factor: NUM {$$ = $1;} ;

NUM: digit {$$ = $1;} ;

digit: '0' {$$ = 0;}
    |'1' {$$ = 1;} 
    |'2' {$$ = 2;} 
    |'3' {$$ = 3;} 
    |'4' {$$ = 4;} 
    |'5' {$$ = 5;} 
    |'6' {$$ = 6;} 
    |'7' {$$ = 7;} 
    |'8' {$$ = 8;} 
    |'9' {$$ = 9;} ;

%%

int yylex(){
    return getchar();}

int main(){
    return yyparse();}

void yyerror(char*s){
    printf("%s",s); }
    """
    print(s)

def sic():
    s="""
    program = open("input.txt", "r").read()
program=program.split('\n')
op=open("opcode.txt", "r").read().split('\n')
sym=open("symtab.txt", "r").read().split('\n')
opcode={}
symtab={}
for i in op:
    temp=i.split(' ')
    opcode[temp[0]]=[temp[1]]
for i in sym:
    temp=i.split(' ')
    symtab[temp[0]]=[temp[1]]
line1=program[0].split(' ')
start=0
program_name=line1[0]
objcode=[]
for i in range(len(line1)):
    if line1[i]=='START':
        start=line1[i+1]
        program_name=line1[i-1]
print("H^",program_name,"^",start,"^",hex((len(program)-3)*3)[2:])
for i in program[1:]:
    lines=i.split()
    for j in range(len(lines)):
        if lines[j] in opcode.keys():
            if lines[j+1] in symtab.keys():
                objcode.append(opcode[lines[j]]+symtab[lines[j+1]])
                continue
print("T^",start,"^",hex(len(objcode)*3)[2:],end='')
for i in objcode:
    print("^",''.join(i),end='');
print()
print("E^",start)

----------------input.txt
    COPY START 1000
LDA ALPHA
STA BETA
LDA GAMMA
ALPHA RESW 1
BETA RESW 1
GAMMA RESW 1
----------------opcode.txt
STA 23
LDA 00
----------------symtab.txt
ALPHA 1006
BETA 1009
GAMMA 100C
    """
    print(s)

def predictive_parser():
    s="""
    table = open("table.txt","r").read()
table = table.split("\n")
T = {'E':0,'S':1,'T':2,'R':3,'F':4}
NT = {'i':0,'+':1,'*':2,'(':3,')':4,'$':5}

p_table = []
for i in table:
    p_table.append(i.split())

#s=i+i*i$
s = input("Enter the input String:")
stack = '$E'
print("\nSTACK","\tINPUT","\t\tOUTPUT")
print(stack,"\t",s)
while(stack[-1]!=s[-1]):

    if stack[-1]==s[0]: #If String 'e' is same as top of stack
        stack = stack[:-1] #Pop same terminals
        s=s[1:]

        print(stack,'\t',s)

    pos = p_table[T[stack[-1]]][NT[s[0]]]
    t = pos[3:]
    stack = stack[:-1]+t[::-1]
    print(stack,'\t',s,'\t\t',pos)

if(stack=='$' and s=='$'):
    print("The String is Parsed Successfully")

    -------------------table.txt
    E->TS - - E->TS - -
- S->+TS - - S-> S->
T->FR - - T->FR - -
- R-> R->*FR - R-> R->
F->i - - F->F(E) - -
    """
    print(s)

def token_separation():
    s="""
    import re

#Taking in Input and store as array
a = open('sample.txt','r')
text = a.read()

key =['if','else','elif','for','while','break','continue','in','range','int','float','char']
id = re.findall("[a-zA-Z0-9$_]",text)
punctuations= [',',"'",'"',".",";",":"]
operators = ['+','-','*','/','=','>','<','<=','>=','==','(',')']

c1, c2 = 0, 0

for l in text.split("\n"):
    print(l)
    for t in l.split():
        if t in key:
            print(t+"-> Keyword")
            c1 +=1
        elif t in id and t not in re.findall("[0-9]",text):
            print(t+"-> Identifier")
            c2+=1
        elif t in punctuations:
            print(t+"->Punctuation")
        elif t in operators:
            print(t+"-> Operators")
    print("\n")

print("Count of keywords: ",c1)
print("Count of identifiers: ",c2)
-----------input - sample.txt
int x ;
list k ;
for i in k :
int x = 10 ;
    """
    print(s)

def sybbol_table():
    s="""
    d_types = ['char','const','double','enum','float','int','long','short','signed',
           'static','unsigned','void'] #PUT AS MANY AS REQUIRED
keywords = ['auto','break','case','char','const','continue','default','do','double',
            'else','enum','extern','float','for','goto','if','int','long','register',
            'return','short','signed','sizeof','static','struct','switch','typedef',
            'union','unsigned','void','volatile','while'] #PUT AS MANY AS REQUIRED

id_key, id_var, id_val = [],[],[]
r_type, num_params, type_params = [],[],[]

a = open('sample.txt','r')
text = a.read()
#print(text)

def l_append(var,val,key,return_type='-', no_params='-',params_type ='-' ):
    id_var.append(var)
    id_val.append(val)
    id_key.append(key)
    r_type.append(return_type)
    num_params.append(no_params)
    type_params.append(params_type)


for l in text.split("\n")[:-1]:
    g = l.split()
    if ';' in g: g.remove(';')
    while (',' in g): g.remove(',')
    print("\nl:",g)
    
    for j in g: #For each token in g (list of each line)
        if j == "=":           #(KEYWORD VARIABLES) WITH VALUES Ex: int b = 5
            print("kvvtemp: ",g)
            vr = g.index(j) - 1
            vl = g.index(j) + 1
            vk = 0
            l_append(g[vr],g[vl],g[vk]) # Ex: int b = 5
            del g[vr:vr+3]
            print("c1",g)

    if ('(' not in g) and len(g)>1: #(KEYWORD VARIABLES) WITHOUT VALUES Ex: int a  
        for i in range(1,len(g)): #0th index contains keyword
            #print(temp[i],0,temp[0])
            l_append(g[i],0,g[0]) # var, val, key

    #FUNCTIONS AND ARGUEMENTS
    if '(' in g:     
        d_end, v_end = [], []
        return_type, var = g[0], g[1]
        del g[0:2]
        
        for i in range(1,len(g)-1): #['(', 'double', 'x', 'double', 'y', ')']
            if g[i] in d_types:
                d_end.append(g[i])
                v_end.append(g[i+1])
            type_par = [d_end,v_end]
        
        l_append(var,'-','-',return_type, (len(g)-2)//2, type_par)  
        print("c2",g)

#PRINT OUT THE SYMBOL TABLE
print ("\nThe symbol table for the C code is: \n")
print ("ID",'\t',"Data Type",'\t',"Return Type",'\t',"InitialValue",
       '\t','\t',"No. of Parameters",'\t',"Type of Parameters")
print("-----",'\t',"---------",'\t',"---------",'\t',"---------",
      "\t\t","---------",'\t\t',"---------",'\n')   

for i in range(0,len(id_key)):
    print(id_key[i],"\t",id_key[i],"\t\t",r_type[i],"\t\t",id_val[i],"\t\t\t",num_params[i],"\t\t\t",type_params[i],"\n")
    ---------input - sample.txt
    int a , b = 5 ;
char c = 'd' ;
double Add ( double x , double y ) ;
    """
    print(s)

def macro_processor():
    s="""
    macros = dict()

f = open("Code.cpp") #Opening the file

for i in f.readlines():
    l = i.split()
    if l[0] == '#define': #Define the Macros
        macros[l[1]] = l[2]

output = []
f.seek(0) # Bring Input pointer back to 0

for i in f.readlines():
    l = i.split()
    if l[0] == '#define': #Ignore the defination lines in code
        continue
    for j in range(len(l)): #Replacing macros in each line
        if l[j] in macros.keys():
            l[j] = macros[l[j]]
    output.append(l) #append each line to output list

print("Macros\t\tDeinition") #Display macros and definations
for m,n in macros.items():
    print(m + "\t\t" + n)

print("\nExpanded code") #Print the output 2D array of lines
for x in output:
    for y in x: 
        print(y, end = " ")
    print()
    -------input - Code.cpp
    #include <stdio.h>
#define PI 3.14
#define AREA(a) (a*a)
int main() {
float r, area;
printf("Enter radius: ");
scanf("%f", &r);
printf("Area: %0.2f", PI * AREA(r) );
return 0;
}
    """
    print(s)

def lex():
    s="""
    %{
int i=0;
%}
%%
[a-zA-Z]*[ ][a-zA-Z]* {i++;}
%%
int yywrap(void){}
int main(){
yyin=fopen("input.txt","r");
yylex();
printf("no of words: %d",i+1);
}
----------input
seg th td yj y
    """
    print(s)

def dfa():
    s="""
    states = input("Enter the states (space-seperated): ").strip().split(" ")
alphabets = input("Enter the alphabets (space-seperated): ").strip().split(" ")
start_state = input("Enter the start state: ").strip()
Final_States = input("Enter the final states (space-seperated): ").strip().split(" ")
transition_function = eval(input("Enter the transition table: "))

curr_state = start_state
walk=""
inp_string = list(input("Enter the input string: (\'#\' for EOF): ").strip())

for i in inp_string:
    if i=="#":
        if curr_state in Final_States:
            print("\nYes")
            break
        else: print("\nNo")
        break
    else:
        curr_state=transition_function[curr_state][i]
        walk+=curr_state+" -> "
        
print("Walk:", start_state+" -> "+walk[:-4])
-----------input
A B C D
a b
A
D
{"A":{"a":"B","b":"A"},"B":{"a":"B","b":"C"},"C":{"a":"B","b":"D"},"D":{"a":"B","b":"A"}}
    """
    print(s)

def loader():
    s="""
    lines = open("input.txt","r").read().split('\n')
obcode =[]
for line in lines:
    obcode.append(line.split('^'))
print(obcode)

print("Name of Program: ",obcode[0][1])

for l in obcode[1:]:
    if l[0]=='E': break
    addr = int(l[1])
    for item in l[3:]:
        print(addr,item[0:2])
        addr +=1
        print(addr,item[2:4])
        addr +=1
        print(addr,item[4:6])
        addr +=1
    print('\n')
    ----------input.txt
    H^SAMPLE^001000^0035
T^001000^0C^001003^071009
T^002000^03^111111
E^001000
    """
    print(s)

def intermediate():
    s="""
    exp=input().split()
prec=['*','/','+','-']
flag=1
t=1

for i in range(len(prec)):
    for j in range(len(exp)):
        if(flag==1 and exp[j]==prec[i]):
            print("t"+str(t)+" = "+exp[j-1]+exp[j]+exp[j+1])
            flag=0
            t+=1
        elif(exp[j]==prec[i]):
            print("t"+str(t)+"= t"+str(t-1)+exp[j]+exp[j+1])
            t+=1
            ---------------input
            a*b+c/d
    """
    print(s)