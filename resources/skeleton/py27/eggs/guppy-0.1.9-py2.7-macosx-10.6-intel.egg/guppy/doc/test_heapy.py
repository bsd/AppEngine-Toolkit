# Tests generated by: guppy.gsl.Tester
# Main source file: /home/sverker/guppy/specs/genguppy.gsl
# Date: Tue Jun 23 16:15:55 2009
class Tester:
    tests = {}
    def get_ex_1(self):
        class C:
            pass
        return C
    def get_ex_2(self):
        class C:
            pass
        return C
    def get_ex_3(self):
        class C:
            pass
        return C
    def get_ex_4(self):
        import sys
        return id(sys)
    def get_ex_5(self):
        class C:
         pass
        return self.hp.Clodo(dictof=C)
    def get_ex_6(self):
        import os
        return os.path.join(os.path.dirname(__file__),'profileexample.hpy')
    def get_ex_7(self):
        import os
        return open(os.path.join(os.path.dirname(__file__),'profileexample.hpy'))
    def get_ex_8(self):
        import os
        return os.path.join(os.path.dirname(__file__),'profileexample.hpy')
    def test_Use(self, arg):
        t0 = arg.Size(0)
        t1 = arg.Nothing
        t2 = arg.Via()
        t3 = arg.Via('[0]')
        t4 = arg.Via('.a')
        t5 = arg.Root
        t6 = arg.Rcs()
        t7 = arg.Rcs(self.get_ex_5())
        t8 = arg.Rcs(self.hp.Clodo.sokind(int)(dictof=()))
        t9 = arg.Type(int)
        t10 = arg.heap()
        t11 = arg.heapg()
        t12 = arg.idset([1])
        t13 = arg.iso()
        t14 = arg.iso(())
        t15 = arg.findex()
        t16 = t15(0)
        t17 = arg.findex(self.hp.Anything)
        t18 = t17(0)
        t19 = arg.heapu()
        t20 = arg.load(self.get_ex_6())
        t21 = arg.load(self.get_ex_7())
        t22 = arg.load(self.get_ex_6(), use_readline=True)
        t23 = arg.load(self.get_ex_7(), use_readline=True)
        t24 = arg.Anything
        t25 = arg.Class(int)
        t26 = arg.Class(self.get_ex_1())
        t27 = arg.Module()
        t28 = arg.Module(name='sys')
        t29 = arg.Module(at=self.get_ex_4())
        t30 = arg.Module(name='sys', at=self.get_ex_4())
        t31 = arg.Unity()
        t32 = arg.Clodo(int)
        t33 = arg.Clodo(self.get_ex_2())
        t34 = arg.Clodo(dictof=())
        t35 = arg.Clodo(dictof=self.get_ex_3())
        t36 = arg.Id(id(None))
        t37 = arg.doc
        t38 = arg.monitor()
        t39 = arg.pb()
        t40 = arg.pb(self.get_ex_8())
        t41 = arg.setref()
        t42 = arg.setrelheap()
        t43 = arg.setrelheap(self.hp.Nothing)
        t44 = arg.setrelheapg()
        t45 = arg.setrelheapg(self.hp.Nothing)
        t46 = arg.setrelheapu()
        t47 = arg.setrelheapu(self.hp.Nothing)
    tests['.tgt.heapykinds.Use'] = test_Use
