print("""
 ########### Expt 4 Lexical Analysis using Python 
 
 import re

# Define the grammar using regular expressions
grammar = [
    ("IDENTIFIER", r"[a-zA-Z_][a-zA-Z0-9_]*"),
    ("NUMBER", r"\d+(\.\d+)?"),
    ("OPERATOR", r"[\+\-\*/]"),
    ("LEFT_PAREN", r"\("),
    ("RIGHT_PAREN", r"\)"),
    ("ASSIGNMENT", r"\="),
]

# Define the function to perform lexical analysis
def lex(input_string):
    tokens = []
    while input_string:
        match = None
        for token_type, pattern in grammar:
            regex = re.compile(pattern)
            match = regex.match(input_string)
            if match:
                value = match.group(0)
                tokens.append((token_type, value))
                input_string = input_string[len(value):].lstrip()
                break
        if not match:
            raise ValueError(f"Invalid input: {input_string}")
    return tokens

# Test the function with an example input string
input_string = input('Input String: ')
tokens = lex(input_string)
print(tokens)



######### All Lex Codes ###########

### File Name :   vowel.l    : 
%{
	int vow_count=0;
	int const_count =0;
%}

%%
[aeiouAEIOU] {vow_count++;}
[a-zA-Z] {const_count++;}
%%
int yywrap(){}
int main()
{
	printf("Enter the string of vowels and consonants: ");
	yylex();
	printf("Number of vowels are: %d\n", vow_count);
	printf("Number of consonants are: %d\n", const_count);
	return 0;
}




########### File Name :   prime.l : 
%{
#include<stdio.h>
#include<stdlib.h>
int flag,c,j;
%}

%%
[0-9]+ {c=atoi(yytext);
		if(c==2){
		    printf("Prime number\n");
		}else if(c==0 || c==1){
		    printf("Not a Prime number\n");
		}else{
		    for(j=2;j<c;j++){
		        if(c%j==0)
		            flag=1;
		    }
		    if(flag==1)
	    	    printf("Not a prime number\n");
		    else if(flag==0)
    		    printf("Prime number\n");
		}
	}
%%

int main()
{
yylex();
return 0;
}


######  File Name :   operator_type.l :

%{
#include<stdio.h>
%}

%%
[\t ]+ ;
[?:]+ { printf("%s is Ternary Operator\n", yytext);}
\+|\-|\*|\/ { printf("%s is Arithmetic Operator\n", yytext);}
\==|\<=|\>=|\<|\>|\!= { printf("%s is Relational Operator\n", yytext);}
\=|\+=|\-=|\*=|\/= { printf("%s is Assignment Operator\n", yytext);}
\++|\-- { printf("%s is Unary Operator\n", yytext);}
\n { ECHO;}
%%

int main()
{
	while(yylex());
}

int yywrap( )
{
	return 1;
}


######### File Name :   oddeven.l :

%{
#include<stdio.h>
int i;
%}

%%

[0-9]+	 {i=atoi(yytext);
		if(i%2==0)
			printf("Even");
		else
		printf("Odd");}
%%

int yywrap(){}
int main()
{
	yylex();
	return 0;
}


####### File Name :   longest_word.l :

%{
#include <string.h>
int counter = 0;
char longestString[30];
%}

%%
[a-zA-Z]+ { if (yyleng > counter) {
	                    counter = yyleng;
                        strcpy(longestString,yytext);
                    }
                }
%%

int main() {
    yylex();
    printf("Largest length: %d\n", counter);
    printf("Largest word: %s\n", longestString);
    return 0;
}



############ File Name :   identifier.l  :  ## Keyowrd & Identifier 

%{
#include<stdio.h>
%}

%%
[\t ]+ ;
[0-9]+|[0-9]*\.[0-9]+ { printf("'%s' is NUMBER\n", yytext);}
#.* { printf("'%s' is COMMENT\n", yytext);}
if|else|while|for|switch|goto|elif|NULL|then|is|not|in { printf("'%s' is KEYWORD\n", yytext);}
\+|\-|\*|\/|\==|\&&|\!|\= ;
[a-zA-Z]|[a-zA-Z][a-zA-Z0-9]+ { printf("'%s' is IDENTIFIER\n", yytext);}
\"[^ \"\n]*\" { printf("'%s' is STRING\n", yytext);}
\n { ECHO;}
%%

int main()
{
	while(yylex());
}

int yywrap( )
{
	return 1;
}





#########  Expt 1 : PASS 1  ######################################

######### FIle Name : assmebler_pass1.py :


import sys

# Assmebler directives
# AD = {"start", "end"}
AD = {
    "start": "AD,01,1",
    "end": "AD,02,0"
    }

# Mnemonics OP Table
MOT = { 
    "DC": "DL,02,1",
    "DS": "DL,01,1",
    'ADD': 'IS,01,2',
    'SUB': 'IS,02,2',
    'MUL': 'IS,03,2',
    'MOVER':'IS,04,2',
    'MOVEM':'IS,05,2',
    'READ': 'IS,09,1',
    'PRINT':'IS,10,1',
    'ORIGIN':'AD,03,1',
    'LTORG': 'AD,05,0'
    }

asm_input = open("dummy.asm", "r", encoding="utf-8")

SymTable = {}
LiteralTable = []
PoolTable = []

loc_counter = 0
started = False
literal_counter = 0
literal_idx = 0

def instruction_code(loc_counter:int, isLabel:bool , instructions:str, *args):
    global literal_idx

    instructions_list = instructions.split(',')
    pair = str("("+ instructions_list[0] + "," + instructions_list[1]+")")

    if isLabel and len(args) != int(instructions_list[2])+1:
        print("{}\t ArguementError, expected {} got {}".format(loc_counter, int(instructions_list[2])+1, len(args)))
        exit()

    if len(args) != int(instructions_list[2]) and instructions != MOT["LTORG"] and not isLabel:
        print("{}\t ArguementError, expected {} got {}".format(loc_counter, instructions_list[2], len(args)))
        exit()
    if loc_counter == 0:
        print("\t", pair, "\t" , end='')
    elif isLabel and args[0] in list(SymTable):
        print(loc_counter, "\t" , '(S,{})'.format(list(SymTable).index(args[0])) , '\t' , pair.strip(' '), '\t', end='')
    else:
        print(loc_counter, "\t" , pair, "\t" , end='')

    for x in args:
        # print(x, end='')
        if instructions == MOT["LTORG"]:
            z = x.strip("=F'")
            print(' (DL,02)(C,{})'.format(z), end='\t')
        elif str(x).isdigit() == True:
            print(' (C,{})'.format(x), end='\t')
        elif str(x).__contains__("REG"):
            reg = ord(x.strip(",REG").lower()) - 96
            print(' (RG,{})'.format(reg), end='\t')
        elif str(x) in list(SymTable) and not isLabel:
            print(' (S,{})'.format(list(SymTable).index(x)), end='\t')
        elif str(x) in [literals[0] for literals in LiteralTable]:
            literal_idx += 1
            print(' (L,{})'.format(literal_idx), end='\t')


    print('')

def pass1(lines_tuple:tuple):
    global loc_counter, started, literal_counter

    # print(f'{started} | {loc_counter}: {lines_tuple}')

    # START and END check
    if lines_tuple[0].lower() in AD.keys():
        if started == False:
            if lines_tuple[0].lower() == "start":
                started = True # Pass 1 has begun
                instruction_code(loc_counter, False, AD["start"], lines_tuple[1])
                if len(lines_tuple) > 1:
                    loc_counter = int(lines_tuple[1])
                    return
            if lines_tuple[0].lower() == "end":
                print("Invalid code!")
                exit()
        else:
            if lines_tuple[0].lower() == "start":
                print("Invalid code!")
                exit()
            if lines_tuple[0].lower() == "end":
                instruction_code(loc_counter, False, AD["end"])
                for literals in LiteralTable:
                    if literals[1] == '?':
                        literals[1] = loc_counter
                        loc_counter += 1

                started = False # Pass 1 has ended
                return
    
    # Check if 1st column is a label or mnemonic
    # If it is a label add/update to symbol table
    # If it is a mnemonic check for literals or symbols used
    if lines_tuple[0] not in MOT.keys() and lines_tuple[1] in MOT.keys():
        # print("Label:", lines_tuple[0])
        # print("Mnemonic:", lines_tuple[1])
        if lines_tuple[1].lower() == "dc":
            SymTable.update({lines_tuple[0]:loc_counter})
            # SymTable.update({lines_tuple[0]:lines_tuple[2]})

        if lines_tuple[1].lower() == "ds":
            SymTable.update({lines_tuple[0]:loc_counter})
            # SymTable.update({lines_tuple[0]:lines_tuple[2]})
            loc_counter = loc_counter + int(lines_tuple[2]) - 1 # -1 for sanity check

        instruction_code(loc_counter, True, MOT[lines_tuple[1]], lines_tuple[0], lines_tuple[2])
    
    if lines_tuple[0] in MOT.keys():
        # print("Mnemonic:", lines_tuple[0])

        if lines_tuple[0].lower() == "origin":
            instruction_code(loc_counter, False, MOT["ORIGIN"], lines_tuple[1])
            loc_counter = int(lines_tuple[1])
            return

        if lines_tuple[0].lower() == "ltorg":
            # instruction_code(loc_counter, False, MOT["LTORG"])
            for literals in LiteralTable:
                # print(literals[0])
                instruction_code(loc_counter, False, MOT["LTORG"], literals[0])
                literals[1] = loc_counter
                loc_counter += 1

            PoolTable.append(literal_counter)
            literal_counter = 0
            return
        
        if lines_tuple[0].lower() == "read" or lines_tuple[0].lower() == "print":
            if lines_tuple[1] not in SymTable.keys():
                SymTable.update({lines_tuple[1]:'?'})

        if lines_tuple[1].lower().rfind("reg") != -1:
            if lines_tuple[2].lower().rfind("=") != -1:
                literal_counter += 1
                # print("Literal Count:", literal_counter)
                LiteralTable.append([lines_tuple[2], '?'])
            elif lines_tuple[2] not in SymTable.keys():
                # print("New Symbol:", lines_tuple[2])
                SymTable.update({lines_tuple[2]:'?'})

        # print(lines_tuple[2])
        instruction_code(loc_counter, False, MOT[lines_tuple[0]], lines_tuple[1], lines_tuple[2])
            

    # Increment Location counter address for next line
    loc_counter += 1

def printSymTable(SymTable: dict):
    # print('-------Symbol Table-------')
    print("{:<10} {:<10}".format('Label', 'Value(Address)'))
    for key, value in SymTable.items():
        print("{:<10} {:<10}".format(key, value))
    print('\n')

def printLiteralTable(LiteralTable: list):
    # print('------Literal Table------')
    print("{:<10} {:<10}".format('Literal', 'Value(Address)'))
    for literals in LiteralTable:
        print("{:<10} {:<10}".format(literals[0], literals[1]))
    print('\n')

def printPoolTable(PoolTable:list):
    # print("Pool Table:", PoolTable)
    print(PoolTable)
    # for pools in PoolTable:
    #     print(pools)

def printIntermediateCode(asm_input:__file__):
    # print("---Intermediate Code---")
    lines_tuple = []
    for lines in asm_input.readlines():
        lines_tuple = lines.strip().split(" ")
        pass1(lines_tuple)
    print("")

def PassOneImpl():
    original_stdout = sys.stdout

    with open('Intermediate_Code.txt', 'w') as f:
        sys.stdout = f
        PoolTable.append(0)
        printIntermediateCode(asm_input)       

    with open('Symbol_Table.txt', 'w') as f:
        sys.stdout = f
        printSymTable(SymTable)

    with open('Literal_Table.txt', 'w') as f:
        sys.stdout = f
        printLiteralTable(LiteralTable)

    with open('Pool_Table.txt', 'w') as f:
        sys.stdout = f
        printPoolTable(PoolTable)

    sys.stdout = original_stdout

PassOneImpl()







#################### Expt : FIRST & FOLLOW ####################

### File Name : first_follow.py

import sys
sys.setrecursionlimit(60)

def first(string):
    first_ = set()
    if string in non_terminals:
        alternatives = productions_dict[string]

        for alternative in alternatives:
            first_2 = first(alternative)
            first_ = first_ |first_2

    elif string in terminals:
        first_ = {string}

    elif string=='' or string=='#':
        first_ = {'#'}

    else:
        first_2 = first(string[0])
        if '#' in first_2:
            i = 1
            while '#' in first_2:
                first_ = first_ | (first_2 - {'#'})
                if string[i:] in terminals:
                    first_ = first_ | {string[i:]}
                    break
                elif string[i:] == '':
                    first_ = first_ | {'#'}
                    break
                first_2 = first(string[i:])
                first_ = first_ | first_2 - {'#'}
                i += 1
        else:
            first_ = first_ | first_2

    return  first_

def follow(nT):
    follow_ = set()
    prods = productions_dict.items()
    if nT==starting_symbol:
        follow_ = follow_ | {'$'}
    for nt,rhs in prods:
        for alt in rhs:
            for char in alt:
                if char==nT:
                    following_str = alt[alt.index(char) + 1:]
                    if following_str=='':
                        if nt==nT:
                            continue
                        else:
                            follow_ = follow_ | follow(nt)
                    else:
                        follow_2 = first(following_str)
                        if '#' in follow_2:
                            follow_ = follow_ | follow_2-{'#'}
                            follow_ = follow_ | follow(nt)
                        else:
                            follow_ = follow_ | follow_2
    return follow_

terminals = list(map(str, input("Enter the terminals: ").replace(',',' ').split()))
non_terminals = list(map(str, input("Enter the non-terminals (First non-terminal should be starting symbol): ").replace(',',' ').split()))

starting_symbol = non_terminals[0]
no_of_productions = int(input("Enter no of productions: "))
productions = []

print("Enter the productions:")
for _ in range(no_of_productions):
    productions.append(input())

productions_dict = {}
for nT in non_terminals:
    productions_dict[nT] = []

for production in productions:
    nonterm_to_prod = production.split("->")
    alternatives = nonterm_to_prod[1].replace('/','|').split("|")
    for alternative in alternatives:
        productions_dict[nonterm_to_prod[0]].append(alternative)

FIRST = {}
FOLLOW = {}

for non_terminal in non_terminals:
    FIRST[non_terminal] = set()
    FOLLOW[non_terminal] = set()
    FIRST[non_terminal] = FIRST[non_terminal] | first(non_terminal)

FOLLOW[starting_symbol] = FOLLOW[starting_symbol] | {'$'}
for non_terminal in non_terminals:
    FOLLOW[non_terminal] = FOLLOW[non_terminal] | follow(non_terminal)

print("{: <15} {: ^30} {: ^20}".format('Non Terminals','First','Follow'))
for non_terminal in non_terminals:
    print("{: ^15} {: <30} {: <20}".format(non_terminal,str(sorted(FIRST[non_terminal])),str(sorted(FOLLOW[non_terminal]))))




""")
