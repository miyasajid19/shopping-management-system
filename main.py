from tkinter import *
from PIL import Image,ImageTk
from tkinter import messagebox,filedialog
import mysql.connector
import random
import os
import shutil
import json
root = Tk()
root.title("SMPK Shopping Centre")
root.iconbitmap(r"images/icon.ico")
bgcolor = "#333"
fgcolor = "lightgreen"
root.configure(bg=bgcolor)
def establish():
    try:
        connection=mysql.connector.connect(host="localhost", password="",user="root",database="smpkshoppingcentre")
        if connection.is_connected():
            return connection
    except Exception as e:
        messagebox.showerror("error","unable to establish connection")
def establish1():
    try:
        connection=mysql.connector.connect(host="localhost", password="",user="root",database="bankingsystem")
        if connection.is_connected():
            return connection
    except Exception as e:
        messagebox.showerror("error","unable to establish connection")
def productid():
    n=random.randint(1000000000,9999999999)
    conn=establish()
    mycursor=conn.cursor()
    mycursor.execute(f"select `id` from `products` where `id`={n}")
    if mycursor.fetchone() is None :
        return n
    else:
        productid()
    conn.commit()
    conn.close()
def home():
    global main
    main.destroy()
    if usertype=='customer':
        customer(id)
    else:
        vendor()
def order(id):
    
    global productlist
    conn=establish()
    mycursor=conn.cursor()
    mycursor.execute(f"SELECT `productid` FROM `order` WHERE `id`={id}")
    data=mycursor.fetchall()

    stringlist=data[0][0]
    productlist=json.loads(stringlist)
    global main
    main.destroy()
    main=Frame(root,background=bgcolor)
    main.pack()
    r = 1
    user=id
    Label(main, text="Product ID", background=bgcolor, fg=fgcolor, font="poppins 20 bold").grid(row=0, column=0,padx=10)
    Label(main, text="Product Name", background=bgcolor, fg=fgcolor, font="poppins 20 bold").grid(row=0, column=1)
    Label(main, text="Action", background=bgcolor, fg=fgcolor, font="poppins 20 bold", justify="center").grid(row=0, column=2, columnspan=3)
    productset=set(productlist)
    productlist=list(productset)
    for i in productlist:
        mycursor.execute(f"select * from `products` where `id`={i}")
        productname=mycursor.fetchone()
        Label(main,text=i,background=bgcolor,fg=fgcolor,font="helvetica 15 italic").grid(row=r,column=0)
        Label(main,text=productname[1],background=bgcolor,fg=fgcolor,font="helvetica 15 italic").grid(row=r,column=1)      
        Button(main, text="reorder", font="poppins 20 italic", bg=bgcolor, fg=fgcolor, border=0,
               command=lambda id=i: check(user,id)).grid(row=r, column=2)

        r += 1
    Button(main, text="Back", font="poppins 20 italic", bg=bgcolor, fg=fgcolor, border=0,
               command=home).grid(row=r,columnspan=4)

    conn.close()
    conn.close()
def head():
    global navbar
    navbar = Frame(root)
    Button(navbar, text="Home", font="poppins 20 italic",command=home, bg=bgcolor, fg=fgcolor, border=0).grid(row=0, column=1)
    Button(navbar, text="cart", font="poppins 20 italic", bg=bgcolor, fg=fgcolor, border=0,command=lambda: cart()).grid(row=0, column=2)
    # search = Entry(navbar, width=30, border=0,background="pink",font="helvetica 23 bold",highlightthickness=5,highlightbackground=bgcolor)  
    # search.grid(row=0, column=3)
    Button(navbar, text="order", font="poppins 20 italic", bg=bgcolor, fg=fgcolor, border=0,command=lambda: order(id)).grid(row=0, column=4)
    Button(navbar, text="exit", font="poppins 20 italic", bg=bgcolor, fg=fgcolor, border=0,command=exit).grid(row=0, column=5)
    navbar.pack()
def foot():
    footer=Frame(root,background=bgcolor)
    footer=Frame(root,background=bgcolor)
    Label(footer,text="built with ❤️ by sajid miya",bg=bgcolor,fg=fgcolor,font="cursive 15 bold").pack()
    Label(footer,text="© 2024 Sajid Miya. All Rights Reserved.",bg=bgcolor,fg=fgcolor,font="cursive 15 bold").pack()
    footer.pack(side="bottom",fill="x")
head()
def paynow():
    try:
        conn = establish1()
        global reciever, password, sender, total, productid1, productlist, id, newquantity
        mycursor = conn.cursor()
        
        senders = sender.get()
        key = password.get()
        recievers = reciever.get()
        
        # Fetch the sender's current amount
        mycursor.execute(f"SELECT `amount` FROM `account` WHERE `casid`={senders} and `passs`='{key}'")
        sendermoney = mycursor.fetchone()[0]
        sendermoney -= total
        
        # Fetch the receiver's current amount
        mycursor.execute(f"SELECT `amount` FROM `account` WHERE `casid`={recievers}")
        recievermoney = mycursor.fetchone()[0]
        recievermoney += total
        
        # Update sender's and receiver's account amounts
        mycursor.execute(f"UPDATE `account` SET `amount`={sendermoney} WHERE `casid`={senders}")
        mycursor.execute(f"UPDATE `account` SET `amount`={recievermoney} WHERE `casid`={recievers}")
        conn.commit()

        # Update the product quantity
        conn = establish()
        mycursor = conn.cursor()
        mycursor.execute(f"SELECT `quantity` FROM `products` WHERE `id`={productid1}")
        data = mycursor.fetchone()[0]
        mycursor.execute(f"UPDATE `products` SET `quantity`='{newquantity}' WHERE `id`='{productid1}'")
        
        # Check if the customer has already ordered the product
        mycursor.execute(f"SELECT `productid` FROM `order` WHERE `id`={id}")
        data = mycursor.fetchone()

        if data:
            # Update existing order
            orderedlist = json.loads(data[0])
            orderedlist.append(productid1)
            mycursor.execute(f"UPDATE `order` SET `productid`='{json.dumps(orderedlist)}' WHERE `id`={id}")
        else:
            # Insert new order
            orderedlist = [productid1]
            mycursor.execute(f"INSERT INTO `order` (`id`, `productid`) VALUES ('{id}', '{json.dumps(orderedlist)}')")

        # Update the customer's cart
        productlist.remove(productid1)
        mycursor.execute(f"UPDATE `customers` SET `cart`='{json.dumps(productlist)}' WHERE `id`='{id}'")
        
        conn.commit()
        conn.close()

        messagebox.showinfo("info", "Payment successful")
        global main
        main.destroy()
        home()

    except Exception as e:
        messagebox.showerror("error", e)

def pay():
    global total,newquantity
    newquantity=int(data[3])-int(no_of_products.get())
    total=data[2]*no_of_products.get()
    global main,reciever,password,sender
    main.destroy()
    main=Frame(root,bg=bgcolor)
    Label(main,text="THIS IS THE SMPK BANKING SYSTEM PORTAL",font="stencil 30 bold",bg=bgcolor,fg="light blue").grid(row=0,column=0,columnspan=2)
    Label(main,text="Total (Nrs.): ",bg=bgcolor,fg=fgcolor,font="helvetica 15 italic").grid(row=1,column=0)
    sum=Entry(main,width=30, font='helvetica 20 bold',bg=fgcolor,fg=bgcolor)
    sum.grid(row=1,column=1)
    sum.insert(0,total)
    sum.config(state="readonly")
    Label(main,text="Reviever :",fg=fgcolor,bg=bgcolor).grid(row=2,column=0)
    reciever=Entry(main,width=30, font='helvetica 20 bold',bg=fgcolor,fg=bgcolor)
    reciever.grid(row=2,column=1)
    reciever.insert(0,"7655595558")
    reciever.config(state="readonly")
    Label(main,text="Sender :",fg=fgcolor,bg=bgcolor).grid(row=3,column=0)
    sender=Entry(main,width=30, font='helvetica 20 bold',bg=fgcolor,fg=bgcolor)
    sender.grid(row=3,column=1)
    
    Label(main,text="Password :",fg=fgcolor,bg=bgcolor).grid(row=4,column=0)
    password=Entry(main,width=30, font='helvetica 20 bold',bg=fgcolor,fg=bgcolor,show="*")
    password.grid(row=4,column=1)

    Button(main,text="Pay Now",fg=bgcolor,bg=fgcolor,font="stencil 10 bold",command=paynow).grid(row=5,column=0,columnspan=2,sticky=N)
    Button(main,text="Back",fg="red",bg=fgcolor,font="stencil 10 bold",command=home).grid(row=6,column=0,columnspan=2,sticky=N)
    main.pack()
def check(id,pid):
    
    global productid1
    productid1=pid
    global data
    conn = establish()
    mycursor = conn.cursor()
    mycursor.execute(f"SELECT `id`, `productname`, `price`, `quantity`, `description` FROM `products` WHERE `id` = {pid}")
    data = mycursor.fetchone()
    conn.commit()
    conn.close()
    global main,no_of_products
    main.destroy()
    main = Frame(root, background=bgcolor)
    def display_image(image_name_without_extension):
        folder_path = "./productimages"
        possible_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
        found = False
        for ext in possible_extensions:
            image_path = os.path.join(folder_path, image_name_without_extension + ext)
            if os.path.exists(image_path):
                found = True
                break
        if found:
            img = Image.open(image_path)
            img = img.resize((250, 250))
            img_tk = ImageTk.PhotoImage(img)
            image_label.config(image=img_tk)
            image_label.image = img_tk
        else:
            pass
    image_label=Label(main)
    image_name_without_extension=f"Product_{pid}"
    image_label.grid(row=0,sticky=N,columnspan=5)
    display_image(image_name_without_extension)
    Label(main, text="Product ID:", background=bgcolor, fg=fgcolor, font="poppins 20 bold").grid(row=1, column=0)
    product_id = Entry(main, width=30, font="helvetica 15 italic")
    product_id.grid(row=1, column=1, sticky=N)
    product_id.insert(0, pid)
    product_id.config(state="readonly")
    Label(main, text="Product Name:", background=bgcolor, fg=fgcolor, font="poppins 20 bold").grid(row=2, column=0)
    product_name = Entry(main, width=30, font="helvetica 15 italic")
    product_name.grid(row=2, column=1, sticky=N)
    product_name.insert(0, data[1])
    product_name.config(state="readonly")
    Label(main, text="Quantity:", background=bgcolor, fg=fgcolor, font="poppins 20 bold").grid(row=3, column=0)
    quantity = Entry(main, width=30, font="helvetica 15 italic")
    quantity.grid(row=3, column=1, sticky=N)
    quantity.insert(0, data[3])
    quantity.config(state="readonly")
    Label(main, text="Unit Price:", background=bgcolor, fg=fgcolor, font="poppins 20 bold").grid(row=4, column=0)
    price = Entry(main, width=30, font="helvetica 15 italic")
    price.grid(row=4, column=1, sticky=N)
    price.insert(0, data[2])
    price.config(state="readonly")
    Label(main, text="Description:", background=bgcolor, fg=fgcolor, font="poppins 20 bold").grid(row=6, column=0)
    description = Text(main, height=4, width=40)
    description.grid(row=6, column=1)
    description.insert(1.0, data[4])
    description.config(state="disabled")
    Label(main, text="Description:", background=bgcolor, fg=fgcolor, font="poppins 20 bold").grid(row=7, column=0)
    no_of_products=Scale(main,from_=0, to=int(data[3]),orient="horizontal",background=bgcolor,fg=fgcolor)
    no_of_products.grid(row=7,column=1)
    Button(main, text="Pay", font="stencil 20 italic", bg=bgcolor, fg=fgcolor, border=0, command=pay).grid(row=8, columnspan=2, sticky=N)
    Button(main, text="Back", font="stencil 20 italic", bg=bgcolor, fg=fgcolor, border=0, command=home).grid(row=9, columnspan=2, sticky=N)
    main.pack()
def removecart(user,id):
    conn = establish()
    mycursor = conn.cursor()

    mycursor.execute(f"SELECT `cart` FROM `customers` WHERE `id`={user}")
    data = mycursor.fetchone()

    if data:
        cart = data[0]
        cart_list = json.loads(cart) if cart else []
        cart_list.remove(id)
        cart_set=set(cart_list)
        cart_list=list(cart_set)

        try:
            mycursor.execute(f"UPDATE `customers` SET `cart`='{json.dumps(cart_list)}' WHERE `id`={user}")
        except mysql.connector.Error as err:
            pass
    conn.commit()
    conn.close()
    home()
def removewishlist(user,id):
    conn = establish()
    mycursor = conn.cursor()

    mycursor.execute(f"SELECT `wishlist` FROM `customers` WHERE `id`={user}")
    data = mycursor.fetchone()

    if data:
        wish = data[0]
        wish_list = json.loads(wish) if wish else []
        wish_list.remove(id)
        wish_set=set(wish_list)
        wish_list=list(wish_set)

        try:
            mycursor.execute(f"UPDATE `customers` SET `wishlist`='{json.dumps(wish_list)}' WHERE `id`={user}")
        except mysql.connector.Error as err:
            pass
    conn.commit()
    conn.close()
    home()
     
def cart():
    conn=establish()
    mycursor=conn.cursor()
    mycursor.execute(f"SELECT `cart` FROM `customers` WHERE `id`={id}")
    data=mycursor.fetchall()
    stringlist=data[0][0]
    global productlist
    productlist=json.loads(stringlist)
    global main
    main.destroy()
    main=Frame(root,background=bgcolor)
    main.pack()
    r = 1
    user=id
    Label(main, text="Product ID", background=bgcolor, fg=fgcolor, font="poppins 20 bold").grid(row=0, column=0,padx=10)
    Label(main, text="Product Name", background=bgcolor, fg=fgcolor, font="poppins 20 bold").grid(row=0, column=1)
    Label(main, text="Action", background=bgcolor, fg=fgcolor, font="poppins 20 bold", justify="center").grid(row=0, column=2, columnspan=3)
    for i in productlist:
        mycursor.execute(f"select `productname` from `products` where `id`={i}")
        productname=mycursor.fetchone()
        Label(main,text=i,background=bgcolor,fg=fgcolor,font="helvetica 15 italic").grid(row=r,column=0)
        Label(main,text=productname[0],background=bgcolor,fg=fgcolor,font="helvetica 15 italic").grid(row=r,column=1)      
        Button(main, text="CHECK OUT", font="poppins 20 italic", bg=bgcolor, fg=fgcolor, border=0,
               command=lambda id=i: check(user,id)).grid(row=r, column=2)
        Button(main, text="Delete", font="poppins 20 italic", bg=bgcolor, fg="red", border=0,
               command=lambda id=i: removecart(user,id)).grid(row=r, column=3)
        r += 1
    Button(main, text="Back", font="poppins 20 italic", bg=bgcolor, fg=fgcolor, border=0,
               command=home).grid(row=r,columnspan=4)

    conn.close()
    conn.close()
def addtocart(pid, id):
    conn = establish()
    mycursor = conn.cursor()

    mycursor.execute(f"SELECT `cart` FROM `customers` WHERE `id`={id}")
    data = mycursor.fetchone()

    if data:
        cart = data[0]
        cart_list = json.loads(cart) if cart else []
        cart_list.append(pid)
        cart_set=set(cart_list)
        cart_list=list(cart_set)

        try:
            mycursor.execute(f"UPDATE `customers` SET `cart`='{json.dumps(cart_list)}' WHERE `id`={id}")
        except mysql.connector.Error as err:
            pass

    else:
        cart_list = [pid]

        try:
            # Convert cart_list to JSON string representation
            cart_json = json.dumps(cart_list)
            mycursor.execute(f"INSERT INTO `customers` (`id`, `cart`, `wishlist`, `status`) VALUES ({id}, '{cart_json}', '[]', 'not yet')")
        except mysql.connector.Error as err:
            pass

    conn.commit()
    conn.close()
def addtowishlist(pid, id):
    conn = establish()
    mycursor = conn.cursor()

    mycursor.execute(f"SELECT `wishlist` FROM `customers` WHERE `id`={id}")
    data = mycursor.fetchone()

    if data:
        wish = data[0]
        wish_list = json.loads(wish) if wish else []
        wish_list.append(pid)
        wish_set=set(wish_list)
        wish_list=list(wish_set)
        try:
            mycursor.execute(f"UPDATE `customers` SET `wishlist`='{json.dumps(wish_list)}' WHERE `id`={id}")
        except mysql.connector.Error as err:
            messagebox.showerror("error",err)
    else:
        wish_list = {pid}

        try:
            # Convert cart_list to JSON string representation
            wish_json = json.dumps(wish_list)
            mycursor.execute(f"INSERT INTO `customers` (`id`, `cart`, `wishlist`, `status`) VALUES ({id}, '{wish_json}', '[]', 'not yet')")
        except mysql.connector.Error as err:
            messagebox.showerror("err",err)

    conn.commit()
    conn.close()
def find(id):
    conn = establish()
    mycursor = conn.cursor()
    mycursor.execute("SELECT * FROM `products`")
    data = mycursor.fetchall()
    conn.close()

    global main
    
    main.destroy()
    main = Frame(root, background=bgcolor)
    main.pack(fill=BOTH, expand=True)

    canvas = Canvas(main, background=bgcolor)
    scrollbar = Scrollbar(main, orient="vertical", command=canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    canvas.pack(side=LEFT, fill=BOTH, expand=True)

    scrollable_frame = Frame(canvas, background=bgcolor)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    scrollable_frame.bind("<Configure>", on_frame_configure)

    def on_mouse_wheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", on_mouse_wheel)
    canvas.bind_all("<Button-4>", on_mouse_wheel)  # Linux and macOS
    canvas.bind_all("<Button-5>", on_mouse_wheel)  # Linux and macOS

    def on_key(event):
        if event.keysym == "Up":
            canvas.yview_scroll(-1, "units")
        elif event.keysym == "Down":
            canvas.yview_scroll(1, "units")

    canvas.bind_all("<Up>", on_key)
    canvas.bind_all("<Down>", on_key)

    r = 1
    Label(scrollable_frame, text="Product Image", bg=bgcolor, fg=fgcolor, font="stencil 20 bold").grid(row=0, column=0,padx=10,pady=10)
    Label(scrollable_frame, text="Product Name", bg=bgcolor, fg=fgcolor, font="stencil 20 bold").grid(row=0, column=1,padx=10,pady=10)
    Label(scrollable_frame, text="Price", bg=bgcolor, fg=fgcolor, font="stencil 20 bold").grid(row=0, column=2,padx=10,pady=10)
    Label(scrollable_frame, text="Available", bg=bgcolor, fg=fgcolor, font="stencil 20 bold").grid(row=0, column=3,padx=10,pady=10)
    Label(scrollable_frame, text="Description", bg=bgcolor, fg=fgcolor, font="stencil 20 bold").grid(row=0, column=4,padx=10,pady=10)
    Label(scrollable_frame, text="Action", bg=bgcolor, fg=fgcolor, font="stencil 20 bold").grid(row=0, column=5,columnspan=2,padx=10,pady=10)

    def display_image(image_name_without_extension, label):
        folder_path = "./productimages"
        possible_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
        found = False
        for ext in possible_extensions:
            image_path = os.path.join(folder_path, image_name_without_extension + ext)
            if os.path.exists(image_path):
                found = True
                break
        if found:
            img = Image.open(image_path)
            img = img.resize((150, 150))
            img_tk = ImageTk.PhotoImage(img)
            label.config(image=img_tk)
            label.image = img_tk
        else:
            pass

    image_labels = []
    for i in range(len(data)):
        image_label = Label(scrollable_frame)
        image_name_without_extension = f"Product_{data[i][0]}"
        image_label.grid(row=r, column=0,pady=10)
        display_image(image_name_without_extension, image_label)
        image_labels.append(image_label)
        Label(scrollable_frame, text=data[i][1], bg=bgcolor, fg=fgcolor, font="helvetica 15 italic", justify="center").grid(row=r, column=1)
        Label(scrollable_frame, text=data[i][3], bg=bgcolor, fg=fgcolor, font="helvetica 15 italic", justify="center").grid(row=r, column=2)
        Label(scrollable_frame, text=data[i][4], bg=bgcolor, fg=fgcolor, font="helvetica 15 italic", justify="center").grid(row=r, column=3)
        Label(scrollable_frame, text=data[i][-2], bg=bgcolor, fg=fgcolor, font="helvetica 15 italic", justify="center", width=30, wraplength=300, anchor="w").grid(row=r, column=4, padx=10)
        img=Image.open(r"images\cart.png" ).resize((50,50))
        img=ImageTk.PhotoImage(img)

        btn=Button(scrollable_frame,image=img,command=lambda pid=data[i][0]: addtocart(pid,id),bg=bgcolor,border=0,bd=0)
        btn.image=img
        btn.grid(row=r,column=5)
        img=Image.open(r"images\wishlist.png").resize((50,50))
        img=ImageTk.PhotoImage(img)

        btn=Button(scrollable_frame,image=img,command=lambda pid=data[i][0]: addtowishlist(pid,id),bg=bgcolor,border=0,bd=0)
        btn.image=img
        btn.grid(row=r,column=6)
        r += 1
    root.geometry("1500x800+0+0")
def removethis(id):
    pass
def wishlist():
    conn=establish()
    mycursor=conn.cursor()
    mycursor.execute(f"SELECT `wishlist` FROM `customers` WHERE `id`={id}")
    data=mycursor.fetchall()
    stringlist=data[0][0]
    productlist=json.loads(stringlist)
    global main
    main.destroy()
    main=Frame(root,background=bgcolor)
    main.pack()
    r = 1
    user=id
    Label(main, text="Product ID", background=bgcolor, fg=fgcolor, font="poppins 20 bold").grid(row=0, column=0,padx=10)
    Label(main, text="Product Name", background=bgcolor, fg=fgcolor, font="poppins 20 bold").grid(row=0, column=1)
    Label(main, text="Action", background=bgcolor, fg=fgcolor, font="poppins 20 bold", justify="center").grid(row=0, column=2, columnspan=3)
    for i in productlist:
        mycursor.execute(f"select `productname` from `products` where `id`={i}")
        productname=mycursor.fetchone()
        Label(main,text=i,background=bgcolor,fg=fgcolor,font="helvetica 15 italic").grid(row=r,column=0)
        Label(main,text=productname[0],background=bgcolor,fg=fgcolor,font="helvetica 15 italic").grid(row=r,column=1)      
        Button(main, text="CHECK OUT", font="poppins 20 italic", bg=bgcolor, fg=fgcolor, border=0,
               command=lambda id=i: check(user,id)).grid(row=r, column=2)
        Button(main, text="Delete", font="poppins 20 italic", bg=bgcolor, fg="red", border=0,
               command=lambda id=i: removewishlist(user,id)).grid(row=r, column=3)
        r += 1
    Button(main, text="Back", font="poppins 20 italic", bg=bgcolor, fg=fgcolor, border=0,
               command=home).grid(row=r,columnspan=4)

    conn.close()
    conn.close()
def customer(id):
    global main
    main=Frame(root,background=bgcolor)

    Button(main, text="Find ", font="poppins 20 italic", bg=bgcolor, fg=fgcolor, border=0,command=lambda : find(id)).grid(row=0, column=0)
    Button(main, text="Cart", font="poppins 20 italic", bg=bgcolor, fg=fgcolor, command=cart,border=0).grid(row=1, column=0)
    Button(main, text="Wishlists", font="poppins 20 italic", bg=bgcolor, fg=fgcolor, border=0,command=wishlist).grid(row=2, column=0)
    Button(main, text="order", font="poppins 20 italic", bg=bgcolor, fg=fgcolor, border=0,command=lambda: order(id)).grid(row=3, column=0)
    main.pack()
def addproduct():
    global file_path,pid,id,key,usertype
    try:
        conn=establish()
        mycursor=conn.cursor()
        mycursor.execute(f"INSERT INTO `products`(`id`, `productname`, `vendor`, `price`, `quantity`, `description`) VALUES ('{pid}','{product_name.get()}','{id}',{price.get()},{quantity.get()},'{description.get("1.0", "end-1c")}')")
        conn.commit()
        conn.close()
        messagebox.showinfo("info","added successfully")
        if not os.path.exists("productimages"):
            os.makedirs("productimages")
        image_name = os.path.basename(file_path)
        _, image_ext = os.path.splitext(image_name)
        new_image_name = f"Product_{pid}{image_ext}"
        destination = os.path.join("productimages", new_image_name)
        shutil.copyfile(file_path, destination)
        messagebox.showinfo("info"," iamge saved successfully")
        vendor()
    except Exception as e:
        pass
def add():
    global main
    main.destroy()
    main = Frame(root, background=bgcolor)
    def upload_image():
        global file_path
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            load_image(file_path)
    def load_image(image_path):
        if uploaded_image_label.winfo_exists():
            uploaded_image_label.grid_forget()
        image = Image.open(image_path)
        image.thumbnail((150, 150))  
        photo = ImageTk.PhotoImage(image)
        uploaded_image_label.config(image=photo)
        uploaded_image_label.image = photo
        uploaded_image_label.grid(row=0, column=0, columnspan=2, pady=10)  
    main = Frame(root, background=bgcolor)
    global pid
    pid = productid()
    global uploaded_image_label
    uploaded_image_label = Label(main)
    uploaded_image_label.grid(row=0, column=0, columnspan=2, pady=10)  
    global product_id,product_name,quantity,price,description
    Label(main, text="Product ID:", background=bgcolor, fg=fgcolor, font="poppins 20 bold").grid(row=1, column=0)
    product_id = Entry(main, width=30, font="helvetica 15 italic")
    product_id.grid(row=1, column=1, sticky=N)
    product_id.insert(0, pid)
    product_id.config(state="readonly")
    Label(main, text="Product Name:", background=bgcolor, fg=fgcolor, font="poppins 20 bold").grid(row=2, column=0)
    product_name = Entry(main, width=30, font="helvetica 15 italic")
    product_name.grid(row=2, column=1, sticky=N)
    Label(main, text="Quantity:", background=bgcolor, fg=fgcolor, font="poppins 20 bold").grid(row=3, column=0)
    quantity = Entry(main, width=30, font="helvetica 15 italic")
    quantity.grid(row=3, column=1, sticky=N)
    Label(main, text="Price:", background=bgcolor, fg=fgcolor, font="poppins 20 bold").grid(row=4, column=0)
    price = Entry(main, width=30, font="helvetica 15 italic")
    price.grid(row=4, column=1, sticky=N)
    upload_button = Button(main, text="Upload Image", command=upload_image)
    upload_button.grid(row=5, column=0, columnspan=2, pady=10)
    Label(main, text="description :", background=bgcolor, fg=fgcolor, font="poppins 20 bold").grid(row=6, column=0)
    description=Text(main,height=4,width=40)
    description.grid(row=6,column=1)
    Button(main, text="Add", font="stencil 20 italic", bg=bgcolor, fg=fgcolor, border=0,command=addproduct).grid(row=7,column=0)
    Button(main, text="Back", font="stencil 20 italic", bg=bgcolor, fg=fgcolor, border=0,command=vendor).grid(row=7,column=1)
    main.pack()
def updatedata():
    global file_path, product_id, product_name, quantity, price, description
    try:
        conn = establish()
        mycursor = conn.cursor()
        mycursor.execute(f"UPDATE `products` SET `productname`='{product_name.get()}', `price`='{price.get()}', `quantity`='{quantity.get()}', `description`='{description.get("1.0", "end-1c")}' WHERE `id`={product_id.get()}")
        conn.commit()
        if file_path:
            if not os.path.exists("productimages"):
                os.makedirs("productimages")
            image_name = os.path.basename(file_path)
            _, image_ext = os.path.splitext(image_name)
            new_image_name = f"Product_{product_id.get()}{image_ext}"
            destination = os.path.join("productimages", new_image_name)
            shutil.copyfile(file_path, destination)
            conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Data updated successfully")
        read()  
    except Exception as e:
        messagebox.showerror("Error", f"Error updating data: {str(e)}")
def update(pid):
    global file_path, product_id, product_name, quantity, price, description
    conn = establish()
    mycursor = conn.cursor()
    mycursor.execute(f"SELECT `id`, `productname`, `price`, `quantity`, `description` FROM `products` WHERE `id` = {pid}")
    data = mycursor.fetchone()
    conn.close()
    global main
    main.destroy()
    main = Frame(root, background=bgcolor)

    def upload_image():
        global file_path
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            load_image(file_path)
    def load_image(image_path):
        image = Image.open(image_path)
        image.thumbnail((250, 250))  
        photo = ImageTk.PhotoImage(image)
        
        image_label.config(image=photo)
        image_label.image = photo
        image_label.grid(row=0, column=0, columnspan=2, pady=10)
    def display_image(image_name_without_extension):
        folder_path = "./productimages"
        possible_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
        found = False
        for ext in possible_extensions:
            image_path = os.path.join(folder_path, image_name_without_extension + ext)
            if os.path.exists(image_path):
                found = True
                break
        if found:
            img = Image.open(image_path)
            img = img.resize((250, 250))
            img_tk = ImageTk.PhotoImage(img)
            image_label.config(image=img_tk)
            image_label.image = img_tk
        else:
            pass
    image_label = Label(main)
    image_name_without_extension = f"Product_{pid}"
    image_label.grid(row=0, sticky=N, columnspan=5)
    display_image(image_name_without_extension)
    product_id = Entry(main, width=30, font="helvetica 15 italic")
    product_id.grid(row=1, column=1, sticky=N)
    product_id.insert(0, pid)
    product_id.config(state="readonly")
    product_name = Entry(main, width=30, font="helvetica 15 italic")
    product_name.grid(row=2, column=1, sticky=N)
    product_name.insert(0, data[1])
    quantity = Entry(main, width=30, font="helvetica 15 italic")
    quantity.grid(row=3, column=1, sticky=N)
    quantity.insert(0, data[3])
    price = Entry(main, width=30, font="helvetica 15 italic")
    price.grid(row=4, column=1, sticky=N)
    price.insert(0, data[2])
    description = Text(main, height=4, width=40)
    description.grid(row=6, column=1)
    description.insert(1.0, data[4])
    upload_button = Button(main, text="Upload Image", command=upload_image)
    upload_button.grid(row=5, column=0, columnspan=2, pady=10)
    Button(main, text="Back", font="stencil 20 italic", bg=bgcolor, fg=fgcolor, border=0, command=read).grid(row=7, column=0, sticky=N)
    Button(main, text="Update", font="stencil 20 italic", bg=bgcolor, fg=fgcolor, border=0, command=updatedata).grid(row=7, column=1, columnspan=2, sticky=N)
    main.pack()
def info(pid):
    conn = establish()
    mycursor = conn.cursor()
    mycursor.execute(f"SELECT `id`, `productname`, `price`, `quantity`, `description` FROM `products` WHERE `id` = {pid}")
    data = mycursor.fetchone()
    conn.commit()
    conn.close()
    global main
    main.destroy()
    main = Frame(root, background=bgcolor)
    def display_image(image_name_without_extension):
        folder_path = "./productimages"
        possible_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
        found = False
        for ext in possible_extensions:
            image_path = os.path.join(folder_path, image_name_without_extension + ext)
            if os.path.exists(image_path):
                found = True
                break
        if found:
            img = Image.open(image_path)
            img = img.resize((250, 250))
            img_tk = ImageTk.PhotoImage(img)
            image_label.config(image=img_tk)
            image_label.image = img_tk
        else:
            pass
    image_label=Label(main)
    image_name_without_extension=f"Product_{pid}"
    image_label.grid(row=0,sticky=N,columnspan=5)
    display_image(image_name_without_extension)
    Label(main, text="Product ID:", background=bgcolor, fg=fgcolor, font="poppins 20 bold").grid(row=1, column=0)
    product_id = Entry(main, width=30, font="helvetica 15 italic")
    product_id.grid(row=1, column=1, sticky=N)
    product_id.insert(0, pid)
    product_id.config(state="readonly")
    Label(main, text="Product Name:", background=bgcolor, fg=fgcolor, font="poppins 20 bold").grid(row=2, column=0)
    product_name = Entry(main, width=30, font="helvetica 15 italic")
    product_name.grid(row=2, column=1, sticky=N)
    product_name.insert(0, data[1])
    product_name.config(state="readonly")
    Label(main, text="Quantity:", background=bgcolor, fg=fgcolor, font="poppins 20 bold").grid(row=3, column=0)
    quantity = Entry(main, width=30, font="helvetica 15 italic")
    quantity.grid(row=3, column=1, sticky=N)
    quantity.insert(0, data[3])
    quantity.config(state="readonly")
    Label(main, text="Price:", background=bgcolor, fg=fgcolor, font="poppins 20 bold").grid(row=4, column=0)
    price = Entry(main, width=30, font="helvetica 15 italic")
    price.grid(row=4, column=1, sticky=N)
    price.insert(0, data[2])
    price.config(state="readonly")
    Label(main, text="Description:", background=bgcolor, fg=fgcolor, font="poppins 20 bold").grid(row=6, column=0)
    description = Text(main, height=4, width=40)
    description.grid(row=6, column=1)
    description.insert(1.0, data[4])
    description.config(state="disabled")
    Button(main, text="Back", font="stencil 20 italic", bg=bgcolor, fg=fgcolor, border=0, command=read).grid(row=7, columnspan=2, sticky=N)
    main.pack()
def deletethis(pid):
    conn = establish()
    mycursor = conn.cursor()
    mycursor.execute(f"SELECT `id`, `productname`, `price`, `quantity`, `description` FROM `products` WHERE `id` = {pid}")
    data = mycursor.fetchone()
    conn.commit()
    conn.close()
    def delete():
        conn=establish()
        mycursor=conn.cursor()
        mycursor.execute(f"delete  from `products` where `id`={pid}")
        conn.commit()
        conn.close()
        image_name_without_extension = f"Product_{pid}"
        folder_path = "./productimages"
        possible_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
        for ext in possible_extensions:
            image_path = os.path.join(folder_path, image_name_without_extension + ext)
            if os.path.exists(image_path):
                os.remove(image_path)
                read()
    global main
    main.destroy()
    main = Frame(root, background=bgcolor)
    def display_image(image_name_without_extension):
        folder_path = "./productimages"
        possible_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
        found = False
        for ext in possible_extensions:
            image_path = os.path.join(folder_path, image_name_without_extension + ext)
            if os.path.exists(image_path):
                found = True
                break
        if found:
            img = Image.open(image_path)
            img = img.resize((250, 250))
            img_tk = ImageTk.PhotoImage(img)
            image_label.config(image=img_tk)
            image_label.image = img_tk
        else:
            pass
    image_label=Label(main)
    image_name_without_extension=f"Product_{pid}"
    image_label.grid(row=0,sticky=N,columnspan=5)
    display_image(image_name_without_extension)
    Label(main, text="Product ID:", background=bgcolor, fg=fgcolor, font="poppins 20 bold").grid(row=1, column=0)
    product_id = Entry(main, width=30, font="helvetica 15 italic")
    product_id.grid(row=1, column=1, sticky=N)
    product_id.insert(0, pid)
    product_id.config(state="readonly")
    Label(main, text="Product Name:", background=bgcolor, fg=fgcolor, font="poppins 20 bold").grid(row=2, column=0)
    product_name = Entry(main, width=30, font="helvetica 15 italic")
    product_name.grid(row=2, column=1, sticky=N)
    product_name.insert(0, data[1])
    product_name.config(state="readonly")
    Label(main, text="Quantity:", background=bgcolor, fg=fgcolor, font="poppins 20 bold").grid(row=3, column=0)
    quantity = Entry(main, width=30, font="helvetica 15 italic")
    quantity.grid(row=3, column=1, sticky=N)
    quantity.insert(0, data[3])
    quantity.config(state="readonly")
    Label(main, text="Price:", background=bgcolor, fg=fgcolor, font="poppins 20 bold").grid(row=4, column=0)
    price = Entry(main, width=30, font="helvetica 15 italic")
    price.grid(row=4, column=1, sticky=N)
    price.insert(0, data[2])
    price.config(state="readonly")
    Label(main, text="Description:", background=bgcolor, fg=fgcolor, font="poppins 20 bold").grid(row=6, column=0)
    description = Text(main, height=4, width=40)
    description.grid(row=6, column=1)
    description.insert(1.0, data[4])
    description.config(state="disabled")
    Button(main, text="Back", font="stencil 20 italic", bg=bgcolor, fg=fgcolor, border=0, command=read).grid(row=7,column=0, sticky=N)
    Button(main, text="Delete", font="stencil 20 italic", bg=bgcolor, fg=fgcolor, border=0, command=delete).grid(row=7, column=1, sticky=N)
    main.pack()
def read():
    global id, main
    conn = establish()
    mycursor = conn.cursor()
    mycursor.execute(f"SELECT `id`, `productname` FROM `products` WHERE `vendor` = '{id}'")
    data = mycursor.fetchall()
    conn.commit()
    conn.close()
    main.destroy()
    main = Frame(root, background=bgcolor)
    r = 1
    Label(main, text="Product ID", background=bgcolor, fg=fgcolor, font="poppins 20 bold").grid(row=0, column=0)
    Label(main, text="Product Name", background=bgcolor, fg=fgcolor, font="poppins 20 bold").grid(row=0, column=1)
    Label(main, text="Action", background=bgcolor, fg=fgcolor, font="poppins 20 bold", justify="center").grid(row=0, column=2, columnspan=3)
    for i in data:
        Label(main, text=i[0], background=bgcolor, fg=fgcolor, font="poppins 20 bold").grid(row=r, column=0)
        Label(main, text=i[1], background=bgcolor, fg=fgcolor, font="poppins 20 bold").grid(row=r, column=1)
        Button(main, text="Info", font="poppins 20 italic", bg=bgcolor, fg=fgcolor, border=0, 
               command=lambda id=i[0]: info(id)).grid(row=r, column=2)
        Button(main, text="Update", font="poppins 20 italic", bg=bgcolor, fg=fgcolor, border=0,
               command=lambda id=i[0]: update(id)).grid(row=r, column=3)
        Button(main, text="Delete", font="poppins 20 italic", bg=bgcolor, fg="red", border=0,
               command=lambda id=i[0]: deletethis(id)).grid(row=r, column=4)
        r += 1
    Button(main, text="Back", font="poppins 20 italic", bg=bgcolor, fg=fgcolor, border=0,
               command=vendor).grid(row=r,columnspan=4)
    main.pack()
def update_selection(value):
    global id_var, name_var, data
    if value.isdigit():  
        id_var.set(value)
        for item in data:
            if item[0] == value:
                name_var.set(item[1])
                break
    else: 
        name_var.set(value)
        for item in data:
            if item[1] == value:
                id_var.set(item[0])
                break
def updatewhat():
    global id_var, name_var, main, root, data
    conn = establish()
    mycursor = conn.cursor()
    mycursor.execute(f"SELECT `id`, `productname` FROM `products` WHERE `vendor` = 1")  # Replace 1 with your actual vendor ID
    data = mycursor.fetchall()
    conn.close()
    ids = [item[0] for item in data]
    names = [item[1] for item in data]
    if main:
        main.destroy()
    main = Frame(root, background=bgcolor)
    main.pack()
    id_var = StringVar(main)
    id_var.set("select id")
    OptionMenu(main, id_var, *ids, command=update_selection).grid(row=0, column=1)
    name_var = StringVar(main)
    name_var.set("select product name")
    OptionMenu(main, name_var, *names, command=update_selection).grid(row=1, column=1)
    Button(main, text="Update", font="poppins 20 italic", bg=bgcolor, fg=fgcolor, border=0,
           command=lambda: update(id_var.get())).grid(row=2, column=0)
    Button(main, text="Back", font="poppins 20 italic", bg=bgcolor, fg=fgcolor, border=0,
           command=lambda: vendor()).grid(row=2, column=1)
def deletewhat():
    global id_var, main, root, data
    conn = establish()
    mycursor = conn.cursor()
    mycursor.execute(f"SELECT `id`, `productname` FROM `products` WHERE `vendor` = 1")  # Replace 1 with your actual vendor ID
    data = mycursor.fetchall()
    conn.close()
    ids = [item[0] for item in data]
    names = [item[1] for item in data]
    if main:
        main.destroy()
    main = Frame(root, background=bgcolor)
    main.pack()
    id_var = StringVar(main)
    id_var.set("select id")
    OptionMenu(main, id_var, *ids, command=update_selection).grid(row=0, column=1)
    name_var = StringVar(main)
    name_var.set("select product name")
    OptionMenu(main, name_var, *names, command=update_selection).grid(row=1, column=1)

    Button(main, text="Delete", font="poppins 20 italic", bg=bgcolor, fg=fgcolor, border=0,
           command=lambda: deletethis(id_var.get())).grid(row=2, column=0)

    Button(main, text="Back", font="poppins 20 italic", bg=bgcolor, fg=fgcolor, border=0,
           command=lambda: vendor()).grid(row=2, column=1)
def vendor():
    global main
    try:
        main.destroy()
    except :
        pass
    main=Frame(root,background=bgcolor)
    global navbar
    navbar.destroy()
    Button(main, text="add new product", font="poppins 20 italic", bg=bgcolor, fg=fgcolor, border=0,command=add).grid(row=0,sticky=N)
    Button(main, text="update  product", font="poppins 20 italic", bg=bgcolor, fg=fgcolor, border=0, command= updatewhat).grid(row=1,sticky=N)
    Button(main, text="delete  product", font="poppins 20 italic", bg=bgcolor, fg=fgcolor, border=0,command=deletewhat).grid(row=2,sticky=N)
    Button(main, text="read new product", font="poppins 20 italic", bg=bgcolor, fg=fgcolor, border=0,command=read).grid(row=3,sticky=N)
    main.pack()

def signup():
    global id,key,usertype
    id=uid.get()
    key=password.get()
    usertype=user.get()
    if(id!='' and key!='' and  usertype!="select type"):
        connect=establish()
        mycursor=connect.cursor()
        mycursor.execute(f"SELECT `phone`, `passkey`, `type` FROM `user` WHERE `phone`='{id}' and `passkey`='{key}' and `type`='{usertype}'")
        data=mycursor.fetchone()
        if  data is not None:
            login.destroy() 
            if data[-1] =="customer":
                customer(id)
                
            else :
                vendor()

        else:
            messagebox.showerror("error","no such user is detected")
        connect.commit()
        connect.close()
    else:
        messagebox.showwarning("info","all field are required")

login=Frame(root,background=bgcolor)
img=Image.open(r"images\login.png")
img=img.resize((550,400))
img=ImageTk.PhotoImage(img)
Label(login,image=img).grid(row=0,sticky=N,columnspan=4,padx=100,pady=20)
Label(login,text="Select : ",background=bgcolor,fg=fgcolor,font="poppins 20 bold").grid(row=1,column=0)
user=StringVar()
options=["customer","vendor"]
OptionMenu(login,user,*options).grid(row=1,column=1,sticky=N)
# user.set("select type")
user.set("customer")
Label(login,text="UID : ",background=bgcolor,fg=fgcolor,font="poppins 20 bold").grid(row=2,column=0)
uid=Entry(login,width=30,font="helvetica 15 italic")
uid.grid(row=2,column=1,sticky=N)
uid.insert(0,"2")
Label(login,text="Password : ",background=bgcolor,fg=fgcolor,font="poppins 20 bold").grid(row=3,column=0)
password=Entry(login,width=30,font="helvetica 15 italic",show="*")
password.grid(row=3,column=1,sticky=N)
password.insert(0,"1")
Button(login,text="Login",background=bgcolor,fg=fgcolor,font="stencil 15 bold",command=signup).grid(row=4,columnspan=3,sticky=N)
login.pack(fill="y")
foot()
root.mainloop()
