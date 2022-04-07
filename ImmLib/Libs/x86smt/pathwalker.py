from sequenceanalyzer import SequenceAnalyzer

class UnsatPathConditionException(Exception):
    pass

class PathWalker:

    """
    A path walker that uses the SequenceAnalyzer to determine
    feasible paths.
    """
    
    def __init__(self, imm, debug=False):
        self.imm = imm
        self.debug = debug
        self.sa = None

    def getAnalysisResults(self, checker=None):
        if self.sa is None:
            raise Exception("You must use walk to perform analysis first")
        
        return self.sa.getAnalysisResults(checker)
    
    def walk(self, path, analysis_mods=[]):
        tail_bb = path.getTailBb()
        tail_bb_end_addr = tail_bb.end_addr

        self.sa = SequenceAnalyzer(self.imm, follow_jmps=False,
                              analysis_mods=analysis_mods)
        self.sa._debug = self.debug
        
        addr_idx = 0        
        while addr_idx < len(path) - 1:
            bb = path[addr_idx]
            addr = bb.start_addr
                
            next_bb = path[addr_idx + 1]
            next_addr = next_bb.start_addr

            if self.debug:
                self.imm.log("ANALYZE BB %s" % hex(bb.start_addr))
                
            if bb.end_op.isConditionalJmp() and \
               bb.end_op.getJmpAddr() == next_addr:
                self.sa.check_jcc_taken = True
                self.sa.check_jcc_not_taken = False
            elif bb.end_op.isConditionalJmp():
                self.sa.check_jcc_not_taken = True
                self.sa.check_jcc_taken = False

            self.sa.analyze(initialaddress=bb.start_addr,
                       stopEIP=bb.end_addr)
            
            if bb.end_op.isConditionalJmp():
                end_str = hex(bb.end_addr)
                next_str = hex(next_addr)
                
                if bb.end_op.getJmpAddr() == next_addr:
                    if self.sa.jcc_taken:
                        if self.debug:
                            self.imm.log("Valid transition from %s to %s" % \
                                (end_str, next_str), bb.end_addr)
                        self.sa.assert_jcc_taken(bb.end_op.getJmpAddr(),
                                           bb.end_addr)                       
                    else:
                        msg = "Infeasible path transition from %s to %s" % \
                            (end_str, next_str)
                        raise UnsatPathConditionException(msg)
                else:
                    if self.sa.jcc_not_taken:
                        if self.debug:
                            self.imm.log("Valid transition from %s to %s" % \
                                (end_str, next_str), bb.end_addr)
                        self.sa.assert_jcc_not_taken()
                    else:
                        msg = "Infeasible path transition from %s to %s" % \
                            (end_str, next_str)
                        raise UnsatPathConditionException(msg)
                    
            self.sa.state.EIP = self.sa.state.solver.lookupVar("EIP")[0]                                    
            addr_idx += 1

        # The final basic block isn't checked within the above loop
        self.sa.analyze(initialaddress=path[-1].start_addr,
                   stopEIP=path[-1].start_addr)
