from tkinter import *


window = Tk()
window.title('Checkers AI')
window.resizable(0, 0)
window.geometry("+440+50")
board = Canvas(window, width=800, height=800)
board.pack()


def load_images():
    global checker
    i1 = PhotoImage(file="res\\1b.gif")
    i2 = PhotoImage(file="res\\1bk.gif")
    i3 = PhotoImage(file="res\\1h.gif")
    i4 = PhotoImage(file="res\\1hk.gif")
    checker = [0, i1, i2, i3, i4]


def new_game():
    global pole
    pole = [[0, 3, 0, 3, 0, 3, 0, 3],
            [3, 0, 3, 0, 3, 0, 3, 0],
            [0, 3, 0, 3, 0, 3, 0, 3],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0]]
    load_images()
    board_draw()


def board_draw():
    global checker
    global pole
    global purple_rect
    global green_rect
    board.delete('all')
    k = 100
    x = 0
    green_rect = board.create_rectangle(-5, -5, -5, -5, outline="purple", width=5)
    purple_rect = board.create_rectangle(-5, -5, -5, -5, outline="red", width=5)
    board.bind("<Motion>", set_green_rect)
    board.bind("<Button-1>", set_purple_rect)
    board.bind("<Button-3>", Check)
    while x < 8 * k:
        y = 1 * k
        while y < 8 * k:
            board.create_rectangle(x, y, x + k, y + k, fill="black")
            y += 2 * k
        x += 2 * k
    x = 1 * k
    while x < 8 * k:
        y = 0
        while y < 8 * k:
            board.create_rectangle(x, y, x + k, y + k, fill="black")
            y += 2 * k
        x += 2 * k
    for y in range(8):
        for x in range(8):
            z = pole[y][x]
            if z != 0:
                board.create_image(k * x, y * k, anchor=NW, image=checker[z])


def set_green_rect(event):
    x, y = (event.x) // 100, (event.y) // 100
    board.coords(green_rect, x * 100, y * 100, x * 100 + 100, y * 100 + 100)


def set_purple_rect(event):
  global  x_poz, y_poz
  x_poz, y_poz = (event.x) // 100, (event.y) // 100
  if pole[y_poz][x_poz] == 1 or pole[y_poz][x_poz] == 2:
    board.coords(purple_rect, x_poz * 100, y_poz * 100, x_poz * 100 + 100, y_poz * 100 + 100)
    #if pole[y_poz][x_poz] == 0:


def Check(event):
    x, y = (event.x) // 100, (event.y) // 100
    if pole[y][x] == 0 and pole[y_poz][x_poz]==1:  # пешка
        ix = x_poz-x
        iy = y_poz - y
        if ix and iy in (-1,-1) or (-1,1) or(1,-1) or(1,1):
            if pole[y + iy + iy][x + ix + ix] == 1:
                pole[y][x] = 1
                pole[y_poz][x_poz] = 0
                board_draw()



#def hod_i():


main_menu = Menu()

file_menu = Menu()
file_menu.add_command(label="Difficulty")

main_menu.add_cascade(label="New Game", command=new_game)
main_menu.add_cascade(label="Options", menu=file_menu)
main_menu.add_cascade(label="Exit", command=exit)
window.config(menu=main_menu)
new_game()
window.mainloop()
