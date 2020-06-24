from pysmt.printers import HRPrinter
from pysmt.utils import quote
from pysmt.shortcuts import Or
def sort_key(l):
    return len(l.args())

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

    def walk_or(self, formula):
        args = sort_pysmt_form(formula.args())
        nw_or = Or(args)
        return HRPrinter.walk_or(self, nw_or)

    def walk_symbol(self, formula):
        self.write(quote(formula.symbol_name().replace("__", ""), style="'"))
