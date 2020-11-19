from tkinter import *
import time
import tkinter
import math
import random

def spelet(bredd, höjd, antalbomber, antaltomma):

    window = Tk()
    rutbild = PhotoImage(file=r"tile.png")
    gråruta = rutbild.subsample(8,8)
    oformateradflagga = PhotoImage(file=r"flag.png")
    flag=oformateradflagga.subsample(36, 36)
    nollan = PhotoImage(file=r"0.png")
    noll = nollan.subsample(8, 8)
    ettan = PhotoImage(file=r"1.png")
    ett = ettan.subsample(8,8)
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

    rutnät = [[0 for h in range(höjd)] for b in range(bredd)]
    antalknapptryck=0

    class ruta:
        grannar=0
        bomb=False
        tom=False
        ursprungsruta=False
        synlig = False


    def konrolleragänser(x, y):
        class kontroll:
            def __init__(self, vänster, höger, upp, ned):
                self.vänster=vänster
                self.höger = höger
                self.upp = upp
                self.ned = ned

        if x < bredd-1 and x > 0 and y < höjd-1 and y > 0:
            return kontroll(-1, 2, 2, -1)
        else:
            if x == 0:
                if y > 0 and y < höjd-1:
                    return kontroll(0, 2, 2, -1)
                elif y == 0:
                    return kontroll(0, 2, 2, 0)
                elif y == höjd-1:
                    return kontroll(0, 2, 1, -1)
            elif x == bredd-1:
                if y > 0 and y < höjd-1:
                    return kontroll(-1, 1, 2, -1)
                elif y == 0:
                    return kontroll(-1, 1, 2, 0)
                elif y == höjd-1:
                    return kontroll(-1, 1, 1, -1)
            elif y == 0:
                return kontroll(-1, 2, 2, 0)
            elif y == höjd-1:
                return kontroll(-1, 2, 1, -1)



    def skapaspelplan(längd, höjd, antalbomber, klickx, klicky, antaltomma):
        spelplan=[[(ruta()) for l in range (längd+1)]for h in range (höjd+1)]
        spelplan[klickx][klicky].tom = True
        tommarutor=1


        while tommarutor < antaltomma:
            print("oke")
            "denna loop skapar det tomma området runt där man klickar första gången"
            tommarutor +=1
            UtgångspunktFörTomtOmrådeX = klickx
            UtgångspunktFörTomtOmrådeY = klicky
            while True:
                if spelplan[UtgångspunktFörTomtOmrådeX][UtgångspunktFörTomtOmrådeY].tom==False:
                    spelplan[UtgångspunktFörTomtOmrådeX][UtgångspunktFörTomtOmrådeY].tom=True
                    spelplan[UtgångspunktFörTomtOmrådeX][UtgångspunktFörTomtOmrådeY].ursprungsruta=True
                    spelplan[UtgångspunktFörTomtOmrådeX][UtgångspunktFörTomtOmrådeY].synlig=True
                    break
                steg=random.randint(1,4)
                if steg == 1 and UtgångspunktFörTomtOmrådeX != längd:
                    UtgångspunktFörTomtOmrådeX += 1
                elif steg == 2 and UtgångspunktFörTomtOmrådeX != 0:
                    UtgångspunktFörTomtOmrådeX -= 1
                elif steg == 3 and UtgångspunktFörTomtOmrådeY != höjd:
                    UtgångspunktFörTomtOmrådeY += 1
                elif steg == 4 and UtgångspunktFörTomtOmrådeY != 0:
                    UtgångspunktFörTomtOmrådeY -= 1


        for x in range (längd):
            for y in range (höjd):
                r = random.random()
                if r < antalbomber:
                    if spelplan[x][y].ursprungsruta==False and spelplan[x][y].bomb==False:
                        "om det inte är en bomb eller uttryckligen tom ruta så placerar den ut en bomb och " \
                        "informerar grannar om att det är en bomb i närhetetn"
                        spelplan[x][y].bomb=True

                        tilldelagrannar = konrolleragänser(x, y)
                        for sida in range(tilldelagrannar.vänster, tilldelagrannar.höger):
                            for höjd in range(tilldelagrannar.ned, tilldelagrannar.upp):
                                spelplan[x + sida][y + höjd].grannar += 1

        for sidled in range (längd):
            for höjdled in range(höjd):
                "om en ruta är helt tom och inte har några grannar tilldelas den attributet TOM"
                if spelplan[sidled][höjdled].grannar == 0 and spelplan[sidled][höjdled].bomb==False:
                    spelplan[sidled][höjdled].tom=True
                    print(spelplan[sidled][höjdled].tom + spelplan[sidled][höjdled].bomb)
        return spelplan


    def åtgärder_vid_synliggörande (x, y):
        spelinfo[x][y].synlig = True
        rutnät[x][y].unbind("<Button-1>")
        rutnät[x][y].unbind("<Button-3>")
        if spelinfo[x][y].bomb ==False:
            if spelinfo[x][y].grannar == 0:
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



    def gör_ruta_synlig(x, y):
        if spelinfo[x][y].bomb==False:
            gränser = konrolleragänser(x, y)
            for sida in range(gränser.vänster, gränser.höger):
                for höjden in range(gränser.ned, gränser.upp):
                    if spelinfo[x + sida][y + höjden].bomb == False:
                        åtgärder_vid_synliggörande(x+sida, y+höjden)
                        if spelinfo[x + sida][y + höjden].tom == True and spelinfo[x + sida][y + höjden].synlig == False:
                            gör_ruta_synlig((x + sida), (y + höjden))
        if spelinfo[x][y].bomb == True:
            rutnät[x][y].config(image=mina)



    def knapptryck (x, y):
        nonlocal antalknapptryck
        if antalknapptryck==0:
            global spelinfo
            spelinfo = skapaspelplan(bredd, höjd,antalbomber, x, y , antaltomma)
            for b in range (bredd):
                for h in range (höjd):
                    gör_ruta_synlig(b, h)
        else:
            gör_ruta_synlig(x, y)
        antalknapptryck +=1


    def återgåfrånfalgga(x, y):
        rutnät[x][y].config(image=gråruta)
        rutnät[x][y].bind("<Button-1>", lambda e, knapptryck=knapptryck:knapptryck(x, y))
        rutnät[x][y].bind("<Button-3>", lambda e, knapptryck=knapptryck:flagga(x, y))

    def flagga (x, y):
        rutnät[x][y].config(image=flag)
        rutnät[x][y].unbind("<Button-1>")
        rutnät[x][y].bind("<Button-3>", lambda e, återgåfrånfalgga=återgåfrånfalgga:återgåfrånfalgga(x, y))


    def skaparuta (rad, kollumn):
        label = Label(window, image=gråruta)
        label.grid(column=kollumn+1, row=rad+1)
        label.bind("<Button-1>", lambda e, knapptryck=knapptryck:knapptryck(rad, kollumn))
        label.bind("<Button-3>", lambda e, flagg=flagga:flagga(rad, kollumn))
        return label


    for x in range(höjd):
        for y in range (bredd):
            rutnät[x][y]=skaparuta(x, y)











    mainloop()

def main():
    window = Tk()



    väljhöjd = Label(window, text="välj höjd på spelplanen, minst 8 enheter: ")
    väljhöjd.grid(row=1, column=1, columnspan=2)
    höjdinput = Entry(window)
    höjdinput.grid(row=1, column=3)
    väljbredd =Label(window, text="välj bredd på spelplanen, minst 8 enheter: ")
    väljbredd.grid(row=2, column=1, columnspan=2)
    breddinput = Entry(window)
    breddinput.grid(row=2, column=3)

    def sätt_igång_spelet(svårighetsgrad):
        spelbredd = int(breddinput.get())
        spelhöjd = int (höjdinput.get())
        if spelbredd>=8 and spelhöjd>=8:
            antaltomma = (spelhöjd*spelbredd)//10
            if antaltomma > 10:
                antaltomma=10
            antalbomber = svårighetsgrad*0.075
            window.destroy()
            tid = time.process_time()
            spelet(spelhöjd, spelbredd, antalbomber, antaltomma)

        else:
            felmeddelande = Label(window, text="kontrollera inputs och försök igen")
            felmeddelande.grid(row=4, column=1, columnspan=3)



    spelasvår = Button(window, text="Expert", command=lambda: sätt_igång_spelet(4)).grid(row=3, column=3)
    spelamedel = Button(window, text="medel", command=lambda: sätt_igång_spelet(3)).grid(row=3, column=2)
    spelalätt = Button(window, text="nybörjare", command=lambda: sätt_igång_spelet(2)).grid(row=3, column=1)
    tomruta = Label(window, text="")
    tomruta.grid(row=4, column=1)

    mainloop()


spelet(10,10,0.6, 9)

