
from tkinter import *
import time as t
import copy
import math
from PyQt5.QtWidgets import *

window = Tk()
window.title('Checkers AI')
window.resizable(0, 0)
window.geometry("+440+50")
board = Canvas(window, width=800, height=800)
board.pack()


def load_images():
    global checker
    i1 = PhotoImage(file="res\\white.png")
    i2 = PhotoImage(file="res\\white_Q.png")
    i3 = PhotoImage(file="res\\black.png")
    i4 = PhotoImage(file="res\\black_Q.png")
    checker = [0, i1, i2, i3, i4]


def new_game():
    global deep
    deep = 7
    global main_field
    main_field = [[0, 3, 0, 3, 0, 3, 0, 3],
                  [3, 0, 3, 0, 3, 0, 3, 0],
                  [0, 3, 0, 3, 0, 3, 0, 3],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [1, 0, 1, 0, 1, 0, 1, 0],
                  [0, 1, 0, 1, 0, 1, 0, 1],
                  [1, 0, 1, 0, 1, 0, 1, 0]]
    load_images()
    board_draw()


def set_difficulty():
    text, ok = QInputDialog('Input Dialog', 'Enter your name')
    print()


def board_draw():
    global checker
    global purple_rect
    global green_rect
    board.delete('all')
    k = 100
    x = 0
    green_rect = board.create_rectangle(-5, -5, -5, -5, outline="purple", width=5)
    purple_rect = board.create_rectangle(-5, -5, -5, -5, outline="red", width=5)
    board.bind("<Motion>", set_green_rect)
    board.bind("<Button-1>", set_purple_rect)
    board.bind("<Button-3>", check_click)
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
            z = main_field[y][x]
            if z != 0:
                board.create_image(k * x, y * k, anchor=NW, image=checker[z])


def animation(x1, y1, x2, y2):
    x = main_field[y2][x2]
    k = 100
    board.create_rectangle(x1 * 100, y1 * 100, x1 * 100 + 100, y1 * 100 + 100, fill="black")
    if x != 0:
        board.create_image(k * x1, y1 * k, anchor=NW, image=checker[x], tag='ani')
    kx = 1 if x1 < x2 else -1
    ky = 1 if y1 < y2 else -1
    for i in range(abs(x1 - x2)):
        for j in range(0, 33):
            board.move('ani', 0.03 * 100 * kx, 0.03 * 100 * ky)
            window.update()
            t.sleep(0.01)


def set_green_rect(event):
    x, y = event.x // 100, event.y // 100
    board.coords(green_rect, x * 100, y * 100, x * 100 + 100, y * 100 + 100)


def set_purple_rect(event):
    global x_poz, y_poz
    x_poz, y_poz = event.x // 100, event.y // 100
    if main_field[y_poz][x_poz] == 1 or main_field[y_poz][x_poz] == 2:
        board.coords(purple_rect, x_poz * 100, y_poz * 100, x_poz * 100 + 100, y_poz * 100 + 100)


def scan(field):
    p_white = 0
    p_black = 0
    for i in range(8):
        for j in range(8):
            if field[j][i] == 1:
                p_white += 1
            if field[j][i] == 2:
                p_white += 3
            if field[j][i] == 3:
                p_black += 1
            if field[j][i] == 4:
                p_black += 3
    return p_black - p_white


def enter(field, deep_i):
    list_of_moving = []
    price = []
    create_black_list(list_of_moving, field)
    while list_of_moving:
        list_of_moving_copy = copy.deepcopy(list_of_moving)
        field_copy = copy.deepcopy(field)
        black_moving(list_of_moving_copy, field_copy)
        price.append(white_move(deep_i + 1, field_copy))
        del list_of_moving[0]
    return price


def black_move(field, deep_i):
    list_of_moving = []
    price = []
    create_black_list(list_of_moving, field)
    if deep_i == deep:
        return scan(field)
    else:
        while list_of_moving:
            field_copy = copy.deepcopy(field)
            list_of_moving_copy = copy.deepcopy(list_of_moving)
            black_moving(list_of_moving_copy, field_copy)
            price.append(white_move(deep_i + 1, field_copy))
            del list_of_moving[0]
        return neuron(price, deep_i)


def white_move(deep_i, field):
    list_of_moving = []
    price = []
    create_white_list(list_of_moving, field)
    if deep_i == deep:
        return scan(field)
    else:
        while list_of_moving:
            field_copy = copy.deepcopy(field)
            list_of_moving_copy = copy.deepcopy(list_of_moving)
            white_moving(list_of_moving_copy, field_copy)
            price.append(black_move(field_copy, deep_i + 1))
            del list_of_moving[0]
        return neuron(price, deep_i)


def create_black_list(list_of_moving, field):
    if check_black_attack(list_of_moving, field):
        list_of_moving = check_black_attack(list_of_moving, field)
    else:
        list_of_moving = hod_black(list_of_moving, field)
    return list_of_moving


def create_white_list(list_of_moving, field):
    if check_white_attack(list_of_moving, field):
        list_of_moving = check_white_attack(list_of_moving, field)
    else:
        list_of_moving = hod_white(list_of_moving, field)
    return list_of_moving


def neuron(price, deep_i=0):
    xe = 0
    for i in range(price.__len__()):
        price[i] *= 1 / (deep_i + 1)
        xe += price[i]
    xe = sigmoid(xe)
    return xe


def sigmoid(x):
    return 1 / (1 + math.exp(-x))


def black_moving(list_of_moving, field):
    list_of_moving_local = []
    if check_black_attack(list_of_moving_local, field):
        b = list_of_moving[0][0]
        xi = b[0]
        yi = b[1]
        b = list_of_moving[0][1]
        x = b[0]
        y = b[1]
        kx = ky = 1
        if x < xi:
            kx = -1
        if y < yi:
            ky = -1
        x_poz2, y_poz2 = xi, yi
        while (x != x_poz2) or (y != y_poz2):
            x_poz2 += kx
            y_poz2 += ky
            if field[y_poz2][x_poz2] != 0:
                if field[yi][xi] == 4:
                    field[y_poz2][x_poz2] = 0
                    field[y][x] = 4
                    field[yi][xi] = 0
                if field[yi][xi] == 3:
                    field[y_poz2][x_poz2] = 0
                    field[y][x] = 3
                    field[yi][xi] = 0
                if y == 7:
                    field[y][x] = 4
        list_of_moving_local = []
        check_black_attack(list_of_moving_local, field)
        if list_of_moving_local != []:
            if (x, y) == list_of_moving_local[0][0]:
                black_moving(list_of_moving_local, field)
    elif hod_black(list_of_moving, field):
        b = list_of_moving[0][0]
        x1 = b[0]
        y1 = b[1]
        b = list_of_moving[0][1]
        x2 = b[0]
        y2 = b[1]
        if field[y1][x1] == 4:
            field[y2][x2] = 4
            field[y1][x1] = 0
        if field[y1][x1] == 3:
            field[y2][x2] = 3
            field[y1][x1] = 0
        if y2 == 7:
            field[y2][x2] = 4


def white_moving(list_of_moving, field):
    list_of_moving_local = []
    if check_white_attack(list_of_moving_local, field):
        b = list_of_moving[0][0]
        xi = b[0]
        yi = b[1]
        b = list_of_moving[0][1]
        x = b[0]
        y = b[1]
        kx = ky = 1
        if x < xi:
            kx = -1
        if y < yi:
            ky = -1
        x_poz2, y_poz2 = xi, yi
        while (x != x_poz2) or (y != y_poz2):
            x_poz2 += kx
            y_poz2 += ky
            if field[y_poz2][x_poz2] != 0:
                if field[yi][xi] == 2:
                    field[y_poz2][x_poz2] = 0
                    field[y][x] = 2
                    field[yi][xi] = 0
                if field[yi][xi] == 1:
                    field[y_poz2][x_poz2] = 0
                    field[y][x] = 1
                    field[yi][xi] = 0
                if y == 0:
                    field[y][x] = 2
        list_of_moving_local = []
        check_white_attack(list_of_moving_local, field)
        if list_of_moving_local != []:
            if (x, y) in list_of_moving:
                white_moving(list_of_moving_local, field)
    elif hod_white(list_of_moving, field):
        b = list_of_moving[0][0]
        x1 = b[0]
        y1 = b[1]
        b = list_of_moving[0][1]
        x2 = b[0]
        y2 = b[1]
        if field[y1][x1] == 2:
            field[y2][x2] = 2
            field[y1][x1] = 0
        if field[y1][x1] == 1:
            field[y2][x2] = 1
            field[y1][x1] = 0
        if y2 == 0:
            field[y2][x2] = 2


def check_click(event):
    list_of_moving = []
    x, y = event.x // 100, event.y // 100
    check = ((x_poz, y_poz), (x, y))
    if check_white_attack(list_of_moving, main_field):
        if check in check_white_attack(list_of_moving, main_field):
            kx = ky = 1
            if x < x_poz:
                kx = -1
            if y < y_poz:
                ky = -1
            x_poz2, y_poz2 = x_poz, y_poz
            while (x != x_poz2) or (y != y_poz2):
                x_poz2 += kx
                y_poz2 += ky
                if main_field[y_poz2][x_poz2] != 0:
                    if main_field[y_poz][x_poz] == 2:
                        main_field[y_poz2][x_poz2] = 0
                        main_field[y][x] = 2
                        main_field[y_poz][x_poz] = 0
                    if main_field[y_poz][x_poz] == 1:
                        main_field[y_poz2][x_poz2] = 0
                        main_field[y][x] = 1
                        main_field[y_poz][x_poz] = 0
                    if y == 0:
                        main_field[y][x] = 2
            animation(x_poz, y_poz, x, y)
            board_draw()
            list_of_moving = []
            check_white_attack(list_of_moving, main_field)
            print(list_of_moving)
            if list_of_moving == []:
                hod_ai()
            elif (x, y) == list_of_moving[0][0]:
                print('')
            else:
                hod_ai()
    elif check in hod_white(list_of_moving, main_field):
        if main_field[y_poz][x_poz] == 1:
            main_field[y][x] = 1
            main_field[y_poz][x_poz] = 0
        if main_field[y_poz][x_poz] == 2:
            main_field[y][x] = 2
            main_field[y_poz][x_poz] = 0
        if y == 0:
            main_field[y][x] = 2
        animation(x_poz, y_poz, x, y)
        board_draw()
        hod_ai()


def max_index(a):
    max_element = 0
    max_i = 0
    for i in range(a.__len__()):
        if a[i] > max_element:
            max_element = a[i]
            max_i = i
    return max_i


def hod_ai():
    field_copy = copy.deepcopy(main_field)
    a = enter(field_copy, 1)
    i = max_index(a)
    list_of_moving = []
    if check_black_attack(list_of_moving, main_field):
        b = list_of_moving[i][0]
        x1 = b[0]
        y1 = b[1]
        b = list_of_moving[i][1]
        x2 = b[0]
        y2 = b[1]
        kx = ky = 1
        if x2 < x1:
            kx = -1
        if y2 < y1:
            ky = -1
        x_poz2, y_poz2 = x1, y1
        while (x2 != x_poz2) or (y2 != y_poz2):
            x_poz2 += kx
            y_poz2 += ky
            if main_field[y_poz2][x_poz2] != 0:
                if main_field[y1][x1] == 4:
                    main_field[y_poz2][x_poz2] = 0
                    main_field[y2][x2] = 4
                    main_field[y1][x1] = 0
                if main_field[y1][x1] == 3:
                    main_field[y_poz2][x_poz2] = 0
                    main_field[y2][x2] = 3
                    main_field[y1][x1] = 0
                if y2 == 7:
                    main_field[y2][x2] = 4
        animation(x1, y1, x2, y2)
        board_draw()
        list_of_moving = []
        check_black_attack(list_of_moving, main_field)
        if list_of_moving == []:
            print('')
        elif (x2, y2) == list_of_moving[0][0]:
            hod_ai()
    elif hod_black(list_of_moving, main_field):
        b = list_of_moving[i][0]
        x1 = b[0]
        y1 = b[1]
        b = list_of_moving[i][1]
        x2 = b[0]
        y2 = b[1]
        if main_field[y1][x1] == 4:
            main_field[y2][x2] = 4
            main_field[y1][x1] = 0
        if main_field[y1][x1] == 3:
            main_field[y2][x2] = 3
            main_field[y1][x1] = 0
        if y2 == 7:
            main_field[y2][x2] = 4
        animation(x1, y1, x2, y2)
        board_draw()


def check_white_attack(list_of_moving, field):
    for y in range(8):
        for x in range(8):
            if field[y][x] == 1:
                for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
                    if 0 <= y + iy + iy <= 7 and 0 <= x + ix + ix <= 7:
                        if field[y + iy][x + ix] == 3 or field[y + iy][x + ix] == 4:
                            if field[y + iy + iy][x + ix + ix] == 0:
                                list_of_moving.append(((x, y), (x + ix + ix, y + iy + iy)))
            if field[y][x] == 2:
                for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
                    osh = 0
                    for i in range(1, 8):
                        if 0 <= y + iy * i <= 7 and 0 <= x + ix * i <= 7:
                            if osh == 1:
                                list_of_moving.append(((x, y), (x + ix * i, y + iy * i)))
                            if field[y + iy * i][x + ix * i] == 3 or field[y + iy * i][x + ix * i] == 4:
                                osh += 1
                            if field[y + iy * i][x + ix * i] == 1 or field[y + iy * i][x + ix * i] == 2 or osh == 2:
                                if osh > 0:
                                    list_of_moving.pop()
                                break
    return list_of_moving


def hod_white(list_of_moving, field):
    for y in range(8):
        for x in range(8):
            if field[y][x] == 1:
                for ix, iy in (-1, -1), (1, -1):
                    if 0 <= y + iy <= 7 and 0 <= x + ix <= 7:
                        if field[y + iy][x + ix] == 0:
                            list_of_moving.append(((x, y), (x + ix, y + iy)))
                        if field[y + iy][x + ix] == 3 or field[y + iy][x + ix] == 4:
                            if 0 <= y + iy * 2 <= 7 and 0 <= x + ix * 2 <= 7:
                                if field[y + iy * 2][x + ix * 2] == 0:
                                    list_of_moving.append(((x, y), (x + ix * 2, y + iy * 2)))
            if field[y][x] == 2:
                for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
                    osh = 0
                    for i in range(1, 8):
                        if 0 <= y + iy * i <= 7 and 0 <= x + ix * i <= 7:
                            if field[y + iy * i][x + ix * i] == 0:
                                list_of_moving.append(((x, y), (x + ix * i, y + iy * i)))
                            if field[y + iy * i][x + ix * i] == 3 or field[y + iy * i][x + ix * i] == 4:
                                osh += 1
                            if field[y + iy * i][x + ix * i] == 1 or field[y + iy * i][x + ix * i] == 2 or osh == 2:
                                break
    return list_of_moving


def check_black_attack(list_of_moving, field):
    for y in range(8):
        for x in range(8):
            if field[y][x] == 3:
                for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
                    if 0 <= y + iy + iy <= 7 and 0 <= x + ix + ix <= 7:
                        if field[y + iy][x + ix] == 1 or field[y + iy][x + ix] == 2:
                            if field[y + iy + iy][x + ix + ix] == 0:
                                list_of_moving.append(((x, y), (x + ix + ix, y + iy + iy)))
            if field[y][x] == 4:
                for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
                    osh = 0
                    for i in range(1, 8):
                        if 0 <= y + iy * i <= 7 and 0 <= x + ix * i <= 7:
                            if osh == 1:
                                list_of_moving.append(((x, y), (x + ix * i, y + iy * i)))
                            if field[y + iy * i][x + ix * i] == 1 or field[y + iy * i][x + ix * i] == 2:
                                osh += 1
                            if field[y + iy * i][x + ix * i] == 3 or field[y + iy * i][x + ix * i] == 4 or osh == 2:
                                if osh > 0:
                                    list_of_moving.pop()
                                break
    return list_of_moving


def hod_black(list_of_moving, field):
    for y in range(8):
        for x in range(8):
            if field[y][x] == 3:
                for ix, iy in (-1, 1), (1, 1):
                    if 0 <= y + iy <= 7 and 0 <= x + ix <= 7:
                        if field[y + iy][x + ix] == 0:
                            list_of_moving.append(((x, y), (x + ix, y + iy)))
                        if field[y + iy][x + ix] == 1 or field[y + iy][x + ix] == 2:
                            if 0 <= y + iy * 2 <= 7 and 0 <= x + ix * 2 <= 7:
                                if field[y + iy * 2][x + ix * 2] == 0:
                                    list_of_moving.append(((x, y), (
                                        x + ix * 2, y + iy * 2)))
            if field[y][x] == 4:
                for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
                    osh = 0
                    for i in range(1, 8):
                        if 0 <= y + iy * i <= 7 and 0 <= x + ix * i <= 7:
                            if field[y + iy * i][x + ix * i] == 0:
                                list_of_moving.append(((x, y), (x + ix * i, y + iy * i)))
                            if field[y + iy * i][x + ix * i] == 1 or field[y + iy * i][x + ix * i] == 2:
                                osh += 1
                            if field[y + iy * i][x + ix * i] == 3 or field[y + iy * i][x + ix * i] == 4 or osh == 2:
                                break
    return list_of_moving


main_menu = Menu()
file_menu = Menu()
file_menu.add_command(label="Difficulty")
main_menu.add_cascade(label="New Game", command=new_game)
main_menu.add_cascade(label="Options", menu=file_menu)
main_menu.add_cascade(label="Exit", command=exit)
window.config(menu=main_menu)
new_game()
window.mainloop()
