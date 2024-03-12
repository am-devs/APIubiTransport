from fastapi import HTTPException, status
import psycopg2
from models.driver import User, Vehicle, Ubication, StatusVehicle


class AdempiereConnect:
    def __init__(self):
        self.connection = None
        self.cursor = None
        

    def connect(self):
        host = "losroques"
        port = 5434
        database = "adempiere"
        username = "adempiere"
        password = "ad3mp13r3sf1d4.*"

        conn_string = f"dbname={database} user={username} password={password} host={host} port={port}"

        try:
            # Establece la conexión
            self.connection = psycopg2.connect(conn_string)

            # Crea un cursor
            self.cursor = self.connection.cursor()

        except psycopg2.Error as e:
            print("Error al conectar a PostgreSQL:", e)

    def login(self, ci:str):
        try:
            # Ejecuta la consulta de prueba
            consulta = "SELECT cb.value as codigo_socio, cb.name as nombre_socio FROM C_BPartner cb  where cb.value=%s;"
            self.cursor.execute(consulta, (ci,))
            # Obtiene el resultado
            resultados = self.cursor.fetchall()
            print("Resultados de la consulta:", resultados)
            if not resultados:
                return None
            for resultado in resultados:
                return User(username=resultado[1], code=resultado[0])

        except psycopg2.Error as e:
            print("Error al ejecutar la consulta:", e)
            return e

    def queryVehicle(self, plate:str,):
        credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            # Ejecuta la consulta de prueba
            consulta = "SELECT name from FTA_VEHICLE where FTA_VEHICLE.VehiclePlate=%s;"
            self.cursor.execute(consulta, (plate,))
            result = self.cursor.fetchall()
            print("Resultados de la consulta:", result)
            for resultado in result:
                return Vehicle(plate=plate)
        
        except psycopg2.Error as e:
            print("Error al ejecutar la consulta:", e)
            return e

    def statusVehicle(self, plate: str):

        credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
        )
        
        consulta =(
            "SELECT DISTINCT ON (vh.vehicleplate) "
                    "vh.vehicleplate AS placa, "
                    "CASE "
                    "WHEN pard.datestop::date = now()::date THEN 'Reparacion'::text "
                    "ELSE 'activo'::text "
                    "END AS parada, "
                    "CASE "
                        "WHEN regp.datedoc < CURRENT_DATE OR repd.datedoc < CURRENT_DATE AND tk.docstatus::text = 'CO'::text THEN 'Sin Ticket'::character varying "
                        "WHEN tk.docstatus::text = 'CO'::text THEN tk.documentno "
                        "WHEN tk.docstatus::text <> 'CO'::text THEN 'Sin Ticket'::character varying "
                        "ELSE 'Sin Ticket'::character varying "
                    "END AS ticket_entrada, "
                    "CASE "
						"WHEN tk.created IS NULL THEN 'Sin Ticket'::text "
						"ELSE to_char(tk.created, 'YYYY-MM-DD HH24:MI:SS') "
					"END AS fecha_ticket, "
                    "CASE "
                        "WHEN tk.fta_entryticket_id = car.fta_entryticket_id AND car.docstatus::text = 'CO'::text AND regp.datedoc < CURRENT_DATE THEN 'Sin Orden Carga'::character varying "
                        "WHEN tk.fta_entryticket_id = car.fta_entryticket_id AND car.docstatus::text = 'CO'::text THEN car.documentno "
                        "ELSE 'Sin Orden Carga'::character varying "
                    "END AS orde_carga, "
                    "CASE "
							"WHEN regp.datedoc < CURRENT_DATE AND car.documentno IS NOT NULL AND tk.operationtype <> 'MOM'::bpchar AND car.docstatus::text = 'CO'::text THEN 'sin viaje'::text "
							"WHEN repd.documentno IS NOT NULL AND car.documentno IS NULL AND tk.operationtype = 'MOM'::bpchar AND repd.datedoc = CURRENT_DATE THEN 'acarreo'::text "
							"WHEN car.documentno IS NOT NULL AND tk.operationtype = 'MOM'::bpchar AND car.docstatus::text = 'CO'::text AND regp.datedoc <> CURRENT_DATE THEN 'sin viaje'::text "
							"WHEN car.documentno IS NOT NULL AND tk.operationtype = 'MOM'::bpchar AND car.docstatus::text = 'CO'::text THEN 'despacho a sucursal'::text "
							"WHEN car.documentno IS NOT NULL AND tk.operationtype <> 'MOM'::bpchar AND car.docstatus::text = 'CO'::text AND regp.datedoc <> CURRENT_DATE THEN 'despacho a cliente'::text "
							"WHEN car.documentno IS NOT NULL AND tk.operationtype <> 'MOM'::bpchar AND car.docstatus::text = 'CO'::text THEN 'despacho a cliente'::text "
							"ELSE 'sin viaje'::text "
						"END AS tipo_de_viaje, "
                    "CASE "
                        "WHEN mov2.m_movementparent_id = mov.m_movement_id AND regp.docstatus::text = 'CO'::text OR repd.docstatus::text = 'CO'::text AND car.docstatus::text = 'CO'::text THEN 'liberado'::text "
                        "WHEN regp.datedoc = CURRENT_DATE AND regp.docstatus::text = 'CO'::text THEN 'transito'::text "
                        "WHEN repd.datedoc = CURRENT_DATE AND repd.docstatus::text = 'CO'::text THEN 'transito'::text "
                        "WHEN req.documentno IS NOT NULL OR car.documentno IS NOT NULL AND car.docstatus::text = 'CO'::text AND regp.documentno IS NULL THEN 'no disponible'::text "
                        "ELSE 'disponible'::text "
                    "END AS estatusvehicle "
            "FROM fta_vehicle vh "
                "LEFT JOIN fta_vehicle_stopline par ON par.fta_vehicle_id = vh.fta_vehicle_id AND par.created::date = now()::date "
                "LEFT JOIN fta_vehicle_stop pard ON pard.fta_vehicle_stop_id = par.fta_vehicle_stop_id "
                "LEFT JOIN m_requisition req ON req.m_requisition_id = pard.m_requisition_id "
                "LEFT JOIN fta_entryticket tk ON tk.fta_vehicle_id = vh.fta_vehicle_id AND tk.datedoc >= CURRENT_DATE AND tk.docstatus::text = 'CO'::text "
                "LEFT JOIN fta_loadorder car ON car.fta_vehicle_id = vh.fta_vehicle_id AND tk.fta_entryticket_id = car.fta_entryticket_id AND car.datedoc >= CURRENT_DATE AND car.docstatus::text = 'CO'::text "
                "LEFT JOIN fta_recordweight regp ON tk.fta_entryticket_id = regp.fta_entryticket_id AND regp.datedoc >= CURRENT_DATE  AND regp.docstatus::text = 'CO'::text "
                "LEFT JOIN dd_recordweight repd ON repd.fta_entryticket_id = tk.fta_entryticket_id AND repd.datedoc >= CURRENT_DATE  AND repd.docstatus::text = 'CO'::text "
                "LEFT JOIN ad_org orgs ON orgs.ad_org_id = repd.ad_org_id OR orgs.ad_org_id = regp.ad_org_id "
                "LEFT JOIN dd_orderline od ON od.dd_orderline_id = repd.dd_orderline_id "
                "LEFT JOIN m_locator loc ON loc.m_warehouse_id = regp.m_warehouse_id OR loc.m_locator_id = od.m_locator_id "
                "LEFT JOIN m_locator loc2 ON loc2.m_locator_id = od.m_locatorto_id "
                "LEFT JOIN m_movement mov ON mov.fta_recordweight_id = regp.fta_recordweight_id OR mov.dd_recordweight_id = repd.dd_recordweight_id AND mov.movementdate = CURRENT_DATE AND mov.docstatus = 'CO'::bpchar "
                "LEFT JOIN m_movement mov2 ON mov2.m_movementparent_id = mov.m_movement_id "
                "LEFT JOIN m_movementline movl ON movl.m_movement_id = mov2.m_movement_id "
                "LEFT JOIN m_locator mloc ON mloc.m_locator_id = movl.m_locator_id "
                "LEFT JOIN ad_org orgd ON orgd.ad_org_id = mov2.ad_org_id "
                "LEFT JOIN c_doctype doct ON doct.c_doctype_id = mov.c_doctype_id "
            "WHERE vh.isowner = 'Y'::bpchar and vh.vehicleplate=%s "
            "ORDER BY vh.vehicleplate, fecha_ticket DESC;")
        try:
            self.cursor.execute(consulta, (plate,))
            result = self.cursor.fetchone()
            print("Resultados de la consulta:", result)
            if result is None:
                print('el resultado de la consulta es None')
                return None
            if result is not None:
                
                print('El resultado de la consulta fueeeeeeee: '+ result[1])
                return StatusVehicle(
                            placa=result[0], 
                            parada=result[1], 
                            ticket_entrada=result[2],
                            fecha_ticket=result[3],
                            orden_carga=result[4],
                            tipo_viaje=result[5],
                            estatus_vehicle=result[6],
                            )
            else:
                return None
        except psycopg2.Error as e:
                    print("Error al ejecutar la consulta:", e)
                    return e

    def getTicket(self, ticket: str):

         consulta =(
            "SELECT DISTINCT ON (vh.vehicleplate) "
                    "vh.vehicleplate AS placa, "
                    "CASE "
                    "WHEN pard.datestop::date = now()::date THEN 'Reparacion'::text "
                    "ELSE 'activo'::text "
                    "END AS parada, "
                    "CASE "
                        "WHEN regp.datedoc < CURRENT_DATE OR repd.datedoc < CURRENT_DATE AND tk.docstatus::text = 'CO'::text THEN 'Sin Ticket'::character varying "
                        "WHEN tk.docstatus::text = 'CO'::text THEN tk.documentno "
                        "WHEN tk.docstatus::text <> 'CO'::text THEN 'Sin Ticket'::character varying "
                        "ELSE 'Sin Ticket'::character varying "
                    "END AS ticket_entrada, "
                    "CASE "
						"WHEN tk.created IS NULL THEN 'Sin Ticket'::text "
						"ELSE to_char(tk.created, 'YYYY-MM-DD HH24:MI:SS') "
					"END AS fecha_ticket, "
                    "CASE "
                        "WHEN tk.fta_entryticket_id = car.fta_entryticket_id AND car.docstatus::text = 'CO'::text AND regp.datedoc < CURRENT_DATE THEN 'Sin Orden Carga'::character varying "
                        "WHEN tk.fta_entryticket_id = car.fta_entryticket_id AND car.docstatus::text = 'CO'::text THEN car.documentno "
                        "ELSE 'Sin Orden Carga'::character varying "
                    "END AS orde_carga, "
                    "CASE "
							"WHEN regp.datedoc < CURRENT_DATE AND car.documentno IS NOT NULL AND tk.operationtype <> 'MOM'::bpchar AND car.docstatus::text = 'CO'::text THEN 'sin viaje'::text "
							"WHEN repd.documentno IS NOT NULL AND car.documentno IS NULL AND tk.operationtype = 'MOM'::bpchar AND repd.datedoc = CURRENT_DATE THEN 'acarreo'::text "
							"WHEN car.documentno IS NOT NULL AND tk.operationtype = 'MOM'::bpchar AND car.docstatus::text = 'CO'::text AND regp.datedoc <> CURRENT_DATE THEN 'sin viaje'::text "
							"WHEN car.documentno IS NOT NULL AND tk.operationtype = 'MOM'::bpchar AND car.docstatus::text = 'CO'::text THEN 'despacho a sucursal'::text "
							"WHEN car.documentno IS NOT NULL AND tk.operationtype <> 'MOM'::bpchar AND car.docstatus::text = 'CO'::text AND regp.datedoc <> CURRENT_DATE THEN 'despacho a cliente'::text "
							"WHEN car.documentno IS NOT NULL AND tk.operationtype <> 'MOM'::bpchar AND car.docstatus::text = 'CO'::text THEN 'despacho a cliente'::text "
							"ELSE 'sin viaje'::text "
						"END AS tipo_de_viaje, "
                    "CASE "
                        "WHEN mov2.m_movementparent_id = mov.m_movement_id AND regp.docstatus::text = 'CO'::text OR repd.docstatus::text = 'CO'::text AND car.docstatus::text = 'CO'::text THEN 'liberado'::text "
                        "WHEN regp.datedoc = CURRENT_DATE AND regp.docstatus::text = 'CO'::text THEN 'transito'::text "
                        "WHEN repd.datedoc = CURRENT_DATE AND repd.docstatus::text = 'CO'::text THEN 'transito'::text "
                        "WHEN req.documentno IS NOT NULL OR car.documentno IS NOT NULL AND car.docstatus::text = 'CO'::text AND regp.documentno IS NULL THEN 'no disponible'::text "
                        "ELSE 'disponible'::text "
                    "END AS estatusvehicle "
            "FROM fta_vehicle vh "
                "LEFT JOIN fta_vehicle_stopline par ON par.fta_vehicle_id = vh.fta_vehicle_id AND par.created::date = now()::date "
                "LEFT JOIN fta_vehicle_stop pard ON pard.fta_vehicle_stop_id = par.fta_vehicle_stop_id "
                "LEFT JOIN m_requisition req ON req.m_requisition_id = pard.m_requisition_id "
                "LEFT JOIN fta_entryticket tk ON tk.fta_vehicle_id = vh.fta_vehicle_id AND tk.datedoc >= CURRENT_DATE AND tk.docstatus::text = 'CO'::text "
                "LEFT JOIN fta_loadorder car ON car.fta_vehicle_id = vh.fta_vehicle_id AND tk.fta_entryticket_id = car.fta_entryticket_id AND car.datedoc >= CURRENT_DATE AND car.docstatus::text = 'CO'::text "
                "LEFT JOIN fta_recordweight regp ON tk.fta_entryticket_id = regp.fta_entryticket_id AND regp.datedoc >= CURRENT_DATE  AND regp.docstatus::text = 'CO'::text "
                "LEFT JOIN dd_recordweight repd ON repd.fta_entryticket_id = tk.fta_entryticket_id AND repd.datedoc >= CURRENT_DATE  AND repd.docstatus::text = 'CO'::text "
                "LEFT JOIN ad_org orgs ON orgs.ad_org_id = repd.ad_org_id OR orgs.ad_org_id = regp.ad_org_id "
                "LEFT JOIN dd_orderline od ON od.dd_orderline_id = repd.dd_orderline_id "
                "LEFT JOIN m_locator loc ON loc.m_warehouse_id = regp.m_warehouse_id OR loc.m_locator_id = od.m_locator_id "
                "LEFT JOIN m_locator loc2 ON loc2.m_locator_id = od.m_locatorto_id "
                "LEFT JOIN m_movement mov ON mov.fta_recordweight_id = regp.fta_recordweight_id OR mov.dd_recordweight_id = repd.dd_recordweight_id AND mov.movementdate = CURRENT_DATE AND mov.docstatus = 'CO'::bpchar "
                "LEFT JOIN m_movement mov2 ON mov2.m_movementparent_id = mov.m_movement_id "
                "LEFT JOIN m_movementline movl ON movl.m_movement_id = mov2.m_movement_id "
                "LEFT JOIN m_locator mloc ON mloc.m_locator_id = movl.m_locator_id "
                "LEFT JOIN ad_org orgd ON orgd.ad_org_id = mov2.ad_org_id "
                "LEFT JOIN c_doctype doct ON doct.c_doctype_id = mov.c_doctype_id "
            "WHERE vh.isowner = 'Y'::bpchar and tk.documentno=%s"
            "ORDER BY vh.vehicleplate, fecha_ticket DESC;")
         try:

                # Ejecuta la consulta de prueba
                self.cursor.execute(consulta, (ticket,))
                result = self.cursor.fetchone()
                print("Resultados de la consulta:", result)
                if result is None:
                    print('el resultado de la consulta es None')
                    return None
                if result is not None:
                    
                    print('El resultado de la consulta fueeeeeeee: '+ result[1])
                    return StatusVehicle(
                                placa=result[0], 
                                parada=result[1], 
                                ticket_entrada=result[2],
                                fecha_ticket=result[3],
                                orden_carga=result[4],
                                tipo_viaje=result[5],
                                estatus_vehicle=result[6],
                                )
                else:
                    return None
         except psycopg2.Error as e:
                    print("Error al ejecutar la consulta:", e)
                    return e

        
    

    def closeConnection(self):
        # Cierra el cursor y la conexión
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

