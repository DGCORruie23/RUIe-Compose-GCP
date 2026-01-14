import os
from django.db.models import Count
from usuario.models import Usuario, Paises, EstadoFuerza, Frases, Municipios, PuntosInternacion, RescatePunto, ConteoRapidoPunto, MsgUpdate
from datetime import date
from datetime import *
from openpyxl import Workbook


# valores_duplicados = RescatePunto.objects.all() \
#         .values('nombre', 'apellidos', 'nacionalidad') \
#         .annotate(veces=Count('idRescate')) \
#         .filter(veces__gt=1) \
#         .order_by('-veces')

# rescates_totales = RescatePunto.objects.all()

# print(f"Rescates totales: {rescates_totales.count()}")
# print(f"Rescates totales: {valores_duplicados.count()}")

# # ---- Embarazadas
# rescates_totales = RescatePunto.objects.all()

# embarazadas_ORs = RescatePunto.objects.filter(embarazo=True) \
#             .values('oficinaRepre') \
#             .annotate(total=Count('idRescate')) \
#             .order_by('-total')

# embarazadas_Nac = RescatePunto.objects.filter(embarazo=True) \
#             .values('nacionalidad') \
#             .annotate(total=Count('idRescate')) \
#             .order_by('-total')

# print("ORS")
# for dato in embarazadas_ORs:
#     print(f'{dato["oficinaRepre"]},{dato["total"]}')

# print("Nacionalidades")
# for dato in embarazadas_Nac:
#     print(f'{dato["nacionalidad"]},{dato["total"]}')

# # ------ termina enbarazadas



# # Datos por fechas

fecha_inicio = date(2025, 1, 1)
fecha_fin = date(2025, 5, 19)

oficinaR = 'BAJA CALIFORNIA'

fechaIN = datetime.strptime(f"{fecha_inicio}", "%Y-%m-%d")
fechaFN = datetime.strptime(f"{fecha_fin}", "%Y-%m-%d")

array_fechas = [(fechaIN + timedelta(days=d)).strftime("%d-%m-%y") for d in range((fechaFN - fechaIN).days + 1)]

rescates_por_oficina = RescatePunto.objects.filter(fecha__in= array_fechas, oficinaRepre=oficinaR) \
    .values('fecha')\
    .annotate(veces=Count('idRescate')) \
    .order_by('fecha')

counts_by_date = { entry['fecha']: entry['veces'] for entry in rescates_por_oficina }

# 3) construir la lista final incluyendo ceros
resultados = []

for d in array_fechas:
    resultados.append({
        'fecha': d,
        'veces': counts_by_date.get(d, 0)
    })

# rescates_por_agente = RescatePunto.objects.filter(fecha__in= array_fechas) \
#     .values('oficinaRepre', 'nombreAgente') \
#     .annotate(veces=Count('idRescate')) \
#     .order_by('oficinaRepre', 'nombreAgente')


# Crear el archivo Excel
ruta_archivo_excel = os.path.join(os.getcwd(), f'test_files/Resc{oficinaR}{fecha_inicio.day:02}_{fecha_inicio.month:02}.xlsx')
wb = Workbook()
ws = wb.active
ws.title = "Rescates por OFICINA"

# Escribir la cabecera
ws.append(["fecha", "Rescates"])

# Llenar el archivo Excel con los datos
for registro in resultados:
    ws.append([registro['fecha'], registro['veces']])

# Guardar el archivo
wb.save(ruta_archivo_excel)
print(f"El archivo Excel ha sido guardado en {ruta_archivo_excel}")

# from usuario.models import Usuario, Paises, EstadoFuerza, Frases, Municipios, PuntosInternacion, RescatePunto
# from django.db.models.functions import Upper
# RescatePunto.objects.update(nacionalidad=Upper('nacionalidad'))
# RescatePunto.objects.update(nombre=Upper('nombre'))
# RescatePunto.objects.update(apellidos=Upper('apellidos'))
# RescatePunto.objects.update(nombreAgente=Upper('nombreAgente'))
# RescatePunto.objects.update(puntoEstra=Upper('puntoEstra'))