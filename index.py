from calendar import weekheader
from cgitb import text
from distutils import command
from distutils.util import execute
from this import s
from tkinter import ttk
from tkinter import *

import sqlite3
from turtle import st
from winreg import QueryInfoKey

class Product:

        db_name = 'database.db'

        def __init__(self, window):
            self.window = window
            self.window.title('Products Application')

            # Creating a Frame Container
            frame =LabelFrame(self.window, text='Registra un nuevo producto')
            frame.grid(row = 2, column = 0, columnspan = 3, pady=20)

            # Name Input
            Label(frame, text='Nombre: ').grid(row='3', column=0)
            self.name=Entry(frame)
            self.name.focus()
            self.name.grid(row=3, column=1)

            #Price Input
            Label(frame, text='Precio: ').grid(row = 4, column = 0)
            self.price= Entry(frame)
            self.price.grid(row = 4, column = 1)

            #Button add product
            ttk.Button(frame, text = 'Agregar producto', command = self.add_product).grid(row = 5, columnspan = 2, sticky=W+E)

            # Output Messages
            self.message = Label(text = '', fg='red')
            self.message.grid(row = 5, column = 0, columnspan=2, sticky=W+E)


            #Table
            self.tree = ttk.Treeview(height=10,columns=2)
            self.tree.grid(row=7, column=0, columnspan=2)
            self.tree.heading('#0', text='Nombre', anchor=CENTER)
            self.tree.heading('#1', text='Precio', anchor=CENTER)

            #Buttons
            ttk.Button(text = 'Borrar', command = self.delete_product).grid(row = 8 , column=0, sticky=W+E )
            ttk.Button(text = 'Editar', command=self.edit_product).grid(row = 8 , column=1, sticky=W+E)

            #Filling the row
            self.get_products()

           

        def run_query(self, query, parameters = {}):
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                result= cursor.execute(query, parameters)
                conn.commit()
            return result

        def get_products(self):
            # cleaning table
            records = self.tree.get_children()
            for element in records:
                self.tree.delete(element)
                
            #quering data
            query = 'SELECT * FROM products ORDER BY name DESC'
            db_rows = self.run_query(query)
            for row in db_rows:
                self.tree.insert('', 0, text = row[1], value = row[2])

        def validation(self):
          return len(self.name.get()) != 0 and len(self.price.get()) != 0


        def add_product(self):
            if self.validation():
                query = 'INSERT INTO products VALUES (NULL, ?, ?)'
                parameters = (self.name.get(), self.price.get())
                self.run_query(query, parameters)
                self.message['text'] = 'Producto {} agregado'.format(self.name.get())
                self.name.delete(0, END)
                self.price.delete(0, END)
            else:
                self.message['text'] = 'Nombre y precio son requeridos'
            self.get_products()

        def delete_product(self):
            self.message['text'] = ''
            try:
                self.tree.item(self.tree.selection())['text'][0]
            except IndexError as e:
                self.message['text'] = 'Por favor selecciona un producto'
                return
            self.message['text'] = ''
            name = self.tree.item(self.tree.selection())['text']
            query = 'DELETE FROM products WHERE name = ?'
            self.run_query(query,(name, ))
            self.message['text'] = 'Producto {} borrado correctamente'.format(name)
            self.get_products()

        def edit_product(self):
            self.message['text'] = ''
            try:
                self.tree.item(self.tree.selection())['text'][0]
            except IndexError as e:
                self.message['text'] = 'Por favor selecciona un producto'
                return
            name = self.tree.item(self.tree.selection())['text']
            old_price = self.tree.item(self.tree.selection())['values'][0]
            self.edit_wind = Toplevel()
            self.edit_wind.title = 'Editar producto'

            #Old Name
            Label(self.edit_wind, text = 'Nombre viejo').grid(row=0, column=1)
            Entry(self.edit_wind, textvariable= StringVar(self.edit_wind, value = name),state='readonly').grid(row=0, column=2)

            #New Name
            Label(self.edit_wind, text = 'New name').grid(row=1, column=1)
            new_name = Entry(self.edit_wind)
            new_name.grid(row = 1, column = 2)

            #Old price
            Label(self.edit_wind, text = 'Precio Viejo').grid(row = 2, column = 1)
            Entry(self.edit_wind, textvariable= StringVar(self.edit_wind, value=old_price), state='readonly').grid(row=2, column=2)

            #New price
            Label(self.edit_wind, text = 'New price').grid(row=3, column=1)
            new_price = Entry(self.edit_wind)
            new_price.grid(row = 3, column = 2)

            Button(self.edit_wind, text = 'Actualizar', command = lambda: self.edit_records(new_name.get(), name, new_price.get(), old_price)).grid(row=4, column=2, sticky=W)
        
        def edit_records(self, new_name, name, new_price , old_price):
            query = 'UPDATE products SET name = ? , price = ? WHERE name = ? AND price = ?'
            parameters = (new_name, new_price, name, old_price)
            self.run_query(query, parameters)
            self.edit_wind.destroy()
            self.message['text'] = 'Producto {} editado correctamente'.format(name)
            self.get_products()


       

if __name__ =='__main__':
    window = Tk()
    application = Product(window)
    window.mainloop()