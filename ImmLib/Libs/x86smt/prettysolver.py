"""
Here we support Expression and Type classes which work as wrappers against the PrettySolver class (which is itself a wrapper around Solver).

Doing so, we can support native python operators over Solver Expressions:
- All comparision expressions are supported (doing a queryFormula over the comparision if we are in a boolean context)
- Conversion to boolean only returns True if it's a VALID answer.
- All arithmetical and logical operations are supported (if you're working with BOOLEAN expressions it uses the appropiate boolean operations)
- It allows you to interact with non-expression operands by casting them to Expression instances where possible:
  - int/longs to constExpr
  - strings to varDef
  - tuples to loadExpr
  - boolean to trueExpr/falseExpr
- It imports expressions from other solver instances automatically
- len(expr) returns the number of bits on a BV (it returns None if BOOLEAN)
- allows slice getting/setting: expr[0:16] returns the lower 16bits of a BV
- cast to int/long if the expression can be evaluated to a constant
- some handy methods were added:
  - vars() return all variable expressions that are involved in the current expression
  - varsnames() same but return the names, no the expressions
  - dump() same as dumpExpr(self)
  - load() set the current expression with a dump
  - other stuff...
"""

from solver_cvc3 import Solver
global psolvers
psolvers={}

class Expression():
    def __init__(self, psolver, addr=None):
        self.psolver = psolver
        self.addr = addr
        self.lang = 0
        self.hash = None
    
    def __getstate__(self):
        """
        Pretty Solvers should not be copied, deepcopied or pickled, so we maintain a global list of already initialized psolvers.
        """
        
        global psolvers
        psolvers[id(self.psolver)]=self.psolver
        return (id(self.psolver), self.addr, self.lang, self.hash)
    
    def __setstate__(self, dump):
        global psolvers
        (tmp, self.addr, self.lang, self.hash) = dump
        self.psolver=psolvers[tmp]
    
    def __str__(self):
        return self.psolver.exprString(self)
    
    def __repr__(self):
        return "<Expression '%s'>"%self.psolver.exprString(self)
    
    def __hash__(self):
        if self.hash == None:
            self.hash=self.psolver.hashExpr(self)
        return self.hash
    
    def _query_(self, exp):
        self.psolver.push()
        res=self.psolver.queryFormula(exp)
        self.psolver.pop()
        if res == 0:
            return False
        elif res == 1:
            return True
        else:
            return None
    
    def convertToExpr(self, b):
        if isinstance(b, Expression):
            if self.psolver.solver.vc != b.psolver.solver.vc:
                b=self.psolver.importExpr(b)
            return b
        
        if isinstance(b, int) or isinstance(b, long):
            return self.psolver.constExpr(b, self.psolver.getBitSizeFromExpr(self))
        
        if isinstance(b, tuple):
            return self.psolver.loadExpr(b)
        
        if isinstance(b, bool) or (isinstance(b, str) and (b.lower() == "true" or b.lower() == "false")):
            if isinstance(b, str):
                if b.lower() == "true": b=True
                else: b=False
            
            if b:
                return self.psolver.trueExpr()
            else:
                return self.psolver.falseExpr()
            
        if isinstance(b, str):
            tmp=self.psolver.lookupVar(b)
            if tmp:
                return tmp[0]
            return self.psolver.varExpr(b)
        
        raise Exception, "Dont know how to convert this to an Expression"
    
    def __eq__(self, b):
        if b == None: return False
        b=self.convertToExpr(b)
        kind=self.psolver.getKind(self.psolver.getType(self))
        if kind == self.psolver.solver._BOOLEAN:
            exp = self.psolver.iffExpr(self, b)
        else:
            exp = self.psolver.eqExpr(self, b)
        return exp
    
    def __ne__(self, b):
        if b == None: return True
        b=self.convertToExpr(b)
        kind=self.psolver.getKind(self.psolver.getType(self))
        if kind == self.psolver.solver._BOOLEAN:
            exp = self.psolver.boolNotExpr(self.psolver.iffExpr(self, b))
        else:
            exp = self.psolver.boolNotExpr(self.psolver.eqExpr(self, b))
        return exp
    
    def __lt__(self, b):
        b=self.convertToExpr(b)
        return self.psolver.ltExpr(self, b)
    
    def __le__(self, b):
        b=self.convertToExpr(b)
        return self.psolver.leExpr(self, b)
    
    def __gt__(self, b):
        b=self.convertToExpr(b)
        return self.psolver.gtExpr(self, b)
    
    def __ge__(self, b):
        b=self.convertToExpr(b)
        return self.psolver.geExpr(self, b)
    
    def __nonzero__(self):
        self.simplify()
        kind=self.psolver.getKind(self.psolver.getType(self))
        if kind == self.psolver.solver._BOOLEAN:
            return self._query_(self)
        else:
            return self._query_(self.psolver.neExpr(self, self.psolver.constExpr(0, self.psolver.getBitSizeFromExpr(self))))
    
    def __len__(self):
        return self.psolver.getBitSizeFromExpr(self)
    
    def __getitem__(self, key):
        if isinstance(key, Expression):
            key=key.__int__()
            if key == None: raise TypeError
        
        if isinstance(key, int) or isinstance(key, long):
            stop = key
            start = key
        else:
            start=key.start
            stop=key.stop-1
        if start == None: start=0
        if stop == 0x7FFFFFFE: stop = self.__len__()-1
        if start < 0 or stop < 0:
            bits=self.psolver.getBitSizeFromExpr(self)
            if start < 0: start = bits + start
            if stop < 0: stop = bits + stop
        
        tmp=self.psolver.extractExpr(self, start, stop)
        tmp.simplify()
        return tmp
    
    def __setitem__(self, key, value):
        if isinstance(key, Expression):
            key=key.__int__()
            if key == None: raise TypeError
        
        value=self.convertToExpr(value)
        
        if isinstance(key, int) or isinstance(key, long):
            stop = key
            start = key
        else:
            start=key.start
            stop=key.stop-1
        if start == None: start=0
        if stop == 0x7FFFFFFE: stop = self.__len__()-1
        if start < 0 or stop < 0:
            bits=self.psolver.getBitSizeFromExpr(self)
            if start < 0: start = bits + start
            if stop < 0: stop = bits + stop

        size=stop-start+1
        if len(value) > size:
            chunk=self.psolver.extractExpr(value, start, stop)
        elif len(value) < size:
            chunk=self.psolver.zeroExtendExpr(value, size)
        else:
            chunk=value
            
        self.addr=self.psolver.assignExpr(self, chunk, size, start).addr
        self.simplify()
    
    def __add__(self, b):
        b=self.convertToExpr(b)
        tmp = self.psolver.addExpr(self, b); tmp.simplify()
        return tmp
    
    def __sub__(self, b):
        b=self.convertToExpr(b)
        tmp = self.psolver.subExpr(self, b); tmp.simplify()
        return tmp
    
    def __floordiv__(self, b):
        b=self.convertToExpr(b)
        tmp = self.psolver.udivExpr(self, b); tmp.simplify()
        return tmp
    
    def __div__(self, b):
        b=self.convertToExpr(b)
        tmp = self.psolver.udivExpr(self, b); tmp.simplify()
        return tmp
    
    def __mod__(self, b):
        b=self.convertToExpr(b)
        tmp = self.psolver.uremExpr(self, b); tmp.simplify()
        return tmp
    
    def __mul__(self, b):
        b=self.convertToExpr(b)
        tmp = self.psolver.umulExpr(self, b); tmp.simplify()
        return tmp
    
    def __lshift__(self, b):
        if isinstance(b, int) or isinstance(b, long):
            tmp = self.psolver.leftShiftExpr(self, b); tmp.simplify()
            return tmp
        b=self.convertToExpr(b)
        tmp = self.psolver.leftShiftExpr(self, b); tmp.simplify()
        return tmp
    
    def __rlshift__(self, b):
        return self.__lshift__(b)
    
    def __rshift__(self, b):
        if isinstance(b, int) or isinstance(b, long):
            tmp = self.psolver.rightShiftExpr(self, b); tmp.simplify()
            return tmp
        b=self.convertToExpr(b)
        tmp = self.psolver.rightShiftExpr(self, b); tmp.simplify()
        return tmp
    
    def __rrshift__(self, b):
        return self.__rshift__(b)
    
    def __and__(self, b):
        b=self.convertToExpr(b)
        kind=self.psolver.getKind(self.psolver.getType(self))
        if kind == self.psolver.solver._BOOLEAN:
            tmp = self.psolver.boolAndExpr(self, b); tmp.simplify()
            return tmp
        else:
            tmp = self.psolver.andExpr(self, b); tmp.simplify()
            return tmp
    
    def __xor__(self, b):
        b=self.convertToExpr(b)
        kind=self.psolver.getKind(self.psolver.getType(self))
        if kind == self.psolver.solver._BOOLEAN:
            tmp = self.psolver.boolXorExpr(self, b); tmp.simplify()
            return tmp
        else:
            tmp = self.psolver.xorExpr(self, b); tmp.simplify()
            return tmp
    
    def __or__(self, b):
        b=self.convertToExpr(b)
        kind=self.psolver.getKind(self.psolver.getType(self))
        if kind == self.psolver.solver._BOOLEAN:
            tmp = self.psolver.boolOrExpr(self, b); tmp.simplify()
            return tmp
        else:
            tmp = self.psolver.orExpr(self, b); tmp.simplify()
            return tmp
    
    def __invert__(self):
        kind=self.psolver.getKind(self.psolver.getType(self))
        if kind == self.psolver.solver._BOOLEAN:
            tmp = self.psolver.boolNotExpr(self); tmp.simplify()
            return tmp
        else:
            tmp = self.psolver.notExpr(self); tmp.simplify()
            return tmp
    
    def __neg__(self):
        tmp = self.psolver.negExpr(self); tmp.simplify()
        return tmp
    
    def __int__(self):
        self.simplify()
        tmp=self.psolver.UConstFromExpr(self)
        if tmp==None:
            raise ValueError, "The expression cannot be evaluated as a constant number"
        return tmp
    
    def __long__(self):
        self.simplify()
        tmp=self.psolver.UConstFromExpr(self)
        if tmp==None:
            raise ValueError, "The expression cannot be evaluated as a constant number"
        return tmp
    
    def vars(self):
        """
        return the variables found in this expression
        """
        return self.psolver.getVarDependency(self, False)
    
    def varsnames(self):
        """
        return the variable's names found in this expression
        """
        return self.psolver.getVarDependency(self, True)
    
    def isSkolem(self):
        return self.psolver.isSkolem(self)
    
    def isClosure(self):
        return self.psolver.isClosure(self)
    
    def existential(self):
        return self.psolver.getExistential(self)

    def kind(self):
        return self.psolver.getKind(self)
    
    def dump(self):
        return self.psolver.dumpExpr(self)
    
    def load(self, dump):
        #this hack allows us to avoid the creation of a new Expression instance
        self.addr = self.psolver.solver.loadExpr(dump)
        self.hash=None

    def simplify(self):
        #this hack allows us to avoid the creation of a new Expression instance
        self.addr = self.psolver.solver.simplify(self.addr)
        self.hash=None
    
    def zeroExtend(self, bits):
        self.addr = self.psolver.solver.zeroExtendExpr(self.addr, bits)
        self.hash=None

    def signExtend(self, bits):
        self.addr = self.psolver.solver.signExtendExpr(self.addr, bits)
        self.hash=None

    def isConstant(self):
        self.simplify()
        tmp=self.psolver.UConstFromExpr(self)
        if tmp == None:
            return False
        return True
    
    def merge(self, mergeDict):
        tmp=self.psolver.mergeExpr(self, mergeDict)
        tmp.simplify()
        return tmp


class Type():
    def __init__(self, psolver, addr=None):
        self.psolver = psolver
        self.addr = addr
        
        
class PrettySolver():
    def __init__(self, solver=None, debug=False):
        if not solver:
            self.solver = Solver()
        else:
            self.solver = solver
        self.initCommonTypes()
        
        self.solver.DEBUG = debug
    
    def setDebug(debug):
        self.solver.DEBUG = debug
        
    def initCommonTypes(self):
        self.bv32bits=self.bvType(32)
        self.bv16bits=self.bvType(16)
        self.bv8bits=self.bvType(8)
        self.booltype=self.boolType()
        self.true=self.trueExpr()
        self.false=self.falseExpr()

    def createExpression(self, addr=None):
        return Expression(self, addr)
        
    def assertFormula(self, exp):
        self.solver.assertFormula(exp.addr)

    def queryFormula(self, exp):
        return self.solver.queryFormula(exp.addr)

    def checkUnsat(self, exp):
        return self.solver.checkUnsat(exp.addr)

    def checkContinue(self):
        return self.solver.checkContinue(exp.addr)

    def restart(self, exp):
        return self.solver.restart(exp.addr)

    def returnFromCheck(self):
        self.solver.returnFromCheck()

    def getCounterExample(self):
        ret=[]
        for e in self.solver.getCounterExample():
            ret.append(Expression(self, e))
        return ret

    def getConcreteModel(self):
        ret=[]
        for e in self.solver.getConcreteModel():
            ret.append(Expression(self, e))
        return ret

    def getUserAssumptions(self):
        ret=[]
        for e in self.solver.getUserAssumptions():
            ret.append(Expression(self, e))
        return ret

    def getInternalAssumptions(self):
        ret=[]
        for e in self.solver.getInternalAssumptions():
            ret.append(Expression(self, e))
        return ret

    def getAssumptions(self):
        ret=[]
        for e in self.solver.getAssumptions():
            ret.append(Expression(self, e))
        return ret

    def getAxioms(self, exp):
        ret=[]
        for e in self.solver.getAxioms(exp.addr):
            ret.append(Expression(self, e))
        return ret

    def getIndex(self, exp):
        return self.solver.getIndex(exp.addr)

    def getExistential(self, exp):
        return Expression(self, self.solver.getExistential(exp.addr))

    def getNumVars(self, exp):
        return self.solver.getNumVars(exp.addr)

    def getVar(self, exp, ind):
        return Expression(self, self.solver.getVar(exp.addr, ind))

    def getArity(self, exp):
        return self.solver.getArity(exp.addr)

    def getChild(self, exp, ind):
        return Expression(self, self.solver.getChild(exp.addr, ind))

    def getBody(self, exp):
        return Expression(self, self.solver.getBody(exp.addr))

    def getKind(self, exp):
        return self.solver.getKind(exp.addr)

    def getClosure(self):
        return Expression(self, self.solver.getClosure())

    def isClosure(self, exp):
        return self.solver.isClosure(exp.addr)

    def isSkolem(self, exp):
        return self.solver.isSkolem(exp.addr)

    def getBoundIndex(self, exp):
        return self.solver.getBoundIndex(exp.addr)
    
    def getFunction(self, exp):
        return Expression(self, self.solver.getFunction(exp.addr))
        
    def incomplete(self):
        return self.solver.incomplete()

    def getProof(self):
        return Expression(self, self.solver.getProof())

    #Context methods
    def stackLevel(self):
        return self.solver.stackLevel()

    def push(self):
        return self.solver.push()

    def pop(self):
        return self.solver.pop()

    def popto(self, level):
        return self.solver.popto(level)

    #Misc functions
    def deleteExpr(self,exp):
        self.solver.deleteExpr(exp.addr)

    def importExpr(self, exp):
        return Expression(self, self.solver.importExpr(exp.addr))

    #returns a simplified Expr
    def simplify(self, exp):
        return Expression(self, self.solver.simplify(exp.addr))

    def parseFile(self, filename):
        self.solver.parseFile(filename)

    #returns a new Bit-Vector Type of <bits> bits
    def bvType(self, bits=32):
        return Type(self, self.solver.bvType(bits))

    def boolType(self):
        return Type(self, self.solver.boolType())

    def boundVarExpr(self, name, uid, vartype=None):
        if vartype: vartype = vartype.addr
        return Expression(self, self.solver.boundVarExpr(name, uid, vartype))
    
    #returns a variable Expr
    def varExpr(self, name, vartype=None):
        if vartype: vartype = vartype.addr
        return Expression(self, self.solver.varExpr(name, vartype))

    #returns a variable Expr initialized with a given Expr
    def varDefExpr(self, name, definition, vartype=None):
        if vartype: vartype = vartype.addr
        return Expression(self, self.solver.varDefExpr(name, definition.addr, vartype))

    def createTypeFromString(self, typename):
        return Type(self, self.solver.createTypeFromString(typename))
    
    def lookupVar(self, name):
        tmp=self.solver.lookupVar(name)
        if not tmp:
            return tmp
        return (Expression(self, tmp[0]), Type(self, tmp[1]))

    #Utils
    def compareExpr(self, exp1, exp2):
        return self.solver.compareExpr(exp1.addr, exp2.addr)

    def exprFromString(self, stri):
        return Expression(self, self.solver.exprFromString(stri))

    def exprFromStringAndLang(self, stri, lang):
        return Expression(self, self.solver.exprFromStringAndLang(stri, lang))

    def exprString(self, exp, lang=None):
        if lang == None: lang = exp.lang
        return self.solver.exprString(exp.addr, lang)

    def getType(self, exp):
        return Type(self, self.solver.getType(exp.addr))

    def getName(self, exp):
        return self.solver.getName(exp.addr)
    
    def getUid(self, exp):
        return self.solver.getUid(exp.addr)

    def typeString(self, t):
        return self.solver.typeString(t.addr)

    def typeStringFromExpr(self, exp):
        return self.solver.typeStringFromExpr(exp.addr)

    def getBitSizeFromExpr(self, exp):
        return self.solver.getBitSizeFromExpr(exp.addr)

    def getKindString(self, kind):
        return self.solver.getKindString(kind)

    def kindString(self, exp):
        return self.solver.kindString(exp.addr)

    def getBoolFromBitvector(self, exp):
        return Expression(self, self.solver.getBoolFromBitvector(exp.addr))

    def getBitvectorFromBool(self, exp, bits=1):
        return Expression(self, self.solver.getBitvectorFromBool(exp.addr))
    
    def skolemizeVar(self, exp, idx):
        return Expression(self, self.solver.skolemizeVar(exp.addr, idx))
    
    def skolemize(self, exp, boundVars, skolemVars):
        r_boundVars = []
        r_skolemVars = []
        for e in boundVars:
            r_boundVars.append(e.addr)
        for e in skolemVars:
            r_skolemVars.append(e.addr)
        return Expression(self, self.solver.skolemize(exp.addr, r_boundVars, r_skolemVars))
    
    def getInt(self, exp):
        return self.solver.getInt(exp.addr)

    #Logic functions
    def impliesExpr(self, hyp, concl):
        return Expression(self, self.solver.impliesExpr(hyp.addr, concl.addr))

    def iffExpr(self, exp1, exp2):
        return Expression(self, self.solver.iffExpr(exp1.addr, exp2.addr))

    def distinctExpr(self, arr_expr):
        tmp=[]
        for e in arr_expr:
            tmp.append(e.addr)
        return Expression(self, self.solver.distinctExpr(tmp))

    def forallExpr(self, Bvars, exp):
        tmp=[]
        for e in Bvars:
            tmp.append(e.addr)
        return Expression(self, self.solver.forallExpr(tmp, exp.addr))
    
    def existsExpr(self, Bvars, exp):
        tmp=[]
        for e in Bvars:
            tmp.append(e.addr)
        return Expression(self, self.solver.existsExpr(tmp, exp.addr))

    def lambdaExpr(self, Bvars, exp):
        tmp=[]
        for e in Bvars:
            tmp.append(e.addr)
        return Expression(self, self.solver.lambdaExpr(tmp, exp.addr))
    
    def iteExpr(self, ifpart, thenpart, elsepart):
        return Expression(self, self.solver.iteExpr(ifpart.addr, thenpart.addr, elsepart.addr))

    def trueExpr(self):
        return Expression(self, self.solver.trueExpr())

    def falseExpr(self):
        return Expression(self, self.solver.falseExpr())

    def boolNotExpr(self, exp):
        return Expression(self, self.solver.boolNotExpr(exp.addr))

    def boolAndExpr(self, exp1, exp2):
        return Expression(self, self.solver.boolAndExpr(exp1.addr, exp2.addr))

    def boolOrExpr(self, exp1, exp2):
        return Expression(self, self.solver.boolOrExpr(exp1.addr, exp2.addr))

    def boolXorExpr(self, exp1, exp2):
        return Expression(self, self.solver.boolXorExpr(exp1.addr, exp2.addr))
    
    #Order functions
    def ltExpr(self, exp1, exp2):
        return Expression(self, self.solver.ltExpr(exp1.addr, exp2.addr))

    def leExpr(self, exp1, exp2):
        return Expression(self, self.solver.leExpr(exp1.addr, exp2.addr))

    def gtExpr(self, exp1, exp2):
        return Expression(self, self.solver.gtExpr(exp1.addr, exp2.addr))

    def geExpr(self, exp1, exp2):
        return Expression(self, self.solver.geExpr(exp1.addr, exp2.addr))

    def sltExpr(self, exp1, exp2):
        return Expression(self, self.solver.sltExpr(exp1.addr, exp2.addr))

    def sleExpr(self, exp1, exp2):
        return Expression(self, self.solver.sleExpr(exp1.addr, exp2.addr))

    def sgtExpr(self, exp1, exp2):
        return Expression(self, self.solver.sgtExpr(exp1.addr, exp2.addr))

    def sgeExpr(self, exp1, exp2):
        return Expression(self, self.solver.sgeExpr(exp1.addr, exp2.addr))

    def eqExpr(self, exp1, exp2):
        return Expression(self, self.solver.eqExpr(exp1.addr, exp2.addr))

    def neExpr(self, exp1, exp2):
        return Expression(self, self.solver.neExpr(exp1.addr, exp2.addr))

    #Bit-Vector functions
    def UConstFromExpr(self, exp):
        return self.solver.UConstFromExpr(exp.addr)

    def constExpr(self, num, bits=32):
        return Expression(self, self.solver.constExpr(num, bits))

    def concatExpr(self, exp1, exp2):
        return Expression(self, self.solver.concatExpr(exp1.addr, exp2.addr))

    def extractExpr(self, exp, start, end):
        return Expression(self, self.solver.extractExpr(exp.addr, start, end))

    def boolExtractExpr(self, exp, bit):
        return Expression(self, self.solver.boolExtractExpr(exp.addr, bit))

    def signExtendExpr(self, exp, bits):
        return Expression(self, self.solver.signExtendExpr(exp.addr, bits))

    def zeroExtendExpr(self, exp, bits):
        return Expression(self, self.solver.zeroExtendExpr(exp.addr, bits))

    #the <bits> here might be an expression or a constant amount
    def leftRotateExpr(self, exp, bits):
        if isinstance(bits, Expression): bits=bits.addr
        return Expression(self, self.solver.leftRotateExpr(exp.addr, bits))

    #the <bits> here might be an expression or a constant amount
    def leftShiftExpr(self, exp, bits, finalsize=None):
        if isinstance(bits, Expression): bits=bits.addr
        return Expression(self, self.solver.leftShiftExpr(exp.addr, bits, finalsize))

    #the <bits> here might be an expression or a constant amount
    def rightArithmeticShiftExpr(self, exp, bits, finalsize=None):
        if isinstance(bits, Expression): bits=bits.addr
        return Expression(self, self.solver.rightArithmeticShiftExpr(exp.addr, bits, finalsize))

    #the <bits> here might be an expression or a constant amount
    def rightRotateExpr(self, exp, bits):
        if isinstance(bits, Expression): bits=bits.addr
        return Expression(self, self.solver.rightRotateExpr(exp.addr, bits))

    #the <bits> here might be an expression or a constant amount
    def rightShiftExpr(self, exp, bits, finalsize=None):
        if isinstance(bits, Expression): bits=bits.addr
        return Expression(self, self.solver.rightShiftExpr(exp.addr, bits, finalsize))

    def notExpr(self, exp):
        return Expression(self, self.solver.notExpr(exp.addr))

    def andExpr(self, exp1, exp2):
        return Expression(self, self.solver.andExpr(exp1.addr, exp2.addr))

    def orExpr(self, exp1, exp2):
        return Expression(self, self.solver.orExpr(exp1.addr, exp2.addr))

    def xorExpr(self, exp1, exp2):
        return Expression(self, self.solver.xorExpr(exp1.addr, exp2.addr))

    def negExpr(self, exp):
        return Expression(self, self.solver.negExpr(exp.addr))

    def addExpr(self, exp1, exp2, bits=None):
        return Expression(self, self.solver.addExpr(exp1.addr, exp2.addr))

    def subExpr(self, exp1, exp2, bits=None):
        return Expression(self, self.solver.subExpr(exp1.addr, exp2.addr))

    def umulExpr(self, exp1, exp2, bits=None):
        return Expression(self, self.solver.umulExpr(exp1.addr, exp2.addr, bits))

    def udivExpr(self, exp1, exp2):
        return Expression(self, self.solver.udivExpr(exp1.addr, exp2.addr))

    def uremExpr(self, exp1, exp2):
        return Expression(self, self.solver.uremExpr(exp1.addr, exp2.addr))

    def sdivExpr(self, exp1, exp2):
        return Expression(self, self.solver.sdivExpr(exp1.addr, exp2.addr))

    def sremExpr(self, exp1, exp2):
        return Expression(self, self.solver.sremExpr(exp1.addr, exp2.addr))

    def smodExpr(self, exp1, exp2):
        return Expression(self, self.solver.smodExpr(exp1.addr, exp2.addr))

    def smulExpr(self, exp1, exp2, bits=None):
        return Expression(self, self.solver.smulExpr(exp1.addr, exp2.addr, bits))

    def assignExpr(self, exp1, exp2, bits=None, endpos=0, pos=0, endbits=None):
        return Expression(self, self.solver.assignExpr(exp1.addr, exp2.addr, bits, endpos, pos, endbits))

    def dumpExpr(self, exp, recursive=False, calchash=False):
        tmp=self.solver.dumpExpr(exp.addr, recursive, calchash)
        self.crc=self.solver.crc
        return tmp
    
    def loadExpr(self, dump, recursive=False, varsdict=None):
        if varsdict:
            tmp={}
            for k,v in varsdict.iteritems():
                tmp[k]=v.addr
            varsdict=tmp
        return Expression(self, self.solver.loadExpr(dump, recursive, varsdict))

    def getVarDependency(self, exp, return_name=False):
        tmp=self.solver.getVarDependency(exp.addr, return_name)
        if return_name:
            return tmp
        ret=[]
        for e in tmp:
            ret.append(Expression(self, e))
        return ret
    
    def hashExpr(self, exp):
        return self.solver.hashExpr(exp.addr)
    
    def mergeExpr(self, exp, varsdict):
        tmp={}
        for k,v in varsdict.iteritems():
            tmp[k]=v.addr
        return Expression(self, self.solver.mergeExpr(exp.addr, tmp))

def mymain():
    sol=PrettySolver()
    sol2=PrettySolver()
    
    v1 = sol.varExpr("v1")
    d = v1.dump()
    
    newvar = sol.createExpression()
    newvar.load(d)
    
    newvar+="v1" #mixed operands work as expected
    
    print v1 > newvar #non-boolean context, it returns a comparision expression
    if v1 == v1: #boolean context, a queryFormula is executed here
        print "GRINGO!"
    
    #sol.assertFormula(v1 == 1) #mixed operands, 1 converted to constExpr
    
    #print newvar[v1] #returns a 1 bit extraction on index 1 because the previous assert
    
    newvar2 = sol2.createExpression()
    newvar2.load(d)
    
    a=newvar2 + v1
    c=v1 + v1
    
    print a.psolver
    print v1.psolver
    
    b={}
    b[a]=True
    print hash(a)
    print a
    print c
    print hash(c)
    
    print "******"
    a=sol.constExpr(0xcafecafe)
    
    
    print (a*2)[0:32]
    print repr(a)

#mymain()
