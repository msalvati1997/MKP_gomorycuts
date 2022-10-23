import solver
from docplex.mp.model import Model
from utils import MKPpopulate,  get_cut_stats
import sys



def solveCplex(instance) :
 # Call the function on a given instance
 c, A, b = MKPpopulate(instance)
 # Define the ranges for variables and constraints
 nCols, nRows = range(len(c)), range(len(b))
 # Create an empty model
 mkp = Model('Mkp')
 # Define decision variables
 x = mkp.binary_var_list(nCols, lb = 0, ub = 1, name = 'x')
 constraints = mkp.add_constraints(sum(A[i][j] * x[j] for j in nCols) <= b[i] for i in nRows)
 profit = mkp.sum(c[j] * x[j] for j in nCols)
 mkp.add_kpi(profit, 'profit')
 objective = mkp.maximize(profit)
 # Tweak some CPLEX parameters so that CPLEX has a harder time to
 # solve the model and our cut separators can actually kick in.
 params = mkp.parameters
 params.threads = 1
 params.mip.strategy.heuristicfreq = -1
 params.mip.cuts.mircut = -1
 params.mip.cuts.implied = -1
 #params.mip.cuts.gomory = -1  ##ONLY GOMORY CUTS 
 params.mip.cuts.flowcovers = -1
 params.mip.cuts.pathcut = -1
 params.mip.cuts.liftproj = -1
 params.mip.cuts.zerohalfcut = -1
 params.mip.cuts.cliques = -1
 params.mip.cuts.covers = -1
 
 mkp.solve()
 # Reporting results
 cuts=get_cut_stats(mkp)
 print(f"-- cuts stats ", cuts)
 print(f"-- total #cuts = {sum(nk for _, nk in cuts.items())}")
 mkp.report()
 with open("solutions/sol_"+instance.split("/")[1], "w") as solfile:
    solfile.write(mkp.solution.to_string())



if __name__ == '__main__':
    if len(sys.argv) == 1:
        solveCplex("istances/mknapcb1_1.txt")
    elif len(sys.argv) == 2:
        solveCplex(sys.argv[1])
    else:
        print("type  ::::python solver.py TESTNAME.txt::::")

