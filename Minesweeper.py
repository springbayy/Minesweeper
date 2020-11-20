from tkinter import *
import time
import math
import random

def slut(tid_start, tid_slut, knapptryck, bombchans):
    "denna funktion kallas på när spelet är slut. den skapar en ruta som visar ens poäng samt "
    "top 10. poängen baseras på passerad tid samt hur många rutor man röjt undan och om man klarar llt eller inte"

    poäng = int((bombchans*knapptryck)/(tid_slut-tid_start+10)*1000)
    toppplista_skriv = open('topplista', 'a')
    toppplista_skriv.write(str(poäng)+'\n')
    toppplista_skriv.close()
    toppplista_läs = open('topplista')
    topplista = toppplista_läs.read()
    sorterad_topplista = topplista.split()
    for n in range (len(sorterad_topplista)):
        sorterad_topplista[n]=int(sorterad_topplista[n])
    sorterad_topplista.sort(reverse=True)

    window = Tk()
    "denna del skapar fönstret"
    rubrik = Label(window, text="Resultat", pady=8, padx=8).grid(row= 1, column=1, columnspan=2)
    din_poäng_text = Label(window, text="Din poäng", pady=8, padx=8).grid(row= 2, column=1)
    din_poäng = Label(window, text=str(poäng), pady=8, padx=8).grid(row=2, column=2)
    bästa_genom_tiderna = Label(window, text="Bästa resultat genom tiderna", pady=8, padx=8).grid(row= 3, column=1, columnspan=2)
    resultat_rutor = [[2] for i  in range (min(10, len(sorterad_topplista)))]
    for rutor in range (min(10, len(sorterad_topplista))):
        resultat_rutor[0]= Label(window, text=str(rutor+1) + ".", pady=8, padx=8).grid(row= (4 + rutor), column=1)
        resultat_rutor[1] = Label(window, text=str(sorterad_topplista[rutor]) + " poäng", pady=8, padx=8).grid(row=4 + rutor, column=2)




def spelet(width, height, bombchans, antaltomma, tid_start):
    "detta är den stora funktionen som skapar minesweeper"
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

    "vital information"
    rutnät = [[0 for h in range(height)] for b in range(width)]
    spelinfo = 0
    antalknapptryck = 0
    korrekta_flaggor= 0
    antalbomber=math.ceil(((width*height)-antaltomma)*bombchans)
    kvar_till_vinst = (width*height) - antalbomber + 1

    def loser():
        "åtgärd om man förlorar BOOM"
        tid_slut = time.time()
        for x in range (width):
            for y in range(height):
                åtgärder_vid_synliggörande(x, y)
        slut(tid_start, tid_slut, antalknapptryck, bombchans)
        info_om_flaggor = Label(window, text="Antal korrekt markerade Minor: " + str(korrekta_flaggor)+ "/"+str(antalbomber)).grid(row=1, column=1, columnspan=height)

    def winner():
        "åtgärd om man röjer alla rutor"
        tid_slut = time.time()
        for x in range(width):
            for y in range(height):
                rutnät[x][y].unbind("<Button-1>")
                rutnät[x][y].unbind("<Button-3>")
                if spelinfo [x][y].bomb==True:
                    rutnät[x][y].config(image=flag)
        slut(tid_start, tid_slut, antalknapptryck/0.75, bombchans)



    def konrolleragänser(x, y):
        "denna funktion kallas på när en del av programmet ska kolla på rutorna runtikring sig"
        "den ollar att inget är utanför listan och returnerar objektet kontroll som har 4 värden som är giltiga ställen att kolla eter i listan"
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
        "denna funtion skapar spelaplanen och returnerar en lista med object 'ruta' som har alla attribut man behöver för varje ruta"

        class ruta:
            grannar = 0
            bomb = False
            tom = False
            ursprungsruta = False
            synlig = False
            flaggad =False

        spelplan = [[ruta() for l in range(height + 1)] for h in range(width + 1)]
        spelplan[klickx][klicky].ursprungsruta = True
        tommarutor = 1

        while tommarutor < antaltomma:
            "denna loop skapar tomma rutorna vid första trycket genom att slumpmässsigt gå runtikring den punkten och tilldela attributet utsprungsruta och tom"
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
            "denna loop placerar ut bomber slumpmässigt"
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
        "om en ruta synliggörs så visas olika bilder beroende på vad det är för någon ruta"
        spelinfo[x][y].synlig = True
        rutnät[x][y].unbind("<Button-1>")
        rutnät[x][y].unbind("<Button-3>")
        if spelinfo[x][y].flaggad == False:
            if spelinfo[x][y].bomb==True:
                print(spelinfo[x][y].flaggad)
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



    def gör_ruta_synlig(x, y):
        "denna funktion gör rutor synliga, den har även uppdraget att via rekursion synliggöra alla rutor i ett samanhängande"
        "område om dem har 0 bomber som grannar"
        if spelinfo[x][y].bomb == False:
            gräns = konrolleragänser(x, y)
            åtgärder_vid_synliggörande(x, y)
            if spelinfo[x][y].grannar == 0:
                for sida in range(gräns.vänster, gräns.höger):
                    for höjden in range(gräns.ned, gräns.upp):
                        if spelinfo[x+sida][y+höjden].synlig==False and spelinfo[x+sida][y+höjden].bomb==False:
                            gör_ruta_synlig(x+sida, y+höjden)
            if kvar_till_vinst == 0:
                "om man röjt alla rutor utan minor vinner man"
                winner()
        elif spelinfo[x][y].bomb == True:
            loser()

    def knapptryck(x, y):
        "denna funktion aktiveras vid varje vänsterklick och om det är första klicket skapar den hela spelplanen (dvs om antalknapptryck==0)"
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
        "låter ruta gå från flagga till vanlig ruta"
        rutnät[x][y].config(image=gråruta)
        rutnät[x][y].bind("<Button-1>", lambda e, knapptryck=knapptryck: knapptryck(x, y))
        rutnät[x][y].bind("<Button-3>", lambda e, knapptryck=knapptryck: flagga(x, y))
        if spelinfo[x][y].bomb ==True:
            spelinfo[x][y].flaggad = False
            nonlocal korrekta_flaggor
            korrekta_flaggor -= 1

    def flagga(x, y):
        "låter en ruta bli o-klickbar och visar flagga"
        rutnät[x][y].config(image=flag)
        rutnät[x][y].unbind("<Button-1>")
        rutnät[x][y].bind("<Button-3>", lambda e, återgåfrånfalgga=återgåfrånfalgga: återgåfrånfalgga(x, y))
        if spelinfo[x][y].bomb ==True:
            spelinfo[x][y].flaggad = True
            print(spelinfo[x][y].flaggad)
            nonlocal korrekta_flaggor
            korrekta_flaggor += 1

    def skaparuta(rad, kollumn):
        "denna funktion skapar spelplanen med alla bilder det första som händer"
        label = Label(window, image=gråruta, cursor="tcross")
        label.grid(column=kollumn + 1, row=rad + 2)
        label.bind("<Button-1>", lambda e, knapptryck=knapptryck: knapptryck(rad, kollumn))
        label.bind("<Button-3>", lambda e, flagg=flagga: flagga(rad, kollumn))
        return label

    for x in range(width):
        for y in range(height):
            rutnät[x][y] = skaparuta(x, y)
            "denna loop har i uppgift att skap alla rutor och att tilldela alla Labels en position i en matris"

    mainloop()


def main():
    "denna funktion sätter alla parametrar för spelet innan man börjar"
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
        "denna funktion sätter igång spelet med de valda parametrar man valt"
        try:
            spelbredd = int(breddinput.get())
            spelhöjd = int(höjdinput.get())
        except ValueError:
            "felhantering"
            felmeddelande = Label(window, text="kontrollera inputs och försök igen")
            felmeddelande.grid(row=4, column=1, columnspan=3)

        else:
            if spelbredd < 8 or spelhöjd < 8:
                "felhantering"
                felmeddelande = Label(window, text="kontrollera inputs och försök igen")
                felmeddelande.grid(row=4, column=1, columnspan=3)
            else:
                tid_start = time.time()
                antaltomma = int(math.sqrt(spelhöjd * spelbredd))
                if antaltomma > 20:
                    antaltomma = 20
                bombchans = svårighetsgrad * 0.07
                window.destroy()
                spelet(spelhöjd, spelbredd, bombchans, antaltomma, tid_start)


    spelasvår = Button(window, text="Expert", command=lambda: sätt_igång_spelet(4)).grid(row=3, column=3)
    spelamedel = Button(window, text="medel", command=lambda: sätt_igång_spelet(3)).grid(row=3, column=2)
    spelalätt = Button(window, text="nybörjare", command=lambda: sätt_igång_spelet(2)).grid(row=3, column=1)
    tomruta = Label(window, text="")
    tomruta.grid(row=4, column=1)

    mainloop()





main()
