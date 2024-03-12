from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from typing import Text, Optional
from datetime import datetime

class User(BaseModel):
    username: str
    code: str | None = None
    password: str | None = None
    admin: bool | None = None
    plate_vehicle: str | None = None
    
class Vehicle(BaseModel):
     plate: str

class Ubication(BaseModel):
    cod_socio: str
    nombre_socio: str | None = None
    parada: str | None = None
    ticket_entrada: str | None = None
    fecha_ticket: str | None = None
    orden_carga:  str | None = None
    tipo_viaje:  str | None = None
    estatus_vehicle: str | None = None
    placa: str 
    latitud:str
    longitud: str

class StatusVehicle(BaseModel):
    placa: str | None = None
    parada: str | None = None
    ticket_entrada: str | None = None
    fecha_ticket: str | None = None
    orden_carga:  str | None = None
    tipo_viaje:  str | None = None
    estatus_vehicle: str | None = None
    status_parada: str | None = None
