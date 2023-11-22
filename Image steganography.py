from tkinter import *
from tkinter import filedialog
from PIL import ImageTk
import sys
import ast
import cv2
import os


def browseFiles():
    global back_but, img_n
    back_but.config(command=lambda: [op_msg.config(text="Welcome!", font=("Cambria", 12), padx=10, bg="#fff1dc", fg="#93493c"), enc_window.destroy(), encryptimg()])
    img_n = filedialog.askopenfilename()
    op_msg.config(text ="Image: "+img_n, font=("Cambria", 12), bg = "#fff1dc", fg = "Black")
    op_msg.grid(row= 0, column= 0, columnspan=3)

with open("database.txt", 'r') as f:
        nl = f.readlines()
new_id = "uid" + str(len(nl))

def encryptimg():
    opening_window.destroy()
    global back_but, enc_window
    back_but.config(command=lambda:[enc_window.destroy(), back_but.destroy(), display_op()])
    back_but.place(x= 20, y =550)
    
    enc_window = Frame(root)
    enc_window.config(bg = "#fff1dc", padx= 0, pady =10)
    enc_window.place(x = 0,y = 30, width= 500, height= 500)

    browse_Img = Button(enc_window)
    browse_Img.config(text = "Browse Image", font=("Cambria", 14),padx = 0, bg = "#93493c", fg = "white", command=lambda:[browseFiles(), browse_Img.destroy()])
    browse_Img.place(x= 180, y = 100 , width = 150, height= 40)
    
    sec_msg = Label(enc_window)
    sec_msg.config(text = "Enter message:", pady =0, font=("Cambria", 13), fg = "#93493c", bg = "#fff1dc")
    sec_msg.place(x= 80, y = 200)

    sec_msg_inp = Entry(enc_window)
    sec_msg_inp.config(font=("Cambria", 13), fg = "#93493c")
    sec_msg_inp.place(x= 220, y = 200, width= 200)

    sec_pwd = Label(enc_window)
    sec_pwd.config(text = "Enter password:", pady =0, font=("Cambria", 13), fg = "#93493c", bg = "#fff1dc")
    sec_pwd.place(x= 80, y = 250)

    sec_pwd_inp = Entry(enc_window)
    sec_pwd_inp.config(font=("Cambria", 13), fg = "#93493c")
    sec_pwd_inp.place(x= 220, y = 250, width= 200)


    def takeinp():
        back_but.destroy()
        global exit_but
        exit_but.destroy()
        global msg, password
        msg= sec_msg_inp.get()
        password = sec_pwd_inp.get()
        encrypt()


    def encrypt():
        try:
            img = cv2.imread(img_n)
            enc_window.destroy()
            d = {}
            c = {}

            for i in range(255):
                d[chr(i)] = i
                c[i] = chr(i)

            m = 0
            n = 0
            z = 0

            for i in range(len(msg)):
                img[n, m, z] = d[msg[i]]
                n = n + 1
                m = m + 1
                z = (z + 1) % 3
    
            cv2.imwrite(f"{new_id}.png", img)
    
            with open("database.txt", 'w') as fl:
                for i in range(len(nl)):
                    fl.write(f"{str(nl[i])}")
                fl.write("\n")
                fl.write(f"{new_id}<br_data>{password}<br_data>{len(msg)}<br_data>{str(c)}")

            final_msgboxbg = Frame(root)
            final_msgboxbg.config(bg = "Dark Blue")
            final_msgboxbg.place(x=98, y = 128, width = 304 , height = 304)

            final_msgbox = Frame(root)
            final_msgbox.config(bg = "#e08b6a")
            final_msgbox.place(x=100, y = 130, width = 300 , height = 300)

            final_msg = Label(final_msgbox, text = "Encryption Successful!")
            final_msg.config( font=("Cambria", 15), fg = "white", bg = "#e08b6a")
            final_msg.place(x=60, y = 60)

            final_id = Label(final_msgbox, text = "Your ID: "+new_id)
            final_id.config(font=("Cambria", 13), fg = "white", bg = "#e08b6a")
            final_id.place(x=100, y=120)

            final_pwd = Label(final_msgbox, text="Password: "+password)
            final_pwd.config(font=("Cambria", 13), fg = "white", bg="#e08b6a")
            final_pwd.place(x=100, y=150)

            final_ok = Button(final_msgbox)
            final_ok.config(text="Continue", font=("Cambria", 13), bg="Light Green", fg ="black", command = lambda:[root.destroy(), stego()])
            final_ok.place(x= 75, y= 200, width= 150)

            final_exit = Button(final_msgbox)
            final_exit.config(text="Exit", font=("Cambria", 13), bg="Light Green", fg ="black", command = exit_fn)
            final_exit.place(x= 75, y= 250, width= 150)
        except:
            op_msg.config(text="Empty Input fields..RETRY!! ", bg="#93493c", fg="white", padx=170)
            lambda:[enc_window.destroy(), encryptimg()]

    sub_but = Button(enc_window)
    sub_but.config(text = "Encrypt Inputs", font=("Cambria", 14),fg= "white", bg = "#93493c" , command = takeinp)
    sub_but.place(x = 180, y = 320 , width = 150, height= 40)

        
def decryptimg():
    opening_window.destroy()
    
    global back_but
    back_but.config(command=lambda:[dec_window.destroy(), back_but.destroy(), display_op()])
    back_but.place(x= 20, y =550)
  
    dec_window =Frame(root)
    dec_window.config(bg = "#fff1dc", padx= 0, pady =10)
    dec_window.place(x = 0,y = 30, width= 500, height= 500)
    
    id = Label(dec_window)
    id.config(text = "Enter your ID :", pady =0, font=("Cambria", 13), fg = "#93493c", bg = "#fff1dc")
    id.place(x= 100, y = 200)

    id_inp = Entry(dec_window)
    id_inp.config(font=("Cambria", 13), fg = "#93493c")
    id_inp.place(x= 220, y = 200, width= 200)
    
    def search_user():
        inp_id = id_inp.get()
        if not os.path.exists(f"{inp_id}.png"):
            op_msg.config(text = "Invalid ID, Try Again",padx= 190, pady =0, font=("Cambria", 13), fg = "white", bg = "#e08b6a")
            decryptimg()  
        else: 
            cstr =""    
            id_inp.destroy()
            op_msg.config(text = "User found", padx= 220, pady =0, font=("Cambria", 13), fg = "white", bg = "#e08b6a") 
            global back_but
            back_but.config(command=lambda:[dec_window.destroy(), back_but.destroy(), decryptimg()])
            back_but.place(x= 20, y =550)
            enterpas()
            global img
            img = cv2.imread(f"{inp_id}.png")
            for lines in nl:
                wordlist = lines.split("<br_data>")
                for num in range(len(wordlist)):
                    if wordlist[num] == inp_id:
                        global pw, msg_len
                        pw = wordlist[num + 1]
                        msg_len = int(wordlist[num + 2])
                        cstr = str(wordlist[num + 3])
                        break
            global c
            c = {}
            c = ast.literal_eval(cstr)
            
    find_but = Button(dec_window)
    find_but.config(text="Find User", font = ("Cambria", 13), bg="#93493c", fg="white", command=search_user)
    find_but.place(x= 200, y = 300, width= 100)      


def decrypt():
    global final_ok, final_exit, exit_but
    message = ""
    n = 0
    m = 0
    z = 0
    
    for i in range(msg_len):
        message = message + c[img[n, m, z]]
        n = n + 1
        m = m + 1
        z = (z + 1) % 3
    dec_window.destroy()
    back_but.destroy()
    exit_but.destroy()

    final_msgboxbg = Frame(root)
    final_msgboxbg.config(bg = "Dark Blue")
    final_msgboxbg.place(x=98, y = 128, width = 304 , height = 304)

    final_msgbox = Frame(root)
    final_msgbox.config(bg = "#e08b6a")
    final_msgbox.place(x=100, y = 130, width = 300 , height = 300)

    final_msg = Label(final_msgbox, text = "Decryption Successful!")
    final_msg.config( font=("Cambria", 15), fg = "white", bg = "#e08b6a")
    final_msg.place(x=50, y = 60)

    final_dec = Label(final_msgbox, text = "Decrypted message: \n"+message)
    final_dec.config(font=("Cambria", 13), fg = "white", bg = "#e08b6a")
    final_dec.place(x=70, y=120)

    final_ok = Button(final_msgbox)
    final_ok.config(text="Continue", font=("Cambria", 13), bg="Light Green", fg ="black", command = lambda:[root.destroy(), stego()])
    final_ok.place(x= 75, y= 170, width= 150)

    final_exit = Button(final_msgbox)
    final_exit.config(text="Exit", font=("Cambria", 13), bg="Light Green", fg ="black", command = exit_fn)
    final_exit.place(x= 75, y= 220, width= 150)


def checkpas():
    pas = pas_inp.get()
    global pw
    if pas == pw:
        decrypt()
    else:
        global exit_but
        back_but.destroy()
        exit_but.destroy()
        final_msgboxbg = Frame(root)
        final_msgboxbg.config(bg = "Dark Blue")
        final_msgboxbg.place(x=98, y = 128, width = 304 , height = 304)

        final_msgbox = Frame(root)
        final_msgbox.config(bg = "#e08b6a")
        final_msgbox.place(x=100, y = 130, width = 300 , height = 300)

        final_msg = Label(final_msgbox, text = "Decryption Failed!")
        final_msg.config( font=("Cambria", 15), fg = "white", bg = "#e08b6a")
        final_msg.place(x=50, y = 60)

        final_dec = Label(final_msgbox, text = "Invalid Password")
        final_dec.config(font=("Cambria", 13), fg = "white", bg = "#e08b6a")
        final_dec.place(x=70, y=120)

        final_ok = Button(final_msgbox)
        final_ok.config(text="Try Again", font=("Cambria", 13), bg="Orange", fg ="black", command = lambda:[dec_window.destroy(), enterpas()])
        final_ok.place(x= 75, y= 170, width= 150)

        final_exit = Button(final_msgbox)
        final_exit.config(text="Quit", font=("Cambria", 13), bg="Orange", fg ="black", command = exit_fn)
        final_exit.place(x= 75, y= 220, width= 150)


def enterpas():
    global dec_window
    dec_window =Frame(root)
    dec_window.config(bg = "#fff1dc", padx= 0, pady =10)
    dec_window.place(x = 0,y = 30, width= 500, height= 500)
    
    pas_lab = Label(dec_window)
    pas_lab.config(text = "Enter Password :", pady =0, font=("Cambria", 13), fg = "#93493c", bg = "#fff1dc")
    pas_lab.place(x= 100, y = 200)

    global pas_inp
    pas_inp = Entry(dec_window)
    pas_inp.config(font=("Cambria", 13), fg = "#93493c")
    pas_inp.place(x= 220, y = 200, width= 200)

    global sub_but                
    sub_but = Button(dec_window)
    sub_but.config(text="Submit", font = ("Cambria", 13), bg="#93493c", fg="white", command=lambda:[exit_but.destroy(), checkpas()] )
    sub_but.place(x= 200, y = 300, width= 100)

    exit_but = Button(root, text="Quit", font=("Cambria", 12), padx=5, bg= "#93493c", fg= "white", command= exit_fn)
    exit_but.place(x= 430, y = 550)


def exit_fn():
    root.destroy()
    sys.exit(0)


def display_op():
    global opening_window, op_msg, back_but, exit_but
    op_msg = Label(root, text= "Welcome!", font=("Cambria", 12), padx=10, bg = "#fff1dc", fg = "#93493c") 
    op_msg.place(x= 0 , y= 0)

    opening_window = Frame(root)
    opening_window.config(bg = "#fff1dc")
    opening_window.place(x = 0,y = 30, width= 500, height= 500)

    enc_but = Button(opening_window, text = "Encrypt", font=("Cambria", 16), command = encryptimg )
    enc_but.config(bg= "#93493c", fg= "white", padx= 0, pady= 0)
    enc_but.place(x = 200, y = 130)

    dec_but = Button(opening_window, text = "Decrypt", font=("Cambria", 16), command = decryptimg )
    dec_but.config(bg= "#93493c", fg= "white", padx= 0, pady= 0)
    dec_but.place(x = 200, y = 330)

    exit_but = Button(root, text="Quit", font=("Cambria", 12), padx=5, bg= "#93493c", fg= "white", command= exit_fn)
    exit_but.place(x= 430, y = 550)

    back_but = Button(root)
    back_but.config(text="Back", font=("Cambria", 12),padx = 5, bg = "#93493c", fg = "white")

    root.mainloop()


def stego():
    global root
    root = Tk()
    root.minsize(500, 600)
    root.maxsize(500, 600)
    icon = ImageTk.PhotoImage(file = 'logo.png')
    root.iconphoto(False, icon)
    root.title("SteganoSafe")
    root.config(bg="#fff1dc")
    display_op()

stego()