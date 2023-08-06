from equasolverpro.components import *
import math

def QuadraticSolver(eq):
    eq = eq.factorizEquation()
    for i in eq.RHS:
        eq.RHS.remove(i)
        i.change_sign()
        eq.LHS.append(i)

    print('Step 1:',eq)

    if len(eq.LHS) == 3:
        try:
            for i in eq.LHS:
                index = eq.LHS.index(i)
                if i.get_power() == 2:
                    temp = i
                    eq.LHS[index] = eq.LHS[0]
                    eq.LHS[0] = temp 
                elif i.get_var() == '':
                    temp = i
                    eq.LHS[index] = eq.LHS[-1]
                    eq.LHS[-1] = temp

            print('Step 2:',eq)

            prod = eq.LHS[0].get_num() * eq.LHS[-1].get_num()
            x = eq.LHS[1].get_num()
            var1 = None
            var2 = None
            
            if prod < 0:
                for i in range(int(prod), int(-prod)+1):
                    for j in range(int(prod), int(-prod)+1):
                        if i*j == prod and i+j == x:
                            variable = eq.LHS[1].get_var()
                            eq.LHS.remove(eq.LHS[1])
                            i = float(i)
                            j = float(j)
                            var1 = Term('-'if i < 0 else '+', -i if i < 0 else i, variable, 1)
                            var2 = Term('-'if j < 0 else '+', -j if j < 0 else j, variable, 1)
                            break
                    else:
                        continue
                    break
            else:
                for i in range(int(-prod), int(prod)+1):
                    for j in range(int(-prod), int(prod)+1):
                        if i*j == prod and (i+j == x):
                            variable = eq.LHS[1].get_var()
                            eq.LHS.remove(eq.LHS[1])
                            i = float(i)
                            j = float(j)
                            var1 = Term('-'if i < 0 else '+', -i if i < 0 else i, variable, 1)
                            var2 = Term('-'if j < 0 else '+', -j if j < 0 else j, variable, 1)
                            break
                    else:
                        continue
                    break

            new_list = []
            new_list.append(eq.LHS[0])
            new_list.append(var1)
            new_list.append(var2)
            new_list.append(eq.LHS[-1])
            eq.LHS = new_list
            print('Step 3:',eq)
            common1 = float(math.gcd(int(eq.LHS[0].get_num()),int(eq.LHS[1].get_num())))
            common1_var = ''
            lhs1 = [eq.LHS[0], eq.LHS[1]]
            for i in lhs1:
                i.set_num_direct(i.get_num() / common1) 
            lhs1[0].power = lhs1[0].get_power() - lhs1[1].get_power()
            common1_var = lhs1[0].get_var()
            lhs1[1].var = ''
            common1 = Term('-'if common1<0 else '+',common1 if common1>0 else -common1\
                , common1_var,1)

            part1 = [common1,lhs1]

            common2 = math.gcd(int(eq.LHS[2].get_num()),int(eq.LHS[3].get_num()))
            lhs2 = [eq.LHS[2], eq.LHS[3]]
            common2_var = ''
            
            for i in lhs2:
                i.set_num_direct(i.get_num() / common2) 
            if lhs2[0].get_var() == lhs2[1].get_var():
                lhs2[0].power = lhs2[0].get_power() - lhs2[1].get_power()
                common2_var = lhs2[0].get_var()
                lhs2[1].var = ''
            common2 = Term('-'if common2<0 else '+',common2 if common2>0 else -common2\
                , common2_var,1)

            part2 = [common2,lhs2]
            eq.LHS = [part1,part2]
            printStatement = ''
            for i in eq.LHS:
                printStatement += str(i[0]) + ' '
                printStatement += '(' + ' '
                for k in i[1]:
                    printStatement += str(k) + ' '
                printStatement += ') ' + ' '
            print('Step 4:',printStatement)
            if eq.LHS[0][1] == eq.LHS[0][1]:
                var1 = [eq.LHS[0][0],eq.LHS[1][0] ]
                var2 = eq.LHS[0][1]
                printStatement = '( '
                for i in var1:
                    printStatement += str(i) + ' '
                printStatement = printStatement + ' )'
                printStatement = printStatement + '( '
                for i in var2:
                    printStatement += str(i) + ' '
                printStatement += ' )'

                print('Step 5:',printStatement)

                solution = (var1[1].get_num()/var1[0].get_num(),\
                    var2[1].get_num()/var2[0].get_num())
                print('Solution: ',solution)
                return solution
        except:
            a = eq.LHS[0].get_num()
            b = eq.LHS[1].get_num()
            c = eq.LHS[2].get_num()

            solution = ((-b + (b*b - 4*a*c)**1/2)/2*a, (-b - (b*b - 4*a*c)**1/2)/2*a)
            return solution

    else:           
        raise Exception()   