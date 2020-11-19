from tkinter import *
import time
import tkinter
import math
import random

def slut(tid_start, tid_slut, knapptryck, bombchans):
    poäng = (tid_slut-tid_start)*(bombchans/knapptryck)


def spelet(width, height, bombchans, antaltomma, tid_start):
    window = Tk()
    rutbild = PhotoImage(file=r"tile.png")
    gråruta = rutbild.subsample(8, 8)
    oformateradflagga = PhotoImage(file=r"flag.png")
    flag = oformateradflagga.subsample(36, 36)
    nollan = PhotoImage(file=r"0.png")
    noll = nollan.subsample(8, 8)
    ettan = PhotoImage(file=r"1.png")
    ett = ettan.subsample(8, 8)
    tvåan = PhotoImage(file=r"2.png")
    två = tvåan.subsample(8, 8)
    trean = PhotoImage(file=r"3.png")
    tre = trean.subsample(8, 8)
    fyran = PhotoImage(file=r"4.png")
    fyra = fyran.subsample(8, 8)
    femman = PhotoImage(file=r"5.png")
    fem = femman.subsample(8, 8)
    sexan = PhotoImage(file=r"6.png")
    sex = sexan.subsample(8, 8)
    minan = PhotoImage(file=r"mina.png")
    mina = minan.subsample(7, 7)

    rutnät = [[0 for h in range(height)] for b in range(width)]
    spelinfo = 0
    antalknapptryck = 0
    antalbomber=math.ceil(((width*height)-antaltomma)*bombchans)
    kvar_till_vinst = (width*height) - antalbomber + 1

    def loser():
        tid_slut = time.time()
        for x in range (width):
            for y in range(height):
                åtgärder_vid_synliggörande(x, y)
        slut(tid_start, tid_slut, antalknapptryck, bombchans)

    def winner():
        tid_slut = time.time()
        for x in range(width):
            for y in range(height):
                rutnät[x][y].unbind("<Button-1>")
                rutnät[x][y].unbind("<Button-3>")
                if spelinfo [x][y].bomb==True:
                    rutnät[x][y].config(image=flag)
        slut(tid_start, tid_slut, antalknapptryck/0.75, bombchans)






    def konrolleragänser(x, y):
        class kontroll:
            def __init__(self, vänster, höger, upp, ned):
                self.vänster = vänster
                self.höger = höger
                self.upp = upp
                self.ned = ned

        if x < width - 1 and x > 0 and y < height - 1 and y > 0:
            return kontroll(-1, 2, 2, -1)
        else:
            if x == 0:
                if y > 0 and y < height - 1:
                    return kontroll(0, 2, 2, -1)
                elif y == 0:
                    return kontroll(0, 2, 2, 0)
                elif y == height - 1:
                    return kontroll(0, 2, 1, -1)
            elif x == width - 1:
                if y > 0 and y < height - 1:
                    return kontroll(-1, 1, 2, -1)
                elif y == 0:
                    return kontroll(-1, 1, 2, 0)
                elif y == height - 1:
                    return kontroll(-1, 1, 1, -1)
            elif y == 0:
                return kontroll(-1, 2, 2, 0)
            elif y == height - 1:
                return kontroll(-1, 2, 1, -1)

    def skapaspelplan(klickx, klicky):

        class ruta:
            grannar = 0
            bomb = False
            tom = False
            ursprungsruta = False
            synlig = False

        spelplan = [[ruta() for l in range(width + 1)] for h in range(height + 1)]
        spelplan[klickx][klicky].ursprungsruta = True
        tommarutor = 1

        while tommarutor < antaltomma:
            "denna loop skapar det tomma området runt där man klickar första gången"
            tommarutor += 1
            UtgångspunktFörTomtOmrådeX = klickx
            UtgångspunktFörTomtOmrådeY = klicky
            while True:
                if spelplan[UtgångspunktFörTomtOmrådeX][UtgångspunktFörTomtOmrådeY].ursprungsruta == False:
                    spelplan[UtgångspunktFörTomtOmrådeX][UtgångspunktFörTomtOmrådeY].ursprungsruta = True
                    break
                steg = random.randint(1, 4)
                if steg == 1 and UtgångspunktFörTomtOmrådeX != width:
                    UtgångspunktFörTomtOmrådeX += 1
                elif steg == 2 and UtgångspunktFörTomtOmrådeX != 0:
                    UtgångspunktFörTomtOmrådeX -= 1
                elif steg == 3 and UtgångspunktFörTomtOmrådeY != height:
                    UtgångspunktFörTomtOmrådeY += 1
                elif steg == 4 and UtgångspunktFörTomtOmrådeY != 0:
                    UtgångspunktFörTomtOmrådeY -= 1

        bomber=0
        while bomber < antalbomber:
            randomX = random.randint(0, width - 1)
            randomY = random.randint(0, height - 1)
            if spelplan[randomX][randomY].ursprungsruta == False and spelplan[randomX][randomY].bomb == False:
                "om det inte är en bomb eller uttryckligen tom ruta så placerar den ut en bomb och " \
                "informerar grannar om att det är en bomb i närhetetn"
                spelplan[randomX][randomY].bomb = True
                tilldelagrannar = konrolleragänser(randomX, randomY)
                for sida in range(tilldelagrannar.vänster, tilldelagrannar.höger):
                    for höjd in range(tilldelagrannar.ned, tilldelagrannar.upp):
                        spelplan[randomX + sida][randomY + höjd].grannar += 1
                bomber+=1


        for sidled in range(width):
            for höjdled in range(height):
                "om en ruta är helt tom och inte har några grannar tilldelas den attributet TOM"
                if spelplan[sidled][höjdled].grannar == 0 and spelplan[sidled][höjdled].bomb == False:
                    spelplan[sidled][höjdled].tom = True

        return spelplan

    def åtgärder_vid_synliggörande(x, y):
        spelinfo[x][y].synlig = True
        rutnät[x][y].unbind("<Button-1>")
        rutnät[x][y].unbind("<Button-3>")
        if spelinfo[x][y].bomb==True:
            rutnät[x][y].config(image=mina)
        elif spelinfo[x][y].grannar == 0:
            rutnät[x][y].config(image=noll)
        elif spelinfo[x][y].grannar == 1:
            rutnät[x][y].config(image=ett)
        elif spelinfo[x][y].grannar == 2:
            rutnät[x][y].config(image=två)
        elif spelinfo[x][y].grannar == 3:
            rutnät[x][y].config(image=tre)
        elif spelinfo[x][y].grannar == 4:
            rutnät[x][y].config(image=fyra)
        elif spelinfo[x][y].grannar == 5:
            rutnät[x][y].config(image=fem)
        elif spelinfo[x][y].grannar == 6:
            rutnät[x][y].config(image=sex)
        nonlocal kvar_till_vinst
        kvar_till_vinst -= 1
        print(kvar_till_vinst)
        if kvar_till_vinst == 0:
            winner()



    def gör_ruta_synlig(x, y):
        if spelinfo[x][y].bomb == False:
            gräns = konrolleragänser(x, y)
            åtgärder_vid_synliggörande(x, y)
            if spelinfo[x][y].grannar == 0:
                for sida in range(gräns.vänster, gräns.höger):
                    for höjden in range(gräns.ned, gräns.upp):
                        if spelinfo[x+sida][y+höjden].synlig==False and spelinfo[x+sida][y+höjden].bomb==False:
                            gör_ruta_synlig(x+sida, y+höjden)
        if spelinfo[x][y].bomb == True:
            loser()

    def knapptryck(x, y):
        nonlocal antalknapptryck
        if antalknapptryck == 0:
            nonlocal spelinfo
            spelinfo = skapaspelplan(x, y)
            gräns = konrolleragänser(x, y)
            for sida in range(gräns.vänster, gräns.höger):
                for höjden in range(gräns.ned, gräns.upp):
                    if spelinfo[x + sida][y + höjden].synlig == False and spelinfo[x + sida][y + höjden].bomb == False:
                        gör_ruta_synlig(x + sida, y + höjden)
        gör_ruta_synlig(x, y)
        antalknapptryck += 1

    def återgåfrånfalgga(x, y):
        rutnät[x][y].config(image=gråruta)
        rutnät[x][y].bind("<Button-1>", lambda e, knapptryck=knapptryck: knapptryck(x, y))
        rutnät[x][y].bind("<Button-3>", lambda e, knapptryck=knapptryck: flagga(x, y))

    def flagga(x, y):
        rutnät[x][y].config(image=flag)
        rutnät[x][y].unbind("<Button-1>")
        rutnät[x][y].bind("<Button-3>", lambda e, återgåfrånfalgga=återgåfrånfalgga: återgåfrånfalgga(x, y))

    def skaparuta(rad, kollumn):
        label = Label(window, image=gråruta, cursor="tcross")
        label.grid(column=kollumn + 1, row=rad + 1)
        label.bind("<Button-1>", lambda e, knapptryck=knapptryck: knapptryck(rad, kollumn))
        label.bind("<Button-3>", lambda e, flagg=flagga: flagga(rad, kollumn))
        return label

    for x in range(width):
        for y in range(height):
            rutnät[x][y] = skaparuta(x, y)

    mainloop()


def main():
    window = Tk()

    väljhöjd = Label(window, text="välj höjd på spelplanen, minst 8 enheter: ")
    väljhöjd.grid(row=1, column=1, columnspan=2)
    höjdinput = Entry(window)
    höjdinput.grid(row=1, column=3)
    väljbredd = Label(window, text="välj bredd på spelplanen, minst 8 enheter: ")
    väljbredd.grid(row=2, column=1, columnspan=2)
    breddinput = Entry(window)
    breddinput.grid(row=2, column=3)

    def sätt_igång_spelet(svårighetsgrad):
        tid_start = time.time()
        spelbredd = int(breddinput.get())
        spelhöjd = int(höjdinput.get())
        if spelbredd >= 8 and spelhöjd >= 8:
            antaltomma = (spelhöjd * spelbredd) // 10
            if antaltomma > 10:
                antaltomma = 10
            bombchans = svårighetsgrad * 0.085
            window.destroy()
            spelet(spelhöjd, spelbredd, bombchans, antaltomma, tid_start)


        else:
            felmeddelande = Label(window, text="kontrollera inputs och försök igen")
            felmeddelande.grid(row=4, column=1, columnspan=3)

    spelasvår = Button(window, text="Expert", command=lambda: sätt_igång_spelet(4)).grid(row=3, column=3)
    spelamedel = Button(window, text="medel", command=lambda: sätt_igång_spelet(3)).grid(row=3, column=2)
    spelalätt = Button(window, text="nybörjare", command=lambda: sätt_igång_spelet(2)).grid(row=3, column=1)
    tomruta = Label(window, text="")
    tomruta.grid(row=4, column=1)

    mainloop()





main()
