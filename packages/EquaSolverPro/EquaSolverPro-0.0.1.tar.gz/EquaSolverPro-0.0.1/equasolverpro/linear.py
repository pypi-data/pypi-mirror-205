from equasolverpro.components import *




def linear_in_one_str(eq):
    equation = Equation.parseEquation(eq)

    print("=>",equation)

    equation.factorize()

    print("=>",equation)

    lhs_num = equation.LHS[0].get_num()
    rhs_num = equation.RHS[0].get_num()
    rhs_num = rhs_num / lhs_num
    equation.RHS[0].num = rhs_num
    equation.LHS[0].num = 1

    print("=>",equation.LHS[0].get_var(), '=', rhs_num)

    return equation.LHS[0].get_var(), rhs_num


def linear_in_one(equation):
    print("=>",equation)

    equation.factorize()

    print("=>",equation)

    lhs_num = equation.LHS[0].get_num()
    rhs_num = equation.RHS[0].get_num()
    rhs_num = rhs_num / lhs_num
    equation.RHS[0].num = rhs_num
    equation.LHS[0].num = 1
    
    print("=>",equation.LHS[0].get_var(), '=', rhs_num)
    return equation.LHS[0].get_var(), rhs_num


def linear_in_two(eq1, eq2):
    equa1 = Equation.parseEquation(eq1)
    equa2 = Equation.parseEquation(eq2)


    equa1.factorize()
    equa2.factorize()

    print('=>', equa1)
    for i in equa1.LHS:
        if not equa1.LHS[0] == i:
            equa1.LHS.remove(i)
            i.change_sign()
            equa1.RHS.append(i)

    divisor = equa1.LHS[0].get_num()

    equa1.LHS[0].set_num(1, '+')
    for i in equa1.RHS:
        num = i.get_num()
        i.set_num_direct(num / divisor)
    print('=>', equa1)
    for i in equa2.LHS:
        if i.get_var() != equa1.LHS[0].get_var():
            equa2.LHS.remove(i)
            i.change_sign()
            equa2.RHS.append(i)
    print('=>', equa2)

    mult = equa2.LHS[0].get_num()

    equa2.LHS.remove(equa2.LHS[0])
    for i in equa1.RHS:
        num = i.get_num()
        i.set_num_direct((num / divisor) * mult)
    equa2.LHS = equa1.RHS
    print('=>', equa2)
    
    secondVar = linear_in_one_str(str(equa2))
    originalEqua1 = Equation.parseEquation(eq1)
    print()
    print('=>',originalEqua1)
    for i in originalEqua1.RHS:
        if i.get_var() == secondVar[0]:
            num = i.get_num() * secondVar[1]
            originalEqua1.RHS.remove(i)
            if num >= 0:
                sign = '+'
                num_coef = num
            else:
                sign = '-'
                num_coef = -num

            originalEqua1.RHS.append(Term(sign, num_coef, '', 1))

    for i in originalEqua1.LHS:
        if i.get_var() == secondVar[0]:
            num = i.get_num() * secondVar[1]
            originalEqua1.LHS.remove(i)
            if num >= 0:
                sign = '+'
                num_coef = num
            else:
                sign = '-'
                num_coef = -num

            originalEqua1.LHS.append(Term(sign, num_coef, '', 1))
    firstVar = linear_in_one(originalEqua1)
    solution = {
        firstVar[0]:firstVar[1],
        secondVar[0]:secondVar[1]
    }
    print("There fore Solution is: \n",solution)
    return solution

