import math as m
from tkinter import *
import time as t

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
    global pole_w
    global deep
    deep = 1
    global spisok
    global p
    p=1
    spisok = []
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
            z = pole[y][x]
            if z != 0:
                board.create_image(k * x, y * k, anchor=NW, image=checker[z])


def animation(x1, y1, x2, y2):
    x = pole[y2][x2]
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
    x, y = (event.x) // 100, (event.y) // 100
    board.coords(green_rect, x * 100, y * 100, x * 100 + 100, y * 100 + 100)


def set_purple_rect(event):
    global x_poz, y_poz
    print('p')
    for i in range(8):
        print(pole[i])
    x_poz, y_poz = (event.x) // 100, (event.y) // 100
    if pole[y_poz][x_poz] == 1 or pole[y_poz][x_poz] == 2:
        board.coords(purple_rect, x_poz * 100, y_poz * 100, x_poz * 100 + 100, y_poz * 100 + 100)


def scan(pole2):
    p_white = 0
    p_black = 0
    for i in range(8):
        for j in range(8):
            if pole2[j][i] == 1: p_white += 1
            if pole2[j][i] == 2: p_white += 3
            if pole2[j][i] == 3: p_black += 1
            if pole2[j][i] == 4: p_black += 3
    return [p_white, p_black]


def etachtyca(pole_d, deepi):
    pole2 = pole_d
    spisok2 = []
    while deepi != deep:
        if check_attack_black_ai(spisok2, pole2) != []:
            spisok2 = check_attack_black_ai(spisok2, pole2)
        else:
            spisok2 = hod_black_ai(spisok2, pole2)
        while deepi < deep:
            f1(spisok2, pole2, deepi)
            deepi += 1
    return pole2


def f1(spisok2,pole2, deepi):
    spisok3 = []
    while spisok2 != []:
        for i in range (8):
            print(pole2[i])
        print('2')
        pole3 = c_attack_black(spisok2, pole2)
        for i in range (8):
            print(pole2[i])
        print('3')
        del spisok2[0]
        if check_attack_white_ai(spisok3, pole3) != []:
            spisok3 = check_attack_white_ai(spisok3, pole3)
        else:
            spisok3 = hod_white_ai(spisok3, pole3)
        while spisok3 != []:
            pole3 = c_attack_white(spisok3, pole3)
            del spisok3[0]
            etachtyca(pole3, deepi)
    return scan(pole3)

def c_attack_black(spisok2, pole2):
    spisok2 = []
    if check_attack_black_ai(spisok2, pole2) != []:
        b = spisok2[0][0]
        xi = b[0]
        yi = b[1]
        b = spisok2[0][1]
        x = b[0]
        y = b[1]
        kx = ky = 1
        if x < xi: kx = -1
        if y < yi: ky = -1
        x_poz2, y_poz2 = xi, yi
        while (x != x_poz2) or (y != y_poz2):
            x_poz2 += kx
            y_poz2 += ky
            if pole2[y_poz2][x_poz2] != 0:
                if pole2[yi][xi] == 4:
                    pole2[y_poz2][x_poz2] = 0
                    pole2[y][x] = 4
                    pole2[yi][xi] = 0
                if pole2[yi][xi] == 3:
                    pole2[y_poz2][x_poz2] = 0
                    pole2[y][x] = 3
                    pole2[yi][xi] = 0
                if y == 7:
                    pole2[y][x] = 4
        spisok2 = []
        check = (x, y)
        check_attack_black_ai(spisok2, pole2)
        if spisok2 == []:
            print('')
        elif check == spisok2[0][0]:
            c_attack_black(spisok2, pole2)
    elif hod_black_ai(spisok2, pole2) != []:
        b = spisok2[0][0]
        x1 = b[0]
        y1 = b[1]
        b = spisok2[0][1]
        x2 = b[0]
        y2 = b[1]
        if pole2[y1][x1] == 4:
            pole2[y2][x2] = 4
            pole2[y1][x1] = 0
        if pole2[y1][x1] == 3:
            pole2[y2][x2] = 3
            pole2[y1][x1] = 0
        if y2 == 7:
            pole2[y2][x2] = 4
    return pole2

def c_attack_white(spisok2, pole2):
    spisok2 =[]
    if check_attack_white_ai(spisok2, pole2) != []:
        b = spisok2[0][0]
        xi = b[0]
        yi = b[1]
        b = spisok2[0][1]
        x = b[0]
        y = b[1]
        kx = ky = 1
        if x < xi: kx = -1
        if y < yi: ky = -1
        x_poz2, y_poz2 = xi, yi
        while (x != x_poz2) or (y != y_poz2):
            x_poz2 += kx
            y_poz2 += ky
            if pole2[y_poz2][x_poz2] != 0:
                if pole2[yi][xi] == 2:
                    pole2[y_poz2][x_poz2] = 0
                    pole2[y][x] = 2
                    pole2[yi][xi] = 0
                if pole2[yi][xi] == 1:
                    pole2[y_poz2][x_poz2] = 0
                    pole2[y][x] = 1
                    pole2[yi][xi] = 0
                if y == 0:
                    pole2[y][x] = 2
        spisok2 = []
        check_attack_white_ai(spisok2, pole2)
        if spisok2 != []:
            if (x, y) == spisok2[0][0]:
                print(' 5664')
                #c_attack_white(spisok2, pole2)
    elif hod_white_ai(spisok2, pole2) != []:
        b = spisok2[0][0]
        x1 = b[0]
        y1 = b[1]
        b = spisok2[0][1]
        x2 = b[0]
        y2 = b[1]
        if pole2[y1][x1] == 2:
            pole2[y2][x2] = 2
            pole2[y1][x1] = 0
        if pole2[y1][x1] == 1:
            pole2[y2][x2] = 1
            pole2[y1][x1] = 0
        if y2 == 0:
            pole2[y2][x2] = 2
    return pole2


def check_click(event):
    spisok = []
    x, y = (event.x) // 100, (event.y) // 100
    check = ((x_poz, y_poz), (x, y))
    if check_attack_white(spisok, pole) != []:
        if check in check_attack_white(spisok, pole):
            kx = ky = 1
            if x < x_poz:
                kx = -1
            if y < y_poz:
                ky = -1
            x_poz2, y_poz2 = x_poz, y_poz
            while (x != x_poz2) or (y != y_poz2):
                x_poz2 += kx
                y_poz2 += ky
                if pole[y_poz2][x_poz2] != 0:
                    if pole[y_poz][x_poz] == 2:
                        pole[y_poz2][x_poz2] = 0
                        pole[y][x] = 2
                        pole[y_poz][x_poz] = 0
                    if pole[y_poz][x_poz] == 1:
                        pole[y_poz2][x_poz2] = 0
                        pole[y][x] = 1
                        pole[y_poz][x_poz] = 0
                    if y == 0:
                        pole[y][x] = 2
            animation(x_poz, y_poz, x, y)
            board_draw()
            spisok = []
            check_attack_white(spisok, pole)
            if spisok == []:
                hod_ai()
            elif (x, y) == spisok[0][0]:
                print(spisok[0][0])
    elif check in hod_white(spisok, pole):
        if pole[y_poz][x_poz] == 1:
            pole[y][x] = 1
            pole[y_poz][x_poz] = 0
        if pole[y_poz][x_poz] == 2:
            pole[y][x] = 2
            pole[y_poz][x_poz] = 0
        if y == 0:
            pole[y][x] = 2
        #animation(x_poz,y_poz,x,y)
        #board_draw()
        animation(x_poz, y_poz, x, y)
        board_draw()
        hod_ai()


def hod_ai():
    spisok = []
    if check_attack_black(spisok,pole) != []:
        b = spisok[0][0]
        x_poz = b[0]
        y_poz = b[1]
        b = spisok[0][1]
        x = b[0]
        y = b[1]
        kx = ky = 1
        if x < x_poz: kx = -1
        if y < y_poz: ky = -1
        x_poz2, y_poz2 = x_poz, y_poz
        while (x != x_poz2) or (y != y_poz2):
            x_poz2 += kx
            y_poz2 += ky
            if pole[y_poz2][x_poz2] != 0:
                if pole[y_poz][x_poz] == 4:
                    pole[y_poz2][x_poz2] = 0
                    pole[y][x] = 4
                    pole[y_poz][x_poz] = 0
                if pole[y_poz][x_poz] == 3:
                    pole[y_poz2][x_poz2] = 0
                    pole[y][x] = 3
                    pole[y_poz][x_poz] = 0
                if y == 7:
                    pole[y][x] = 4
        animation(x_poz, y_poz, x, y)
        board_draw()
       # check_c()
        spisok = []
        check = (x, y)
        check_attack_black(spisok, pole)
        if spisok ==[]:
            print('')
        elif check == spisok[0][0]:
            hod_ai()
    elif hod_black(spisok, pole) != []:
        b = spisok[0][0]
        x1 = b[0]
        y1 = b[1]
        b = spisok[0][1]
        x2 = b[0]
        y2 = b[1]
        if pole[y1][x1] == 4:
            pole[y2][x2] = 4
            pole[y1][x1] = 0
        if pole[y1][x1] == 3:
            pole[y2][x2] = 3
            pole[y1][x1] = 0
        if y2 == 7:
            pole[y2][x2] = 4
        animation(x1, y1, x2, y2)
        board_draw()
        pole_w = pole
        etachtyca(pole_w, 0)
        print('1')
        for i in range (8):
            print(pole[i])


def check_attack_white_ai(spisok1, pole1):
    hod_white_attack_ai(spisok1, pole1)
    return spisok1


def check_attack_black_ai(spisok1, pole1):
    hod_black_attack_ai(spisok1, pole1)
    return spisok1

def hod_white_attack_ai(spisok1, pole1):
    for y in range(8):
        for x in range(8):
            if pole1[y][x] == 1:
                for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
                    if 0 <= y + iy + iy <= 7 and 0 <= x + ix + ix <= 7:
                        if pole1[y + iy][x + ix] == 3 or pole1[y + iy][x + ix] == 4:
                            if pole1[y + iy + iy][x + ix + ix] == 0:
                                spisok1.append(((x, y), (x + ix + ix, y + iy + iy)))
            if pole1[y][x] == 2:
                for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
                    osh = 0
                    for i in range(1, 8):
                        if 0 <= y + iy * i <= 7 and 0 <= x + ix * i <= 7:
                            if osh == 1:
                                spisok1.append(((x, y), (x + ix * i, y + iy * i)))
                            if pole1[y + iy * i][x + ix * i] == 3 or pole1[y + iy * i][x + ix * i] == 4:
                                osh += 1
                            if pole1[y + iy * i][x + ix * i] == 1 or pole1[y + iy * i][x + ix * i] == 2 or osh == 2:
                                if osh > 0: spisok1.pop()
                                break
    return spisok1

def hod_white_ai(spisok1, pole1):
    for y in range(8):
        for x in range(8):
            if pole1[y][x] == 1:
                for ix, iy in (-1, -1), (1, -1):
                    if 0 <= y + iy <= 7 and 0 <= x + ix <= 7:
                        if pole1[y + iy][x + ix] == 0:
                            spisok1.append(((x, y), (x + ix, y + iy)))
                        if pole1[y + iy][x + ix] == 3 or pole1[y + iy][x + ix] == 4:
                            if 0 <= y + iy * 2 <= 7 and 0 <= x + ix * 2 <= 7:
                                if pole1[y + iy * 2][x + ix * 2] == 0:
                                    spisok1.append(((x, y), (x + ix * 2, y + iy * 2)))
            if pole1[y][x] == 2:
                for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
                    osh = 0
                    for i in range(1, 8):
                        if 0 <= y + iy * i <= 7 and 0 <= x + ix * i <= 7:
                            if pole1[y + iy * i][x + ix * i] == 0:
                                spisok1.append(((x, y), (x + ix * i, y + iy * i)))
                            if pole1[y + iy * i][x + ix * i] == 3 or pole1[y + iy * i][x + ix * i] == 4:
                                osh += 1
                            if pole1[y + iy * i][x + ix * i] == 1 or pole1[y + iy * i][x + ix * i] == 2 or osh == 2:
                                break
    return spisok1


def hod_black_attack_ai(spisok1, pole1):
    for y in range(8):
        for x in range(8):
            if pole1[y][x] == 3:
                for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
                    if 0 <= y + iy + iy <= 7 and 0 <= x + ix + ix <= 7:
                        if pole1[y + iy][x + ix] == 1 or pole1[y + iy][x + ix] == 2:
                            if pole1[y + iy + iy][x + ix + ix] == 0:
                                spisok1.append(((x, y), (x + ix + ix, y + iy + iy)))
            if pole1[y][x] == 4:
                for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
                    osh = 0
                    for i in range(1, 8):
                        if 0 <= y + iy * i <= 7 and 0 <= x + ix * i <= 7:
                            if osh == 1:
                                spisok1.append(((x, y), (x + ix * i, y + iy * i)))
                            if pole1[y + iy * i][x + ix * i] == 1 or pole1[y + iy * i][x + ix * i] == 2:
                                osh += 1
                            if pole1[y + iy * i][x + ix * i] == 3 or pole1[y + iy * i][x + ix * i] == 4 or osh == 2:
                                if osh > 0: spisok1.pop()
                                break
    return spisok1

def hod_black_ai(spisok1, pole1):
    for y in range(8):
        for x in range(8):
            if pole1[y][x] == 3:
                for ix, iy in (-1, 1), (1, 1):
                    if 0 <= y + iy <= 7 and 0 <= x + ix <= 7:
                        if pole1[y + iy][x + ix] == 0:
                            spisok1.append(((x, y), (x + ix, y + iy)))
                        if pole1[y + iy][x + ix] == 1 or pole1[y + iy][x + ix] == 2:
                            if 0 <= y + iy * 2 <= 7 and 0 <= x + ix * 2 <= 7:
                                if pole1[y + iy * 2][x + ix * 2] == 0:
                                    spisok1.append(((x, y), (
                                    x + ix * 2, y + iy * 2)))
            if pole1[y][x] == 4:
                for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
                    osh = 0
                    for i in range(1, 8):
                        if 0 <= y + iy * i <= 7 and 0 <= x + ix * i <= 7:
                            if pole1[y + iy * i][x + ix * i] == 0:
                                spisok1.append(((x, y), (x + ix * i, y + iy * i)))
                            if pole1[y + iy * i][x + ix * i] == 1 or pole1[y + iy * i][x + ix * i] == 2:
                                osh += 1
                            if pole1[y + iy * i][x + ix * i] == 3 or pole1[y + iy * i][x + ix * i] == 4 or osh == 2:
                                break
    return spisok1


def check_attack_white(spisok, pole):
    hod_white_attack(spisok, pole)
    return spisok


def check_attack_black(spisok, pole):
    hod_black_attack(spisok, pole)
    return spisok

def hod_white_attack(spisok, pole):
    for y in range(8):
        for x in range(8):
            if pole[y][x] == 1:
                for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
                    if 0 <= y + iy + iy <= 7 and 0 <= x + ix + ix <= 7:
                        if pole[y + iy][x + ix] == 3 or pole[y + iy][x + ix] == 4:
                            if pole[y + iy + iy][x + ix + ix] == 0:
                                spisok.append(((x, y), (x + ix + ix, y + iy + iy)))
            if pole[y][x] == 2:
                for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
                    osh = 0
                    for i in range(1, 8):
                        if 0 <= y + iy * i <= 7 and 0 <= x + ix * i <= 7:
                            if osh == 1:
                                spisok.append(((x, y), (x + ix * i, y + iy * i)))
                            if pole[y + iy * i][x + ix * i] == 3 or pole[y + iy * i][x + ix * i] == 4:
                                osh += 1
                            if pole[y + iy * i][x + ix * i] == 1 or pole[y + iy * i][x + ix * i] == 2 or osh == 2:
                                if osh > 0: spisok.pop()
                                break
    return spisok

def hod_white(spisok, pole):
    for y in range(8):
        for x in range(8):
            if pole[y][x] == 1:
                for ix, iy in (-1, -1), (1, -1):
                    if 0 <= y + iy <= 7 and 0 <= x + ix <= 7:
                        if pole[y + iy][x + ix] == 0:
                            spisok.append(((x, y), (x + ix, y + iy)))
                        if pole[y + iy][x + ix] == 3 or pole[y + iy][x + ix] == 4:
                            if 0 <= y + iy * 2 <= 7 and 0 <= x + ix * 2 <= 7:
                                if pole[y + iy * 2][x + ix * 2] == 0:
                                    spisok.append(((x, y), (x + ix * 2, y + iy * 2)))
            if pole[y][x] == 2:
                for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
                    osh = 0
                    for i in range(1, 8):
                        if 0 <= y + iy * i <= 7 and 0 <= x + ix * i <= 7:
                            if pole[y + iy * i][x + ix * i] == 0:
                                spisok.append(((x, y), (x + ix * i, y + iy * i)))
                            if pole[y + iy * i][x + ix * i] == 3 or pole[y + iy * i][x + ix * i] == 4:
                                osh += 1
                            if pole[y + iy * i][x + ix * i] == 1 or pole[y + iy * i][x + ix * i] == 2 or osh == 2:
                                break
    return spisok


def hod_black_attack(spisok, pole):
    for y in range(8):
        for x in range(8):
            if pole[y][x] == 3:
                for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
                    if 0 <= y + iy + iy <= 7 and 0 <= x + ix + ix <= 7:
                        if pole[y + iy][x + ix] == 1 or pole[y + iy][x + ix] == 2:
                            if pole[y + iy + iy][x + ix + ix] == 0:
                                spisok.append(((x, y), (x + ix + ix, y + iy + iy)))
            if pole[y][x] == 4:
                for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
                    osh = 0
                    for i in range(1, 8):
                        if 0 <= y + iy * i <= 7 and 0 <= x + ix * i <= 7:
                            if osh == 1:
                                spisok.append(((x, y), (x + ix * i, y + iy * i)))
                            if pole[y + iy * i][x + ix * i] == 1 or pole[y + iy * i][x + ix * i] == 2:
                                osh += 1
                            if pole[y + iy * i][x + ix * i] == 3 or pole[y + iy * i][x + ix * i] == 4 or osh == 2:
                                if osh > 0: spisok.pop()
                                break
    return spisok

def hod_black(spisok, pole):
    for y in range(8):
        for x in range(8):
            if pole[y][x] == 3:
                for ix, iy in (-1, 1), (1, 1):
                    if 0 <= y + iy <= 7 and 0 <= x + ix <= 7:
                        if pole[y + iy][x + ix] == 0:
                            spisok.append(((x, y), (x + ix, y + iy)))
                        if pole[y + iy][x + ix] == 1 or pole[y + iy][x + ix] == 2:
                            if 0 <= y + iy * 2 <= 7 and 0 <= x + ix * 2 <= 7:
                                if pole[y + iy * 2][x + ix * 2] == 0:
                                    spisok.append(((x, y), (
                                    x + ix * 2, y + iy * 2)))
            if pole[y][x] == 4:
                for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
                    osh = 0
                    for i in range(1, 8):
                        if 0 <= y + iy * i <= 7 and 0 <= x + ix * i <= 7:
                            if pole[y + iy * i][x + ix * i] == 0:
                                spisok.append(((x, y), (x + ix * i, y + iy * i)))
                            if pole[y + iy * i][x + ix * i] == 1 or pole[y + iy * i][x + ix * i] == 2:
                                osh += 1
                            if pole[y + iy * i][x + ix * i] == 3 or pole[y + iy * i][x + ix * i] == 4 or osh == 2:
                                break
    return spisok


#def hod_i(event):


main_menu = Menu()

file_menu = Menu()
file_menu.add_command(label="Difficulty")

main_menu.add_cascade(label="New Game", command=new_game)
main_menu.add_cascade(label="Options", menu=file_menu)
main_menu.add_cascade(label="Exit", command=exit)
window.config(menu=main_menu)
new_game()
window.mainloop()
