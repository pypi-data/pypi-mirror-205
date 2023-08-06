# Author: Snehashish Laskar
# Date: 1st April 2023
# Copyright (c) 2023 Snehashish Laskar
import math

class Term:
    """
    A term is the most fundamental structural unit of any equation.
    Multiple terms together form an expression and two expressions
    with an equality sign form an equation. This data type is used
    to break down the equation into different term to deal with handling
    each term separately. This helps simplify the process of solving and
    factorizing the equation into the simplest form possible.

    Each term consists of 3 main components :
     1. The Numerical Coefficient like 2 from 2x^2
     2. The Variable Coefficient like x from 2x^2
     3. The power on the variable like ^2 from 2x^2
     4. The sign - or + to determine the sign on the term
    """
    def __init__(self, sign, num_coef, var, power):
        self.sign = sign
        self.num_coef = num_coef
        self.var = var
        self.power = power
        self.num = float(sign + str(num_coef))

    def get_sign(self):
        return self.sign

    def set_num_coef(self, num):
        self.num_coef = num
        self.num = float(self.sign + str(self.num_coef))

    def set_num(self, coef, sign):
        self.num_coef = coef
        self.sign = sign
        self.num = float(self.sign + str(self.num_coef))

    def set_num_direct(self, num):
        if num >= 0:
            self.sign = '+'
            self.num_coef = num
        else:
            self.sign = '-'
            self.num_coef = -(num)

    def get_num_coef(self):
        return self.num_coef

    def get_var(self):
        return self.var

    def get_power(self):
        return self.power

    def get_num(self):
        return self.num

    # Function to change the sign of the term when switching sides
    def change_sign(self):
        if self.get_sign() == '-':
            self.sign = '+'
        elif self.get_sign() == '+':
            self.sign = '-'
        self.num = float(self.sign + str(self.num_coef))

    # Function to get the numerical value of
    def value(self):
        if self.get_power() > 1:
            return self.get_sign() + str(self.get_num_coef()) + self.get_var() + "^" + str(self.get_power())
        return self.get_sign() + str(self.get_num_coef()) + self.get_var()

    # Functions to enable to print the term
    def __str__(self):
        if self.get_power() > 1:
            return self.get_sign() + str(self.get_num_coef()) + self.get_var() + "^" + str(self.get_power())
        return self.get_sign() + str(self.get_num_coef()) + self.get_var()

    def __repr__(self):
        if self.get_power() > 1:
            return self.get_sign() + str(self.get_num_coef()) + self.get_var() + "^" + str(self.get_power())
        return self.get_sign() + str(self.get_num_coef()) + self.get_var()


class Equation:

    def __init__(self):
        self.LHS = []
        self.RHS = []

    def get_lhs(self):
        return self.LHS

    def get_rhs(self):
        return self.RHS

    def value(self):
        var = ''
        if self.LHS != []:
            for i in self.LHS:
                var += i.get_sign() + " " + i.value().replace(i.get_sign(), '') + " "
        else:
            var += '0 '
        var += "= "
        if self.RHS != []:
            for i in self.RHS:
                var += i.get_sign() + " " + i.value().replace(i.get_sign(), '') + " "
        else:
            var += '0'
        return var

    def add(self, term1, term2):
        if term1.get_var() == term2.get_var() and term1.get_power() == term2.get_power():
            Sum = term1.get_num() + term2.get_num()
            if Sum >= 0:
                sign = '+'
                num_coef = Sum
            else:
                sign = '-'
                num_coef = -(Sum)

            new_term = Term(sign, num_coef, term1.get_var(), term1.get_power())

            return new_term
        else:
            return 'unequal'

    @staticmethod
    def addTwo(term1, term2):
        if term1.get_var() == term2.get_var() and term1.get_power() == term2.get_power():
            Sum = term1.get_num() + term2.get_num()
            if Sum >= 0:
                sign = '+'
                num_coef = Sum
            else:
                sign = '-'
                num_coef = -Sum

            new_term = Term(sign, num_coef, term1.get_var(), term1.get_power())

            return new_term
        else:
            return 'unequal'

    # Helper function and not to be accesible to user
    def factorize(self):

        # Step 1: Move all the variable terms to LHS and all the number to RHS
        lhs = []
        rhs = []
        for i in self.LHS:
            if i.get_var() == '':
                temp = i
                temp.change_sign()
                rhs.append(temp)
            else:
                lhs.append(i)
        for i in self.RHS:
            if i.get_var() != '':
                temp = i
                temp.change_sign()
                lhs.append(temp)
            else:
                rhs.append(i)
        self.LHS = lhs
        self.RHS = rhs

        lhs = self.LHS
        rhs = self.RHS

        for i in lhs:
            for k in lhs:
                if i != k and Equation.addTwo(i, k) != 'unequal':
                    new = self.addTwo(i, k)
                    lhs.remove(k)
                    lhs.remove(i)
                    lhs.append(new)
        for i in rhs:
            for k in rhs:
                if i != k and Equation.addTwo(i, k) != 'unequal':
                    new = self.addTwo(i, k)
                    rhs.remove(k)
                    rhs.remove(i)
                    rhs.append(new)

        equa = Equation()
        equa.LHS = lhs
        equa.RHS = rhs
        return equa

    def factorizEquation(self):
        equation = self
        lhs = equation.LHS
        rhs = equation.RHS

        for i in rhs:
            i.change_sign()
            lhs.append(i)
        rhs = []

        for i in lhs:
            for k in lhs:
                if i != k and Equation.addTwo(i, k) != 'unequal':

                    try:
                        new = Equation.addTwo(i, k)
                        lhs.remove(i)
                        lhs.remove(k)
                        lhs.append(new)
                    except:
                        pass
        equa = Equation()
        equa.LHS = lhs
        equa.RHS = rhs
        return equa.factorize()

    @staticmethod
    def parseEquation(eq):
        lhs = ''
        rhs = ''
        lhs = eq.split('=')[0].split()
        rhs = eq.split('=')[1].split()
        Lhs = []
        Rhs = []

        for i in lhs:

            index = lhs.index(i)
            if i == '+' or i == '-':
                continue
            if lhs[index - 1] == '+' or lhs[index - 1] == '-':
                sign = lhs[index - 1]
            else:
                sign = '+'
            if '^' in i:
                power = int(i.split('^')[1])
                i = i.split('^')[0]
            else:
                power = 1
            num_coef_str = ''.join([j for j in i if j.isdigit()])

            variable = ''.join([j for j in i if j.isalpha()])
            Lhs.append(Term(sign, float(num_coef_str), variable, power))

        for i in rhs:

            index = rhs.index(i)
            if i == '+' or i == '-':
                continue
            if rhs[index - 1] == '+' or rhs[index - 1] == '-':
                sign = rhs[index - 1]
            else:
                sign = '+'
            if '^' in i:
                power = int(i.split('^')[1])
                i = i.split('^')[0]
            else:
                power = 1

            num_coef_str = ''.join([j for j in i if j.isdigit()])

            variable = ''.join([j for j in i if j.isalpha()])
            Rhs.append(Term(sign, float(num_coef_str), variable, power))

        eq = Equation()
        eq.LHS = Lhs
        eq.RHS = Rhs
        return eq

    def __repr__(self):
        var = ''
        if self.LHS != []:
            for i in self.LHS:
                var += i.get_sign() + " " + i.value().replace(i.get_sign(), '') + " "
        else:
            var += '0 '
        var += "= "
        if self.RHS != []:
            for i in self.RHS:
                var += i.get_sign() + " " + i.value().replace(i.get_sign(), '') + " "
        else:
            var += '0'
        return var

    def __str__(self):
        var = ''
        if self.LHS != []:
            for i in self.LHS:
                var += i.get_sign() + " " + i.value().replace(i.get_sign(), '') + " "
        else:
            var += '0 '
        var += "= "
        if self.RHS != []:
            for i in self.RHS:
                var += i.get_sign() + " " + i.value().replace(i.get_sign(), '') + " "
        else:
            var += '0'
        return var

