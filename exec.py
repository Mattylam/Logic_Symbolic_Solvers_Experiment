def isValid(s):
    stack = []
    c = {")": "("}
    for i in s:
        if i in c:  # if it is a closing parenthesis, if it is key value in c
            if stack and stack[-1] == c[i]:
                # if stack is not empty and the last element added into stack is the correct closing bracket
                stack.pop()
            else:  # if stack is empty and a closing bracket here means we cannot close it
                print('here')
                print(stack)
                return False
        else:  # if it is a open parenthesis
            if i == "(":
                stack.append(i)
    if len(stack) > 0:
        print(stack)
        return False
    else:
        return True

def isOpenValid(s):
    stack = []
    c = {"(": ")"}
    for i in reversed(s):
        if i in c:  # if it is a closing parenthesis, if it is key value in c
            if stack and stack[-1] == c[i]:
                # if stack is not empty and the last element added into stack is the correct closing bracket
                stack.pop()
            else:  # if stack is empty and a closing bracket here means we cannot close it
                return False
        else:  # if it is a open parenthesis
            if i == ")":
                stack.append(i)
    if len(stack) > 0:
        print(stack)
        return False
    else:
        return True

# def Close_Parenthesis(line):
#     if isValid(line):
#         output = line
#     else:
#         print("1")
#         output = line + ')'
#     # if isOpenValid(output):
#     #     output = output
#     # else:
#     #     if output[-1] == ')':
#     #         print("1")
#     #         print(output)
#     #         output = output[:-1]
#     return output

def change_translation(text):
    lines = text.split('\n')
    check = True
    for i in range(len(lines)):
        lines[i] = Close_Parenthesis(lines[i])
        if not isValid(lines[i]):
            check = False
    t = '\n'.join(lines)
    return t, check

text =  "\n\n# Each yumpus is not small.\nForAll([x], Implies(Yumpus(x), Not(Small(x))))\n\n# Each yumpus is a dumpus.\nForAll([x], Implies(Yumpus(x), Dumpus(x))))\n\n# Each dumpus is opaque.\nForAll([x], Implies(Dumpus(x), Opaque(x))))\n\n# Every dumpus is a jompus.\nForAll([x], Implies(Dumpus(x), Jompus(x))))\n\n# Each jompus is shy.\nForAll([x], Implies(Jompus(x), Shy(x))))\n\n# Each numpus is sour.\nForAll([x], Implies(Numpus(x), Sour(x))))\n\n# Every jompus is a tumpus.\nForAll([x], Implies(Jompus(x), Tumpus(x))))\n\n# Each tumpus is brown.\nForAll([x], Implies(Tumpus(x), Brown(x))))\n\n# Each tumpus is a vumpus.\nForAll([x], Implies(Tumpus(x), Vumpus(x))))\n\n# Vumpuses are dull.\nForAll([x], Implies(Vumpus(x), Dull(x))))\n\n# Vumpuses are wumpuses.\nForAll([x], Implies(Vumpus(x), Wumpus(x))))\n\n# Every wumpus is not sour.\nForAll([x], Implies(Wumpus(x), Not(Sour(x))))))\n\n# Wumpuses are rompuses.\nForAll([x], Implies(Wumpus(x), Rompus(x))))\n\n# Each rompus is not luminous.\nForAll([x], Implies(Rompus(x), Not(Luminous(x))))\n\n# Rompuses are impuses.\nForAll([x], Implies(Rompus(x), Impus(x))))\n\n# Stella is a dumpus.\nDumpus(Stella)\n\n\n\n# Question: Is the following statement true or false? Stella is sour.\nreturn Sour(Stella)"
line = "ForAll([x], Implies(Yumpus(x), Not(Small(x)"
def Close_Parenthesis(line):
    stack = {'(':0, ')':0}
    for i in line:
        if i in stack.keys():
            stack[i] += 1
    if stack['('] == stack[')']:
        return line
    elif stack['('] > stack[')']:
        n = stack['('] - stack[')']
        for _ in range(n):
            line = line + ')'
        return line
    else:
        n = stack[')'] - stack['(']
        for _ in range(n):
            line = line[:-1]
        return line


a = Close_Parenthesis(line)
print(a)

d = "# \nForAll([x], Implies(Tumpus(x), Large(x))))\nForAll([x], Implies(Tumpus(x), Wumpus(x))))\nForAll([x], Implies(Wumpus(x), Not(Opaque(x)))))\nForAll([x], Implies(Dumpus(x), Not(Dull(x)))))\nForAll([x], Implies(Wumpus(x), Rompus(x))))\nForAll([x], Implies(Rompus(x), Brown(x))))\nForAll([x], Implies(Rompus(x), Vumpus(x))))\nForAll([x], Implies(Vumpus(x), Temperate(x))))\nForAll([x], Implies(Vumpus(x), Jompus(x))))\nForAll([x], Implies(Jompus(x), Dull(x))))\nForAll([x], Implies(Jompus(x), Numpus(x))))\nForAll([x], Implies(Numpus(x), Liquid(x))))\nForAll([x], Implies(Numpus(x), Impus(x))))\nForAll([x], Implies(Impus(x), Spicy(x))))\nForAll([x], Implies(Impus(x), Yumpus(x))))\nForAll([x], Implies(Yumpus(x), Not(Nervous(x)))))\nForAll([x], Implies(Yumpus(x), Zumpus(x))))\nTumpus(Wren))"
print(d)