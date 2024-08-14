import tkinter as tk
import pyodbc as db
import ssl 
import smtplib
import cv2
from pathlib import Path
import os
import numpy as np
from PIL import Image as im
from PIL import ImageTk as itk
from tkinter import filedialog
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from email.message import EmailMessage
from tkinter.messagebox import showinfo
from tkcalendar import DateEntry
conn = db.connect('Driver={SQL Server};'
                      'Server=TUNLU-PC;'
                      'Database=TermProjectOOP;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()   
class RawMaterials():
    def __init__(self,name,dofsup,nameofsup,storexpire,scode,descrip):
        self.__name=name
        self.__dofsup=dofsup
        self.__nameofsup=nameofsup
        self.__storexpire=storexpire
        self.__scode=scode
        self.__descrip=descrip
    def get_name(self):
        return self.__name
    def get_dofsup(self):
        return self.__dofsup
    def get_nameofsup(self):
        return self.__nameofsup
    def get_storexpire(self):
        return self.__storexpire
    def get_scode(self):
        return self.__scode
    def get_descrip(self):
        return self.__descrip
    def set_name(self,name):
        self.__name=name
    def set_dofsup(self,dofsup):
        self.__dofsup=dofsup
    def set_nameofsup(self,nameofsup):
        self.__nameofsup=nameofsup
    def set_storexpire(self,expire):
        self.__storexpire=expire
    def set_scode(self,scode):
        self.__scode=scode
    def set_descrip(self,descrip):
        self.__descrip=descrip            
class Products(RawMaterials):
    def __init__(self,name,dofproduct,nameofcus,productexpire,scode,descrip):
        self.__name=name
        self.__dofproduct=dofproduct
        self.__nameofcus=nameofcus
        self.__productexpire=productexpire
        self.__scode=scode
        self.__descrip=descrip
    def get_name(self):
        return self.__name
    def get_dofproduct(self):
        return self.__dofproduct
    def get_nameofcus(self):
        return self.__nameofcus
    def get_productexpire(self):
        return self.__productexpire
    def get_scode(self):
        return self.__scode
    def get_descrip(self):
        return self.__descrip
    def set_name(self,name):
        self.__name=name
    def set_dofproduct(self,dofproduct):
        self.__dofproduct=dofproduct
    def set_nameofcus(self,nameofcus):
        self.__nameofcus=nameofcus
    def set_productexpire(self,expire):
        self.__productexpire=expire
    def set_scode(self,scode):
        self.__scode=scode
    def set_descrip(self,descrip):
        self.__descrip=descrip      
def Visualize():
    cap = cv2.VideoCapture(0)
    while True:
        _, frame = cap.read()
        cv2.imshow('Input', frame)
        key = cv2.waitKey(1)
        if key == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
def RawMatValues(bid):
    allvalues=cursor.execute("select name,Dateofpurchase,NameofSupplier,StorageExpirationDate,StorageCode,RawImagePath,Description,Count from tbl_rawmaterials where ID= ? ",(int(bid)))
    allvalues = cursor.fetchall()    
    temp=[]
    for i in allvalues:
        temp.append(i)    
    list1=str(temp[0])
    x=list1.replace("'","")
    y=x.replace("\r\n","")
    z=y.replace("(","")    
    sa=z.split(",") 
    data_a=sa[0]
    data_b=sa[1]
    data_c=sa[2]
    data_d=sa[3]
    data_e=sa[4]
    data_f=sa[6]
    data_g=sa[5]
    data_h=sa[7]
    frmShowRawinfo(data_a,data_b,data_c,data_d,data_e,data_f,data_g,data_h)     
def ProductsValues(event):
    allvalues=cursor.execute("select tbl_product.Name,tbl_product.DateOfProduction,tbl_product.CustomerName ,tbl_product.ProductExpirationDate,tbl_product.StorageCode,tbl_product.Description,tbl_product.ImagePath,tbl_product.Count from tbl_product inner join tbl_user on tbl_product.UserID=tbl_user.ID where tbl_product.Name= ? ",(selected_product.get()))
    allvalues = cursor.fetchall()    
    temp=[]
    for i in allvalues:
        temp.append(i)    
    list1=str(temp[0])
    x=list1.replace("'","")
    y=x.replace("\r\n","")
    z=y.replace("(","")    
    sa=z.split(",")    
    data_a=sa[0]
    data_b=sa[1]
    data_c=sa[2]
    data_d=sa[3]
    data_e=sa[4]
    data_f=sa[5]
    data_g=sa[6]
    data_h=sa[7]
    frmShowProduct(data_a,data_b,data_c,data_d,data_e,data_f,data_g,data_h) 
def btnAuth(username,password):   
    exactpass=cursor.execute("select name from tbl_user where username = ? and password = ?",(username,password))
    exactpass=cursor.fetchone()     
    if exactpass != None:        
        frmShowProduct()
    elif password=="":
        showinfo(title="Result",message="You have to fill the blanks and try again")
    else:
        showinfo(title="Result",message="Password is incorrect please try again")

    conn.commit()    
def select_file():   
   path.set(filedialog.askopenfilename(title="Select an Image", filetype=(('image    files','*.png'),('all files','*.*'))))
   if path.get()=="":
       showinfo(title="ERROR!!",message="You have to Select your image and try again")
   else:
       img=im.open(path.get())
       img=itk.PhotoImage(img)
       imgframe = Frame(firstWindow,bg="black",width=500,height=300)
       imgframe.place(x=400,y=350)
       label= Label(imgframe, image= img)
       label.image= img
       label.grid()
def user_changed(event):
    showinfo(title="Result",message=f'You Selected {selected_user.get()}!')
def btnCodeSender(mail):
    if mail=="":
        showinfo(title="Result",message="Please select your email from combobox")
    else:
        pass1=cursor.execute("select password from tbl_user where email = ?",(mail))
        pass1=cursor.fetchone()
        email_sender="termproject99@gmail.com"
        email_password="nqpmkxpuwynfrnbv"
        email_reciever=mail
        subject="Your Password"
        strmail="Your Password is :"+str(pass1)
        em=EmailMessage()
        em['From']= email_sender
        em['To']=email_reciever
        em['Subject']=subject
        context=ssl.create_default_context()
        em.set_content(strmail)
        with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
            smtp.login(email_sender,email_password)
            smtp.sendmail(email_sender,email_reciever,em.as_string())
        showinfo(title="Result",message="Your Password succesfully sended")      
def frmForgetPass(event):    
    for i in firstWindow.winfo_children():
        i.destroy()     
    firstWindow.title("Forget my password")
    firstWindow.geometry("690x690")
    frmForgetPassword=Frame(bg="#212943",width=690,height=690)
    frmForgetPassword.place(x=0,y=0)  
    lblEmail=Label(frmForgetPassword,text="Select Your Email Adress :",foreground="#e4bc9b",font=("Helvetica 16 bold italic"),bg="#212943")
    lblEmail.place(x=35,y=300)
    selected_email=tk.StringVar()
    cursor.execute('select email from tbl_user')
    resultmails=cursor.fetchall()
    results_for_comboboxmail = [result[0] for result in resultmails]     
    cbEmail=ttk.Combobox(frmForgetPassword,textvariable=selected_email,values=results_for_comboboxmail,width=40)    
    cbEmail.place(x=350,y=305)
    photosend1=im.open("./Photos/sendcode.png")
    photosendcode=itk.PhotoImage(photosend1)    
    btnReturn=ttk.Button(frmForgetPassword,image=photoreturn,command=frmLogin)    
    btnReturn.place(x=100,y=600) 
    ttk.Style().configure("TButton", padding=0,background="#212943")
    style = ttk.Style()
    style.theme_use('alt')
    style.configure('TButton', background = '#212943', foreground = 'white', width = 20, borderwidth=1, focusthickness=3, focuscolor='none')
    style.map('TButton', background=[('active','#212943')])    
    btnExit1=ttk.Button(frmForgetPassword,image=photoexit,command=DestroyBeforeAsk)
    btnExit1.place(x=25,y=600)
    btnSendCode=ttk.Button(frmForgetPassword,image=photosendcode,command=lambda:btnCodeSender(selected_email.get()))
    btnSendCode.place(x=475,y=600)
    firstWindow.mainloop()
def DestroyBeforeAsk():
    if messagebox.askokcancel("Quit","Do you want to quit?"):
        firstWindow.destroy()
def AddNewUser(name,surname,username,password,email):    
    if name=="" and surname=="" and username=="" and password=="" and email=="":
        showinfo(title="Result",message="Please fill all the blanks and try again")
    else:
        checkexistence=cursor.execute("select name from tbl_user where username = ? ",(username))
        checkexistence=cursor.fetchone()
        if checkexistence!=None:
            showinfo(title="Result",message="this username is registered in the system, please different username")
        else:           
            cursor.execute("insert into tbl_user(name,surname,username,password,email) values (?,?,?,?,?)",(name,surname,username,password,email))
            conn.commit()
            showinfo(title="Result",message="New User succesfully added!!")        
def NewUserFrame():
    for i in firstWindow.winfo_children():
        i.destroy()     
    firstWindow.title("New User")
    firstWindow.geometry("690x690")
    firstWindow.overrideredirect(True) 
    frmNewUser=Frame(bg="#212943",width=690,height=690)
    frmNewUser.place(x=0,y=0)
    lblname=Label(frmNewUser,text="Enter Your Name :",foreground="#e4bc9b",font=("Helvetica 14 bold italic"),bg="#212943")
    lblname.place(x=75,y=90)
    lblsurname=Label(frmNewUser,text="Enter Your Surname :",foreground="#e4bc9b",font=("Helvetica 14 bold italic"),bg="#212943")
    lblsurname.place(x=75,y=190)
    lblusername=Label(frmNewUser,text="Enter Your User Name :",foreground="#e4bc9b",font=("Helvetica 14 bold italic"),bg="#212943")
    lblusername.place(x=75,y=290)
    lblpassword=Label(frmNewUser,text="Enter Your Password :",foreground="#e4bc9b",font=("Helvetica 14 bold italic"),bg="#212943")
    lblpassword.place(x=75,y=390)
    lblattention=Label(frmNewUser,text="Please enter your e-mail correct, In case of losing your password, we will send a code to the e-mail you entered.",foreground="#e4bc9b",font=("Arial",8),bg="#212943")
    lblattention.place(x=75,y=530)
    lblemail=Label(frmNewUser,text="Enter Your E-Mail Adress :",foreground="#e4bc9b",font=("Helvetica 14 bold italic"),bg="#212943")
    lblemail.place(x=75,y=490)
    txtname=Entry(frmNewUser,width=45)
    txtname.place(x=350,y=95)
    txtsurname=Entry(frmNewUser,width=45)
    txtsurname.place(x=350,y=195)
    txtusername=Entry(frmNewUser,width=45)
    txtusername.place(x=350,y=295)
    txtpassword=Entry(frmNewUser,width=45)
    txtpassword.place(x=350,y=395)
    txtemail=Entry(frmNewUser,width=45)
    txtemail.place(x=350,y=495) 
    photosign1=im.open("./Photos/signup.png")
    photosignup=itk.PhotoImage(photosign1)
    ttk.Style().configure("TButton", padding=0,background="#212943")
    style = ttk.Style()
    style.theme_use('alt')
    style.configure('TButton', background = '#212943', foreground = 'white', width = 20, borderwidth=1, focusthickness=3, focuscolor='none')
    style.map('TButton', background=[('active','#212943')])    
    btnExit1=ttk.Button(frmNewUser,image=photoexit,command=DestroyBeforeAsk)
    btnExit1.place(x=25,y=600)
    btnSignup=ttk.Button(frmNewUser,image=photosignup,command=lambda: AddNewUser(txtname.get(), txtsurname.get(), txtusername.get(),txtpassword.get(),txtemail.get()))    
    btnSignup.place(x=475,y=600) 
    btnReturn=ttk.Button(frmNewUser,image=photoreturn,command=frmLogin)    
    btnReturn.place(x=100,y=600) 
    firstWindow.mainloop()
def xd(button: tk.Button):
    if button.config('relief')[-1] == 'sunken':
        button.config(relief="raised")
        button.config(background="#e4bc9b")
        button.config(foreground="#212943")
        return 0
    else:
        button.config(relief="sunken")
        button.config(background="saddlebrown")
        button.config(foreground="white")
        return 1
def frmLogin():
    for i in firstWindow.winfo_children():
        i.destroy()
    frame1=Frame(bg="#212943",width=690,height=690)
    frame1.place(x=0,y=0)    
    lblLogo=ttk.Label(frame1,image=photoLogo)
    lblLogo.configure(background='#212943')
    lblLogo.place(x=185,y=25)
    lblKadi=Label(frame1,text="Select Your Username :",foreground="#e4bc9b",font=("Helvetica 19 bold italic"),bg="#212943")
    lblKadi.place(x=35,y=350)
    lblPass=Label(frame1,text="Password :",foreground="#e4bc9b",font=("Helvetica 19 bold italic"),bg="#212943")
    lblPass.place(x=35,y=435)    
    cursor.execute('select username from tbl_user')
    results=cursor.fetchall()
    results_for_combobox = [result[0] for result in results] 
    cbUsername=ttk.Combobox(frame1,width=37,textvariable=selected_user,values=results_for_combobox)
    cbUsername.place(x=350,y=360)
    cbUsername.bind("<<ComboboxSelected>>",user_changed)
    txtPass1=Entry(frame1,width=40,show="*")
    txtPass1.place(x=350,y=445)
    lblForgetPass=Label(frame1,text="F̲o̲r̲g̲o̲t̲ ̲m̲y̲ ̲p̲a̲s̲s̲w̲o̲r̲d̲",fg="#e4bc9b",bg="#212943",font=("Helvetica 10 bold italic"))
    lblForgetPass.place(x=35,y=490)
    lblForgetPass.bind("<Button-1>",frmForgetPass)   
    photonewus=im.open("./Photos/btnNewUser.png")
    photonewuser=itk.PhotoImage(photonewus)  
    photolog=im.open("./Photos/login2.PNG")
    photologin=itk.PhotoImage(photolog)  
    ttk.Style().configure("TButton", padding=0,background="#212943")
    style = ttk.Style()
    style.theme_use('alt')
    style.configure('TButton', background = '#212943', foreground = 'white', width = 20, borderwidth=1, focusthickness=3, focuscolor='none')
    style.map('TButton', background=[('active','#212943')])    
    btnExit=ttk.Button(frame1,image=photoexit,command=DestroyBeforeAsk)     
    btnExit.place(x=35,y=570)
    btnNewUser=ttk.Button(frame1,image=photonewuser,command=NewUserFrame)
    btnNewUser.place(x=135,y=575)
    btnLogin=ttk.Button(frame1,image=photologin,command=lambda:btnAuth(selected_user.get(),txtPass1.get()))
    btnLogin.place(x=475,y=570)
    firstWindow.mainloop()
def AddNewProduct(UsID,Pname,DateProduction,DateExpire,StorageCode,Description,CustName,Raw1,Raw2,Raw3,Raw4,Raw5,ImagePath):
    if Pname=="" and DateProduction=="" and DateExpire=="" and StorageCode=="" and Description=="" and ImagePath=="" and CustName=="":
        showinfo(title="Result",message="Please fill all the blanks and try again")
    else:
        sa=str(UsID)
        sa.replace("'","")
        ba=sa.replace("(","")
        ca=ba.replace(")","")
        da=ca.replace(",","")
        ea=da.replace(" ","")
        checkexistence=cursor.execute("select ID from tbl_product where Name = ? ",(Pname))
        checkexistence=cursor.fetchone()
        if checkexistence!=None:
            showinfo(title="Result",message="This Product has allready exists,Try to add different Product")
        else:           
            cursor.execute("insert into tbl_product(UserID,Name,DateOfProduction,ProductExpirationDate,StorageCode,Description,CustomerName,ImagePath,RawMaterial1,RawMaterial2,RawMaterial3,RawMaterial4,RawMaterial5) values (?,?,?,?,?,?,?,?,?,?,?,?,?)",(int(ea),Pname,DateProduction,DateExpire,StorageCode,Description,CustName,ImagePath,Raw1,Raw2,Raw3,Raw4,Raw5))
            conn.commit()
            showinfo(title="Result",message="New Product succesfully added!!")
def btnRawMatInfo():   
    frmAddProduct()    
def frmShowRawinfo(data_a="",data_b="",data_c="",data_d="",data_e="",data_f="",data_g="",data_h=""):
    for i in firstWindow.winfo_children():
        i.destroy()
    frame2 =tk.Frame(bg="#212943", width=690, height=690)
    frame2.place(x=0, y=0)
    lblname = tk.Label(frame2, text="Raw Materials Name :", foreground="#e4bc9b", font=("Helvetica 13 bold italic"),
                    bg="#212943")
    lblname.place(x=15, y=105)
    txtname1 = tk.Entry(frame2, width=28)
    if data_a:
        txtname1.insert(0, data_a)
    txtname1.place(x=230, y=107)
    txtname1.config(state='readonly')
    lbldop = tk.Label(frame2, text="Date of Purchase :", foreground="#e4bc9b", font=("Helvetica 13 bold italic"),
                   bg="#212943")
    lbldop.place(x=15, y=165)
    txtdop1 = tk.Entry(frame2, width=28)
    if data_b:
        txtdop1.insert(0, data_b)
    txtdop1.place(x=230, y=167)
    txtdop1.config(state='readonly')
    lblnamesup = tk.Label(frame2, text="Name of Supplier :", foreground="#e4bc9b", font=("Helvetica 13 bold italic"),
                   bg="#212943")
    lblnamesup.place(x=15, y=225)
    txtnameofsup = tk.Entry(frame2, width=28)
    if data_c:
        txtnameofsup.insert(0, data_c)
    txtnameofsup.place(x=230, y=227)
    txtnameofsup.config(state='readonly')
    lblexpire= tk.Label(frame2, text="Material Expiration Date :", foreground="#e4bc9b",
                   font=("Helvetica 13 bold italic"), bg="#212943")
    lblexpire.place(x=15, y=285)
    txtexpire = tk.Entry(frame2, width=28)
    if data_d:
        txtexpire.insert(0, data_d)
    txtexpire.place(x=230, y=287)
    txtexpire.config(state='readonly')
    lblstoragecode = tk.Label(frame2, text="Storage Code :", foreground="#e4bc9b",
                           font=("Helvetica 13 bold italic"), bg="#212943")
    lblstoragecode.place(x=15, y=345)
    txtsc1 = tk.Entry(frame2, width=28)
    if data_e:
        txtsc1.insert(0, data_e)
    txtsc1.place(x=230, y=347)
    txtsc1.config(state='readonly')
    lbldescription = tk.Label(frame2, text="Description :", foreground="#e4bc9b",
                           font=("Helvetica 13 bold italic"), bg="#212943")
    lbldescription.place(x=15, y=465)
    lblCount=Label(frame2,text="Counts :",foreground="#e4bc9b",font=("Helvetica 13 bold italic"),bg="#212943")
    lblCount.place(x=15,y=407)
    txtCount=tk.Entry(frame2,width=28)  
    if data_h:
        sa=data_h.replace(")","")
        txtCount.insert(0,sa)
    txtCount.place(x=230,y=405)
    txtCount.config(state='readonly')
    txtsc2 = tk.Text(frame2, height=5, width=35)
    if data_f:
        txtsc2.insert("end-1c", data_f)
    txtsc2.place(x=230, y=467) 
    if data_g:
        if data_a=='Sugar':
            lblLogo=ttk.Label(frame2,image=photoaddsugar)
            lblLogo.configure(background='#212943')
            lblLogo.place(x=465,y=135)
        elif data_a=='Extract':
            lblLogo=ttk.Label(frame2,image=photoaddexctr)
            lblLogo.configure(background='#212943')
            lblLogo.place(x=465,y=135)
        elif data_a=='Caffeine':
            lblLogo=ttk.Label(frame2,image=photoaddcaf)
            lblLogo.configure(background='#212943')
            lblLogo.place(x=465,y=125)
        elif data_a=='Milk':
            lblLogo=ttk.Label(frame2,image=photoaddmilk)
            lblLogo.configure(background='#212943')
            lblLogo.place(x=465,y=75)
        elif data_a=='Ice':
            lblLogo=ttk.Label(frame2,image=photoAddice)
            lblLogo.configure(background='#212943')
            lblLogo.place(x=465,y=135)
        else:
            lblLogo=ttk.Label(frame2,image=photoLogo)
            lblLogo.configure(background='#212943')
            lblLogo.place(x=465,y=75)
        
    ttk.Style().configure("TButton", padding=0,background="#212943")
    style = ttk.Style()
    style.theme_use('alt')
    style.configure('TButton', background = '#212943', foreground = 'white', width = 20, borderwidth=1, focusthickness=3, focuscolor='none')
    style.map('TButton', background=[('active','#212943')])    
    btnExit=ttk.Button(frame2,image=photoexit,command=DestroyBeforeAsk)
    btnExit.place(x=20,y=600)
    btnReturn=ttk.Button(frame2,image=photoreturn,command=frmAddProduct)
    btnReturn.place(x=110,y=600)    
def frmShowProduct(data_a="",data_b="",data_c="",data_d="",data_e="",data_f="",data_g="",data_h=""):
    for i in firstWindow.winfo_children():
        i.destroy()
    frmShowProduct=Frame(bg="#212943",width=690,height=690)
    frmShowProduct.place(x=0,y=0)
    exactpass=cursor.execute("select name +' '+ surname from tbl_user where username = ?",(selected_user.get()))
    exactpass=cursor.fetchone()
    sa=str(exactpass)
    ba=sa.replace("(","")
    ca=ba.replace(")","")
    da=ca.replace("'","")
    xa=da.replace(",","")
    lblwelcome= Label(frmShowProduct, text="Welcome to our Coffe House "+str(xa),foreground="#e4bc9b",font=("Helvetica 11 bold italic"),bg="#212943") 
    lblwelcome.place(x=15,y=15)
    lblproduct= Label(frmShowProduct, text="Select Your Product :",foreground="#e4bc9b",font=("Helvetica 13 bold italic"),bg="#212943")
    lblproduct.place(x=15,y=55)    
    cursor.execute('select Name from tbl_product')
    results=cursor.fetchall()
    results_for_combobox = [result[0] for result in results] 
    cbProducts=ttk.Combobox(frmShowProduct,width=25,textvariable=selected_product,values=results_for_combobox)
    cbProducts.place(x=230,y=57)     
    cbProducts.bind("<<ComboboxSelected>>",ProductsValues)
    lblname=Label(frmShowProduct,text="Name :",foreground="#e4bc9b",font=("Helvetica 13 bold italic"),bg="#212943")
    lblname.place(x=15,y=110)
    txtname1=Entry(frmShowProduct,width=28)
    if data_a:
        txtname1.insert(0,data_a)
    txtname1.place(x=230,y=112)
    txtname1.config(state='readonly')
    lbldop=Label(frmShowProduct, text="Date of Product :",foreground="#e4bc9b",font=("Helvetica 13 bold italic"),bg="#212943")
    lbldop.place(x=15,y=165)
    txtdop1=Entry(frmShowProduct,width=28)
    if data_b:                           
        txtdop1.insert(0,data_b)
    txtdop1.place(x=230,y=167)
    txtdop1.config(state='readonly')
    lblnoc=Label(frmShowProduct,text="Name of Customer :",foreground="#e4bc9b",font=("Helvetica 13 bold italic"),bg="#212943")
    lblnoc.place(x=15,y=220)
    txtdop2=Entry(frmShowProduct,width=28)
    if data_c:                           
        txtdop2.insert(0,data_c)
    txtdop2.place(x=230,y=222)
    txtdop2.config(state='readonly')
    lblped=Label(frmShowProduct,text="Product Expiration Date :",foreground="#e4bc9b",font=("Helvetica 13 bold italic"),bg="#212943")
    lblped.place(x=15,y=280)
    txtped1=Entry(frmShowProduct,width=28)
    if data_d:                           
        txtped1.insert(0,data_d)
    txtped1.place(x=230,y=282)
    txtped1.config(state='readonly')
    lblstoragecode=Label(frmShowProduct,text="Storage Code :",foreground="#e4bc9b",font=("Helvetica 13 bold italic"),bg="#212943")
    lblstoragecode.place(x=15,y=335)
    txtsc1=Entry(frmShowProduct,width=28)
    if data_e:                           
        txtsc1.insert(0,data_e)
    txtsc1.place(x=230,y=337)
    txtsc1.config(state='readonly')
    lbllorm=Label(frmShowProduct,text="List of Raw Materials :",foreground="#e4bc9b",font=("Helvetica 13 bold italic"),bg="#212943")
    lbllorm.place(x=15,y=390)
    selected_rawmat=tk.StringVar()
    cursor.execute('select Name from tbl_rawmaterials')
    results1=cursor.fetchall()
    results_for_combobox1 = [result[0] for result in results1]
    cbRawMat=ttk.Combobox(frmShowProduct,width=25,textvariable=selected_rawmat,values=results_for_combobox1) 
    cbRawMat.set("Click Here")
    cbRawMat.place(x=230,y=392)    
    lblCount=Label(frmShowProduct,text="Counts :",foreground="#e4bc9b",font=("Helvetica 13 bold italic"),bg="#212943")
    lblCount.place(x=15,y=445)
    txtCount=Entry(frmShowProduct,width=28)  
    if data_h:
        sa=data_h.replace(")","")
        txtCount.insert(0,sa)
    txtCount.place(x=230,y=447)
    txtCount.config(state='readonly')
    lbldescription=Label(frmShowProduct,text="Description :",foreground="#e4bc9b",font=("Helvetica 13 bold italic"),bg="#212943")    
    lbldescription.place(x=15,y=505)   
    txtsc2=Text(frmShowProduct,height = 5, width = 35)
    sa=""
    if data_f:
        txtsc2.insert("end-1c",data_f)
    if data_g:
        if data_a=='Caramel Macchiato':
            lblLogo=ttk.Label(frmShowProduct,image=photoaddcaram)
            lblLogo.configure(background='#212943')
            sa=photoaddcaram
            lblLogo.place(x=465,y=75)
        elif data_a=='Ice Americano':
            lblLogo=ttk.Label(frmShowProduct,image=photoaddiceamer)
            lblLogo.configure(background='#212943')
            sa=photoaddiceamer
            lblLogo.place(x=465,y=75)
        elif data_a=='Iced Mocha':
            lblLogo=ttk.Label(frmShowProduct,image=photoaddmocha)
            lblLogo.configure(background='#212943')
            sa=photoaddmocha
            lblLogo.place(x=465,y=75)
        elif data_a=='Latte':
            lblLogo=ttk.Label(frmShowProduct,image=photoaddlatte)
            lblLogo.configure(background='#212943')
            sa=photoaddlatte
            lblLogo.place(x=465,y=75)
        elif data_a=='Cool Lime':
            lblLogo=ttk.Label(frmShowProduct,image=photoaddcool)
            lblLogo.configure(background='#212943')
            sa=photoaddcool
            lblLogo.place(x=465,y=75)
        else:
            lblLogo=ttk.Label(frmShowProduct,image=photoLogo2)
            lblLogo.configure(background='#212943')
            sa=photoLogo2
            lblLogo.place(x=465,y=75)
    txtsc2.place(x=230,y=507)     
    ttk.Style().configure("TButton", padding=0,background="#212943")
    style = ttk.Style()
    style.theme_use('alt')
    style.configure('TButton', background = '#212943', foreground = 'white', width = 20, borderwidth=1, focusthickness=3, focuscolor='none')
    style.map('TButton', background=[('active','#212943')])    
    btnExit=ttk.Button(frmShowProduct,image=photoexit,command=DestroyBeforeAsk)
    btnExit.place(x=15,y=610)
    btncam=ttk.Button(frmShowProduct,image=photoCam,command=Visualize)
    btncam.place(x=100,y=610)
    if data_a:
        btnopencv=ttk.Button(frmShowProduct,image=photoaddopencv,command=DestroyBeforeAsk)
        btnopencv.place(x=425,y=300)
    btnproduct=ttk.Button(frmShowProduct,image=photoAddProduct,command=frmAddProduct)
    btnproduct.place(x=450,y=610)    
def frmAddProduct():    
    for i in firstWindow.winfo_children():
        i.destroy()
    frmAddProduct=Frame(bg="#212943",width=690,height=690)
    frmAddProduct.place(x=0,y=0)
    lblLogo=ttk.Label(frmAddProduct,image=photoLogo2)
    lblLogo.configure(background="#212943")
    lblLogo.place(x=455,y=15)
    lblProduct=Label(frmAddProduct,text="Product Name :",foreground="#e4bc9b",font=("Helvetica 13 bold italic"),bg="#212943")
    lblProduct.place(x=20,y=25)
    txtProduct=Entry(frmAddProduct,width=30)
    txtProduct.place(x=220,y=28)
    lblDate=Label(frmAddProduct,text="Date of Production :",foreground="#e4bc9b",font=("Helvetica 13 bold italic"),bg="#212943")
    lblDate.place(x=20,y=70)
    txtDate=DateEntry(frmAddProduct,selectmode='day',foreground="#e4bc9b",font=("Helvetica 11 bold italic"),bg="#212943",width=20)
    txtDate.place(x=220,y=73)    
    lblCustomer=Label(frmAddProduct,text="Name of Customer :",foreground="#e4bc9b",font=("Helvetica 13 bold italic"),bg="#212943")
    lblCustomer.place(x=20,y=120)
    txtCustomer=Entry(frmAddProduct,width=30)
    txtCustomer.place(x=220,y=123)
    lblExpiration=Label(frmAddProduct,text="Product Expiration Date :",foreground="#e4bc9b",font=("Helvetica 13 bold italic"),bg="#212943")
    lblExpiration.place(x=20,y=170)
    txtExpiration=DateEntry(frmAddProduct,selectmode='day',foreground="#e4bc9b",font=("Helvetica 11 bold italic"),bg="#212943",width=20)
    txtExpiration.place(x=220,y=173)
    lblStorage=Label(frmAddProduct,text="Storage Code :",foreground="#e4bc9b",font=("Helvetica 13 bold italic"),bg="#212943")
    lblStorage.place(x=20,y=220)
    txtStorage=Entry(frmAddProduct,width=30)
    txtStorage.place(x=220,y=223)
    lblMaterial=Label(frmAddProduct,text="List of Raw Materials :",foreground="#e4bc9b",font=("Helvetica 11 bold italic"),bg="#212943")
    lblMaterial.place(x=20,y=270)
    btnmaterial1 = tk.Button(frmAddProduct, text="Sugar",bg="#e4bc9b",activebackground="saddlebrown",foreground="#212943",font=("Helvetica 11 bold italic"),relief="raised",command =lambda:xd(btnmaterial1))   
    btnmaterial1.bind('<Double-Button-1>', lambda event, a=1:RawMatValues(a))   
    btnmaterial1.place(x=220,y=270)
    btnmaterial2=tk.Button(frmAddProduct, text="Extract",bg="#e4bc9b",activebackground="saddlebrown",foreground="#212943",font=("Helvetica 11 bold italic"),relief="raised",command =lambda:xd(btnmaterial2))
    btnmaterial2.bind('<Double-Button-1>', lambda event, a=2:RawMatValues(a))
    btnmaterial2.place(x=320,y=270)
    btnmaterial3=tk.Button(frmAddProduct, text="Caffeine",bg="#e4bc9b",activebackground="saddlebrown",foreground="#212943",font=("Helvetica 11 bold italic"),relief="raised",command =lambda:xd(btnmaterial3))
    btnmaterial3.bind('<Double-Button-1>', lambda event, a=6:RawMatValues(a))
    btnmaterial3.place(x=420,y=270)
    btnmaterial4=tk.Button(frmAddProduct, text="Milk",bg="#e4bc9b",activebackground="saddlebrown",foreground="#212943",font=("Helvetica 11 bold italic"),relief="raised",command =lambda:xd(btnmaterial4))
    btnmaterial4.bind('<Double-Button-1>', lambda event, a=7:RawMatValues(a))
    btnmaterial4.place(x=520,y=270)
    btnmaterial5=tk.Button(frmAddProduct, text="Ice",bg="#e4bc9b",activebackground="saddlebrown",foreground="#212943",font=("Helvetica 11 bold italic"),relief="raised",command =lambda:xd(btnmaterial5))
    btnmaterial5.bind('<Double-Button-1>', lambda event, a=8:RawMatValues(a))
    btnmaterial5.place(x=620,y=270)
    lblImage=Label(frmAddProduct,text="Select on Image :",foreground="#e4bc9b",font=("Helvetica 11 bold italic"),bg="#212943")
    lblImage.place(x=20,y=320)
    btnImage=ttk.Button(frmAddProduct,command=select_file,image=photoSelect)    
    btnImage.place(x=220,y=315)    
    txtImage=Entry(firstWindow,width=45,textvariable=path)
    txtImage.config(state='readonly')
    txtImage.place(x=20,y=360)    
    lblNote=Label(frmAddProduct,text="Note: Image must be png, be careful. ",foreground="#e4bc9b",font=("Helvetica 11 bold italic"),bg="#212943")
    lblNote.place(x=20,y=400)
    lblDescription=Label(frmAddProduct,text="Description :",foreground="#e4bc9b",font=("Helvetica 13 bold italic"),bg="#212943")
    lblDescription.place(x=20,y=440)
    txtDescription=Text(frmAddProduct,width=30,height=5)
    txtDescription.place(x=20,y=477)
    ttk.Style().configure("TButton", padding=0,background="#212943")
    style = ttk.Style()
    style.theme_use('alt')
    style.configure('TButton', background = '#212943', foreground = 'white', width = 20, borderwidth=1, focusthickness=3, focuscolor='none')
    style.map('TButton', background=[('active','#212943')])    
    btnExit=ttk.Button(frmAddProduct,image=photoexit,command=DestroyBeforeAsk)
    btnExit.place(x=20,y=600)
    btnReturn=ttk.Button(frmAddProduct,image=photoreturn,command=frmShowProduct)
    btnReturn.place(x=110,y=600)        
    usID=cursor.execute("select ID from tbl_user where username = ?",(selected_user.get()))
    usID=cursor.fetchone()    
    btnProduct=ttk.Button(frmAddProduct,image=photoAddProduct,command=lambda: AddNewProduct(usID, txtProduct.get(), txtDate.get(),txtExpiration.get(),txtStorage.get(),txtDescription.get("1.0",'end-1c'),txtCustomer.get(),1,1,1,1,1,txtImage.get()))       
    btnProduct.place(x=425,y=600)
firstWindow=tk.Tk()
screen_width = firstWindow.winfo_screenwidth()
screen_height = firstWindow.winfo_screenheight()
firstWindow.geometry(f"690x690+{(screen_width//2)-400}+{(screen_height//2)-400}") 
firstWindow.overrideredirect(True) 
firstWindow.title("Giriş Ekranı")
firstWindow.geometry("690x690")
path=StringVar()
photoexit1=im.open("./Photos/exit-icons-20.png")
photoexit=itk.PhotoImage(photoexit1)
photologo1=im.open("./Photos/Logo.png")
photoLogo=itk.PhotoImage(photologo1)
photologo2=im.open("./Photos/Logo2.png")
photoLogo2=itk.PhotoImage(photologo2)
photoselect1=im.open("./Photos/selectimage.PNG")
photoSelect=itk.PhotoImage(photoselect1)
photoCam1=im.open("./Photos/openCamera.PNG")
photoCam=itk.PhotoImage(photoCam1)
photoreturn1=im.open("./Photos/Return.png")
photoreturn=itk.PhotoImage(photoreturn1)
photoAddpro=im.open("./Photos/btnProduct.png")
photoAddProduct=itk.PhotoImage(photoAddpro)
photoice=im.open("./Photos/ice.png")
photoAddice=itk.PhotoImage(photoice)
photocaf=im.open("./Photos/caffeine.png")
photoaddcaf=itk.PhotoImage(photocaf)
photocaram=im.open("./Photos/caramelmac.png")
photoaddcaram=itk.PhotoImage(photocaram)
photocool=im.open("./Photos/coolime.png")
photoaddcool=itk.PhotoImage(photocool)
photoexctr=im.open("./Photos/exctract.png")
photoaddexctr=itk.PhotoImage(photoexctr)
photoiceamer=im.open("./Photos/ice-americano.png")
photoaddiceamer=itk.PhotoImage(photoiceamer)
photomocha=im.open("./Photos/icemocha.png")
photoaddmocha=itk.PhotoImage(photomocha)
photolatte=im.open("./Photos/Latte.png")
photoaddlatte=itk.PhotoImage(photolatte)
photosugar=im.open("./Photos/sugar.png")
photoaddsugar=itk.PhotoImage(photosugar)
photomilk=im.open("./Photos/milk.png")
photopencv=im.open("./Photos/opencv.png")
photoaddopencv=itk.PhotoImage(photopencv)
photoaddmilk=itk.PhotoImage(photomilk)
selected_user=tk.StringVar()
selected_product=tk.StringVar()
productList=[]
frmLogin()



