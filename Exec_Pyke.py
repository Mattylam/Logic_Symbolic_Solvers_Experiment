from pyke_solver import Pyke_Program

    # Answer: B
logic_program = """Predicates:
Dependent($x, bool) ::: x is a person dependent on caffeine.
Drinks($x, bool) ::: x regularly drinks coffee.
Jokes($x, bool) ::: x jokes about being addicted to caffeine.
Unaware($x, bool) ::: x is unaware that caffeine is a drug.
Student($x, bool) ::: x is a student.
Facts:
Drinks($x, True) >>> Dependent($x, True) ::: All people who regularly drink coffee are dependent on caffeine.
Drinks($x, True) >>> Jokes($x, False) 
Drinks($x, False) >>> Jokes($x, True)  
Jokes($x, False) >>> Drinks($x, True) 
Jokes($x, True)  >>> Drinks($x, False) ::: People either regularly drink coffee or joke about being addicted to caffeine.
Jokes($x, True) >>> Unaware($x, False) ::: No one who jokes about being addicted to caffeine is unaware that caffeine is a drug. 

Query:
Drinks(Rina, True) >>> Unaware(Rina, False)::: Rina is either a person who jokes about being addicted to caffeine or is unaware that caffeine is a drug.
"""
pyke_program = Pyke_Program(logic_program, 'ProofWriter')
print(pyke_program.flag)
print(pyke_program.Rules)
print(pyke_program.Facts)
print(pyke_program.Query)
result, error_message = pyke_program.execute_program()
print(result)
print(error_message)


def parse_forward_rule(f_index, rule):
    premise, conclusion = rule.split('>>>')
    premise = premise.strip()
    # split the premise into multiple facts if needed
    premise = premise.split('&&')
    premise_list = [p.strip() for p in premise]

    conclusion = conclusion.strip()
    # split the conclusion into multiple facts if needed
    conclusion = conclusion.split('&&')
    conclusion_list = [c.strip() for c in conclusion]

    # create the Pyke rule
    pyke_rule = f'''fact{f_index}\n\tforeach'''
    for p in premise_list:
        pyke_rule += f'''\n\t\tfacts.{p}'''
    pyke_rule += f'''\n\tassert'''
    for c in conclusion_list:
        pyke_rule += f'''\n\t\tfacts.{c}'''
    return pyke_rule

rule = 'Drinks($x, True) && Jokes($x, False) >>> Dependent($x, True)'
a = parse_forward_rule(7, rule)
print(a)