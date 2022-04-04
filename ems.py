"""
# f for font
# y for gap

"""

#============================================================

from tkinter import *
from tkinter.messagebox import * 
from tkinter.scrolledtext import * 
from sqlite3 import * 
from datetime import * 
import matplotlib.pyplot as plt
import pandas as pd
import requests

#============================================================
# window and button opration 
#============================================================
# add window opraton


def f1():
	main_window.withdraw()
	add_window.deiconify()

def f2():
	add_window.withdraw()
	main_window.deiconify()

def save():
	global id	
	try:	
		id =int(aw_ent_eid.get())
	except ValueError:
		showerror("issue", "enter only number in id" )
		
	
	name = aw_ent_ename.get()
	
	try:
		salary = int(aw_ent_esalary.get())
	except ValueError:
		showerror("Salary", "Salary shoud not empty")
	
	
	con = None

	try:
		con = connect("employees.db")
		cursor = con.cursor()
		sql = "create table if not exists employee(id int primary key, name varchar(30), salary int)"
		cursor.execute(sql)
		sql = "insert into employee values('%d', '%s', '%d')"


		if id <= 0:
			raise Exception("enter valid number for Id")
			con.rollback()

		elif not all(x.isalpha() for x in name):
			showerror("name", "enter only alphabet in Name")
			con.rollback()	

		elif len(name) <= 1:
			showerror("name","enter at least 2 characters in Name")
			con.rollback()	

		elif salary <= 7999:
			raise Exception("Salary shoud be more than 8000")
			con.rollback()

		else:
			cursor.execute(sql % (id, name, salary) )
			con.commit()
			showinfo("recored", "added")

	except IntegrityError as a:	
		showerror("issue", "id exist")
		con.rollback()

	except Exception as e:
		showerror("issuse", e)
		con.rollback()

	finally:
		if con is not None:
			con.close()
			aw_ent_eid.delete(0, END)
			aw_ent_ename.delete(0, END)
			aw_ent_esalary.delete(0, END)

#============================================================
# view window

def f3():
	main_window.withdraw()
	view_window.deiconify()
	
	vw_emp_data.delete(1.0, END)
	info = ""
	
	try:
		con = connect("employees.db")
		cursor = con.cursor()
		sql = "select * from employee"
		cursor.execute(sql)
		data = cursor.fetchall()
		for d in data:
			info = info + " id = " + str(d[0]) + " name = " + str(d[1]) + " salary = " + str(d[2]) + "\n"

		vw_emp_data.insert(INSERT, info)

	except Exception as e:

		showerror("issue", e)
	finally:

		if con is not None:
			con.close()

def f4():
	view_window.withdraw()
	main_window.deiconify()
#============================================================
# update window

def f5():
	main_window.withdraw()
	update_window.deiconify()
def f6():
	update_window.withdraw()
	main_window.deiconify()

def f7():
	global id
	
	try:	
		id = int(uw_ent_eid.get())
	except ValueError:
		showerror("issue", "enter only number in id" )
		
	name = uw_ent_ename.get()
	
	try:
		salary = int(uw_ent_esalary.get())
	except ValueError:
		showerror("Salary", "Salary shoud not empty")
	
	con = None

	try:
		con = connect("employees.db")
		cursor = con.cursor()
		sql = "update employee set name ='%s', salary = '%d' where id='%d'"

		if id <= 0:
			showerror("issue", "enter valid numbers for Id")
			con.rollback()

		elif not all(x.isalpha() for x in name):
			showerror("name", "enter only alphabet in Name")
			con.rollback()	

		elif len(name) <= 1:
			showerror("name","enter at least 2 characters in Name")
			con.rollback()	

		elif salary <= 7999:
			showerror("salary", "Salary shoud be more than 8000")
			con.rollback()
		else:
			cursor.execute(sql %(name, salary, id))
			if cursor.rowcount == 1:
				con.commit()
				showinfo("update","record update")
			else:
				showerror("issue", "id does not exists")
	
	except Exception as e:
		showerror("issue", e)
		print(e)
		con.rollback()

	finally:
		if con is not None:
			con.close()
			uw_ent_eid.delete(0, END)
			uw_ent_ename.delete(0, END)
			uw_ent_esalary.delete(0, END)

	

#============================================================
# delete window
def f13():
	main_window.withdraw()
	delete_window.deiconify()

def f14():
	delete_window.withdraw()
	main_window.deiconify()

def f15():
	global id
	try:
		id = int(dw_ent_eid.get())
	except ValueError:
		showerror("id", "shoud not empty")

	con = None

	try:
		con = connect("employees.db")
		cursor = con.cursor()
		sql = "delete from employee where id ='%d'"
		cursor.execute(sql % (id))
		if cursor.rowcount == 1:
			con.commit()
			showinfo(id, "record deleted")
		else:
			showerror(id, " does not exists")
			con.rollback()
	
	except Exception as e:
		showerror("issue", e)

	finally:
		if con is not None:
			con.close()
			dw_ent_eid.delete(0, END)
#===========================================================
# chart window
def f16():
	main_window.withdraw()
	chart_window.deiconify()

def f17():
	chart_window.withdraw()
	main_window.deiconify()

def f18():
	con = None

	try:
		con = connect("employees.db")
		cursor = con.cursor()
		df = pd.read_sql("select name, salary from employee order by salary desc limit 5", con)

		df.to_csv("employee.csv", index = False)
		
	
	except Exception as e:
		showerror("issue", e)
		

	finally:
		if con is not None:
			con.close()
	

	data = pd.read_csv("employee.csv")
	name = data["name"].tolist()
	salary = data["salary"].tolist()
	plt.bar(name, salary, width=0.4, color=["black", "red", "green", "blue", "yellow"])
	plt.xlabel("name")
	plt.ylabel("salary")
	plt.title("Best Employee")
	plt.grid()
	plt.show()
	chart_window.withdraw()
	main_window.deiconify()
	
#============================================================

# main window

main_window = Tk()
main_window.title("E . M . S")
main_window.geometry("500x600+100+100")

f = ("Arial", 20, "bold")
y = 5

mw_btn_add = Button(main_window, text="Add", font=f, width=7, command=f1)
mw_btn_add.pack(pady=y)

mw_btn_view = Button(main_window, text="View", font=f, width=7, command=f3)
mw_btn_view.pack(pady=y)

mw_btn_update = Button(main_window, text="Update", font=f, width=7, command=f5)
mw_btn_update.pack(pady=y)

mw_btn_delete = Button(main_window, text="Delete", font=f, width=7, command=f13)
mw_btn_delete.pack(pady=y)

mw_btn_charts = Button(main_window, text="Charts", font=f, width=7,command=f16)
mw_btn_charts.pack(pady=y)

response = requests.get("http://api.quotable.io/random")
json_resp = response.json()

qoute = json_resp["content"]
author = json_resp["author"]
quote = qoute + "\n\t"+ "by " + author

msg = Message(main_window, text = quote,padx=180, pady=200, bd=5, relief = GROOVE)
msg.config(bg='white', fg='black', font=('verdana', 18))
msg.pack()


    
#============================================================

# add window
	
add_window = Toplevel(main_window)
add_window.title("Add Employee Details")
add_window.geometry("500x500+100+100")

aw_lab_eid = Label(add_window, text="Enter Employee Id", font=f)
aw_lab_eid.pack(pady=y)

aw_ent_eid = Entry(add_window, font=f)
aw_ent_eid.pack(pady=y)

aw_lab_ename = Label(add_window, text="Enter Employee Name", font=f)
aw_lab_ename.pack(pady=y)

aw_ent_ename = Entry(add_window, font=f)
aw_ent_ename.pack(pady=y)

aw_lab_esalary = Label(add_window, text="Enter Employee Salary", font=f)
aw_lab_esalary.pack(pady=y)

aw_ent_esalary = Entry(add_window, font=f)
aw_ent_esalary.pack(pady=y)

aw_btn_save = Button(add_window, text="Save",font=f, width=7, command=save)
aw_btn_save.pack(pady=y)

aw_btn_back= Button(add_window, text="Back", font=f, width=7, command=f2)
aw_btn_back.pack(pady=y)

add_window.withdraw()

#============================================================

# view window

view_window = Toplevel(main_window)
view_window.title("Employees Details")
view_window.geometry("500x500+100+100")

vw_emp_data = ScrolledText(view_window,width=35, height=10, font=f)
vw_emp_data.pack(pady=y)
vw_btn_back = Button(view_window, text="Back", font=f, command=f4)
vw_btn_back.pack(pady=y)
view_window.withdraw()

#============================================================

# update window

update_window = Toplevel(main_window)
update_window.title("update Details")
update_window.geometry("500x500+100+100")

uw_lab_eid = Label(update_window, text="Enter Employee Id", font=f)
uw_lab_eid.pack(pady=y)

uw_ent_eid = Entry(update_window, font=f)
uw_ent_eid.pack(pady=y)

uw_lab_ename = Label(update_window, text="Enter Employee Name", font=f)
uw_lab_ename.pack(pady=y)

uw_ent_ename = Entry(update_window, font=f)
uw_ent_ename.pack(pady=y)

uw_lab_esalary = Label(update_window, text="Enter Employee Salary", font=f)
uw_lab_esalary.pack(pady=y)

uw_ent_esalary = Entry(update_window, font=f)
uw_ent_esalary.pack(pady=y)

uw_btn_update = Button(update_window, text="Update",font=f, width=7, command=f7)
uw_btn_update.pack(pady=y)

uw_btn_back= Button(update_window, text="Back", font=f, width=7, command=f6)
uw_btn_back.pack(pady=y)

update_window.withdraw()




#============================================================# delete window
delete_window = Toplevel(main_window)
delete_window.title("update Details")
delete_window.geometry("500x500+100+100")

dw_lab_eid = Label(delete_window, text = "enter id", font=f)
dw_lab_eid.pack(pady=y)
dw_ent_eid = Entry(delete_window, font=f)
dw_ent_eid.pack(pady=y)

dw_btn_delete_emp = Button(delete_window, text="Delete Employee",font=f, width=14, command=f15)
dw_btn_delete_emp.pack(pady=y)
dw_btn_back = Button(delete_window, text="Back", font=f, width=14,command=f14)
dw_btn_back.pack(pady=y)
delete_window.withdraw()
#============================================================
# chart window
chart_window = Toplevel(main_window)
chart_window.title("chart")
chart_window.geometry("500x500+100+100")

cw_btn_show_chart = Button(chart_window, text="Show Chart",font=f, width=14,command=f18)
cw_btn_show_chart.place(x = 130, y = 100)
cw_btn_back = Button(chart_window, text="Back", font=f, width=14,command=f17)
cw_btn_back.place(x = 130, y = 200)



chart_window.withdraw()


main_window.mainloop()