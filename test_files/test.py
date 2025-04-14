import os
from django.db.models import Count
from usuario.models import Usuario, Paises, EstadoFuerza, Frases, Municipios, PuntosInternacion, RescatePunto, ConteoRapidoPunto, MsgUpdate
from datetime import date
from datetime import *
from openpyxl import Workbook


fecha_inicio = date(2025, 1, 1)
fecha_fin = date(2025, 4, 9)

fechaIN = datetime.strptime(f"{fecha_inicio}", "%Y-%m-%d")
fechaFN = datetime.strptime(f"{fecha_fin}", "%Y-%m-%d")

array_fechas = [(fechaIN + timedelta(days=d)).strftime("%d-%m-%y") for d in range((fechaFN - fechaIN).days + 1)]

rescates_por_agente = RescatePunto.objects.filter(fecha__in= array_fechas) \
    .values('oficinaRepre', 'nombreAgente') \
    .annotate(veces=Count('idRescate')) \
    .order_by('oficinaRepre', 'nombreAgente')


# Crear el archivo Excel
ruta_archivo_excel = os.path.join(os.getcwd(), f'test_files/RescXusuarios{fecha_inicio.day:02}_{fecha_inicio.month:02}.xlsx')
wb = Workbook()
ws = wb.active
ws.title = "Rescates por usuarios"

# Escribir la cabecera
ws.append(["oficinaRepre", "nombreAgente", "Rescates"])

# Llenar el archivo Excel con los datos
for registro in rescates_por_agente:
    ws.append([registro['oficinaRepre'], registro['nombreAgente'], registro['veces']])

# Guardar el archivo
wb.save(ruta_archivo_excel)
print(f"El archivo Excel ha sido guardado en {ruta_archivo_excel}")