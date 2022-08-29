""" 
Importamos las librerias necesarias
para el programa
"""
from pymongo import MongoClient
from bson.objectid import ObjectId
import sys
from tkinter import YES, messagebox

#///////////////////////////////////////
#CLASE PARA ACCEDER A LA BASE DE DATOS
#/////////////////////////////////////////

class ConexionBd:
    """
    Clase ConexionBd
    Atributos
    ---------
        bdNombre : str
            nombre de la base de datos
        Url : str
            Direccion de la base de datos
        coleccion : str
            Nombre de la coleccion
    Metodos
    ---------
        def __init__(self,bdNombre,Url,coleccion):
            metodo constructor de la clase
        def ConectarBd(self):
            Conecta la base de datos creando una instancia del objeto
    """
    def __init__(self,bdNombre,Url,coleccion):
        """
        Metodo constructor de la clase
        Parametros
        -----------
            bdNombre : str
                nombre de la base de datos
            Url : str
                Direccion de la base de datos
            coleccion : str
                Nombre de la coleccion
        """
        self.bdNombre=bdNombre
        self.Url=Url
        self.coleccion=coleccion

    def ConectarBd(self):
        """
        REALIZA LA CONEXION DE LA BD CREANDO LA INSTANCIA DEL OBJETO
        """
        cliente=MongoClient(self.Url)
        baseDatos=cliente[self.bdNombre]        
        cnn=baseDatos[self.coleccion]
        return cnn

             
"""ESTABLECEMOS EL OBJETO CONEXION DE MANERA GLOBAL PARA LA CLASE USUARIOS"""
Cn=ConexionBd(bdNombre='IMC',Url='mongodb://localhost',coleccion='Usuarios')

class DaoUsu:
    """
    Clase DaoUsu
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
            
        def insertarUsuario(self):
            guarda los datos en la base de datos

        def actualizarUsuario(self,id):
            Actualiza los datos en la base de datos

        def eliminarUsuario(self,id):():
            elimina los datos dentro de la base de datos

        def consultarTodosUsu():
            consulta si los datos se encuentran en la base de datos

        def consultarUnoUsu(self):
            consulta si un registro se encuentra en la base de datos
    """
    
    def __init__(self,nombres,apellidos,sexo,edad,usuario,clave):
        """
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
        """
        self.nombres=nombres
        self.apellidos=apellidos
        self.sexo=sexo
        self.edad=edad
        self.usuario=usuario
        self.clave=clave
        

    def insertarUsuario(self):
        """
        guarda los datos en la base de datos
        """
        try:
            Cn.ConectarBd().insert_one({'nombres':self.nombres,'apellidos':self.apellidos,'sexo':self.sexo,'edad':self.edad,'usuario':self.usuario,'clave':self.clave})
            messagebox.showinfo('Guardando','Se guardó correctamente el registro actual.')
        except Exception:
            e=sys.exc_info()[1]
            messagebox.showerror('Error',e.args[0]) 

    def actualizarUsuario(self,id):
        """
        Actualiza los datos en la base de datos
        """
        try:
            self.id=id
            idBuscar={"_id":ObjectId(self.id)}
            nuevosValores= {"$set":{'nombres':self.nombres,'apellidos':self.apellidos,'sexo':self.sexo,'edad':self.edad,'usuario':self.usuario,'clave':self.clave}}
            #PASAMOS EL DATO QUE SE ENCUENTRA EN LAS CAJAS DE TEXTO COMO PARAMETRO DE CADA ELEMENTO DE LA COLECCIO
            Cn.ConectarBd().update_one(idBuscar,nuevosValores)
            messagebox.showinfo('Actualizando','Se actualizo correctamente el registro actual.')
        except Exception:
            e=sys.exc_info()[1]
            messagebox.showerror('Error',e.args[0])

    def eliminarUsuario(self,id):
        """
        elimina los datos dentro de la base de datos
        """
        try:
            if messagebox.askyesno("Confirmación","¿Esta seguro de eliminar el registro seleccionado?")==YES:
                #SE ELIMINA EL REGISTRO SELECCIONADO
                self.id=str(id)
                idBuscar={"_id":ObjectId(self.id)}
                Cn.ConectarBd().delete_one(idBuscar)
                messagebox.showinfo('Eliminando','Se eliminó correctamente el registro actual.')
            else:
                messagebox.showinfo("Registros no afectados","No se eliminó ningún registro por que no se confirmó.")
        except Exception:
            e=sys.exc_info()[1]
            messagebox.showerror('Error',e.args[0])

    def consultarTodosUsu(self):
        """
        consulta si los datos se encuentran en la base de datos
        """
        try:
            #Consultando los datos
            resultados=Cn.ConectarBd().find()
            return resultados
        except Exception:
            e=sys.exc_info()[1]
            messagebox.showerror('Error',e.args[0])
        
        
    def consultarUnoUsu(self,id):
        """
        consulta si un registro se encuentra en la base de datos
        """
        try:
            self.id=str(id)
            idBuscar={"_id":ObjectId(self.id)}
            #Consultando los datos
            resultados=Cn.ConectarBd().find_one(idBuscar)
            return resultados
        except Exception:
            e=sys.exc_info()[1]
            messagebox.showerror('Error',e.args[0])


"""ESTABLECEMOS EL OBJETO CONEXION DE MANERA GLOBAL PARA LA CLASE CONTROL"""
Cn2=ConexionBd(bdNombre='IMC',Url='mongodb://localhost',coleccion='Control')

class DaoCon:
    """
    Clase DaoCon
    Atributos
    ----------
        edad: str
            edad del usuario
        estatura: str
            estatura del Usuario
        peso: int
            peso del Usuario
        fecha: str
            fecha del registro
        imc: str
            imc del Usuario
        estado : str
            estado del usuario respecto a su peso
    
    Metodos
    ----------
        def __init__(self, edad,estatura,peso,fecha,imc,estado):
            Constructor de la clase
            
        def insertarControl(self):
            guarda los datos en la coleccion Controles

        def actualizarControl(self,id):
            Actualiza los datos en la coleccion Controles

        def eliminarControl(self,id):():
            elimina los datos dentro de la coleccion Controles

        def consultarTodosCon():
            consulta si los datos se encuentran en la coleccion Controles

        def consultarUnoCon(self):
            consulta si un registro se encuentra en la coleccion Controles
            
        def calcularIMC(estatura,peso):
            METODO QUE CALCULA EL IMC Y EN QUE ESTADO DE PESO SE ENCUENTRA
    """
    def __init__(self,edad,estatura,peso,fecha,imc,estado):
        self.edad=edad
        self.estatura=estatura
        self.peso=peso
        self.fecha=fecha
        self.imc=imc
        self.estado=estado

    def insertarControl(self):
        """
        guarda los datos en la coleccion Controles
        """
        try:
            Cn2.ConectarBd().insert_one({'edad':self.edad,'estatura':self.estatura,'peso':self.peso,'fecha':self.fecha,'imc':self.imc,'estado':self.estado})
            messagebox.showinfo('Guardando','Se guardó correctamente el registro actual.')
        except Exception:
            e=sys.exc_info()[1]
            messagebox.showerror('Error',e.args[0]) 

    def actualizarControl(self,id):
        """
        Actualiza los datos en la coleccion Controles
        """
        try:
            self.id=id
            idBuscar={"_id":ObjectId(self.id)}
            nuevosValores= {"$set": {'edad':self.edad,'estatura':self.estatura,'peso':self.peso,'fecha':self.fecha,'imc':self.imc,'estado':self.estado}}
            #PASAMOS EL DATO QUE SE ENCUENTRA EN LAS CAJAS DE TEXTO COMO PARAMETRO DE CADA ELEMENTO DE LA COLECCIO
            Cn2.ConectarBd().update_one(idBuscar,nuevosValores)
            messagebox.showinfo('Actualizando','Se actualizo correctamente el registro actual.')
        except Exception:
            e=sys.exc_info()[1]
            messagebox.showerror('Error',e.args[0])
    
    def eliminarControl(self,id):
        """
        elimina los datos dentro de la coleccion Controles
        """
        try:
            if messagebox.askyesno("Confirmación","¿Esta seguro de eliminar el registro seleccionado?")==YES:
                #SE ELIMINA EL REGISTRO SELECCIONADO
                self.id=str(id)
                idBuscar={"_id":ObjectId(self.id)}
                Cn2.ConectarBd().delete_one(idBuscar)
                messagebox.showinfo('Eliminando','Se eliminó correctamente el registro actual.')
            else:
                messagebox.showinfo("Registros no afectados","No se eliminó ningún registro por que no se confirmó.")
        except Exception:
            e=sys.exc_info()[1]
            messagebox.showerror('Error',e.args[0])

    def consultarTodosCon(self):
        """
        consulta si los datos se encuentran en la coleccion Controles
        """
        try:
            #Consultando los datos
            resultados=Cn2.ConectarBd().find({})
            return resultados
        except Exception:
            e=sys.exc_info()[1]
            messagebox.showerror('Error',e.args[0])
        
        
    def consultarUnoCon(self,id):
        """
        consulta si un registro se encuentra en la coleccion Controles
        """
        try:
            self.id=id
            idBuscar={"_id":ObjectId(self.id)}
            #Consultando los datos
            resultados=Cn2.ConectarBd().find_one(idBuscar)
            return resultados
        except Exception:
            e=sys.exc_info()[1]
            messagebox.showerror('Error',e.args[0])

    def calcularIMC(estatura,peso):
        """METODO QUE CALCULA EL IMC Y EN QUE ESTADO DE PESO SE ENCUENTRA"""
        x=float(estatura)
        y=float(peso)
        imc1=float(y/(x**2))
                
        imcR=round(imc1,2)

                
        """ESTABLECEMOS EN QUE RANGO DE LA TABLA IMC ESTA EL USUARIO"""
        if float(imcR)<float(18.5):
            return "Peso Bajo"
        elif 24.9 > float(imcR) > 18.5:
            return "Peso Normal"
        elif float(imcR)>24.9:
            return "Sobrepeso"
        elif 29.9 > float(imcR) < 25:
            return "Preobesidad"
        elif float(imcR)>29.9:
            return "Obesidad"
        else:
            messagebox.showwarning("Error", "CASILLAS VACIAS." )

    
    
