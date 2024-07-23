import sys

sys.path.append('.')

import re
import os
import pickle

from Z3_utils import make_z3_enum_line, execute_z3_test

class Z3_Program:
    def __init__(self, logic_program: str, assumption) -> None:
        self.logic_program, self.flag = self.change_translation(logic_program.strip())
        #self.flag = True
        self.assumption = assumption

    def break_down_func_var(self):
        pass
    # Fix Parenthesis issue here
    def isValid(self,s):
        stack = []
        c = {")": "("}
        for i in s:
            if i in c:  # if it is a closing parenthesis, if it is key value in c
                if stack and stack[-1] == c[i]:
                    # if stack is not empty and the last element added into stack is the correct closing bracket
                    stack.pop()
                else:  # if stack is empty and a closing bracket here means we cannot close it
                    return False
            else:  # if it is a open parenthesis
                if i == "(":
                    stack.append(i)
        if len(stack) > 0:
            return False
        else:
            return True

    # def Close_Parenthesis(self,line):
    #     if self.isValid(line):
    #         return line
    #     else:
    #         return line + ')'
    def Close_Parenthesis(self, line):
        stack = {'(': 0, ')': 0}
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

    def change_translation(self, text):
        lines = text.split('\n')
        check = True
        for i in range(len(lines)):
            lines[i] = self.Close_Parenthesis(lines[i])
            # if not self.isValid(lines[i]):
            #     check = False
        t = '\n'.join(lines)
        return t, check

    PREDEFIND_FUNCS = ["ForAll", "Exist", "And", "Or", "Not", "Implies", "Xor"]
    PREDEFIND_QUNT_VARS = ["x"]


    def extract_var_and_func(self, line):
        #VAR_REGEX = r"[_a-zA-Z]+[,)]"
        VAR_REGEX = r"[_a-zA-Z0-9]+[,)]"
        FUNC_REGEX = r"[_a-zA-Z0-9]+[(]"
        all_vars = re.findall(VAR_REGEX, line)
        all_funcs = re.findall(FUNC_REGEX, line)
        all_vars = [all_vars.rstrip(",)") for all_vars in all_vars]
        all_funcs = [all_funcs.rstrip("(") for all_funcs in all_funcs]
        return all_vars, all_funcs


    def determine_func_n_args(self, code, func):
        start_pos = code.find(func + "(")
        end_pos = code.find(")", start_pos)
        num_args = code[start_pos + len(func) + 1:end_pos].count(",") + 1
        return num_args


    def proof_exec(self, code, return_code=False):
        try:
            lines = code.splitlines()
            lines = [l.strip() for l in lines]
            lines = [l for l in lines if l and not l.startswith("#")]
            assert lines[-1].startswith("return")
            result_line = lines[-1]
            lines = lines[:-1]

            vars = set()
            functions = set()
            PREDEFIND_FUNCS = ["ForAll", "Exist", "And", "Or", "Not", "Implies", "Exists"]
            PREDEFIND_QUNT_VARS = ["x"]

            for line in lines:
                line_vars, line_funcs = self.extract_var_and_func(line)
                vars.update(line_vars)
                functions.update(line_funcs)

            vars = [v for v in vars if v not in PREDEFIND_QUNT_VARS]
            functions = [f for f in functions if f not in PREDEFIND_FUNCS]

            func_n_args = {}
            for func in functions:
                func_n_args[func] = self.determine_func_n_args(code, func)
            functions = sorted(functions, key=lambda x: func_n_args[x])

            translated_lines = []
            translated_lines.append(make_z3_enum_line("ThingsSort", vars))

            for func in functions:
                num_args = func_n_args[func]
                translated_lines.append("{} = Function('{}', {}, BoolSort())".format(func, func, ", ".join(["ThingsSort"]*num_args)))
            translated_lines.append("x = Const('x', ThingsSort)")
            translated_lines.append("precond = []")

            for line in lines:
                translated_lines.append("precond.append({})".format(line))

            translated_lines.append("s = Solver()")
            translated_lines.append("s.add(precond)")

            return_clause = result_line.split("return")[1].strip()
            translated_lines.append("s.add(Not({}))".format(return_clause))
            translated_lines.extend([
                "if s.check() == unsat:",
                "    print('True')",
                "else:",
                "    print('False')",
            ])
            translated_lines = ["from z3 import *"] + translated_lines

            code = "\n".join(translated_lines)
            result = execute_z3_test(code)
            if return_code:
                return code, result
            else:
                return result
        except:
            return False, "Parse Error"

    def proof_OWA_exec(self,code, return_code=False):
        try:
            lines = code.splitlines()
            lines = [l.strip() for l in lines]
            lines = [l for l in lines if l and not l.startswith("#")]
            assert lines[-1].startswith("return")
            result_line = lines[-1]
            lines = lines[:-1]
            PREDEFIND_FUNCS = ["ForAll", "Exist", "And", "Or", "Not", "Implies","Xor", "Exists"]
            PREDEFIND_QUNT_VARS = ["x"]
            vars = set()
            functions = set()

            for line in lines:
                line_vars, line_funcs = self.extract_var_and_func(line)
                vars.update(line_vars)
                functions.update(line_funcs)

            vars = [v for v in vars if v not in PREDEFIND_QUNT_VARS]
            functions = [f for f in functions if f not in PREDEFIND_FUNCS]

            func_n_args = {}
            for func in functions:
                func_n_args[func] = self.determine_func_n_args(code, func)
            functions = sorted(functions, key=lambda x: func_n_args[x])

            translated_lines = []
            translated_lines.append(make_z3_enum_line("ThingsSort", vars))

            for func in functions:
                num_args = func_n_args[func]
                translated_lines.append(
                    "{} = Function('{}', {}, BoolSort())".format(func, func, ", ".join(["ThingsSort"] * num_args)))
            translated_lines.append("x = Const('x', ThingsSort)")
            translated_lines.append("precond = []")

            for line in lines:
                translated_lines.append("precond.append({})".format(line))

            translated_lines.append("s = Solver()")
            translated_lines.append("s.add(precond)")
            translated_lines.extend([
                "def isConsistent(solver, predicate):",
                "    solver.push()",
                "    solver.add(predicate)",
                "    r = solver.check()",
                "    solver.pop()",
                "    if r == sat:",
                "        return True",
                "    elif r == unsat:",
                "        return False",
                "    else:",
                "        raise Exception(" + "'SolverInconclusive'" + ") ",
            ])

            return_clause = result_line.split("return")[1].strip()
            translated_lines.append("pos = isConsistent(s,{})".format(return_clause))
            translated_lines.append("neg = isConsistent(s,Not({}))".format(return_clause))
            translated_lines.extend([
                "if pos and neg:",
                "    print('Unknown')",
                "elif pos:",
                "    print('True')",
                "elif neg:",
                "    print('False')",
                "else:",
                "    raise Exception(" + "'facts are inconsistent'" + ") "
            ])
            translated_lines = ["from z3 import *"] + translated_lines

            code = "\n".join(translated_lines)
            #print(code)
            result = execute_z3_test(code)
            if return_code:
                return code, result
            else:
                return result
        except:
            return False, "Parse Error"

    def execute_program(self):
        if self.assumption == "CWA":
            Exec, answer = self.proof_exec(self.logic_program.strip())
        else:
            Exec, answer = self.proof_OWA_exec(self.logic_program.strip())
        # Exec tells us if there was an error
        if not Exec:
            error_message = answer
            answer = None
        else:
            error_message = ""
        return answer, error_message
    def answer_mapping(self, answer):
        if answer == 'True':
            return 'A'
        elif answer == 'False':
            return 'B'
        elif answer == 'Unknown':
            return 'C'
            #return 'B'
        else:
            raise Exception("Answer not recognized")

# Test the solver here
if __name__=="__main__":
    test = '''
    # Anne is quiet.
    quiet(Anne)
    # Erin is furry.
    furry(Erin)
    # Erin is green. 
    green(Erin)
    # Fiona is furry.
    furry(Fiona)
    # Fiona is quiet.
    quiet(Fiona)
    # Fiona is red.
    red(Fiona)
    # Fiona is rough.
    rough(Fiona) 
    # Fiona is white.
    white(Fiona) 
    # Harry is furry. 
    furry(Harry)
    # Harry is quiet.
    quiet(Harry)
    # Harry is white.
    white(Harry) 
    # Young people are furry.
    ForAll([x], Implies(young(x), furry(x)))
    # If Anne is quiet then Anne is red. 
    Implies(quiet(Anne), red(Anne))
    # Young, green people are rough.
    ForAll([x], Implies(And(young(x), green(x)),rough(x)))
    # If someone is green then they are white.
    ForAll([x], Implies(green(x), white(x)))
    #If someone is furry and quiet then they are white. 
    ForAll([x], Implies(And(furry(x), quiet(x)),white(x)))
    # If someone is young and white then they are rough. 
    ForAll([x], Implies(And(young(x), white(x)),rough(x)))
    # All red people are young.
    ForAll([x], Implies(red(x), young(x)))

    # Question: The statement "Anne is white" is True or False?
    return white(Anne) '''

    test1 =  "    # Charlie is big.\n    big(Charlie)\n    # Charlie is cold.\n    cold(Charlie)\n    # Charlie is red.\n    red(Charlie)\n    # Charlie is smart.\n    smart(Charlie)\n    # Erin is nice.\n    nice(Erin)\n    # Erin is quiet.\n    quiet(Erin)\n    # Erin is red.\n    red(Erin)\n    # Erin is smart.\n    smart(Erin)\n    # Fiona is big.\n    big(Fiona)\n    # Fiona is white.\n    white(Fiona)\n    # Harry is cold.\n    cold(Harry)\n    # Harry is red.\n    red(Harry)\n    # Cold things are quiet.\n    ForAll([x], Implies(cold(x), quiet(x)))\n    # Quiet things are nice.\n    ForAll([x], Implies(quiet(x), nice(x)))\n    # If Harry is white and Harry is smart then Harry is quiet.\n    ForAll([x], Implies(And(white(x), smart(x)), quiet(x)))\n    # If something is red then it is white.\n    ForAll([x], Implies(red(x), white(x)))\n    # If Fiona is red then Fiona is cold.\n    ForAll([x], Implies(red(Fiona), cold(Fiona)))\n    # Nice things are big.\n    ForAll([x], Implies(nice(x), big(x)))\n\n    # Question: the following statement true, false, or unknown? Charlie is big.\n    return big(Charlie)"
    #test1 =       "    # Anne is not big.\n    big(Anne)\n    # Anne is kind.\n    kind(Anne)\n    # Anne is smart.\n    smart(Anne)\n    # Anne is young.\n    young(Anne)\n    # Charlie is kind.\n    kind(Charlie)\n    # Dave is not blue.\n    Not(blue(Dave))\n    # Fiona is blue.\n    blue(Fiona)\n    # All young people are smart.\n    ForAll([x], Implies(young(x), smart(x)))\n    # If someone is big then they are not kind.\n    ForAll([x], Implies(big(x), Not(kind(x)))\n    # If someone is furry and kind then they are round.\n    ForAll([x], Implies(And(furry(x), kind(x)), round(x)))\n    # If Anne is furry then Anne is smart.\n    Implies(furry(Anne), smart(Anne))\n    # If someone is blue and round then they are furry.\n    ForAll([x], Implies(And(blue(x), round(x)), furry(x)))\n    # If someone is young then they are furry.\n    ForAll([x], Implies(young(x), furry(x)))\n    # If Dave is young and Dave is not kind then Dave is round.\n    Implies(And(young(Dave), Not(kind(Dave))), round(Dave))\n    # All round people are not blue.\n    ForAll([x], Implies(round(x), Not(blue(x)))\n\n    # Question: the following statement true, false, or unknown? Anne is not young.\n    return Not(young(Anne))"

    test2 = "# All cats are mammals.\nMammal(cat)\n# Some pets are not mammals.\nExists([x], Implies(Pet(x), Not(Mammal(x)))\n# Question: No pets are cats.\nreturn Not(Pet(cat))"

    test3 = "# There are four seasons in a year: Spring, Summer, Fall, and Winter.\nseasons = [Spring, Summer, Fall, Winter]\n# All students who want to have a long vacation love summer the most.\nForAll([x], Implies(Student(x) & LongVacation(x), FavoriteSeason(x) == Summer)\n# Emma's favorite season is summer.\nFavoriteSeason(Emma) == Summer\n# Mia's favorite season is not the same as Emma's.\nFavoriteSeason(Mia) != FavoriteSeason(Emma)\n# James wants to have a long vacation.\nLongVacation(James)\n# Question: James's favorite season is summer.\nreturn FavoriteSeason(James) == Summer"

    test4 = """
# Each yumpus is not small.
ForAll([x], Implies(Yumpus(x), Not(Small(x)))

# Each yumpus is a dumpus.
ForAll([x], Implies(Yumpus(x), Dumpus(x)))

# Each dumpus is opaque.
ForAll([x], Implies(Dumpus(x), Opaque(x)))

# Every dumpus is a jompus.
ForAll([x], Implies(Dumpus(x), Jompus(x)))

# Each jompus is shy.
ForAll([x], Implies(Jompus(x), Shy(x)))

# Each numpus is sour.
ForAll([x], Implies(Numpus(x), Sour(x)))

# Every jompus is a tumpus.
ForAll([x], Implies(Jompus(x), Tumpus(x)))

# Each tumpus is brown.
ForAll([x], Implies(Tumpus(x), Brown(x)))

# Each tumpus is a vumpus.
ForAll([x], Implies(Tumpus(x), Vumpus(x)))

# Vumpuses are dull.
ForAll([x], Implies(Vumpus(x), Dull(x)))

# Vumpuses are wumpuses.
ForAll([x], Implies(Vumpus(x), Wumpus(x)))

# Every wumpus is not sour.
ForAll([x], Implies(Wumpus(x), Not(Sour(x))))

# Wumpuses are rompuses.
ForAll([x], Implies(Wumpus(x), Rompus(x)))

# Each rompus is not luminous.
ForAll([x], Implies(Rompus(x), Not(Luminous(x))))))))

# Rompuses are impuses.
ForAll([x], Implies(Rompus(x), Impus(x)))

# Stella is a dumpus.
Dumpus(Stella)

# Question: Is the following statement true or false? Stella is sour.
return Sour(Stella)
"""
    a = Z3_Program(test4, assumption="OWA")
    answer, error_message = a.execute_program()
    print(test4)
    print(answer)
    print(error_message)