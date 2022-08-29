"""
IMPORTAMOS LA CLASE DE NEGOCIO DE DATOS
"""
import BackEnd as Dao 
"""
traigo todos los elementos de la biblioteca
"""
from tkinter import * 
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sys
from tkinter import font
from bson.objectid import ObjectId
from datetime import date
#HAGO LA CONEXION CON MONGODB
from pymongo import MongoClient
#IMPORTAMOS LA CLASE PARA EXPORTAR PDF
from classPDF import *


class Usuarios:
    '''
    Clase Usuarios.
    
    Atributos
    ----------
        nombre: str
            ventana destinada a interfaces
        apellido: str
            Apellido del Usuario
        edad: int
            edad del Usuario
        usuario: str
            usuario de la persona
        clave: str
            Clave con la que va acceder el Usuario a su cuenta
    
    Metodos
    ----------
        def __init__(self, nombre,apellido,correo,usuario,clave,sexo):
            Constructor de la clase
            
        def registroUsuario(self):
            Se piden diversos datos necesarios para el registro de
            ----------
            guarda los datos en la base de datos

        def eliminar():
            elimina datis de la base de datos

        def editar():
            edita datos dentro de la base de datos

        def actualizar():
            actualiza la base de datos con los que habian sido editados
        
        def validar()
            exige al usuario llenar todos los campos para el registro
        
        def limpiar():
            limpia las cajas de texto.

        def obtenerVista(self):
            permite visualizar los usuarios registrados y algunos
            detalles mas.
    '''

    def __init__(self,nombre,apellido,sexo,edad,usuario,clave):
        '''
        Construye todos los atributos necesarios para el Usuario.
        Parametros
        ----------
            nombre: str
                Nombre del Usuario
            apellido: str
                Apellido del Usuario
            sexo: str
                sexo del Usuario
            edad: str
                edad del Usuario
            usuario: str
                usuario a registrar
            clave: str
                Clave con la que va acceder el Usuario a su cuenta
        '''
        self.nombre=nombre
        self.apellido=apellido
        self.sexo=sexo
        self.edad=edad
        self.usuario=usuario
        self.clave=clave

    def registroUsuario(self, ventana):
        
        """Permite que el usuario se registre
        ingresando una serie de datos.

        Parametros
        ----------
            ventana: str
                permite crear las interfaces
        """
        self.window=ventana
        self.window.title('Registro de Usuarios')
        self.window.geometry("1600x600") 
        
        """CREAMOS DOS CONTENEDORES"""
        contenedor=LabelFrame(self.window, text='Registro de Usuario')
        contenedor.grid(row=0, column=0, columnspan=2,pady=5)

        contenedorLv=LabelFrame(self.window, text='')
        contenedorLv.grid(row=13, column=0, columnspan=2,pady=5)
        
        """CREAR ETIQUETAS CON SUS CAJAS DE TEXTO """
        Label(contenedor,text='Nombres:', bg="light blue").grid(row=1, column=0,sticky=W+E)
        self.nombre=Entry(contenedor)
        self.nombre.grid(row=1,column=1,sticky=W+E)

        Label(contenedor,text='Apellidos:', bg="light blue").grid(row=2, column=0,sticky=W+E)
        self.apellido=Entry(contenedor)
        self.apellido.grid(row=2,column=1,sticky=W+E)

        Label(contenedor,text='Edad:', bg="light blue").grid(row=3, column=0,sticky=W+E)
        self.edad=Entry(contenedor)
        self.edad.grid(row=3,column=1,sticky=W+E)

        Label(contenedor,text='Usuario:', bg="light blue").grid(row=4, column=0,sticky=W+E)
        self.usuario=Entry(contenedor)
        self.usuario.grid(row=4,column=1,sticky=W+E)

        Label(contenedor,text='Contraseña:', bg="light blue").grid(row=5, column=0,sticky=W+E)
        self.clave=Entry(contenedor ,show="*")
        self.clave.grid(row=5,column=1,sticky=W+E)

        Label (contenedor, text="Sexo",bg = "light blue").grid(row=6, column=0,sticky=W+E)
        self.sexo = Entry (contenedor)
        self.sexo=StringVar(contenedor)
        opcionesSexo=["Masculino","Femenino"]
        opcionesSexo=OptionMenu(contenedor,self.sexo,*opcionesSexo)
        opcionesSexo.grid(row=6, column=1, columnspan=1,pady=5,sticky=W+E)


        """CREAMOS UNA VISTA DE DATOS"""
        columnas = ('#1', '#2', '#3', '#4', '#5')
        self.vista=ttk.Treeview(contenedorLv,height=14,columns=columnas)
        self.vista.grid(row=13,column=0, columnspan=2)
        self.vista.heading('#0',text='Id',anchor=CENTER)
        self.vista.heading('#1',text='Nombres',anchor=CENTER)
        self.vista.heading('#2',text='Apellidos',anchor=CENTER)
        self.vista.heading('#3',text='Sexo',anchor=CENTER)
        self.vista.heading('#4',text='Edad',anchor=CENTER)
        self.vista.heading('#5',text='Usuario',anchor=CENTER)

        """LLENAMOS DE DATOS LA VISTA"""
        self.ObtenerVista()

        def Salir():
            ventana.destroy()

        """CREAMOS LOS BOTONES QUE VAMOS A DEJAR ACTIVOS EN LA EDICION"""
        ttk.Button(contenedor, text='Guardar',command=self.Guardar).grid(row=10, column=0,sticky=W+E)
        ttk.Button(contenedor, text='Eliminar',command=self.Eliminar).grid(row=10, column=1,sticky=W+E)
        ttk.Button(contenedor, text='Actualizar',command=self.Actualizar).grid(row=11, column=0,sticky=W+E)
        ttk.Button(contenedor, text='Salir',command=Salir).grid(row=11, column=1,sticky=W+E)  
        ttk.Button(contenedor, text='Editar',command=self.Editar).grid(row=12, column=0,sticky=W+E)                                     
        
    def ObtenerVista(self):
        """
        METODO PARA CONSULTAR LA COLECCION COMPLETA
        """
        registros=self.vista.get_children()
        for elemento in registros:
            self.vista.delete(elemento)
        """Consultando los datos"""
        self.adapatadorUsu=Dao.DaoUsu(nombres=self.nombre.get(),apellidos=self.apellido.get(),sexo=self.sexo.get(),edad=self.edad.get(),usuario=self.usuario.get(),clave=self.clave.get())
        resultados=self.adapatadorUsu.consultarTodosUsu()
        """llenando los datos"""
        for Fila in resultados:
            self.vista.insert('', 0, text= Fila["_id"],
            values = (Fila["nombres"],Fila["apellidos"],Fila["sexo"],Fila["edad"],Fila["usuario"]))
    
    def limpiarCajas(self):
        """
        SE LIMPIAN LOS CUADROS DE TEXTO PRIMERO
        """
        self.nombre.delete(0,END)
        self.apellido.delete(0,END)
        self.edad.delete(0,END)
        self.usuario.delete(0,END)
        self.clave.delete(0,END)
                       
    def validar(self):
        """
        VALIDACION DE LOS DATOS
        """
        return len(self.nombre.get())!=0 and len(self.apellido.get())!=0 and len(self.sexo.get())!=0 and len(self.edad.get())!=0 and len(self.usuario.get())!=0 and len(self.clave.get())!=0
        
    def Guardar(self):
        """
        METODO PARA GUARDAR UN REGISTRO
        """
        try:
            """REALIZAMOS EL GUARDADO DEL REGISTRO SI ES QUE NO HAY ERRORES"""
            if self.validar():
                """INSTANCIAMOS EL OBJETO DE DATOS USUARIO"""
                self.adapatadorUsu=Dao.DaoUsu(nombres=self.nombre.get(),apellidos=self.apellido.get(),sexo=self.sexo.get(),edad=self.edad.get(),usuario=self.usuario.get(),clave=self.clave.get())
                self.adapatadorUsu.insertarUsuario()
                self.ObtenerVista()
                self.limpiarCajas()
            else:
                messagebox.showwarning("Error de validación","Ingrese información requerida, hay campos sin llenar.")
        except Exception:
                e=sys.exc_info()[1]
                messagebox.showerror('Error',e.args[0])

    def Eliminar(self):
        """
        METODO PARA ELIMINAR UN REGISTRO
        """
        """REALIZAMOS LA ELIMINACION DEL REGISTRO SI ES QUE NO HAY ERRORES"""
        try:
            """CAPTURAMOS EL ID DEL REGISTRO SELECCIONADO EN LA VISTA(LISTVIEW)"""
            self.vista.item(self.vista.selection())['text'][0]
        except IndexError as e:
            messagebox.showerror("Error","Seleccione un registro para eliminar.")
            return
        idUsu=self.vista.item(self.vista.selection())['text']
        self.adapatadorUsu.eliminarUsuario(idUsu)
        self.ObtenerVista()

    def Actualizar(self): 
        """
        METODO PARA ACTUZALIZAR UN REGISTRO
        """ 
        try:
            if self.validar():
                """CAPTURAMOS EL ID DEL REGISTRO SELECCIONADO EN LA VISTA(LISTVIEW)"""
                idUsu=str(self.vista.item(self.vista.selection())['text'])
                self.adapatadorUsu=Dao.DaoUsu(nombres=self.nombre.get(),apellidos=self.apellido.get(),sexo=self.sexo.get(),edad=self.edad.get(),usuario=self.usuario.get(),clave=self.clave.get())
                self.adapatadorUsu.actualizarUsuario(idUsu)
                self.ObtenerVista()
                self.limpiarCajas()
            else:
                messagebox.showwarning("Error de validación","Ingrese información requerida, hay campos sin llenar.")
        except Exception as e:
            e=sys.exc_info()[1]
            messagebox.showerror('Error',e.args[0])      

    def Editar(self):
        """
        METODO PARA EDITAR UN REGISTRO
        """
        try:
            """CAPTURAMOS EL ID DEL REGISTRO SELECCIONADO EN LA VISTA(LISTVIEW)"""
            self.vista.item(self.vista.selection())['text'][0]
        except IndexError as e:
            messagebox.showerror("Error","Seleccione un registro para editar.")
            return
        
        self.limpiarCajas()
        """CAPTURAMOS EL ID DEL REGISTRO SELECCIONADO EN LA VISTA(LISTVIEW)"""
        id=str(self.vista.item(self.vista.selection())['text'])
        res=self.adapatadorUsu.consultarUnoUsu(id)
        self.nombre.insert(0,str(res['nombres']))
        self.apellido.insert(0,str(res['apellidos']))
        self.edad.insert(0,str(res['edad']))
        self.usuario.insert(0,str(res['usuario']))
        self.clave.insert(0,str(res['clave']))


#////////////////////////////////////////////
#MENU PRINICIPAL DEL SISTEMA
#///////////////////////////////////////////

class menuPrincipal:
    '''
    Atributos
    ----------
    ventana:str
        crea la interfaz correspondiente
    
    Metodo
    ----------
    def __init__(self, ventana):
        Constructor de la clase
        
    def salir(self):
        sale por completo del programa/cierra interfaces.

    def Registrarse():
        permite abrir las interfaces de la clase Usuario

    def obtenerVista(self):
        permite visualizar las interfaces de la clase Control

    
    '''
    def __init__(self,ventana):
        """
        Metodo constructor
        ---------------
        """
        self.window=ventana
        self.window.title('Menu Principal Control de Indice de Masa Corporal')
        self.window.geometry("600x200+400+300")
              
        """CREAMOS UN CONTENEDOR"""
        contenedor=LabelFrame(self.window, text='Menu Principal')
        contenedor.grid(row=0, column=0, columnspan=2,pady=5)

        def Salir():
            """Destruye todas las interfaces"""
            ventana.destroy()

        def Registrarse():
            """Metodo que permite abrir las interfaces correspondiente al
            registro de los Usuarios"""
            ventana = Toplevel()
            aplicacion=Usuarios("","","","","","")
            aplicacion.registroUsuario(ventana)
            ventana.mainloop()
        
        def Control():
            """metodo que abre la interfaz correspondiente a control"""
            ventanaReg = Toplevel()
            aplicacion=Inicio_Sesion("","")
            aplicacion.inicioSesion(ventanaReg)
            ventanaReg.mainloop()

        """CREAMOS LOS BOTONES"""
        ttk.Button(contenedor, text='CONTROL DE IMC',command=Control).grid(row=4, column=0,sticky=W+E)
        ttk.Button(contenedor, text='REGISTRARSE',command=Registrarse).grid(row=4, column=1,sticky=W+E)
        ttk.Button(contenedor, text='SALIR', command=Salir).grid(row=4, column=2,sticky=W+E)


#/////////////////////////////////////////////////
#CLASE PARA CREAR LA INTERFAZ DE INICIO DE SESION
#////////////////////////////////////////////////

class Inicio_Sesion:
    '''
    Clase Inicio_Sesion.
    
    Atributos
    ----------
        usuario: str
            usuario para acceder a la cuenta
        clave: str
            Clave con la que va acceder el Usuario a su cuenta
    
    Metodo
    ----------
    def __init__(self, usuario, clave):
        Constructor de la clase
        
        En este apartado el usuario validara' sus datos para comprobar
        si se enuentra o no registrado
        ----------
        def validarAcceso()
            valida que los datos sean correctos
        
        def Salir():
            sale de la interfaz.
        '''
    def __init__(self, usuario, clave):
        '''
        Construye todos los atributos necesarios para el Usuario.
            Parametros
            ----------
            usuario: str
                Registro del usuario de la cuenta
            clave: str
                Clave con la que va acceder el Usuario a su cuenta
        '''
        self.usuario=usuario
        self.clave=clave

        #ESTABLECEMOS LAS VARIABLES DE CONEXION DE LA BD
        MongoUrl='mongodb://localhost'
        cliente=MongoClient(MongoUrl)
        Bd=cliente['IMC']
        self.coleccion=Bd['Usuarios']

    def inicioSesion(self, VentanaInicio):
        """Permite que el usuario ingrese sus credenciales
        para verificar si ya se registro'.

        Parametros
        ----------
        ventana: str
            permite crear las interfaces

        """
        """creacion de la interfaz 'Inicio de Sesion' """
        self.window=VentanaInicio
        self.window.title('Inicio de Sesión')
        self.window.geometry("200x100+550+350")

        """ESTABLECEMOS LAS VARIABLES DE CONEXION DE LA BD"""
        MongoUrl='mongodb://localhost'
        cliente=MongoClient(MongoUrl)
        Bd=cliente['IMC']
        self.coleccion=Bd['Usuarios']

        """CREAMOS UN CONTENEDOR"""
        contenedor=LabelFrame(self.window, text='Ingrese sus credenciales')
        contenedor.grid(row=0, column=0, columnspan=2,pady=5)

        """CREAR ETIQUETAS CON SUS CAJAS DE TEXTO"""
        Label(contenedor,text='Usuario:', bg="light blue").grid(row=1, column=0,sticky=W+E)
        self.usuario=Entry(contenedor)
        self.usuario.grid(row=1,column=1,sticky=W+E)

        Label(contenedor,text='Clave:', bg="light blue").grid(row=2, column=0,sticky=W+E)
        self.clave=Entry(contenedor,show="*")
        self.clave.grid(row=2,column=1,sticky=W+E)

        def ValidarAcceso():
            """EVALUAMOS SI TIENE ACCESO O NO"""

            idBuscar={"usuario":str(self.usuario.get()),"clave":str(self.clave.get())}
            resultados=self.coleccion.find_one(idBuscar)
            if resultados==None:
                messagebox.showwarning("Acceso Denegado","Usuario o Contraseña no existe.")
            else:
                ventanaControl = Toplevel()
                aplicacion=Control("","","","","")
                aplicacion.CalculosIMC(ventanaControl)
                ventanaControl.mainloop()
            Salir()
            
        def Salir():
            """CREAMOS EL SUB-METODO PARA SALIR DE LA VENTANA"""
            VentanaInicio.destroy()

        """CREAMOS LOS BOTONES"""
        ttk.Button(contenedor, text='Aceptar',command=ValidarAcceso).grid(row=3, column=0,sticky=W+E)
        ttk.Button(contenedor, text='Cancelar',command=Salir).grid(row=3, column=1,sticky=W+E)


#//////////////////////
#CLASE CONTROL DE IMC
#/////////////////////

class Control:
    '''
    Clase control.
    Atributos
    ----------
        peso : str
            peso del usuario
        altura: str
            altura del Usuario
        edad: str
            edad del Usuario
    
    Metodo
    ----------
        def __init__(self, peso, estatura, edad):
            Constructor de la clase
            
        def calculosIMC(self):
            En este apartado se realizan los calculos del IMC para determinar en que estado de
            peso se encuentr
        
        def ObtenerVista(self):
            METODO PARA CONSULTAR LA COLECCION COMPLETA

        def guardar():
            guarda los datos en la base de datos

        def eliminar():
            elimina datis de la base de datos

        def editar():
            edita datos dentro de la base de datos

        def actualizar():
            actualiza la base de datos con los que habian sido editados
            
        def validar()
            exige al usuario llenar todos los campos para el registro
            
        def limpiar():
            limpia las cajas de texto.

        def calculoIMC():
            determina la etapa exacta de la masa corporal del usuario, partiendo por su IMC
    '''

    def __init__(self, peso, estatura, edad,estado,actividad):
        '''
        Construye todos los atributos necesarios para el Usuario.
        Parametros
        ----------
            peso: float
                peso del usuario
            estatura: float
                estatura del usuario
            edad: int
                edad del usuario
        '''
        self.peso=peso
        self.estatura=estatura
        self.edad=edad
        self.estado=estado
        self.actividad=actividad
    
    def CalculosIMC(self, ventana):
        """
        Permite que el usuario ingrese sus datos como peso, altura, edad
        para gnerar el imc.
        Parametros
        ----------
            ventana: str
                permite crear las interfaces
        """
        self.window=ventana
        self.window.title('Control de Indice de Masa Corporal')
        self.window.geometry("1200x650")

  
        """CREAMOS UN CONTENEDOR PARA LAS CAJAS DE TEXTO Y BOTONES"""
        contenedor=LabelFrame(self.window, text='Datos Requeridos')
        contenedor.grid(row=0, column=0, columnspan=2,pady=5)

        """CREAR ETIQUETAS CON SUS CAJAS DE TEXTO """
        Label(contenedor,text='Peso [kg]:', bg="light blue").grid(row=1, column=0,sticky=W+E)
        self.peso=Entry(contenedor)
        self.peso.grid(row=1,column=1,sticky=W+E)

        Label(contenedor,text='Estatura [m]:', bg="light blue").grid(row=2, column=0,sticky=W+E)
        self.estatura=Entry(contenedor)
        self.estatura.grid(row=2,column=1,sticky=W+E)

        Label(contenedor,text='Edad:', bg="light blue").grid(row=3, column=0,sticky=W+E)
        self.edad=Entry(contenedor)
        self.edad.grid(row=3,column=1,sticky=W+E)

        Label(contenedor,text='Fecha:', bg="light blue").grid(row=4, column=0,sticky=W+E)
        self.fecha=Entry(contenedor)
        self.fecha.grid(row=4, column=1)
        self.fecha.insert(0,str(date.today()))


        Label(contenedor,text='IMC:', bg="light green").grid(row=5, column=0,sticky=W+E)
        self.imc=Entry(contenedor)
        self.imc.grid(row=5, column=1,sticky=W+E)
        
        Label(contenedor,text='Estado:', bg="light green").grid(row=6, column=0,sticky=W+E)
        self.estado=Entry(contenedor)
        self.estado.grid(row=6, column=1,sticky=W+E)

        """CREAMOS EL CONTENEDOR PARA EL LISTVIEW"""
        contenedorLv=LabelFrame(self.window, text='')
        contenedorLv.grid(row=14, column=0, columnspan=2,pady=5)

        """CREAMOS UNA VISTA DE DATOS"""
        columnas = ('#1', '#2', '#3', '#4', '#5','#6','#7')
        self.vista=ttk.Treeview(contenedorLv,height=17,columns=columnas)
        self.vista.grid(row=9,column=0, columnspan=10,padx=5)
        self.vista.column('#0',width=200)
        self.vista.column('#1',width=100)
        self.vista.column('#2',width=100)
        self.vista.column('#3',width=100)
        self.vista.column('#4',width=100)
        self.vista.column('#5',width=100)
        self.vista.column('#6',width=280)
        self.vista.heading('#0',text='Id',anchor=CENTER)
        self.vista.heading('#1',text='Fecha',anchor=CENTER)
        self.vista.heading('#2',text='Peso [Kg]',anchor=CENTER)
        self.vista.heading('#3',text='Estatura [m]',anchor=CENTER)
        self.vista.heading('#4',text='Edad',anchor=CENTER)
        self.vista.heading('#5',text='IMC',anchor=CENTER)
        self.vista.heading('#6',text='Estado',anchor=CENTER)

        """LLENAMOS DE DATOS LA VISTA"""
        self.ObtenerVista()

        def Salir():
            """Destruye la interfaz creada"""
            ventana.destroy()
        
        def Imprimir():
            try:
                pdf=PDF(orientation='P',unit='mm',format='A4')
                pdf.add_page()
                pdf.logo('logo.png', 0, 0, 60, 15)
                pdf.textos('texto.txt')
                pdf.title("Informe de cálculo calorico")
                pdf.set_author('Jhonson Mendoza')
                pdf.output('informe.pdf','F')
            except Exception as e:
                e=sys.exc_info()[1]
                messagebox.showerror('Error',e.args[0]) 
           
        
        """CREAMOS LOS BOTONES QUE VAMOS A DEJAR ACTIVOS EN LA EDICION"""
        ttk.Button(contenedor, text='Guardar',command=self.Guardar).grid(row=10, column=0,sticky=W+E)
        ttk.Button(contenedor, text='Eliminar',command=self.Eliminar).grid(row=10, column=1,sticky=W+E)
        ttk.Button(contenedor, text='Editar',command=self.Editar).grid(row=11, column=0,sticky=W+E)
        Button(contenedor, text='IMC', bg="light green", command=self.calculoIMC).grid(row=11, column=1,sticky=W+E)
        ttk.Button(contenedor, text='Actualizar',command=self.Actualizar).grid(row=12, column=0,sticky=W+E) 
        ttk.Button(contenedor, text='Salir',command=Salir).grid(row=12, column=1,sticky=W+E)  
        Button(contenedorLv,text='Calculo Calorico',command=Imprimir,bg = "light blue").grid(row=13, column=4,sticky=W+E,padx=10,pady=10,columnspan=2) 
        Label (contenedorLv, text="Nivel de Actividad",bg = "light blue").grid(row=13, column=1,padx=10,pady=10,columnspan=2)
        actividad = Entry (contenedorLv)
        actividad=StringVar(contenedorLv)
        nivelAct=["Poco o Ningun ejercicio","Ejercicio ligero", "Ejercicio Moderado", "Ejercicio Fuerte", "Ejercicio muy Fuerte"]
        nivelAct=OptionMenu(contenedorLv,actividad,*nivelAct)
        nivelAct.grid(row=13, column=2,padx=10,pady=10,columnspan=2)

    def ObtenerVista(self):
        """
        METODO PARA CONSULTAR LA COLECCION COMPLETA
        """
        #Limpiando la vista
        registros=self.vista.get_children()
        for elemento in registros:
            self.vista.delete(elemento)

        """Consultando los datos"""
        self.adapatadorCon=Dao.DaoCon(fecha=self.fecha.get(),peso=self.peso.get(),estatura=self.estatura.get(),edad=self.edad.get(),imc=self.imc.get(),estado=self.estado.get())
        resultados=self.adapatadorCon.consultarTodosCon()
        """llenando los datos"""
        for Fila in resultados:
           self.vista.insert('', 0, text= Fila["_id"],
            values = (Fila["fecha"],Fila["peso"],Fila["estatura"],Fila["edad"],Fila["imc"],Fila['estado']))

    def Guardar(self):
        """
        METODO PARA GUARDAR UN REGISTRO
        """
        #REALIZAMOS EL GUARDADO DEL REGISTRO SI ES QUE NO HAY ERRORES
        try:
            if self.validar():
                """INSTANCIAMOS EL OBJETO DE DATOS USUARIO"""
                self.adapatadorCon=Dao.DaoCon(fecha=self.fecha.get(),peso=self.peso.get(),estatura=self.estatura.get(),edad=self.edad.get(),imc=self.imc.get(),estado=self.estado.get())
                self.adapatadorCon.insertarControl()
                self.ObtenerVista()
                self.limpiarCajas()
            else:
                messagebox.showwarning("Error de validación","Ingrese información requerida, hay campos sin llenar.")
        except Exception:
                e=sys.exc_info()[1]
                messagebox.showerror('Error',e.args[0])

    def Eliminar(self):
        """
        METODO PARA ELIMINAR UN REGISTRO
        """

        #REALIZAMOS LA ELIMINACION DEL REGISTRO SI ES QUE NO HAY ERRORES
        try:
            """CAPTURAMOS EL ID DEL REGISTRO SELECCIONADO EN LA VISTA(LISTVIEW)"""
            self.vista.item(self.vista.selection())['text'][0]
        except IndexError as e:
            messagebox.showerror("Error","Seleccione un registro para eliminar.")
            return
        idUsu=self.vista.item(self.vista.selection())['text']
        self.adapatadorCon.eliminarControl(idUsu)
        self.ObtenerVista()

    def Actualizar(self):  
        """
        METODO PARA ACTUZALIZAR UN REGISTRO
        """
        try:
            if self.validar():
                #CAPTURAMOS EL ID DEL REGISTRO SELECCIONADO EN LA VISTA(LISTVIEW)
                idCon=str(self.vista.item(self.vista.selection())['text'])
                self.adapatadorCon=Dao.DaoCon(fecha=self.fecha.get(),peso=self.peso.get(),estatura=self.estatura.get(),edad=self.edad.get(),imc=self.imc.get(),estado=self.estado.get())
                self.adapatadorCon.actualizarControl(idCon)
                self.ObtenerVista()
                self.limpiarCajas()
            else:
                messagebox.showwarning("Error de validación","Ingrese información requerida, hay campos sin llenar.")
        except Exception as e:
            e=sys.exc_info()[1]
            messagebox.showerror('Error',e.args[0])      

    def Editar(self):
    
        """VERIFICAMOS QUE SE HAYA SELECCIONADO EL REGISTRO A EDITAR"""
        try:
            """CAPTURAMOS EL ID DEL REGISTRO SELECCIONADO EN LA VISTA(LISTVIEW)"""
            self.vista.item(self.vista.selection())['text'][0]
        except IndexError as e:
            messagebox.showerror("Error","Seleccione un registro para editar.")
            return
            
        """CAPTURAMOS EL ID DEL REGISTRO SELECCIONADO EN LA VISTA(LISTVIEW)"""
        id=str(self.vista.item(self.vista.selection())['text'])
        res=self.adapatadorCon.consultarUnoCon(id)

        """SE LIMPIAN LOS CUADRO DE TEXTO PRIMERO"""
        self.limpiarCajas()

        self.fecha.insert(0,str(res['fecha']))
        self.peso.insert(0,str(res['peso']))
        self.estatura.insert(0,str(res['estatura']))
        self.edad.insert(0,str(res['edad']))
        self.imc.insert(0,str(res['imc']))
        self.estado.insert(0,str(res['estado']))
        
    def validar(self):
        """
        VALIDACION DE LOS DATOS
        """
        return len(self.fecha.get())!=0 and len(self.peso.get())!=0 and len(self.estatura.get())!=0 and len(self.edad.get())!=0 

    def limpiarCajas(self):
        """
        Limpia las cajas de texto
        """
        self.fecha.delete(0,END)
        self.peso.delete(0,END)
        self.estatura.delete(0,END)
        self.edad.delete(0,END)    
        self.imc.delete(0,END)   
        self.estado.delete(0,END)
           

    def calculoIMC(self):
        """
        METODO QUE CALCULA EL IMC Y EN QUE ESTADO DE PESO SE ENCUENTRA
        """
        if self.validar():
            x=float(self.estatura.get())
            y=float(self.peso.get())
            imc1=float(y/(x**2))
                
            imcR=round(imc1,2)
            self.imc.delete(0,END)
            self.imc.insert(0,str(round(imcR,2)))
            self.estado.delete(0,END)
            imcR=float(self.imc.get())
                
            """ESTABLECEMOS EN QUE RANGO DE LA TABLA IMC ESTA EL USUARIO"""
            if float(imcR)<float(18.5):
                self.estado.insert(0,"Peso Bajo")
            elif 24.9 > float(imcR) > 18.5:
                self.estado.insert(0,"Peso Normal")
            elif float(imcR)>24.9:
                self.estado.insert(0,"Sobrepeso")
            elif 29.9 > float(imcR) < 25:
                self.estado.insert(0,"Preobesidad")
            elif float(imcR)>29.9:
                self.estado.insert(0,"Obesidad")
            else:
                messagebox.showwarning("Error", "CASILLAS VACIAS." )
        


    