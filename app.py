from tkinter import *
from tkinter import ttk, messagebox
import center_tk_window as ctw
from pymysql import *
from tkinter.messagebox import askyesno

# getting last id from the table
# select id from location_shop order by id desc limit 1


def db_connection():
        global db_conn
        db_conn = connect(host = 'localhost', user = 'root', password = '$sys$', database = 'payment')
        global db_cursor
        db_cursor = db_conn.cursor()
        return db_conn, db_cursor

def insert_user_register():
    fields = []
    if fld1_check.get():
        fields.append(fld1.cget('text'))
    if fld2_check.get():
        fields.append(fld2.cget('text'))
    if fld3_check.get():
        fields.append(fld3.cget('text'))
    if fld4_check.get():
        fields.append(fld4.cget('text'))

    mysql_db, db_cursor = db_connection()
    insert_user_sql = 'insert into users(username, password, account) values(%s,%s,2000)'
    values = (usr.get(), pwd.get())
    db_cursor.execute(insert_user_sql, values)

    last_usr_id = 'select id from users order by id desc limit 1'
    db_cursor.execute(last_usr_id)
    usr_id = db_cursor.fetchone()  
    user_id.set(str(usr_id[0]))
    insert_field_sql = 'insert into fields(fieldname, user_id) values(%s, %s)'
    for field in fields:
        db_cursor.execute(insert_field_sql, (field, usr_id))

    mysql_db.commit()
    mysql_db.close()
    messagebox.showinfo('Success!', 'You have successfully created your account!')
    dashboard(usr.get())



def sign_in_window():
    window.withdraw()  # with withdraw function you can hide the window
    sign_in = Tk()
    sign_in.geometry('300x200')
    sign_in.title('Payment App | Sign In')
    sign_in.configure(bg='bisque')
    ctw.center_on_screen(sign_in)

    def back_to_sign_up():   
        window.deiconify() # this shows back the signup window again
        sign_in.withdraw() # this hides the sign_in window

    def sign_into_dashboard():
        mysql_db, db_cursor = db_connection()
        find_user_id = 'select id from users where username = %s and password = %s'
        nonlocal usr_sign_in, pwd_sign_in
        values = (usr_sign_in.get(), pwd_sign_in.get())
        db_cursor.execute(find_user_id,values)
        found_id = db_cursor.fetchone()

        if usr_sign_in.get() == "" or pwd_sign_in.get() == "":
            messagebox.showerror("Error", "Please provide all the details!")
        else:
            if found_id != None:
                user_id.set(str(found_id[0]))
                sign_in.withdraw()
                dashboard(usr_sign_in.get()) 
            else:
                messagebox.showerror('Fail', 'Sign In Failed. Please try again!')

        mysql_db.commit()
        mysql_db.close()


    btn_goto_sign_up = Button(sign_in, text = 'Sign Up', cursor = 'hand2', bd = 0, width = 10, height = 1, command = back_to_sign_up )
    btn_goto_sign_up.place(x = 200, y = 10)

    Label(sign_in, text = 'Username', bg = 'bisque').place(x = 50, y = 50)
    usr_sign_in = Entry(sign_in, justify= CENTER)
    usr_sign_in.place(x = 120, y = 50)

    Label(sign_in, text = 'Password', bg = 'bisque').place(x = 50, y = 80)
    pwd_sign_in = Entry(sign_in, show= '*', justify= CENTER)
    pwd_sign_in.place(x = 120, y = 80)

    btn_sign_in = Button(sign_in, text = 'Sign In', cursor= 'hand2', bd = 0, width = 28, height = 1,command= sign_into_dashboard)
    btn_sign_in.place(x = 50, y = 130)



def dashboard(username):
    dash = Tk()
    dash.geometry('500x500')
    dash.title('Payment App | Dashboard')
    dash.configure(bg='bisque')
    ctw.center_on_screen(dash)

    def sign_out():
        dash.withdraw()
        window.deiconify()

    def clear_form():
        users_cbox.current(0)
        pay.delete(0,END)


    btn_sign_out = Button(dash, text = 'Sign Out', cursor = 'hand2', bd = 0, width = 10, height = 1, command = sign_out )
    btn_sign_out.place(x = 350, y = 10)

    mysql_db, db_cursor = db_connection()

    Label(dash, text = 'Welcome '+username, bg = 'bisque').place(x = 100, y = 100)

    balance_sql = 'select account from users where id = %s'
    db_cursor.execute(balance_sql, user_id.get())
    current_balance = db_cursor.fetchone()
    show_balance = Label(dash, text = f'Balance: {current_balance[0]} AZN', bg = 'bisque')
    show_balance.place(x = 100, y = 130)

    fields_sql = 'select fieldname from fields where user_id = %s'
    db_cursor.execute(fields_sql, user_id.get())
    fieldnames = db_cursor.fetchall()
    Label(dash, text = 'Fields:', bg = 'bisque').place(x = 100, y = 160)
    y_size = 160 
    for field in fieldnames:
        Label(dash, text = field[0], bg = 'bisque').place(x = 150, y = y_size)
        y_size += 30

    users_sql = 'select id,username from users where id <> %s'
    db_cursor.execute(users_sql, user_id.get())
    users_name_id = db_cursor.fetchall()
    print(users_name_id)
    users_cbox = ttk.Combobox(dash, cursor = 'hand2',state = 'readonly', justify = CENTER, width = 25)
    users_cbox['values'] = ['--Select user to pay--',]+ [username[1] for username in users_name_id]
    users_cbox.current(0)
    users_cbox.place(x = 270, y = 100)
    mysql_db.commit()
    mysql_db.close()

    Label(dash, text = 'Pay amount:', bg = 'bisque').place(x = 270, y = 130)
    pay = Entry(dash, justify= CENTER, width= 28)
    pay.place(x = 270, y = 160)

    def send_amount():
        mysql_db, db_cursor = db_connection()
        nonlocal users_name_id
        for user in users_name_id:
            if users_cbox.get() == user[1]:
                amount = pay.get()
                if amount < 0:
                    messagebox.showerror('Error', 'You cannot withdraw money!')
                if users_cbox.get == '--Select user to pay--' or pay.get() == 0:
                    messagebox.showerror('Error','Provide with all of the details!')
                    break
                else:

                    values_payer = (amount,user_id.get()) 
                    send_pay = 'update users set account = account - %s where id = %s'
                    db_cursor.execute(send_pay, values_payer)

                    values_client =  (amount, str(user[0]))
                    get_pay = 'update users set account = account + %s where id = %s'
                    db_cursor.execute(get_pay, values_client)

                    # get the updated balance
                    balance_sql = 'select account from users where id = %s'
                    db_cursor.execute(balance_sql, user_id.get())
                    nonlocal current_balance
                    current_balance = db_cursor.fetchone()
                    show_balance.config(text = f'Balance: {current_balance[0]} AZN')
                    clear_form()

                    mysql_db.commit()
                    mysql_db.close()

                    messagebox.showinfo('Success payment', 'Your payment has been sent!') 
                    break


    btn_send = Button(dash, text = 'Send pay', cursor = 'hand2', bd = 0, width = 24, height = 1, command= send_amount)
    btn_send.place(x = 270, y = 190)


window = Tk()
window.geometry('450x350')
window.title('Payment App | Sign Up')
window.configure(bg='bisque')
ctw.center_on_screen(window)


user_id = StringVar()  # we use this global variable to access the user id at any time

btn_goto_sign_in = Button(window, text = 'Sign In', cursor = 'hand2', bd = 0, width = 15, height = 2, command = sign_in_window)
btn_goto_sign_in.place(x = 330, y = 10)

Label(window, text = 'Username', bg = 'bisque').place(x = 100, y = 50)
usr = Entry(window, justify= CENTER)
usr.place(x = 170, y = 50)

Label(window, text = 'Password', bg = 'bisque').place(x = 100, y = 80)
pwd = Entry(window, show= '*', justify= CENTER)
pwd.place(x = 170, y = 80)

if usr.get() or pwd.get() == "":
    messagebox.showerror('Invalid Credinentials','Username or Password is invalid!!')
    #break

Label(window, text = 'Fields', bg = 'bisque').place(x = 100, y = 110)

fld1_check = IntVar()
fld1 = Checkbutton(window, text = 'Data Scientist',  bg = 'bisque', cursor= 'hand2', variable= fld1_check)
fld1.place(x = 170, y = 110)

fld2_check = IntVar()
fld2 = Checkbutton(window, text = 'Data Analytics',  bg = 'bisque', cursor= 'hand2',variable= fld2_check)
fld2.place(x = 170, y = 140)

fld3_check = IntVar()
fld3 = Checkbutton(window, text = 'SQL Developer',  bg = 'bisque', cursor= 'hand2',variable= fld3_check)
fld3.place(x = 170, y = 170)

fld4_check = IntVar()
fld4 = Checkbutton(window, text = 'Software Engineer',  bg = 'bisque', cursor= 'hand2',variable= fld4_check)
fld4.place(x = 170, y = 200)


btn_submit = Button(window, text = 'Submit', cursor= 'hand2', bd = 0, width = 28, height = 2, command= insert_user_register)
btn_submit.place(x = 100, y = 250)

if fld1_check and fld2_check and fld3_check and fld4_check == "":
    messagebox.showerror("Fail","Please Select your field(-s)!")
    break

window.mainloop()
