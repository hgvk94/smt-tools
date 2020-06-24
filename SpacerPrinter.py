from pysmt.printers import HRPrinter
from pysmt.utils import quote
from pysmt.shortcuts import Or, get_formula_size, Equals
def sort_key(l):
    return get_formula_size(l)

def sort_pysmt_form(l):
    return sorted(l, key=sort_key)

class SpacerPrinter(HRPrinter):
    def __init__(self, stream):
        HRPrinter.__init__(self, stream)

    #copy paste the implementation of walk_nary from HRPrinter
    #do not know how to wait for yield to finish and then print \n
    def walk_nary_with_nl(self, formula, ops):
        self.write('(')
        args = formula.args()
        args = sort_pysmt_form(args)
        for s in args[:-1]:
            yield s
            self.write('\n')
            self.write(ops)
        yield args[-1]
        self.write(')\n')

    def walk_and(self, formula):
        return self.walk_nary_with_nl(formula, "& ")

    def walk_equals(self, formula):
        args = formula.args()
        f = args[0]
        rhs = args[1]
        f_args = f.args()
        if f.is_plus() and len(f_args) == 2:
            rhs_zero = rhs.is_real_constant(0)
            s_arg = f_args[1]
            is_mone = s_arg.is_times() and s_arg.args()[0].is_real_constant(-1)
            if rhs_zero and is_mone:
                nw_eq = Equals(f_args[0], s_arg.args()[1])
                return HRPrinter.walk_equals(self, nw_eq)
        return HRPrinter.walk_equals(self, formula)

    def walk_or(self, formula):
        args = sort_pysmt_form(formula.args())
        nw_or = Or(args)
        return HRPrinter.walk_or(self, nw_or)

    def walk_symbol(self, formula):
        self.write(quote(formula.symbol_name().replace("__", ""), style="'"))
