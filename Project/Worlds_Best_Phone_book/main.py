import os
import sqlite3
import tkinter as tk
from tkinter import ttk



# Создание базы данных и таблицы контактов
class DB():
    def __init__(self):
        self.conn = sqlite3.connect('db.db')
        self.c = self.conn.cursor()
        self.c.execute("""CREATE TABLE IF NOT EXISTS contacts (
                       id INTEGER PRIMARY KEY,
                       name TEXT,
                       phone TEXT,
                       email TEXT
                       );
        """)
        
        self.conn.commit()

db = DB()



# Функция для отображения контактов в таблице
def show_contacts():
    for row in tree.get_children():
        tree.delete(row)
    db.c.execute('SELECT * FROM contacts')
    contacts = db.c.fetchall()
    for contact in contacts:
        tree.insert('', 'end', values=contact)

# Функция для добавления контакта
def add_contact():
    def save_contact():
        name = name_entry.get()
        phone = phone_entry.get()
        email = email_entry.get()
        db.c.execute('INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)', (name, phone, email))
        db.conn.commit()
        show_contacts()
        add_window.destroy()

    add_window = tk.Toplevel(root)
    add_window.title('Добавить контакт')
    name_label = tk.Label(add_window, text='Имя:')
    name_entry = tk.Entry(add_window)
    phone_label = tk.Label(add_window, text='Телефон:')
    phone_entry = tk.Entry(add_window)
    email_label = tk.Label(add_window, text='Email:')
    email_entry = tk.Entry(add_window)
    save_button = tk.Button(add_window, text='Сохранить', command=save_contact)
    name_label.pack()
    name_entry.pack()
    phone_label.pack()
    phone_entry.pack()
    email_label.pack()
    email_entry.pack()
    save_button.pack()

# Функция для обновления контакта
def update_contact():
    def save_contact():
        name = name_entry.get()
        phone = phone_entry.get()
        email = email_entry.get()
        db.c.execute('UPDATE contacts SET name=?, phone=?, email=? WHERE id=?', (name, phone, email, selected_id))
        db.conn.commit()
        show_contacts()
        update_window.destroy()

    selected_item = tree.selection()[0]
    selected_id = tree.item(selected_item)['values'][0]
    db.c.execute('SELECT * FROM contacts WHERE id=?', (selected_id,))
    contact = db.c.fetchone()

    update_window = tk.Toplevel(root)
    update_window.title('Обновить контакт')
    name_label = tk.Label(update_window, text='Имя:')
    name_entry = tk.Entry(update_window)
    name_entry.insert(0, contact[1])
    phone_label = tk.Label(update_window, text='Телефон:')
    phone_entry = tk.Entry(update_window)
    phone_entry.insert(0, contact[2])
    email_label = tk.Label(update_window, text='Email:')
    email_entry = tk.Entry(update_window)
    email_entry.insert(0, contact[3])
    save_button = tk.Button(update_window, text='Сохранить', command=save_contact)
    name_label.pack()
    name_entry.pack()
    phone_label.pack()
    phone_entry.pack()
    email_label.pack()
    email_entry.pack()
    save_button.pack()

# Функция для удаления контактов
def delete_contacts():
    for selected_item in tree.selection():
        selected_id = tree.item(selected_item)['values'][0]
        db.c.execute('DELETE FROM contacts WHERE id=?', (selected_id,))
        db.conn.commit()
        tree.delete(selected_item)

# Функция для поиска контактов
def search_contacts():
    def search_contact():
        search_text = search_entry.get()
        db.c.execute('SELECT * FROM contacts WHERE name LIKE ?', ('%' + search_text + '%',))
        contacts = db.c.fetchall()
        for row in tree.get_children():
            tree.delete(row)
        for contact in contacts:
            tree.insert('', 'end', values=contact)
        search_window.destroy()

    search_window = tk.Toplevel(root)
    search_window.title('Поиск контактов')
    search_label = tk.Label(search_window, text='Введите имя контакта:')
    search_entry = tk.Entry(search_window)
    search_button = tk.Button(search_window, text='Найти', command=search_contact)
    search_label.pack()
    search_entry.pack()
    search_button.pack()

# Функция для обновления данных в таблице
def refresh_table():
    show_contacts()

# Создание главного окна приложения
root = tk.Tk()
root.title('World`s best phone book')

# Создание верхней панели с кнопками
toolbar = tk.Frame(root)

add_picture = tk.PhotoImage(file='img/add.png')
add_button = tk.Button(toolbar, command=add_contact, image=add_picture)

update_picture = tk.PhotoImage(file='img/update.png')
update_button = tk.Button(toolbar, command=update_contact, image=update_picture)

delete_picture = tk.PhotoImage(file='img/delete.png')
delete_button = tk.Button(toolbar, command=delete_contacts, image=delete_picture)

search_picture = tk.PhotoImage(file='img/search.png')
search_button = tk.Button(toolbar, command=search_contacts, image=search_picture)

refresh_picture = tk.PhotoImage(file='img/refresh.png')
refresh_button = tk.Button(toolbar, command=refresh_table, image=refresh_picture)

add_button.pack(side=tk.LEFT)
update_button.pack(side=tk.LEFT)
delete_button.pack(side=tk.LEFT)
search_button.pack(side=tk.LEFT)
refresh_button.pack(side=tk.LEFT)

toolbar.pack(side=tk.TOP, fill=tk.X)

# Создание таблицы для отображения контактов
tree = ttk.Treeview(root, columns=('id', 'name', 'phone', 'email'), show='headings')
tree.heading('id', text='ID')
tree.heading('name', text='Имя')
tree.heading('phone', text='Телефон')
tree.heading('email', text='Email')
tree.column('id', width=50)
tree.column('name', width=150)
tree.column('phone', width=150)
tree.column('email', width=150)
tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Отображение контактов в таблице
show_contacts()

# Запуск главного цикла приложения
root.mainloop()

# Закрытие базы данных
db.conn.close()