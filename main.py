import numpy as np
from gauss_latex import GaussSolution

def main():
    mat = np.array([[ 2,  5,  7, 1, 0 ,0],
                    [ 6,  3,  4, 0, 1, 0],
                    [ 5, -2, -3, 0, 0, 1]])
        
    solver = GaussSolution(mat, 4)
    solver.add(0,2)
    solver.add(0,1,-1)
    solver.add(1,2,-1)
    solver.add(1,0,-1)
    solver.add(2,0,-5)
    solver.add(1,2,2)
    solver.add(2,1,2)
    solver.add(1,2)
    solver.mult(2,-1)
    # print(solver.mat)
    # print(solver.get_mat())
    # print(solver.get_solution())
    # for cmd in solver.command_history:
        # print(cmd)
    
    print(solver.get_latex())
    # print(solver.get_latex_preamble())

if __name__ == "__main__":
    main()
