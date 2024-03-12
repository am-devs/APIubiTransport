import psycopg2
import json
from datetime import datetime
from models.driver import Ubication, StatusVehicle

class NevadaConnect:

    def __init__(self):
        self.connection = None
        self.cursor = None
        

    def connect(self):
        host = "VMNevada"
        port = 5434
        database ='transporte'
        username ='admin'
        password = "14nc4r1n4*"

        conn_string = f"dbname={database} user={username} password={password} host={host} port={port}"

        try:
            # Establece la conexión
            self.connection = psycopg2.connect(conn_string)

            # Crea un cursor
            self.cursor = self.connection.cursor()

        except psycopg2.Error as e:
            print("Error al conectar a PostgreSQL:", e)

    def post_ubi(self, ubi: Ubication):
        try:
            # Ejecuta la consulta de prueba
            fecha = datetime.now()
            formato_fecha = fecha.strftime("%d-%m-%Y, %H:%M:%S")
            consulta = "INSERT INTO ubication (cod_socio, nombre_socio, placa, latitud, longitud, fecha) VALUES (%s, %s, %s, %s, %s, %s)"
            self.cursor.execute(consulta, (ubi.cod_socio, ubi.nombre_socio, ubi.placa, ubi.latitud, ubi.longitud, formato_fecha))
            self.connection.commit()
            consulta = "SELECT * FROM last_ubication lb WHERE lb.placa=%s;"
            self.cursor.execute(consulta, (ubi.placa,))
            self.connection.commit()
            result = self.cursor.fetchone()
            if result is not None:
                consulta = "UPDATE last_ubication SET cod_socio= %s ,nombre_socio= %s, latitud = %s, longitud = %s, fecha=%s WHERE last_ubication.placa = %s"
                self.cursor.execute(consulta, (ubi.cod_socio, ubi.nombre_socio ,ubi.latitud, ubi.longitud, formato_fecha, ubi.placa,))
                self.connection.commit()
                return 1
            else:
                consulta = "INSERT INTO last_ubication (cod_socio, nombre_socio, placa, latitud, longitud, fecha) VALUES (%s, %s, %s, %s, %s, %s)"
                self.cursor.execute(consulta, (ubi.cod_socio, ubi.nombre_socio, ubi.placa, ubi.latitud, ubi.longitud, formato_fecha))
                self.connection.commit()
                return 2    
        except psycopg2.Error as e:
           print("Error al ejecutar la consulta:", e)
           return e
        
    def getLocations(self):
        try:
            consulta = "select cod_socio, placa, latitud, longitud from ubication"
            self.cursor.execute(consulta)
            self.connection.commit()
            result = self.cursor.fetchall()
            response = []
            if result is not None:
                for resultado in result:
                    ubication = Ubication(
                        cod_socio=resultado[0],
                        placa=resultado[1],
                        latitud=str(resultado[2]),
                        longitud=str(resultado[3])
                    )
                    response.append(ubication)

                return response
            else:
                return None
        except psycopg2.Error as e:
           print("Error al ejecutar la consulta:", e)
           return e
        
    def getLastLocations(self):
        try:
            consulta = "select cod_socio, nombre_socio, placa, latitud, longitud from last_ubication"
            consulta = "SELECT la.cod_socio, la.nombre_socio, la.placa, la.latitud, la.longitud FROM last_ubication AS la WHERE TO_TIMESTAMP(la.fecha, 'DD-MM-YYYY') = CURRENT_DATE"
            self.cursor.execute(consulta,)
            self.connection.commit()
            result = self.cursor.fetchall()   
            response = []  
            if result is not None:       
                for resultado in result:
                    ubication = Ubication(
                        cod_socio=resultado[0],
                        nombre_socio=resultado[1],
                        placa=resultado[2],
                        latitud=str(resultado[3]),
                        longitud=str(resultado[4])
                    )
                    response.append(ubication)

                return response
            else:
                return None
            
        except psycopg2.Error as e:
           print("Error al ejecutar la consulta:", e)
           return e


    def getLocationSpecific(self, placa:str):
        try:
            consulta = "select cod_socio, placa, latitud, longitud from last_ubication where last_ubication.placa = %s"
            self.cursor.execute(consulta, (placa,))
            self.connection.commit()
            result = self.cursor.fetchone()     
            if result is not None:       
                for resultado in result:
                    ubication = Ubication(
                        cod_socio=resultado[0],
                        placa=resultado[1],
                        latitud=str(resultado[2]),
                        longitud=str(resultado[3])
                    )
                    return ubication
            else:
                return None
            
        except psycopg2.Error as e:
           print("Error al ejecutar la consulta:", e)
           return e
    
    def getAllTickets(self):
         try:
            consulta = "select placa, parada, ticket_entrada,  fecha_ticket, orde_carga, tipo_de_viaje, estatusvehicle, status_parada from ticket_stop"
            self.cursor.execute(consulta,)
            result = self.cursor.fetchall() 
            print('TESTTT CONSULTAAA')
            print(result)
            response = []  
            if result is not None:
                for res in result:
                  
                  status_vehicle = StatusVehicle(
                    placa=res[0],
                    parada=res[1],
                    ticket_entrada=res[2],
                    fecha_ticket=res[3],
                    orden_carga=res[4],
                    tipo_viaje=res[5],
                    estatus_vehicle=res[6],
                    status_parada=res[7]
                    )
                  response.append(status_vehicle)
                
                return response
            else:
                return None

         except psycopg2.Error as e:
           print("Error al ejecutar la consulta:", e)
           return e

    def getTicket(self, ticket:str):
        try:
            consulta = "select placa, parada, ticket_entrada,  fecha_ticket, orde_carga, tipo_de_viaje, estatusvehicle, status_parada from ticket_stop where ticket_stop.ticket_entrada = %s"
            self.cursor.execute(consulta, (ticket,))
            result = self.cursor.fetchone() 
            print('TESTTT CONSULTAAA')
            print(result)
            if result is not None:
                return StatusVehicle(
                    placa=result[0],
                    parada=result[1],
                    ticket_entrada=result[2],
                    fecha_ticket=result[3],
                    orden_carga=result[4],
                    tipo_viaje=result[5],
                    estatus_vehicle=result[6],
                    status_parada=result[7]
                    )
            else:
                return None

        except psycopg2.Error as e:
           print("Error al ejecutar la consulta:", e)
           return e
        
    def insertTicket(self, status_vehicle:StatusVehicle, parada: str):
        try:
            consulta = "INSERT INTO ticket_stop (placa, parada, ticket_entrada, fecha_ticket, orde_carga, tipo_de_viaje, estatusvehicle, status_parada) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            self.cursor.execute(consulta, (status_vehicle.placa, status_vehicle.parada,
                                           status_vehicle.ticket_entrada, status_vehicle.fecha_ticket, status_vehicle.orden_carga,
                                           status_vehicle.tipo_viaje, status_vehicle.estatus_vehicle, parada))
            self.connection.commit()
        except psycopg2.Error as e:
           print("Error al ejecutar la consulta:", e)
           return e
    
    def completeTicket(self, status_vehicle:StatusVehicle):
        try:        
            consulta = "UPDATE ticket_stop SET status_parada='completado' where ticket_stop.ticket_entrada = %s"
            self.cursor.execute(consulta, (status_vehicle.ticket_entrada,))
            self.connection.commit()

        except psycopg2.Error as e:
           print("Error al ejecutar la consulta:", e)
           return e
        
    def stopvigilance(self, status_vehicle: StatusVehicle):
        try:       
            print(status_vehicle.ticket_entrada)
            consulta = "UPDATE ticket_stop SET status_parada='vigilancia' where ticket_stop.ticket_entrada = %s"
            self.cursor.execute(consulta, (status_vehicle.ticket_entrada,))
            self.connection.commit()

        except psycopg2.Error as e:
           print("Error al ejecutar la consulta:", e)
           return e
    
    def stopromana(self, status_vehicle: StatusVehicle):
        try:       
            print(status_vehicle.ticket_entrada)
            consulta = "UPDATE ticket_stop SET status_parada='romana' where ticket_stop.ticket_entrada = %s"
            self.cursor.execute(consulta, (status_vehicle.ticket_entrada,))
            self.connection.commit()

        except psycopg2.Error as e:
           print("Error al ejecutar la consulta:", e)
           return e
    
    def stoptransport(self, status_vehicle: StatusVehicle):
        try:       
            print(status_vehicle.ticket_entrada)
            consulta = "UPDATE ticket_stop SET status_parada='taller' where ticket_stop.ticket_entrada = %s"
            self.cursor.execute(consulta, (status_vehicle.ticket_entrada,))
            self.connection.commit()

        except psycopg2.Error as e:
           print("Error al ejecutar la consulta:", e)
           return e
    
    def stop1(self, status_vehicle: StatusVehicle):
        try:       
            print(status_vehicle.ticket_entrada)
            consulta = "UPDATE ticket_stop SET status_parada='p1' where ticket_stop.ticket_entrada = %s"
            self.cursor.execute(consulta, (status_vehicle.ticket_entrada,))
            self.connection.commit()

        except psycopg2.Error as e:
           print("Error al ejecutar la consulta:", e)
           return e
    
    def stop2(self, status_vehicle: StatusVehicle):
        try:       
            print(status_vehicle.ticket_entrada)
            consulta = "UPDATE ticket_stop SET status_parada='p2' where ticket_stop.ticket_entrada = %s"
            self.cursor.execute(consulta, (status_vehicle.ticket_entrada,))
            self.connection.commit()

        except psycopg2.Error as e:
           print("Error al ejecutar la consulta:", e)
           return e
        
    def stop3(self, status_vehicle: StatusVehicle):
        try:       
            print(status_vehicle.ticket_entrada)
            consulta = "UPDATE ticket_stop SET status_parada='p3' where ticket_stop.ticket_entrada = %s"
            self.cursor.execute(consulta, (status_vehicle.ticket_entrada,))
            self.connection.commit()

        except psycopg2.Error as e:
           print("Error al ejecutar la consulta:", e)
           return e
    
    def stop4(self, status_vehicle: StatusVehicle):
        try:       
            print(status_vehicle.ticket_entrada)
            consulta = "UPDATE ticket_stop SET status_parada='p4' where ticket_stop.ticket_entrada = %s"
            self.cursor.execute(consulta, (status_vehicle.ticket_entrada,))
            self.connection.commit()

        except psycopg2.Error as e:
           print("Error al ejecutar la consulta:", e)
           return e
    def stop5(self, status_vehicle: StatusVehicle):
        try:       
            print(status_vehicle.ticket_entrada)
            consulta = "UPDATE ticket_stop SET status_parada='p5' where ticket_stop.ticket_entrada = %s"
            self.cursor.execute(consulta, (status_vehicle.ticket_entrada,))
            self.connection.commit()

        except psycopg2.Error as e:
           print("Error al ejecutar la consulta:", e)
           return e
        
    def closeConnection(self):
        # Cierra el cursor y la conexión
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

