from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from models.driver import Ubication, StatusVehicle
from .logins import get_current_user
from models.tokenModels import User
from services.nevada import NevadaConnect
from services.adempiere import AdempiereConnect

router = APIRouter()

#ruta que ingresa la ubicacion de los choferes en BD Nevada
@router.post('/ubicacion')
def save_ubi(current_user: Annotated[User, Depends(get_current_user)], ubicacion: Ubication):
    #codigo que insertara en la base de datos nevada las ubicaciones de los choferes
    try:
        conn_nevada = NevadaConnect()
        conn_nevada.connect()
        result  = conn_nevada.post_ubi(ubicacion)
        if result == 1:
            return {'detail':'Se Insertaron y Actualizaron los datos Correctamente'}
        if result == 2:
            return {'detail':'Se Insertaron los datos Correctamente'}
        else:
            return HTTPException(status_code=404, detail="Error al insertar datos") 
    finally:
        conn_nevada.closeConnection()

#ruta que obtiene las ubicaciones de todos los choferes en el dia de hoy, vehiculos, en transito y no disponibles
@router.get('/locations')
def get_locations(current_user: Annotated[User, Depends(get_current_user)]):
     try:
        conn_nevada = NevadaConnect()
        conn_nevada.connect()
        ubications  = conn_nevada.getLastLocations()
        if ubications is None:
            return HTTPException(status_code=404, detail="Error al realizar consulta")  
        if ubications:
            try:
                conn_adempiere = AdempiereConnect()
                conn_adempiere.connect()
                
                for ubi in ubications:
                    status_vehicle = conn_adempiere.statusVehicle(ubi.placa)
                    if status_vehicle is None:
                        ubi.parada = 'No posee'
                        ubi.ticket_entrada = 'No posee'
                        ubi.ticket_entrada ='No posee'
                        ubi.fecha_ticket ='No posee'
                        ubi.orden_carga = 'No posee'
                        ubi.tipo_viaje = 'No posee'
                        ubi.estatus_vehicle ='No posee'

                    if  status_vehicle is not None:
                        ubi.parada = status_vehicle.parada
                        ubi.ticket_entrada = status_vehicle.ticket_entrada
                        ubi.fecha_ticket = status_vehicle.fecha_ticket
                        ubi.orden_carga = status_vehicle.orden_carga
                        ubi.tipo_viaje = status_vehicle.tipo_viaje
                        ubi.estatus_vehicle = status_vehicle.estatus_vehicle
                    print(ubi) 
                return ubications

            finally:
                conn_adempiere.closeConnection
               
     finally:
        conn_nevada.closeConnection()

@router.get('/location/specific/{placa}')
def get_locations(current_user: Annotated[User, Depends(get_current_user)], placa: str):
     try:
        conn_nevada = NevadaConnect()
        conn_nevada.connect()
        ubication  = conn_nevada.getLocationSpecific(placa)
        if ubication is None:
            return HTTPException(status_code=404, detail="Error al realizar consulta")
        if ubication:
            return ubication
        else:
            return HTTPException(status_code=404, detail="No autorizado") 
     finally:
        conn_nevada.closeConnection()
