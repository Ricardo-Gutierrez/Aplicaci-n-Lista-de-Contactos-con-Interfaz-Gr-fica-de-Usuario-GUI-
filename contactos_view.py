import tkinter as tk 
import tkinter.messagebox as mb
from contactos import Contacto

class ContactosList(tk.Frame):
    def __init__ (self,master,**kwargs):
        super().__init__ (master)
        self.list=tk.Listbox(self,**kwargs)
        bar=tk.Scrollbar(self, command=self.list.yview)

        self.list.config(yscrollcommand=bar.set)
        bar.pack(side=tk.RIGHT, fill=tk.Y)
        self.list.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    def insert(self, contact, index=tk.END):
        text="{},{}".format(contact.last_name,contact.first_name)
        self.list.insert(index, text)   

    def delete(self, index):
        self.list.delete(index, index)

    def update(self,contact,index):
        self.delete(index)
        self.insert(contact,index)

    def double_click(self,callback):
        handler= lambda _: callback(self.list.curselection()[0])
        self.list.bind("<Double-Button-1>",handler)

class ContactosForm(tk.LabelFrame):
    campos=("Last name","Fist name","Email","Phone")

    def __init__(self,master, **kwargs):
        super().__init__ (master, text="contacts", padx=10, pady=10, **kwargs)
        self.frame= tk.Frame(self)
        self.frame.pack()
        self.entries= list(map(self.create_campo, enumerate(self.campos)))

    def create_campo(self,campo):
        position, texto=campo   
        label = tk.Label(self.frame, text=texto)   
        entry = tk.Entry(self.frame)  
        label.grid(row=position, column=0, pady=10)
        entry.grid(row=position, column=1, pady=10)
        return entry

    def get_data(self):
        values=[e.get() for e in self.entries]
        print("values", values)
        try:
            return Contacto(*values)
        except ValueError as e:
            tk.messagebox.showerror("Error", str(e), parent=self)  

    def load_details(self,contact):
        values=(contact.last_name, contact.first_name, contact.email, contact.phone)
        for entry, value in  zip(self.entries,values):

            entry.delete(tk.END)
            entry.insert(0,value)

    def clear(self):
        for entry in self.entries:
            entry.delete(0,tk.END)

    # Formulario para actualizar contacto en MAster
class ActualizarContactosForm(ContactosForm):
    def __init__ (self, master,**kwargs):
        super().__init__(master,**kwargs)
        self.Button_save=tk.Button(self, text="save")
        self.Button_delete=tk.Button(self, text="delete")

        self.Button_save.pack (side=tk.RIGHT, ipadx=5, padx=5, pady=5)
        self.Button_delete.pack(side=tk.RIGHT, ipadx=5, padx=5, pady=5)


class ContactoNuevo(tk.Toplevel):
    def __init__(self,parent):
        super().__init__(parent)
        self.contact=None
        self.form=ContactosForm(self)
        self.form.pack(padx=10,pady=10)
        self.button_add=tk.Button(self, text= "Agregar Contacto", command= self.confirm)
        self.button_add.pack()


    def confirm(self):
        print("Confirm contact")
        print("Adding new contact...")
        self.contact=self.form.get_data()
        if self.contact:
            self.destroy()


    def show(self):
        self.grab_set()
        self.wait_window()
        return self.contact


class ContactosView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("LISTA DE CONTACTOS")
        #self.geometry('500x500')
        self.button_new =tk.Button(self, text="New Contact")
        self.button_new.pack(side=tk.BOTTOM, pady=5)

        #Agregar a la clase Contactos view la lista
        self.list=ContactosList(self, height=15)
        self.list.pack(side=tk.LEFT, padx=10, pady=10)


        #Agregar formulario para actualizar
        self.updateform= ActualizarContactosForm (self)
        self.updateform.pack(padx=10,pady=10)


    def set_controller(self,controller):
        self.button_new.config(command=controller.create_contact)
        #Enlazar con el controlador
        self.updateform.Button_save.config(command=controller.update_contact)
        self.updateform.Button_delete.config(command=controller.delete_contact)
        self.list.double_click(controller.select_contact)

    def add_contact(self,contac):
        self.list.insert(contac) 

    def add_contact(self,contact):
        self.list.insert(contact)

    def update_contact(self,contact,index):
        self.list.update(contact, index)

    def remove_contact(self,index):
        self.updateform.clear()
        self.list.delete(index)

    def get_data(self):
        return self.updateform.get_data()

    def load_details(self, contact):
        self.updateform.load_details(contact)
