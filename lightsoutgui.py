# coding: utf-8

"""
GUI for the Light Out solver.
"""

import sys
import tkinter as tk
from itertools import product

import numpy as np

import lightsout

BUTTON_SIZE = 23


class ButtonGrid(tk.Frame, object):
    
    def __init__(self, master, size, callback=None):
        tk.Frame.__init__(self, master)
        
        buttons = [[None]*size for i in range(size)]
        for r,c in product(range(size), range(size)):
            buttons[r][c] = tk.Label(self, bitmap="gray12", bg="red",
                                width=BUTTON_SIZE, height=BUTTON_SIZE)
            buttons[r][c].grid(row=r, column=c, padx=2, pady=2)
        
        for btn in sum(buttons, []):
            btn.bind("<Button-1>", self.button_pressed)
        
        self.buttons = buttons
        self.callback = callback
        self.size = size
    
    def button_pressed(self, event):
        if event.widget["bg"] == "red":
            event.widget["bg"] = "green"
        else:
            event.widget["bg"] = "red"
        if self.callback is not None:
            self.callback(self.get_board())
    
    def get_board(self):
        # board = map(lambda x:x["bg"]=="green", sum(self.buttons, []))
        board = [i["bg"] == "green" for i in sum(self.buttons, [])]
        return np.reshape(board, (self.size, self.size))
    
    def set_solution(self, solution):
        if solution is None:
            for btn in sum(self.buttons, []):
                btn["bitmap"] = "gray12"
            return
        
        assert solution.shape[0]==solution.shape[1]==self.size
        
        for r,c in product(range(self.size), range(self.size)):
            if solution[r,c]:
                self.buttons[r][c]["bitmap"] = "gray75"
            else:
                self.buttons[r][c]["bitmap"] = "gray12"
    

class App(tk.Frame):
    
    def __init__(self, master, size=5):
        tk.Frame.__init__(self, master, width=1000, height=1000)
        self.pack(fill="both")
        
        self.solver = lightsout.LightsOut(size)
        
        self.buttongrid = ButtonGrid(self, size, callback=self.solve)
        self.buttongrid.pack(padx=10, pady=10)
        
        self.info = tk.Label(self, text="")
        self.info.pack(side="bottom")
    
    def solve(self, board):
        
        if not self.solver.issolvable(board):
            self.info["text"] = "Not solvable"
            self.buttongrid.set_solution(None)
            return
        
        self.info["text"] = ""
        self.buttongrid.set_solution(self.solver.solve(board))
    

def main():
    
    size = 5
    if len(sys.argv) > 1:
        size = int(sys.argv[1])
    else:
        print("""Use

    {} <board_size>

to indicate the board size (default=5)""".format(sys.argv[0]))
    
    root = tk.Tk()
    app = App(root, size)
    app.master.title("Lights Out solver")
    root.mainloop()


if __name__ == '__main__':
    main()
