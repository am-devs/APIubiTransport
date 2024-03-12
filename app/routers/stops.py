from typing import Annotated
from models.tokenModels import User
from services.nevada import NevadaConnect
from services.adempiere import AdempiereConnect
from fastapi import APIRouter, Depends, HTTPException
from .logins import get_current_user

router = APIRouter()

@router.get('/location/stop/alltickets', tags=["Stops"],)
def get_Tickets(current_user: Annotated[User, Depends(get_current_user)]):
    try:
        conn_nevada = NevadaConnect()
        conn_nevada.connect()
        tickets_nevada = conn_nevada.getAllTickets()
        print(tickets_nevada)
        if tickets_nevada is None:
            return ({'Mensaje':'No hay datos guardados en la base de datos.'})
        
        if tickets_nevada is not None:
            
            return tickets_nevada
    finally:
        conn_nevada.closeConnection

@router.get('/location/stop/workshop/{ticket}', tags=["Stops"],)
def update_ticket(ticket: str):
    try:
        conn_adempiere = AdempiereConnect()
        conn_adempiere.connect()
        ticket_status = conn_adempiere.getTicket(ticket)

        if ticket_status is None:
            return HTTPException(status_code=404, detail="El ticket no existe en Adempiere")
        
        if ticket_status is not None:
            try:
                conn_nevada = NevadaConnect()
                conn_nevada.connect()
                ticket_nevada = conn_nevada.getTicket(ticket)
                print(ticket_nevada)
                if ticket_status.orden_carga == 'Sin Orden Carga':

                    if ticket_nevada is None:
                        
                        conn_nevada.insertTicket(ticket_status, 'taller')
                        return ({'Mensaje':'Ticket insertado y actualizado a vigilancia'})
                    
                    if ticket_nevada is not None:
                        conn_nevada.stoptransport(ticket_nevada)
                        return ({'Mensaje':'ticket actualizado a vigilancia'})
                else:
                    conn_nevada.completeTicket(ticket_nevada)
                    return ({'Mensaje':'Ticket Completado'})
                
            finally:
                conn_nevada.closeConnection


    finally:
        conn_adempiere.closeConnection

#Metodo para insertar ticket en tabla de tickets en nevada con parada en Vigilancia.
@router.get('/location/stop/updatevigilance/{ticket}', tags=["Stops"],)
def update_ticket(ticket: str):
    try:
        conn_adempiere = AdempiereConnect()
        conn_adempiere.connect()
        ticket_status = conn_adempiere.getTicket(ticket)

        if ticket_status is None:
            return HTTPException(status_code=404, detail="El ticket no existe en Adempiere")
        
        if ticket_status is not None:
            try:
                conn_nevada = NevadaConnect()
                conn_nevada.connect()
                ticket_nevada = conn_nevada.getTicket(ticket)
                print(ticket_nevada)
                if ticket_status.orden_carga == 'Sin Orden Carga':

                    if ticket_nevada is None:
                        
                        conn_nevada.insertTicket(ticket_status, 'vigilancia')
                        return ({'Mensaje':'Ticket insertado y actualizado a vigilancia'})
                    
                    if ticket_nevada is not None:
                        conn_nevada.stopvigilance(ticket_nevada)
                        return ({'Mensaje':'ticket actualizado a vigilancia'})
                else:
                    conn_nevada.completeTicket(ticket_nevada)
                    return ({'Mensaje':'Ticket Completado'})
                
            finally:
                conn_nevada.closeConnection


    finally:
        conn_adempiere.closeConnection

@router.get('/location/stop/updateromana/{ticket}', tags=["Stops"])
def update_ticket(ticket: str):
    try:
        conn_adempiere = AdempiereConnect()
        conn_adempiere.connect()
        ticket_status = conn_adempiere.getTicket(ticket)

        if ticket_status is None:
            return HTTPException(status_code=404, detail="El ticket no existe en Adempiere")
        
        if ticket_status is not None:
            try:
                conn_nevada = NevadaConnect()
                conn_nevada.connect()
                ticket_nevada = conn_nevada.getTicket(ticket)
                print(ticket_nevada)
                if ticket_status.orden_carga == 'Sin Orden Carga':

                    if ticket_nevada is None:
                        
                        conn_nevada.insertTicket(ticket_status, 'romana')
                        return ({'Mensaje':'Ticket insertado y actualizado a romana'})
                    
                    if ticket_nevada is not None:
                        conn_nevada.stopromana(ticket_nevada)
                        return ({'Mensaje':'ticket actualizado a romana'})
                else:
                    conn_nevada.completeTicket(ticket_nevada)
                    return ({'Mensaje':'Ticket Completado'})
                
            finally:
                conn_nevada.closeConnection


    finally:
        conn_adempiere.closeConnection

@router.get('/location/stop/updatep1/{ticket}', tags=["Stops"])
def update_ticket(ticket: str):
    try:
        conn_adempiere = AdempiereConnect()
        conn_adempiere.connect()
        ticket_status = conn_adempiere.getTicket(ticket)

        if ticket_status is None:
            return HTTPException(status_code=404, detail="El ticket no existe en Adempiere")
        
        if ticket_status is not None:
            try:
                conn_nevada = NevadaConnect()
                conn_nevada.connect()
                ticket_nevada = conn_nevada.getTicket(ticket)
                print(ticket_nevada)
                if ticket_status.orden_carga == 'Sin Orden Carga':

                    if ticket_nevada is None:
                        
                        conn_nevada.insertTicket(ticket_status, 'p1')
                        return ({'Mensaje':'Ticket insertado y actualizado a vigilancia'})
                    
                    if ticket_nevada is not None:
                        conn_nevada.stop1(ticket_nevada)
                        return ({'Mensaje':'ticket actualizado a parada 1'})
                else:
                    conn_nevada.completeTicket(ticket_nevada)
                    return ({'Mensaje':'Ticket Completado'})
                
            finally:
                conn_nevada.closeConnection


    finally:
        conn_adempiere.closeConnection



@router.get('/location/stop/updatep2/{ticket}', tags=["Stops"])
def update_ticket(ticket: str):
    try:
        conn_adempiere = AdempiereConnect()
        conn_adempiere.connect()
        ticket_status = conn_adempiere.getTicket(ticket)

        if ticket_status is None:
            return HTTPException(status_code=404, detail="El ticket no existe en Adempiere")
        
        if ticket_status is not None:
            try:
                conn_nevada = NevadaConnect()
                conn_nevada.connect()
                ticket_nevada = conn_nevada.getTicket(ticket)
                print(ticket_nevada)
                if ticket_status.orden_carga == 'Sin Orden Carga':

                    if ticket_nevada is None:
                        
                        conn_nevada.insertTicket(ticket_status, 'p2')
                        return ({'Mensaje':'Ticket insertado y actualizado a vigilancia'})
                    
                    if ticket_nevada is not None:
                        conn_nevada.stop2(ticket_nevada)
                        return ({'Mensaje':'ticket actualizado a parada 2'})
                else:
                    conn_nevada.completeTicket(ticket_nevada)
                    return ({'Mensaje':'Ticket Completado'})
                
            finally:
                conn_nevada.closeConnection


    finally:
        conn_adempiere.closeConnection


@router.get('/location/stop/updatep3/{ticket}', tags=["Stops"])
def update_ticket(ticket: str):
    try:
        conn_adempiere = AdempiereConnect()
        conn_adempiere.connect()
        ticket_status = conn_adempiere.getTicket(ticket)

        if ticket_status is None:
            return HTTPException(status_code=404, detail="El ticket no existe en Adempiere")
        
        if ticket_status is not None:
            try:
                conn_nevada = NevadaConnect()
                conn_nevada.connect()
                ticket_nevada = conn_nevada.getTicket(ticket)
                print(ticket_nevada)
                if ticket_status.orden_carga == 'Sin Orden Carga':

                    if ticket_nevada is None:
                        
                        conn_nevada.insertTicket(ticket_status, 'p3')
                        return ({'Mensaje':'Ticket insertado y actualizado a vigilancia'})
                    
                    if ticket_nevada is not None:
                        conn_nevada.stop3(ticket_nevada)
                        return ({'Mensaje':'ticket actualizado a parada 3'})
                else:
                    conn_nevada.completeTicket(ticket_nevada)
                    return ({'Mensaje':'Ticket Completado'})
                
            finally:
                conn_nevada.closeConnection


    finally:
        conn_adempiere.closeConnection

@router.get('/location/stop/updatep4/{ticket}', tags=["Stops"])
def update_ticket(ticket: str):
    try:
        conn_adempiere = AdempiereConnect()
        conn_adempiere.connect()
        ticket_status = conn_adempiere.getTicket(ticket)

        if ticket_status is None:
            return HTTPException(status_code=404, detail="El ticket no existe en Adempiere")
        
        if ticket_status is not None:
            try:
                conn_nevada = NevadaConnect()
                conn_nevada.connect()
                ticket_nevada = conn_nevada.getTicket(ticket)
                print(ticket_nevada)
                if ticket_status.orden_carga == 'Sin Orden Carga':

                    if ticket_nevada is None:
                        
                        conn_nevada.insertTicket(ticket_status, 'p4')
                        return ({'Mensaje':'Ticket insertado y actualizado a vigilancia'})
                    
                    if ticket_nevada is not None:
                        conn_nevada.stop4(ticket_nevada)
                        return ({'Mensaje':'ticket actualizado a parada 4'})
                else:
                    conn_nevada.completeTicgetAllTicketsket(ticket_nevada)
                    return ({'Mensaje':'Ticket Completado'})
                
            finally:
                conn_nevada.closeConnection


    finally:
        conn_adempiere.closeConnection

@router.get('/location/stop/updatep5/{ticket}', tags=["Stops"])
def update_ticket(ticket: str):
    try:
        conn_adempiere = AdempiereConnect()
        conn_adempiere.connect()
        ticket_status = conn_adempiere.getTicket(ticket)

        if ticket_status is None:
            return HTTPException(status_code=404, detail="El ticket no existe en Adempiere")
        
        if ticket_status is not None:
            try:
                conn_nevada = NevadaConnect()
                conn_nevada.connect()
                ticket_nevada = conn_nevada.getTicket(ticket)
                print(ticket_nevada)
                if ticket_status.orden_carga == 'Sin Orden Carga':

                    if ticket_nevada is None:
                        
                        conn_nevada.insertTicket(ticket_status, 'p5')
                        return ({'Mensaje':'Ticket insertado y actualizado a p5'})
                    
                    if ticket_nevada is not None:
                        conn_nevada.stop5(ticket_nevada)
                        return ({'Mensaje':'ticket actualizado a parada 5'})
                else:
                    conn_nevada.completeTicket(ticket_nevada)
                    return ({'Mensaje':'Ticket Completado'})
                
            finally:
                conn_nevada.closeConnection


    finally:
        conn_adempiere.closeConnection
    