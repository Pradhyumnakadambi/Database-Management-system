import tkinter
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector as sc
import pickle

# Establishing connection to SQL database
sql_con = sc.connect(host="localhost", user='root', passwd="12345", database="School", port=3307)
cursor = sql_con.cursor()

# Creation of window
Root = tkinter.Tk()
Root.configure(bg='black')
Root.resizable(False, False)
frame = tkinter.Frame(Root)
frame.pack()
Root.geometry("550x450")


# Table structure - width of columns
def indent(table):
    temp = 0
    sz = []
    sz1 = []
    while temp < 5:
        for row in table:
            for elm in range(len(row)):
                if elm == temp:
                    sz.append(len(str(row[temp])))
                else:
                    continue
        if sz:
            sz1.append(max(sz))
        temp += 1
        sz = []
    return sz1


# Table structure - Main
# Displaying record(s)
class tab:
    def __init__(self, table):
        self.table = table
        self.root = tkinter.Tk()
        rows = len(self.table)
        columns = len(self.table[0])
        wid = indent(self.table)
        ret = tkinter.Button(self.root, text="Close", command=self.root.destroy)
        ret.grid(row=rows + 1, column=0, sticky=tkinter.W)
        for i in range(rows):
            for j in range(columns):
                if i == 0:
                    selfent = tkinter.Entry(self.root, width=wid[j], fg='black',
                                            font=('Ariel', 16, "bold"))
                else:
                    selfent = tkinter.Entry(self.root, width=wid[j], fg='black',
                                            font=('Calibre(body)', 16))
                selfent.grid(row=i, column=j)
                selfent.insert(tkinter.END, table[i][j])

    def destroy(self):
        self.root.destroy()


# Destroying widgets on screen
class Screen_clear:
    def __init__(self, *argv):
        for i in argv:
            i.destroy()

    def mn(self, fun):
        fun


# Main menu
def main():
    global Root, hd, inst, disp, srech, updt, delt, qt

    hd = tkinter.Label(Root, text="Prison Management System", font=('calibre', 12, 'italic', 'bold'))
    inst = tkinter.Button(Root, text="Insert data", command=insert, font=('calibre', 10), height=2, width=12)
    disp = tkinter.Button(Root, text="Display records", command=display, font=('calibre', 10), height=2, width=12)
    srech = tkinter.Button(Root, text="Search records", command=search, font=('calibre', 10), height=2, width=12)
    updt = tkinter.Button(Root, text="Update records", command=update, font=('calibre', 10), height=2, width=12)
    delt = tkinter.Button(Root, text="Delete records", command=delete, font=('calibre', 10), height=2, width=12)
    qt = tkinter.Button(Root, text="Quit", command=quit, font=('calibre', 10),  height=2, width=12)

    Root.configure(bg='black')

    hd.pack()
    inst.place(x=25, y=50)
    disp.place(x=415, y=50)
    srech.place(x=25, y=100)
    updt.place(x=415, y=100)
    delt.place(x=25, y=150)
    qt.place(x=415, y=150)


# Displaying personal information of inmates
def display_info():
    def srch():
        cursor.execute("Select prisonID from prison")
        nm = cursor.fetchall()
        prs = Prsent.get()
        with open("Prisoner.dat", 'rb') as file:
            rec = []
            try:
                while True:
                    try:
                        D = pickle.load(file)
                        rec.append(D)
                    except EOFError:
                        break
            except FileNotFoundError:
                print("File not found.")

        rw = 3
        rcrd = None
        flag = 2
        for i in range(len(nm)):
            if prs in nm[i]:
                for j in range(len(rec)):
                    if prs == (rec[j]["PrisonID"]):
                        flag = 1
                        rcrd = rec[j]
                        break
                    else:
                        flag = 0

        if flag == 1:
            widg = Screen_clear(prslab, Prsent, fnd, ret, frame)
            lab = tkinter.Label(Root, text=f"PrisonID: {rcrd['PrisonID']}",
                                font=('calibre', 10, 'bold'), bg='black', fg='white')
            lab.grid(row=1, column=0, sticky=tkinter.W, padx=10, pady=10)
            L = [lab]
            for i in rcrd["Information"]:
                inflab = tkinter.Label(Root, text=f'{i}: {rcrd["Information"][i]}',
                                       font=('calibre', 10, 'bold'), bg='black', fg='white')
                L.append(inflab)
                inflab.grid(row=rw, column=0, sticky=tkinter.W, padx=10, pady=10)
                rw += 1

            def fun():
                L.append(butn)
                for i in L:
                    i.destroy()
                widg.mn(display_info())

            butn = tkinter.Button(Root, text="<- Go back", command=fun)
            butn.grid(row=rw, column=0, padx=10, sticky=tkinter.W)

        elif flag == 0:
            messagebox.showerror(title="Error", message="No information has been added to this record.")
            Prsent.delete(0, tkinter.END)

        else:
            messagebox.showerror(title="Error", message="Record not found.")
            Prsent.delete(0, tkinter.END)

    def fun():
        widg = Screen_clear(prslab, Prsent, fnd, ret, frame)
        widg.mn(display())

    prslab = tkinter.Label(Root, text="PrisonID", font='calibre, 10', bg='black', fg='white')
    Prs = tkinter.StringVar()
    Prsent = tkinter.Entry(Root, textvariable=Prs)
    prslab.grid(row=0, column=0, sticky=tkinter.W, padx=10, pady=10)
    Prsent.grid(row=0, column=1, sticky=tkinter.W, padx=10, pady=10)

    fnd = tkinter.Button(Root, text="Find", command=srch)
    ret = tkinter.Button(Root, text="<- Go back", command=fun)
    fnd.grid(row=1, column=1, sticky=tkinter.E, padx=10)
    ret.grid(row=1, column=0, sticky=tkinter.W, padx=10)


# Information on crime
def crime():
    def srch():
        crm = crment.get().lower()
        crment.delete(0, tkinter.END)
        with open("Crime.dat", 'rb') as file:
            try:
                while True:
                    try:
                        L = pickle.load(file)
                        x = L.keys()
                        flag = False
                        for i in x:
                            if crm.lower() == i.lower():
                                Screen_clear(crmlab, crment, but, mn)
                                msg = tkinter.Message(Root, text=L[i], font=('calibre', 12), bg='black', fg='white',
                                                      width=500)

                                def fun():
                                    widg = Screen_clear(msg, ret)
                                    widg.mn(crime())

                                ret = tkinter.Button(Root, text="<- Go back", command=fun)
                                msg.pack()
                                ret.pack(side=tkinter.LEFT)
                                flag = True
                        if flag:
                            break
                    except EOFError:
                        msg = messagebox.showerror(title="Error", message="Crime not in database.")
                        break

            except FileNotFoundError:
                msg = messagebox.showerror(title="Error", message="File not found.")

    def retr():
        widg = Screen_clear(crmlab, crment, but, mn)
        widg.mn(display())

    crmlab = tkinter.Label(Root, text="Crime", font=('calibre', 10), bg="black", fg="white")
    crmst = tkinter.StringVar()
    crment = tkinter.Entry(Root, textvariable=crmst)
    but = tkinter.Button(Root, text="Enter", command=srch)
    mn = tkinter.Button(Root, text="<- Go back", command=retr)

    crmlab.grid(row=0, column=0, sticky=tkinter.W, padx=10, pady=10)
    crment.grid(row=0, column=1, sticky=tkinter.W, padx=10, pady=10)
    but.grid(row=1, column=1, sticky=tkinter.E, padx=10, pady=10)
    mn.grid(row=1, column=0, sticky=tkinter.W, padx=10, pady=10)


# Displaying entire table
def display():
    Screen_clear(hd, inst, disp, srech, updt, delt, qt)

    def disrec():
        global t
        cursor.execute("describe prison")
        nm = cursor.fetchall()
        header = [i[j] for i in nm for j in range(len(i)) if j == 0]
        cursor.execute("select * from Prison")
        table = cursor.fetchall()
        table.insert(0, header)
        t = tab(table)

    def fun(func):
        try:
            t.destroy()
        except:
            pass
        widg = Screen_clear(but1, but2, but3, but4, frame)
        widg.mn(func())

    but1 = tkinter.Button(Root, text="View all records", command=disrec, font=('calibre', 10))
    but2 = tkinter.Button(Root, text="View prisoner data", command=lambda: fun(display_info), font=('calibre', 10))
    but3 = tkinter.Button(Root, text="Information on crimes", command=lambda: fun(crime), font=('calibre', 10))
    but4 = tkinter.Button(Root, text="Return to menu", command=lambda: fun(main), font=('calibre', 10))

    but1.pack(pady=10)
    but2.pack(pady=10)
    but3.pack(pady=10)
    but4.pack(pady=10)


# Personal details of inmates
def add():
    cursor.execute("Select prisonID from prison")
    nm = cursor.fetchall()

    prslb = tkinter.Label(Root, text="PrisonID", font=('calibre', 10), bg='black', fg='white', padx=10, pady=10)
    prsee = tkinter.StringVar()
    prsent = tkinter.Entry(Root, textvariable=prsee)
    prslb.grid(row=0, column=0, sticky=tkinter.W, padx=10)
    prsent.grid(row=0, column=1, sticky=tkinter.W, padx=10)

    def appnd():
        prs = prsent.get()
        cursor.execute(f"Select * from Prison where prisonID = '{prs}'")
        rec = cursor.fetchone()
        cursor.execute("Describe prison")
        desc = cursor.fetchall()
        header = [i[j] for i in desc for j in range(len(i)) if j == 0]

        def apd():
            for i in nm:
                if prs in i:
                    Screen_clear(prslb, ent, Gb, prsent)
                    table = [header, rec]
                    t = tab(table)

                    gen_lab = tkinter.Label(Root, text="Gender", font=('calibre', 10), bg='black', fg='white',
                                            padx=10, pady=10)
                    nat_lab = tkinter.Label(Root, text="Nationality", font=('calibre', 10), bg='black', fg='white',
                                            padx=10, pady=10)
                    pf_lab = tkinter.Label(Root, text="Physical features", font=('calibre', 10), bg='black', fg='white',
                                           padx=10, pady=10)
                    dob_lab = tkinter.Label(Root, text="Date of birth", font=('calibre', 10), bg='black', fg='white',
                                            padx=10, pady=10)
                    add_lab = tkinter.Label(Root, text="Last known address", font=('calibre', 10), bg='black',
                                            fg='white', padx=10, pady=10)
                    pc_lab = tkinter.Label(Root, text="Past crimes", font=('calibre', 10), bg='black', fg='white',
                                           padx=10, pady=10)
                    fm_lab = tkinter.Label(Root, text="Family situation", font=('calibre', 10), bg='black', fg='white',
                                           padx=10, pady=10)
                    imp_lab = tkinter.Label(Root, text="Date of imprisonment", font=('calibre', 10), bg='black',
                                            fg='white', padx=10, pady=10)
                    rel_lab = tkinter.Label(Root, text="Date of release", font=('calibre', 10), bg='black', fg='white',
                                            padx=10, pady=10)

                    gen_ent = tkinter.StringVar()
                    nat_ent = tkinter.StringVar()
                    pf_ent = tkinter.StringVar()
                    dob_ent = tkinter.StringVar()
                    add_ent = tkinter.StringVar()
                    pc_ent = tkinter.StringVar()
                    fm_ent = tkinter.StringVar()
                    imp_ent = tkinter.StringVar()
                    rel_ent = tkinter.StringVar()

                    gen_e = tkinter.Entry(Root, textvariable=gen_ent)
                    nat_e = tkinter.Entry(Root, textvariable=nat_ent)
                    pf_e = tkinter.Entry(Root, textvariable=pf_ent)
                    dob_e = tkinter.Entry(Root, textvariable=dob_ent)
                    add_e = tkinter.Entry(Root, textvariable=add_ent)
                    pc_e = tkinter.Entry(Root, textvariable=pc_ent)
                    fm_e = tkinter.Entry(Root, textvariable=fm_ent)
                    imp_e = tkinter.Entry(Root, textvariable=imp_ent)
                    rel_e = tkinter.Entry(Root, textvariable=rel_ent)

                    gen_lab.grid(row=0, column=0, sticky=tkinter.W, padx=10)
                    gen_e.grid(row=0, column=1, sticky=tkinter.W, padx=10)
                    nat_lab.grid(row=1, column=0, sticky=tkinter.W, padx=10)
                    nat_e.grid(row=1, column=1, sticky=tkinter.W, padx=10)
                    pf_lab.grid(row=2, column=0, sticky=tkinter.W, padx=10)
                    pf_e.grid(row=2, column=1, sticky=tkinter.W, padx=10)
                    dob_lab.grid(row=3, column=0, sticky=tkinter.W, padx=10)
                    dob_e.grid(row=3, column=1, sticky=tkinter.W, padx=10)
                    add_lab.grid(row=4, column=0, sticky=tkinter.W, padx=10)
                    add_e.grid(row=4, column=1, sticky=tkinter.W, padx=10)
                    pc_lab.grid(row=5, column=0, sticky=tkinter.W, padx=10)
                    pc_e.grid(row=5, column=1, sticky=tkinter.W, padx=10)
                    fm_lab.grid(row=6, column=0, sticky=tkinter.W, padx=10)
                    fm_e.grid(row=6, column=1, sticky=tkinter.W, padx=10)
                    imp_lab.grid(row=7, column=0, sticky=tkinter.W, padx=10)
                    imp_e.grid(row=7, column=1, sticky=tkinter.W, padx=10)
                    rel_lab.grid(row=8, column=0, sticky=tkinter.W, padx=10)
                    rel_e.grid(row=8, column=1, sticky=tkinter.W, padx=10)

                    def adif():
                        gen = gen_e.get()
                        nat = nat_e.get()
                        pf = pf_e.get()
                        dob = dob_e.get()
                        address = add_e.get()
                        pc = pc_e.get()
                        fm = fm_e.get()
                        imp = imp_e.get()
                        rel = rel_e.get()

                        cursor.execute("Select name from prison")
                        nm1 = cursor.fetchall()
                        x = 0
                        for i in range(len(nm)):
                            if nm[i][0] == prs:
                                x = i
                                break

                        name = nm1[x][0]

                        with open("Prisoner.dat", 'ab') as fil:
                            inf = {"Prisoner": name,
                                   "Gender": gen,
                                   "Nationality": nat,
                                   "Physical features": pf,
                                   "Date of Birth": dob,
                                   "Last known address": address,
                                   "Past Crimes": pc,
                                   "Family situation": fm,
                                   "Date of imprisonment": imp,
                                   "Date of release": rel}
                            d = {"PrisonID": prs, "Information": inf}
                            pickle.dump(d, fil)

                        messagebox.showinfo(title="Success", message="Information has been added")
                        widg = Screen_clear(ad, gb, gen_lab, nat_lab, pf_lab, dob_lab, add_lab, pc_lab, fm_lab, imp_lab,
                                            rel_lab,
                                            gen_e, nat_e, pf_e, dob_e, add_e, pc_e, fm_e, imp_e, rel_e)
                        t.destroy()
                        widg.mn(add())

                    def fun1():
                        t.destroy()
                        widg = Screen_clear(ad, gb, gen_lab, nat_lab, pf_lab, dob_lab, add_lab, pc_lab, fm_lab, imp_lab,
                                            rel_lab,
                                            gen_e, nat_e, pf_e, dob_e, add_e, pc_e, fm_e, imp_e, rel_e)
                        widg.mn(add())

                    ad = tkinter.Button(Root, text="Add information", command=adif)
                    ad.grid(row=9, column=1, sticky=tkinter.E, padx=10, pady=10)
                    gb = tkinter.Button(Root, text="<- Go back", command=fun1)
                    gb.grid(row=9, column=0, sticky=tkinter.W, padx=10, pady=10)
                    break
            else:
                messagebox.showerror(title="Error", message="Prisoner not found")
                prsent.delete(0, tkinter.END)

        flag = 0
        with open("Prisoner.dat", 'rb') as file:
            try:
                while True:
                    try:
                        d = pickle.load(file)
                        if d["PrisonID"] == prs:
                            flag = 1
                    except EOFError:
                        break
            except FileNotFoundError:
                pass
        if flag == 1:
            txt = "Would you like to overwrite the existing information?"
            x = messagebox.askyesno("Warning", txt)
            if x:
                file = open("Prisoner.dat", 'rb')
                l = []
                while True:
                    try:
                        d = pickle.load(file)
                        l.append(d)
                    except EOFError:
                        break
                file = open("Prisoner.dat", 'wb')
                for i in l:
                    if i["PrisonID"] != prs:
                        pickle.dump(i, file)
                    else:
                        continue
                file.close()
                apd()
            else:
                pass
        else:
            apd()

    def fun():
        widg = Screen_clear(prslb, prsent, Gb, ent)
        widg.mn(insert())

    ent = tkinter.Button(Root, text="Enter", command=appnd)
    ent.grid(row=1, column=1, sticky=tkinter.E, padx=10, pady=10)
    Gb = tkinter.Button(Root, text="<- Go back", command=fun)
    Gb.grid(row=1, column=0, padx=10, pady=10)


# Appending records
def insert():
    Screen_clear(hd, inst, disp, srech, updt, delt, qt)

    prison_id = tkinter.StringVar()
    name = tkinter.StringVar()
    crm = tkinter.StringVar()
    sntc = tkinter.StringVar()
    bail = tkinter.StringVar()

    def insrec():
        Screen_clear(but1, but2, but3, frame)
        ID = tkinter.Label(Root, text="Prison ID", font=('calibre', 10), bg='black', fg='white', padx=10, pady=10)
        Name = tkinter.Label(Root, text="Name", font=('calibre', 10), bg='black', fg='white', padx=10, pady=10)
        crim = tkinter.Label(Root, text="Crime", font=('calibre', 10), bg='black', fg='white', padx=10, pady=10)
        snt = tkinter.Label(Root, text="Sentence", font=('calibre', 10), bg='black', fg='white', padx=10, pady=10)
        bal = tkinter.Label(Root, text="Bail", font=('calibre', 10), bg='black', fg='white', padx=10, pady=10)

        i_dent = tkinter.Entry(Root, textvariable=prison_id)
        name_ent = tkinter.Entry(Root, textvariable=name)
        crime_ent = tkinter.Entry(Root, textvariable=crm)
        sentence_ent = tkinter.Entry(Root, textvariable=sntc)
        bail_ent = tkinter.Entry(Root, textvariable=bail)

        name_ent.insert(0, "Unknown")
        sentence_ent.insert(0, "-")
        bail_ent.insert(0, "-")

        def submit():
            prsid = i_dent.get()
            nam = name_ent.get()
            cr = crime_ent.get()
            snc = sentence_ent.get()
            bai = bail_ent.get()

            if nam == "":
                nam = "Unknown"
            if snc == "":
                snc = "-"
            if bai == "":
                bai = "-"

            if prsid != "" and cr != "":
                try:
                    cursor.execute(f"Insert into Prison values('{prsid}', '{nam}', '{cr}', '{snc}', '{bai}')")
                    sql_con.commit()

                    i_dent.delete(0, tkinter.END)
                    name_ent.delete(0, tkinter.END)
                    name_ent.insert(0, "Unknown")
                    crime_ent.delete(0, tkinter.END)
                    sentence_ent.delete(0, tkinter.END)
                    sentence_ent.insert(0, "-")
                    bail_ent.delete(0, tkinter.END)
                    bail_ent.insert(0, "-")
                    messagebox.showinfo(title="Success", message="Record has been added")

                except sc.errors.IntegrityError:
                    messagebox.showerror(title="Error", message="PrisonID already exists.")

                except sc.errors.DataError:
                    messagebox.showerror(title="Error", message="Data too long for some column(s).")
            else:
                messagebox.showerror(title="Error", message="Some fields are empty.")

        ID.grid(row=0, column=0, sticky=tkinter.W, padx=10)
        i_dent.grid(row=0, column=1, sticky=tkinter.W, padx=10)
        Name.grid(row=1, column=0, sticky=tkinter.W, padx=10)
        name_ent.grid(row=1, column=1, sticky=tkinter.W, padx=10)
        crim.grid(row=2, column=0, sticky=tkinter.W, padx=10)
        crime_ent.grid(row=2, column=1, sticky=tkinter.W, padx=10)
        snt.grid(row=3, column=0, sticky=tkinter.W, padx=10)
        sentence_ent.grid(row=3, column=1, sticky=tkinter.W, padx=10)
        bal.grid(row=4, column=0, sticky=tkinter.W, padx=10)
        bail_ent.grid(row=4, column=1, sticky=tkinter.W, padx=10)

        def fun():
            widg = Screen_clear(ID, i_dent, Name, name_ent, crim, crime_ent, snt, sentence_ent, bal, bail_ent, frame,
                                ret, sub)
            widg.mn(insert())

        ret = tkinter.Button(Root, text="<- Go back", command=fun)
        ret.grid(row=5, column=0, sticky=tkinter.W, padx=10, pady=10)
        sub = tkinter.Button(Root, text="Insert", command=submit)
        sub.grid(row=5, column=1, sticky=tkinter.E, padx=10, pady=10)

    def fun():
        widg = Screen_clear(but1, but2, but3)
        widg.mn(main())

    def fun1():
        widg = Screen_clear(but1, but2, but3, frame)
        widg.mn(add())

    but1 = tkinter.Button(Root, text="Insert records", command=insrec, font=('calibre', 10))
    but2 = tkinter.Button(Root, text="Insert prisoner information", command=fun1, font=('calibre', 10))
    but3 = tkinter.Button(Root, text="Return to menu", command=fun, font=('calibre', 10))

    but1.pack(pady=10)
    but2.pack(pady=10)
    but3.pack(pady=10)


# Searching for a record
def search():
    global flgl
    flgl = True
    Screen_clear(hd, inst, disp, srech, updt, delt, qt, frame)

    fld = tkinter.StringVar()
    cursor.execute("describe prison")
    nm = cursor.fetchall()
    header = [i[j] for i in nm for j in range(len(i)) if j == 0]
    fl = tkinter.Label(Root, text="Field", font='calibre, 10', bg='black', fg='white')
    fldent = tkinter.Entry(Root, textvariable=fld)
    fl.grid(row=0, column=0, sticky=tkinter.W, padx=10)
    fldent.grid(row=0, column=1, sticky=tkinter.W, padx=10)

    def srch():
        global flgl
        flgl = False
        flag = False
        field = fldent.get()
        field = field.capitalize()
        for i in header:
            if field.lower() == i.lower():
                flag = True

        if not flag:
            fldent.delete(0, tkinter.END)
            messagebox.showerror(title="Error", message="Field does not exist.")
            flgl = True

        else:
            val = tkinter.StringVar()
            valab = tkinter.Label(Root, text=f"{field}", font='calibre, 10', bg='black', fg='white')
            valent = tkinter.Entry(Root, textvariable=val)
            valab.grid(row=1, column=0, sticky=tkinter.W, padx=10, pady=10)
            valent.grid(row=1, column=1, sticky=tkinter.W, padx=10, pady=10)

            def fnd():
                global flgl, t
                value = valent.get()
                value = value.capitalize()
                field = fldent.get()
                cursor.execute(f"(Select * from prison where {field} = '{value}')")
                table = cursor.fetchall()

                if table != []:
                    table.insert(0, header)
                    t = tab(table)
                    flgl = True
                else:
                    messagebox.showerror(title="Error", message="Record not found.")
                    flgl = True

                valab.destroy()
                valent.destroy()
                ent.destroy()
                fldent.delete(0, tkinter.END)

            ent = tkinter.Button(Root, text="Search", command=fnd)
            ent.grid(row=2, column=2)

    def fun():
        if flgl:
            try:
                t.destroy()
            except:
                pass
            widg = Screen_clear(ret, ent, fl, fldent, frame)
            widg.mn(main())
        else:
            messagebox.showerror(title="Error", message="Please complete the process")

    ret = tkinter.Button(Root, text="Return to menu", command=fun, font=('calibre', 10))
    ret.grid(row=2, column=0, sticky=tkinter.W, padx=10, pady=10)
    ent = tkinter.Button(Root, text="Enter", command=srch, font=('calibre', 10))
    ent.grid(row=2, column=2, sticky=tkinter.E, padx=10, pady=10)


# Updating a record
def update():
    Screen_clear(hd, inst, disp, srech, updt, delt, qt, frame)
    global flg, entr, fldbt
    entr = tkinter.Button(Root)
    fldbt = tkinter.Button(Root)

    cursor.execute("describe prison")
    nm = cursor.fetchall()
    header = [i[j] for i in nm for j in range(len(i)) if j == 0]
    prs = tkinter.StringVar()
    prslab = tkinter.Label(Root, text="Prison ID", font=('calibre', 10), bg='black', fg='white')
    prsent = tkinter.Entry(Root, textvariable=prs)
    prslab.grid(row=0, column=0, sticky=tkinter.W, padx=10, pady=10)
    prsent.grid(row=0, column=1, sticky=tkinter.W, padx=10, pady=10)
    flg = True

    def upd():
        global flg, fldbt, entr, t
        prsid = prsent.get()
        cursor.execute(f"Select * from prison where prisonID = '{prsid}'")
        rec = cursor.fetchone()
        table = []
        flg = False

        if rec is not None:
            sub.destroy()
            table.append(header)
            table.append(rec)
            t = tab(table)

            fld = tkinter.StringVar()
            fl = tkinter.Label(Root, text="Field", font=('calibre', 10), bg='black', fg='white')
            fldent = tkinter.Entry(Root, textvariable=fld)
            fl.grid(row=1, column=0, sticky=tkinter.W, padx=10)
            fldent.grid(row=1, column=1, sticky=tkinter.W, padx=10)

            def updt():
                global flg
                flag = False
                fldval = fldent.get()
                for i in header:
                    if i.lower() == fldval.lower():
                        flag = True
                        break
                    else:
                        flag = False

                if not flag:
                    fldent.delete(0, tkinter.END)
                    messagebox.showerror(title="Error", message="Field does not exist.")
                else:
                    fldval = fldval.capitalize()
                    flg = False
                    fldbt.destroy()
                    newfl = tkinter.StringVar()
                    newflab = tkinter.Label(Root, text=f"New {fldval}", font=('calibre', 10), bg='black', fg='white')
                    newfent = tkinter.Entry(Root, textvariable=newfl)
                    newflab.grid(row=2, column=0, sticky=tkinter.W, padx=10, pady=10)
                    newfent.grid(row=2, column=1, sticky=tkinter.W, padx=10, pady=10)

                    def upfn():
                        global flg, entr
                        newfen = newfent.get()
                        try:
                            cursor.execute(f"Update prison set {fldval} = '{newfen}' where prisonID = '{prsid}'")
                            sql_con.commit()

                            if fldval.lower() in ["prisonid", "name"]:
                                file = open("Prisoner.dat", 'rb')
                                L = []
                                while True:
                                    try:
                                        D = pickle.load(file)
                                        L.append(D)
                                    except EOFError:
                                        break
                                file.close()

                                for i in L:
                                    if i["PrisonID"] == prsid:
                                        if fldval.lower() == "name":
                                            i["Information"]["Prisoner"] = newfen
                                            break
                                        else:
                                            i["PrisonID"] = newfen
                                            break

                                file = open("Prisoner.dat", 'wb')
                                for i in L:
                                    pickle.dump(i, file)
                                file.close()

                            messagebox.showinfo(title="Success", message="Record has been updated")
                            t.destroy()
                            flg = True

                            Screen_clear(fl, fldent, newflab, newfent, up)
                            prsent.delete(0, tkinter.END)
                            entr = tkinter.Button(Root, text="Enter", command=upd)
                            entr.grid(row=3, column=1, sticky=tkinter.E, padx=10, pady=10)

                        except sc.errors.IntegrityError:
                            messagebox.showerror(title="Error", message="PrisonID already exists")

                    up = tkinter.Button(Root, text="Update", command=upfn)
                    up.grid(row=3, column=1, sticky=tkinter.E, padx=10, pady=10)
                    entr.destroy()

            fldbt = tkinter.Button(Root, text="Enter", command=updt)
            fldbt.grid(row=3, column=1, sticky=tkinter.E, padx=10, pady=10)

        else:
            prsent.delete(0, tkinter.END)
            messagebox.showerror(title="Error", message="Record does not exist.")
            flg = True

    def fun():
        if flg:
            widg = Screen_clear(ret, entr, frame, sub, prsent, prslab, fldbt)
            widg.mn(main())
        else:
            messagebox.showerror(title="Error", message="Please complete the process")

    ret = tkinter.Button(Root, text="Return to menu", command=fun)
    ret.grid(row=3, column=0, sticky=tkinter.W, padx=10, pady=10)

    sub = tkinter.Button(Root, text="Enter", command=upd)
    sub.grid(row=3, column=1, sticky=tkinter.E, padx=10, pady=10)


# Deleting a record
def delete():
    Screen_clear(hd, inst, disp, srech, updt, delt, qt, frame)

    prsnid = tkinter.StringVar()
    idn = tkinter.Label(Root, text="Prison ID", font=('calibre', 10), bg='black', fg='white')
    prsnident = tkinter.Entry(Root, textvariable=prsnid)
    idn.grid(row=0, column=0, sticky=tkinter.W, padx=10)
    prsnident.grid(row=0, column=1, sticky=tkinter.W, padx=10)

    def deletefile(x):
        file = open("Prisoner.dat", 'rb')
        L = []

        while True:
            try:
                D = pickle.load(file)
                L.append(D)
            except EOFError:
                break
        file = open("Prisoner.dat", 'wb')
        for i in L:
            if i["PrisonID"] != x:
                pickle.dump(i, file)
            else:
                continue
        file.close()

    def displ():
        prsid = prsnident.get()
        cursor.execute("Select * from Prison where PrisonID = '%s'" % prsid)
        rec = cursor.fetchone()

        if rec is not None:
            table = []
            cursor.execute("describe prison")
            nm = cursor.fetchall()
            header = [i[j] for i in nm for j in range(len(i)) if j == 0]
            table.append(header)
            table.append(rec)
            t = tab(table)
            prsnident.delete(0, tkinter.END)
            x = messagebox.askokcancel(title="Confirm", message="The record is going to be permanently deleted")

            if x:
                cursor.execute("Delete from prison where PrisonID ='%s'" % prsid)
                sql_con.commit()
                deletefile(prsid)
                t.destroy()
            else:
                t.destroy()
                prsnident.delete(0, tkinter.END)

        else:
            messagebox.showerror(title="Error", message="Record does not exist")
            prsnident.delete(0, tkinter.END)

    def fun():
        widg = Screen_clear(subm, ret, idn, prsnident)
        widg.mn(main())

    subm = tkinter.Button(Root, text="Submit", command=displ, font=('calibre', 10))
    subm.grid(row=1, column=2, sticky=tkinter.W, padx=10, pady=10)
    ret = tkinter.Button(Root, text="Return to menu", command=fun, font=('calibre', 10))
    ret.grid(row=1, column=0, sticky=tkinter.E, padx=10, pady=10)


# UserID & password to access database
def password():
    frame = tkinter.Frame(Root)
    frame.pack(side=tkinter.TOP)

    btframe = tkinter.Frame(Root)
    btframe.pack(side=tkinter.TOP)
    bttframe = tkinter.Frame(Root)
    bttframe.pack(side=tkinter.TOP)

    frame.configure(bg='black')
    btframe.configure(bg='black')
    bttframe.configure(bg='black')

    def logn():
        usr_id = usrent.get()
        passwrd = pasent.get()
        if usr_id == "Abcde" and passwrd == "12345":
            widg = Screen_clear(usr, usrent, pas, pasent, log, btframe, bttframe, frame, hd, label)
            widg.mn(main())
        elif usr_id == "Abcde" or passwrd == "12345":
            pasent.delete(0, tkinter.END)
            messagebox.showerror(title="Error", message="UserID or password is incorrect")
        else:
            messagebox.showerror(title="Error", message="Account does not exist")
            pasent.delete(0, tkinter.END)
            usrent.delete(0, tkinter.END)

    userid = tkinter.StringVar()
    paswrd = tkinter.StringVar()

    hd = tkinter.Label(frame, text="Prison Management System", font=('calibre', 12, 'italic', 'bold'))

    usr = tkinter.Label(btframe, text="Username", font=('calibre', 11), bg='black', fg='white')
    usrent = tkinter.Entry(btframe, textvariable=userid)

    pas = tkinter.Label(bttframe, text="Password", font=('calibre', 11), bg='black', fg='white')
    pasent = tkinter.Entry(bttframe, textvariable=paswrd, show='*')
    log = tkinter.Button(bttframe, text="Login", command=logn)

    image = Image.open("prisonback.jpg")
    image = image.resize((290, 230))
    photo = ImageTk.PhotoImage(image)
    label = tkinter.Label(frame, image=photo)
    label.image = photo

    hd.pack()
    label.pack(pady=10)
    log.pack(side=tkinter.BOTTOM, padx=10, pady=10)
    pas.pack(side=tkinter.LEFT, padx=10)
    pasent.pack(side=tkinter.RIGHT, padx=10)
    usr.pack(side=tkinter.LEFT, padx=9)
    usrent.pack(side=tkinter.RIGHT, padx=10)

    Root.mainloop()


def frontpage():
    frame1 = tkinter.Frame(Root)
    frame1.pack()
    frame1.configure(bg="black")
    frame2 = tkinter.Frame(Root)
    frame2.pack()
    frame2.configure(bg="black")

    def fun():
        Screen_clear(header, lab1, lab2, lab3, frame1, frame2)
        password()

    header = tkinter.Label(frame1, text="Grade 12 Computer Science Project", font=('calibre', 15, 'italic', 'bold'))
    lab1 = tkinter.Label(frame2, text="Project: Prison Management System", font=('calibre', 12),
                         bg="black", fg="white")
    lab2 = tkinter.Label(frame2, text="Done by: Pradhyumna, Srinandana", font=('calibre', 12),
                         bg="black", fg="white")
    lab3 = tkinter.Button(frame2, text="Click here to continue", font=('calibre', 12), command=fun)
    header.pack(padx=10, pady=15)
    lab1.pack(padx=10, pady=10)
    lab2.pack(padx=10, pady=10)
    lab3.pack(padx=10, pady=10)
    Root.mainloop()

password()
