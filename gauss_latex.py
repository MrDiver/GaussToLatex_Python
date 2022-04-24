from typing import List
import numpy as np

class GaussSolution:
    def __init__(self, mat: np.ndarray, line_position: int):
        if len(mat.shape) > 2:
            raise Exception("Matrix has more than 2 dimensions")
        self.length = mat.shape[0]
        self.line_position = line_position
        self.mat = mat.copy()
        self.command_history: List[str] = []
        self.matrix_history: List[np.ndarray] = [self.mat.copy()]
    
    def mult(self, row_i: int, n:int):
        if self.length<=row_i:
            raise Exception(f"IndexOutOfBounds: Row {row_i} is not inside Matrix")
        self.mat[row_i, :] *= n
        self.command_history.append(f"\mult{{{row_i}}}{{\cdot {n}}}")
        self.matrix_history.append(self.mat.copy())
        
    def swap(self, row_i: int, row_j:int):
        if self.length<=row_i:
            raise Exception(f"IndexOutOfBounds: Row i {row_i} is not inside Matrix")
        if self.length<=row_j:
            raise Exception(f"IndexOutOfBounds: Row j {row_i} is not inside Matrix")

        tmp = self.mat[row_i,:].copy()
        self.mat[row_i,:] = self.mat[row_j,:]
        self.mat[row_j,:] = tmp
        self.command_history.append(f"\swap{{{row_i}}}{{{row_j}}}")
        self.matrix_history.append(self.mat.copy())
        
    def add(self, row_i: int, row_j:int, n:int = 1):
        if self.length<=row_i:
            raise Exception(f"IndexOutOfBounds: Row i {row_i} is not inside Matrix")
        if self.length<=row_j:
            raise Exception(f"IndexOutOfBounds: Row j {row_i} is not inside Matrix")

        self.mat[row_i,:] += n * self.mat[row_j,:]
        if n != 1:
            self.command_history.append(f"\\add[{n}]{{{row_i}}}{{{row_j}}}")
        else:
            self.command_history.append(f"\\add{{{row_i}}}{{{row_j}}}")
        self.matrix_history.append(self.mat.copy())
        
    def get_mat(self):
        return self.mat[:,:self.length]
    
    def get_solution(self):
        return self.mat[:,self.length:]
    
    def _get_mat_latex(self, mat:np.ndarray, comm:str = None):
        def if_int(n):
            if n%1.0!=0.0:
                return n
            else:
                return int(n)
    
        s = "\\begin{gmatrix}[p]\n"
        for row in mat:
            i = 0
            for e in row[:-1]:
                s += f"\t{if_int(e)}\t&"
                if self.line_position == i:
                    s += f"\\addline\t&"
                i += 1
            s += f"\t{if_int(row[-1])} \t\\\\\n"
        s = s[:-3] + "\n"
        
        if comm is not None:
            s += "\t\\rowops\n"
            s += f"\t{comm}\n"
            
        s += "\\end{gmatrix}"
        return s
        
    def get_latex_preamble(self):
        s = "% Put this in your preamble for matrix code to work\n"
        s += "\\usepackage{gauss}\n"
        s += r"\newcommand\addline{\span\omit\raisebox{-1.4ex}[1ex][1ex]{\makebox[0pt]{\hspace{2\arraycolsep}\rule{0.5pt}{1.1\baselineskip}}}\span\omit}" + "\n"
        return s
    
    def get_latex(self, columns = 2):
        s = "% Put this in your document\n"
        s += "\\begin{align*}\n"
        for i,(cmd, mat) in enumerate(zip(self.command_history,self.matrix_history)):
            # print(self._get_mat_latex(mat, cmd))
            if i % columns != 0:
                s += "&&"
            s += "&"
            s += self._get_mat_latex(mat, cmd) + "\n"
            s += "&\\rightarrow"
            if (i+1) % columns == 0:
                s += "\\\\"
            s += "\n"
        if len(self.matrix_history) % columns == 0:
            s += "&&"
        s += "&"+self._get_mat_latex(self.mat) + "\n"
        s += "\\end{align*}"
        return s
