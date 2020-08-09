#!/usr/bin/env python3
# coding: utf-8

import os
import sys

# Python2
# import Tkinter as tk
# import tkMessageBox as messagebox
# import ttk

# Python3
import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk

os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

import string_def as sdf
import string_rec as src
import string_data as sda
import string_lr as slr


def run_click():
    # run_btn.grid_forget()
    # data_exp_label_text.set("Recording...")
    messagebox.showinfo("Rcording", "After ckicking [OK] button,\nplease hit your racket face near PC.")

    sdef = sdf.StringDef(stype)
    main_s = ""
    cross_s = ""
    if main_s_comb.get() != "":
        main_s = sdef.get_key_from_name(main_s_comb.get())
    if cross_s_comb.get() != "":
        cross_s = sdef.get_key_from_name(cross_s_comb.get())

    args = ""
    if stype == "B":
        args = sda.get_argstr(stype, main_t_comb.get(), cross_t_comb.get(), main_s, cross_s, "", "", "")
    if stype == "T":
        args = sda.get_argstr(stype, main_t_comb.get(), cross_t_comb.get(), main_s, cross_s, size_comb.get(), main_n_comb.get(), cross_n_comb.get())

    csv_append = 0
    if data_comb.get() == "Yes":
        csv_append = 1

    if csv_append == 0:
        srec = src.StringRec(args, "tmp/")
    if csv_append == 1:
        srec = src.StringRec(args)

    # data_exp_label_text.set("Calculating...")

    tension = []
    for filename in srec.get_file_list():
        sdata = sda.StringData()
        sdata.make_data(filename, csv_append)
        sl = slr.StringLr01(stype)
        xlist = sl.get_lrdata_xlist(sdata)
        tension.append(sl.get_lrcal_tension(xlist))

    srec.init_file_list()

    rstr = ""
    total = 0.0
    avg = 0.0
    for i, val in enumerate(tension):
        rstr += str(i+1) + ": " + str(round(val, 2)) + " Lbs\n"
        total += float(val)
    avg = total/len(tension)
    rstr += "Average: " + str(round(avg, 2)) + " Lbs"
    messagebox.showinfo("Results", rstr)

    main_win.focus_force()
    # main_win.destroy()

def make_win():
    global main_win
    main_win = tk.Tk()
    win_w = main_win.winfo_screenwidth()
    win_h = main_win.winfo_screenheight()
    app_w = 530
    app_h = 290
    if stype == "B":
        app_h = 200
    main_win.geometry(get_center_geometry_str(win_w, win_h, app_w, app_h))
    main_win.title("Stringing DATA")

    main_frm = ttk.Frame(main_win)
    main_frm.grid(column=0, row=0, sticky=tk.NSEW, padx=5, pady=10)

    sdef = sdf.StringDef(stype)
    if stype == "T":
        t_list = list(range(0,81))
        t_current = 50
    if stype == "B":
        t_list = list(range(0,41))
        t_current = 20

    main_t_label = ttk.Label(main_frm, text="Main Tension")
    global main_t_comb
    main_t_comb = ttk.Combobox(main_frm, values=t_list, state="readonly", width=5)
    main_t_comb.current(t_current)
    cross_t_label = ttk.Label(main_frm, text="Cross Tension")
    global cross_t_comb
    cross_t_comb = ttk.Combobox(main_frm, values=t_list, state="readonly", width=5)
    main_s_label = ttk.Label(main_frm, text="Main String")
    global main_s_comb
    main_s_comb = ttk.Combobox(main_frm, values=sdef.get_name_list(), state="readonly", width=30)
    main_s_comb.current(0)
    cross_s_label = ttk.Label(main_frm, text="Cross String")
    global cross_s_comb
    cross_s_comb = ttk.Combobox(main_frm, values=sdef.get_name_list(), state="readonly", width=30)

    if stype == "T":
        s_list = list(range(0,141))
        size_label = ttk.Label(main_frm, text="Face Size (in2)")
        global size_comb
        size_comb = ttk.Combobox(main_frm, values=s_list, state="readonly", width=5)
        size_comb.current(100)
        pat_list = list(range(0,31))
        main_n_label = ttk.Label(main_frm, text="Main Number")
        global main_n_comb
        main_n_comb = ttk.Combobox(main_frm, values=pat_list, state="readonly", width=5)
        main_n_comb.current(16)
        cross_n_label = ttk.Label(main_frm, text="Cross Number")
        global cross_n_comb
        cross_n_comb = ttk.Combobox(main_frm, values=pat_list, state="readonly", width=5)
        cross_n_comb.current(19)

    data_label = ttk.Label(main_frm, text="Append DATA")
    global data_exp_label
    global data_exp_label_text
    data_exp_label_text = tk.StringVar()
    data_exp_label_text.set("If you have just finished stringing, select Append DATA = Yes.")
    data_exp_label = ttk.Label(main_frm, textvariable=data_exp_label_text)
    global data_comb
    data_comb = ttk.Combobox(main_frm, values=["Yes", "No"], state="readonly", width=5)
    data_comb.current(1)
    global run_btn
    run_btn = ttk.Button(main_frm, text="RUN", command=run_click)

    main_t_label.grid(column=0, row=0)
    main_t_comb.grid(column=1, row=0, sticky=tk.W, padx=5)
    cross_t_label.grid(column=0, row=1)
    cross_t_comb.grid(column=1, row=1, sticky=tk.W, padx=5)
    main_s_label.grid(column=0, row=2)
    main_s_comb.grid(column=1, row=2, sticky=tk.W, padx=5)
    cross_s_label.grid(column=0, row=3)
    cross_s_comb.grid(column=1, row=3, sticky=tk.W, padx=5)
    if stype == "T":
        size_label.grid(column=0, row=4)
        size_comb.grid(column=1, row=4, sticky=tk.W, padx=5)
        main_n_label.grid(column=0, row=5)
        main_n_comb.grid(column=1, row=5, sticky=tk.W, padx=5)
        cross_n_label.grid(column=0, row=6)
        cross_n_comb.grid(column=1, row=6, sticky=tk.W, padx=5)
        data_label.grid(column=0, row=7)
        data_comb.grid(column=1, row=7, sticky=tk.W, padx=5)
        data_exp_label.grid(column=1, row=8)
        run_btn.grid(column=1, row=9)
    else:
        data_label.grid(column=0, row=4)
        data_comb.grid(column=1, row=4, sticky=tk.W, padx=5)
        data_exp_label.grid(column=1, row=5)
        run_btn.grid(column=1, row=6)

    main_win.columnconfigure(0, weight=1)
    main_win.rowconfigure(0, weight=1)
    main_win.columnconfigure(0, weight=1)

    main_win.mainloop()

def stype_click_t():
    global stype
    stype = "T"
    main_win.destroy()
    make_win()

def stype_click_b():
    global stype
    stype = "B"
    main_win.destroy()
    make_win()

def get_center_geometry_str(win_w, win_h, app_w, app_h):
    center_w = int((win_w-app_w)/2)
    center_h = int((win_h-app_h)/2)
    return str(app_w)+"x"+str(app_h)+"+"+str(center_w)+"+"+str(center_h)


main_win = tk.Tk()
win_w = main_win.winfo_screenwidth()
win_h = main_win.winfo_screenheight()
app_w = 300
app_h = 330
main_win.geometry(get_center_geometry_str(win_w, win_h, app_w, app_h))

main_win.title("Get Tension")
main_win.configure(bg="white")
logo = tk.PhotoImage(file="logo_270.gif")
logo_label = tk.Label(main_win, image=logo)
py_logo = tk.PhotoImage(file="python-powered-w-200x80.gif")
py_logo_label = tk.Label(main_win, image=py_logo)
label = tk.Label(text="Please select type of sports.")
copy_label = tk.Label(text="Copyright (C) 2020 Yukihiko Sugimura.")
t_btn = ttk.Button(main_win, text="Tennis", command=stype_click_t)
b_btn = ttk.Button(main_win, text="Badminton", command=stype_click_b)

logo_label.pack()
label.pack()
t_btn.pack(fill="x")
b_btn.pack(fill="x")
py_logo_label.pack()
copy_label.pack()

main_win.mainloop()
