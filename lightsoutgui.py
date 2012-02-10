# coding: utf-8

import sys
import Tkinter as tk
from itertools import product

import numpy as np

import lightsout

max_size = 9
button_size = 23

class ButtonGrid(tk.Frame, object):
    
    def __init__(self, master, callback=None):
        tk.Frame.__init__(self, master)
        
        buttons = [[None]*max_size for i in xrange(max_size)]
        buttons_pos = {}
        for r,c in product(xrange(max_size), xrange(max_size)):
            buttons[r][c] = tk.Label(self, bitmap="gray12", bg="red",
                                width=button_size, height=button_size)
            buttons_pos[buttons[r][c]] = (r,c)
        
        for btn in sum(buttons, []):
            btn.bind("<Button-1>", self.button_pressed)
        
        self.buttons = buttons
        self.buttons_pos = buttons_pos
        self.callback = callback
    
    def set_size(self, size):
        size = int(size)
        
        self._size = size
        
        for btn in sum(self.buttons, []):
            btn.grid_forget()
        
        for r,c in product(xrange(size), xrange(size)):
            self.buttons[r][c].grid(row=r, column=c, padx=2, pady=2)
        # Clear the solution.
        if self.callback is not None:
            self.callback(self.get_board())
    
    def button_pressed(self, event):
        if event.widget["bg"] == "red":
            event.widget["bg"] = "green"
        else:
            event.widget["bg"] = "red"
        if self.callback is not None:
            self.callback(self.get_board())
    
    def get_board(self):
        
        board = map(lambda x:x["bg"]=="green", sum(self.buttons, []))
        board = np.reshape(board, (max_size, max_size))
        return board[:self._size, :self._size]
    
    def set_solution(self, solution):
        if solution is None:
            for btn in sum(self.buttons, []):
                btn["bitmap"] = "gray12"
            return
        
        assert solution.shape[0]==solution.shape[1]==self._size
        
        for r,c in product(xrange(self._size), xrange(self._size)):
            if solution[r,c]:
                self.buttons[r][c]["bitmap"] = "gray75"
            else:
                self.buttons[r][c]["bitmap"] = "gray12"
    
    size = property(lambda self: self._size, set_size)


class App(tk.Frame):
    
    def __init__(self, master):
        tk.Frame.__init__(self, master, width=1000, height=1000)
        self.pack(fill="both")
        
        buttongrid = ButtonGrid(self, callback=self.solve)
        
        scale = tk.Scale(self, from_=1, to=max_size, 
                        orient=tk.HORIZONTAL, command=self.scale_changed)
        scale.set(5)
        scale.pack(fill='x', padx=10)
        buttongrid.pack(padx=10, pady=10)
        
        self.scale = scale
        self.buttongrid = buttongrid
    
    def scale_changed(self, value):
        value = int(value)
        self.solver = lightsout.LightsOut(value)
        self.buttongrid.size = value
    
    def solve(self, board):
        if not self.solver.issolvable(board):
            print "Current board is not solvable"
            self.buttongrid.set_solution(None)
            return
        
        self.buttongrid.set_solution(self.solver.solve(board))
    

def main():
    
    root = tk.Tk()
    app = App(root)
    app.master.title("Lights Out solver")
    root.mainloop()

if __name__ == '__main__':
    main()
