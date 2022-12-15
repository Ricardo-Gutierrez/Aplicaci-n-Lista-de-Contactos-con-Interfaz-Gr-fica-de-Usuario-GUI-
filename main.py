import sqlite3
from contactos_view import ContactosView
from contactos_controller import ContactosController
from contactos_repository import ContactsRepository
def main():
        with sqlite3.connect("contactos.db") as conn:
            c= conn.cursor()
            c.execute('''SELECT count (name) FROM sqlite_master WHERE type= 'table' and name='contacts' ''')
            if c.fetchone() [0]==1:
                print("Tabla existe")

                repo= ContactsRepository(conn)
                view=ContactosView()
                controller=ContactosController(repo,view)
                view.set_controller(controller)
                controller.start()
            else:
                c.execute(""" CREATE TABLE Contacts(
                    last_name text,
                    first_name text,
                    email text,
                    phone text

                )""")
            

if __name__=="__main__":
    main()