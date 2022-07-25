from cProfile import label
from cgitb import text
from ctypes import alignment
from tkinter import * # Para la interfaz grafica
from tkinter import messagebox # Para los mensajes de alerta emergentes
import sqlite3 # Para la base de datos que usaremos
from turtle import right
from xml.dom.minidom import Identified
import easygui
from more_itertools import padded # Para poder hacer un mensaje emergente con un input dialog



# ---------------------------------------------------------------------------------
# Nuestra aplicacion se llamara root
root = Tk(); # Tk es una clase para crear ventanas

# Creamos las variables StringVar() para poder trabajar con los campos de Texto tipo ENTRY
# Son variables de texto que son asignadas al texto de los Entrys cuando los creamos 
# para poder manejar su contenido
miId= StringVar()
miNombre = StringVar()
miPass = StringVar()
miApellido = StringVar()
miDireccion = StringVar()



# ------------------------------------------------------------------------------------
#     Funciones
# ------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------
# Funcion para la conexion a la BBDD
def conexionBBDD():
    try:
        miConexion = sqlite3.connect("Usuarios")
        miCursor= miConexion.cursor()
        miCursor.execute(''' CREATE TABLE DATOSUSUARIOS(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            NOMBRE_USUARIO VARCHAR(50),
            PASSWORD VARCHAR(50),
            APELLIDOS VARCHAR(50),
            DIRECCION VARCHAR(50),
            COMENTARIOS VARCHAR(100)
        )''')
        # Despues de crear una tabla recibimos si se creo con exito o no
        # El mensaje emergente necesita el titulo dela ventana, y su mensaje
        messagebox.showinfo("BBDD", "BBDD creada con éxito.")
    except:
        messagebox.showwarning("Atención", "La BBDD ya existe.")



# ------------------------------------------------------------------------------------
# Funcion para salir de la Aplicacion, donde antes de salir se pedira confirmacion
def salir_aplicacion():
    valor = messagebox.askquestion("Salir", "¿Deseas salir de la Aplicación?")

    if valor == "yes":
        root.destroy()



# ------------------------------------------------------------------------------------
# Funcion para borrar los campos
# Los campos que son de tipo ENTRY (todos menos el de Comentarios) 
# necesitan borrarse de una forma especial: Usando StringVar() y seteandolo a cadena vacia
# En cambio para un cuadro de texto (tipo Text), usaremos delete, indicandole que lo borraremos
# desde el principio, hasta el final (punto de partida= 1.0, punto final= END)
def borrar_campos():
    miId.set("")
    miNombre.set("")
    miPass.set("")
    miApellido.set("")
    miDireccion.set("")
    cuadroComentario.delete(1.0, END)
    


# -----------------------------------------------------------------------------------
def licencia():
    messagebox.showinfo("Licencia", "Licencia para mataal! ..." 
    + "naa, es broma, el que lo quiera usar, que lo disfrute :)")



# -----------------------------------------------------------------------------------
# Funcion para el Acerca de...
def acercaDe():
    messagebox.showinfo("Acerca de...", "Función creada por Jorge Alvarez Ceñal" 
    + "\nSiguiendo, como siempre, los pasos de Juan Díaz, de Pildoras Informaticas") 


# ------------------------------------------------------------------------------------
# Funcion que abre un cuadro de dialogo en el que pide el ID de un usuario y 
# devuelve el valor introducido. En el parámetro especificaremos que operacion queremos hacer
def pedirID(texto):
    idElegido = easygui.integerbox("Escribe el ID del usuario", f"Escribe el ID del usuario que deséas{texto}")
    return idElegido



# ------------------------------------------------------------------------------------
#                                  CRUD 
# Para realizar las consultas con el cursor, usaremos siempre fetchall, 
# aunque solo busquemos un objeto. 
# La razon es: 
#   fetchall devuelve una lista de tuplas 
#   fetchone devuelve una tupla. 
# De cara a trabajar vamos a necesitar objetos del tipo lista de tuplas
# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------
# Funcion CRUD --> CREATE : Insertar campo
def insertar_registro():
    try:
        miConexion = sqlite3.connect("Usuarios") # Creamos la conexion
        miCursor = miConexion.cursor() # Creamos el cursor

        miCursor.execute(f''' INSERT INTO DATOSUSUARIOS(
            NOMBRE_USUARIO, PASSWORD, APELLIDOS, DIRECCION, COMENTARIOS)
            VALUES(
                '{miNombre.get()}','{miPass.get()}','{miApellido.get()}',
                '{miDireccion.get()}', '{cuadroComentario.get("1.0", END)}'
            )''')
        miConexion.commit()
        borrar_campos()
        messagebox.showinfo("Inserción Correcta", "Registro insertado")
    except Exception as ex:
        messagebox.showerror("Error en la inserción","No se ha podido insertar: " + str(ex))
    


# ------------------------------------------------------------------------------------
# Funcion CRUD --> SELECT : Leer campos de un usuario buscado por su ID
def seleccionar():
    # Por si acaso hay campos usados, los borramos primero
    borrar_campos()

    # Necesito pedir al usuario el ID que necesitamos saber
    idElegido = pedirID("seleccionar")
    seleccionarPorId(idElegido)



# -----------------------------------------------------------------------------------
# Funcion para seleccionar un registro basandose en el ID.
def seleccionarPorId(idElegido):
    miConexion = sqlite3.connect("Usuarios")
    miCursor = miConexion.cursor()
    miCursor.execute(f'''SELECT ID, NOMBRE_USUARIO, PASSWORD, APELLIDOS, DIRECCION, COMENTARIOS
    FROM DATOSUSUARIOS WHERE ID="{idElegido}"''')
    
    usuario = miCursor.fetchall() 
    pasarUsuarioCampos(usuario)



# ---------------------------------------------------------------------------------
# Funcion para pasar un usuario (en formato lista de tuplas) a los campos de la app
def pasarUsuarioCampos(usuario):
    try:
        if len(usuario) > 0:       
            for dts_usuario in usuario:
                miId.set(str(dts_usuario[0]))
                miNombre.set(dts_usuario[1])
                miPass.set(dts_usuario[2])
                miApellido.set(dts_usuario[3])
                miDireccion.set(dts_usuario[4])
                # Para el text usamos el metodo insert, dandole la posicion de inicio
                cuadroComentario.insert(1.0, dts_usuario[5])
    except Exception as ex:
        print("Error en pasarUsuarioCampos: " + str(ex))



# ------------------------------------------------------------------------------------
# Funcion CRUD --> UPDATE : Modificar campo
def actualizar_registro():
    try:
        idUsuario = pedirID("actualizar")

        conexion = sqlite3.connect("Usuarios")
        cursor = conexion.cursor()
        
        cursor.execute(f'''UPDATE DATOSUSUARIOS SET 
        NOMBRE_USUARIO = "{miNombre.get()}",
        PASSWORD = "{miPass.get()}",
        APELLIDOS = "{miApellido.get()}",
        DIRECCION ="{miDireccion.get()}",
        COMENTARIOS = "{cuadroComentario.get(1.0, END)}" 
        WHERE ID="{idUsuario}";
        ''')
        conexion.commit()

        borrar_campos()
        messagebox.showinfo("Actualización OK", f'''Actualización del registro {idUsuario} 
        realizada con éxito''')
    except Exception as ex:
        messagebox.showerror("Error en la actualización", 
        f"Error producido en la actualización: {str(ex)}")



# ------------------------------------------------------------------------------------
# Funcion CRUD --> DELETE : Borrar registro
def borrar_registro():
    idElegido = pedirID("borrar")
    if existeUsuario(idElegido) == True:
        seguro = messagebox.askyesno("Precaución", f'''Seguro que quieres borrar el registro {idElegido}?
        Almacena los datos: {sacar_usuario_txt(idElegido)}''')
        
        if seguro == 1: # askyesno devuelve 1 como yes y vacio como no
            try:
                conexion = sqlite3.connect("Usuarios")
                cursor = conexion.cursor()

                cursor.execute(f'''DELETE FROM DATOSUSUARIOS WHERE ID="{idElegido}"; ''')
                conexion.commit()
                messagebox.showinfo("Borrado OK", f"Registro id:{idElegido} borrado con éxito")
                borrar_campos()
            except Exception as ex:
                messagebox.showerror("Error al borrar", 
                f''' No se ha podido borrar el registro con id: {idElegido}:
                {str(ex)}''')
    else:
        messagebox.showinfo("No existe el ID", f"Lo siento, no existe el registro con ID {idElegido}")


# Funcion para saber si existe un registro por su ID
def existeUsuario(idElegido):
    try:
        conexion = sqlite3.connect("Usuarios")
        cursor = conexion.cursor()

        cursor.execute(f'''SELECT COUNT(*) FROM DATOSUSUARIOS WHERE ID={idElegido}; ''')
        conexion.commit()
        resultado = cursor.fetchone()
        if str(resultado[0]) == '0':
            return False
        elif str(resultado[0]) == '1':
            return True

    except:
        pass


# ------------------------------------------------------------------------------------
# Funcion para sacar en formato texto los datos de un usuario
# Usaremos esta funcion en la anterior, la de borrar registro, mostrando antes de borrar
# el registro que intentamos borrar, mediante un mensaje emergente
def sacar_usuario_txt(idElegido):
    usuario =""
    miConexion = sqlite3.connect("Usuarios")
    miCursor = miConexion.cursor()
    miCursor.execute(f'''SELECT ID, NOMBRE_USUARIO, PASSWORD, APELLIDOS, DIRECCION, COMENTARIOS
    FROM DATOSUSUARIOS WHERE ID="{idElegido}"''')
    
    usuario = miCursor.fetchall() # Si hiceramos fetch one solo cogeria un campo
    if len(usuario) > 0:
        
        for dts_usuario in usuario:
            usuario = f'''
            ID: str({idElegido})
            Nombre: {dts_usuario[1]} 
            Password: {dts_usuario[2]} 
            Apellidos: {dts_usuario[3]} 
            Dirección: {dts_usuario[4]} 
            Comentarios: {dts_usuario[5]}'''
    return usuario




# ---------------------------------------------------------------------------------
# Funcion para el boton de Anterior
def btnAnterior():
    conexion = sqlite3.connect('Usuarios')
    miCursor = conexion.cursor()

    # Vamos a comprobar que el campo de Id no este vacio, y que sea un valor mayor de cero
    if len(miId.get()) > 0 and int(miId.get()) > 0:
        idElegido = miId.get()
        miCursor.execute(f'''SELECT ID, NOMBRE_USUARIO, PASSWORD, APELLIDOS,DIRECCION, COMENTARIOS
        FROM DATOSUSUARIOS WHERE ID < {idElegido} ORDER BY ID DESC LIMIT 1;''')
        miUsuario = miCursor.fetchall()

    else:
        miCursor.execute(f'''SELECT ID, NOMBRE_USUARIO, PASSWORD, APELLIDOS,DIRECCION, COMENTARIOS
        FROM DATOSUSUARIOS ORDER BY ID LIMIT 1;''')
        miUsuario = miCursor.fetchall()

    # Si encontramos algun registro, pues borramos los campos y pasamos los datos
    if  len(miUsuario)>0:
        borrar_campos()
        pasarUsuarioCampos(miUsuario)



# -----------------------------------------------------------------------------------
def btnSiguiente():
    conexion = sqlite3.connect('Usuarios')
    miCursor = conexion.cursor()
    miUsuario = []

    if len(miId.get()) > 0:
        idElegido = miId.get()
        miCursor.execute(f'''SELECT ID, NOMBRE_USUARIO, PASSWORD, APELLIDOS,DIRECCION, COMENTARIOS
        FROM DATOSUSUARIOS WHERE ID > {idElegido} ORDER BY ID LIMIT 1;''')
        miUsuario = miCursor.fetchall()
    else:
        miCursor.execute(f'''SELECT ID, NOMBRE_USUARIO, PASSWORD, APELLIDOS,DIRECCION, COMENTARIOS
        FROM DATOSUSUARIOS ORDER BY ID DESC LIMIT 1;''')
        miUsuario = miCursor.fetchall()


    # Si encontramos algun registro, pues borramos los campos y pasamos los datos
    if  len(miUsuario)>0:
        borrar_campos()
        pasarUsuarioCampos(miUsuario)




# ------------------------------------------------------------------------------------
#            Interfaz
# ------------------------------------------------------------------------------------

# Creamos la barra de menu superior
barraMenu = Menu(root)
root.config(menu=barraMenu, width=300, height=500)


# Creamos los submenus que este dentro de la barra de menu superior
bbddMenu = Menu(barraMenu, tearoff=0) # tearoff a 1 pone una linea divisoria en el principio
borrarMenu = Menu(barraMenu, tearoff=0)
crudMenu = Menu(barraMenu, tearoff=0)
ayudaMenu = Menu(barraMenu, tearoff=0)

# El primer submenu tendra los elementos de conectar a la BBDD y Salir
bbddMenu.add_command(label="Conectar", command=conexionBBDD)
bbddMenu.add_command(label="Salir", command=salir_aplicacion)

# El segundo submenu tendra un elemento para borrar los campos de la interfaz
borrarMenu.add_command(label="Borrar campos", command=borrar_campos)

# El tercer submenu tendra los elementos para realizar CRUD
crudMenu.add_command(label="Crear", command=insertar_registro)
crudMenu.add_command(label="Leer", command=seleccionar)
crudMenu.add_command(label="Actualizar", command=actualizar_registro)
crudMenu.add_command(label="Borrar", command=borrar_registro)

#El cuarto y ultimo submenu tendra elementos de ayuda
ayudaMenu.add_command(label="Licencia", command =licencia)
ayudaMenu.add_command(label="Acerca de...", command=acercaDe)

# Ahora tenemos que pasar cada barra de menu a la interfaz dandole un nombre
barraMenu.add_cascade(label="BBDD", menu=bbddMenu)
barraMenu.add_cascade(label="Borrar", menu =borrarMenu)
barraMenu.add_cascade(label="Menu CRUD", menu=crudMenu)
barraMenu.add_cascade(label="Ayuda", menu=ayudaMenu)

# ------------------------------------------------------------------------------------
# Creo un Frame para usar unos botones de Anterior y Siguiente para moverme por la tabla
miFrameAntSig = Frame(root)
miFrameAntSig.pack()
btnAnterior = Button(miFrameAntSig, text="Anterior", command=btnAnterior)
btnSiguiente = Button(miFrameAntSig, text="Siguiente", command=btnSiguiente)

btnAnterior.grid(row=0, column=0)
btnSiguiente.grid(row=0, column=2)

lblVacio = Label(miFrameAntSig, text="Usuarios", padx=60)
lblVacio.grid(row=0, column=1)

# ------------------------------------------------------------------------------------
# Vamos a crear la zona central con los Frames de Etiquetas y Campos

# Vamos a crear los Frames para los campos de la BBDD
# Creamos el Frame emparentandolo desde root
miFrame = Frame(root)
miFrame.pack()

# Creamos las entradas de texto (Entry), pasando como parametro la variable StringVar
# que creamos en el principio, para poder borrar su texto con el boton del menu superior
cuadroID = Entry(miFrame, textvariable=miId)
cuadroID.grid(row=0, column=1, padx=10, pady=10)
cuadroID.config(state='readonly', fg="red", justify="right")

cuadroNombre = Entry(miFrame, textvariable=miNombre)
cuadroNombre.grid(row=1, column=1, padx=10, pady=10)

cuadroPass = Entry(miFrame, textvariable=miPass)
cuadroPass.grid(row=2, column=1, padx=10, pady=10)
# El campo de password no queremos que muestre la clave, asi que haremos que escriba '?'
cuadroPass.config(show='?')

cuadroApellido = Entry(miFrame, textvariable=miApellido)
cuadroApellido.grid(row=3, column=1, padx=10, pady=10)

cuadroDireccion = Entry(miFrame, textvariable=miDireccion)
cuadroDireccion.grid(row=4, column=1, padx=10, pady=10)

# El cuadro de comentario es de tipo Text, ya que permite multilineas 
# (5 lineas visibles en pantalla )
cuadroComentario = Text(miFrame, width=20, height=5)
cuadroComentario.grid(row=5, column=1, padx=10, pady=10)

# Creamos una barra de scrollbar para el comentario
# Debe ponerse en la columna 2 ( la 1 es para el campo de comentario)
# Para ubicarlo mejor, le ponemos el param sticky a nsew
scrollVertical = Scrollbar(miFrame, command=cuadroComentario.yview)
scrollVertical.grid(row=5, column=2, sticky="nsew") 

# Ahora ya le asociamos al cuadro de comentario, la barra de scroll
cuadroComentario.config(yscrollcommand=scrollVertical.set)


# ------------------------------------------------------------------------------------
# Ahora vamos a poner las etiquetas de los campos
labelID = Label(miFrame,text="ID :")
labelID.grid(row=0, column=0, sticky="e", padx=10, pady=10)

labelNombre = Label(miFrame, text="Nombre :")
labelNombre.grid(row=1, column=0, sticky="e", padx=10, pady=10)

LabelPass = Label(miFrame, text="Password :")
LabelPass.grid(row=2, column=0, sticky="e", padx=10, pady=10)

LabelApellidos = Label(miFrame, text="Apellidos :")
LabelApellidos.grid(row=3, column=0, sticky="e", padx=10, pady=10)

labelDireccion = Label(miFrame, text="Direccion: ")
labelDireccion.grid(row=4, column=0, sticky="e", padx=10, pady=10)

labelComentario = Label(miFrame, text="Comentarios: ")
labelComentario.grid(row=5, column=0, sticky="e", padx=10, pady=10)



# ------------------------------------------------------------------------------------
# Vamos a crear el menu inferior
miFrameInferior = Frame(root) # Pertenece al padre de todos
miFrameInferior.pack()

botonCrear = Button(miFrameInferior, text="Crear", command=insertar_registro)
botonCrear.grid(row=1, column=0, sticky="e", padx=10, pady=10)

botonLeer = Button(miFrameInferior, text="Leer", command=seleccionar)
botonLeer.grid(row=1, column=1, sticky="e", padx=10, pady=10)

botonActualizar = Button(miFrameInferior, text="Actualizar", command=actualizar_registro)
botonActualizar.grid(row=1, column=2, sticky="e", padx=10, pady=10)

botonBorrar = Button(miFrameInferior, text="Borrar", command=borrar_registro)
botonBorrar.grid(row=1, column=3, sticky="e", padx=10, pady=10)


# Ejecutamos nuestra aplicacion
root.mainloop()