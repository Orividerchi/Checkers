from tkinter import *
from GUI import new_game

window = Tk()
window.title('Checkers')
window.resizable(0, 0)
window.minsize(100, 300)
btn = Button(master=window, text="New Game", command=new_game)
btn.pack()

window.mainloop()