from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from usuarioL.models import usuarioL
from usuario.models import RescatePunto, EstadoFuerza, PuntosInternacion, Municipios, Paises, Usuario
from datetime import *
from django.db.models import Count
from openpyxl import Workbook
from openpyxl import load_workbook
import os

# Create your views here.
@login_required
def estadistica(request):
    if request.method == 'GET':
        return render(request, "estadistica/indexE.html")
    
@login_required
def busqueda(request):
    if request.method == 'GET':
        return render(request, "estadistica/buscar.html")
    
@login_required
def reincidencia(request):
    if request.method == 'GET':
        return render(request, "estadistica/reincidentes.html")
    
@login_required
def reincidentes_xdia_ajax(request):
    if request.method == 'GET' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':

        fecha = request.GET.get('fecha', '')

        # Convertir el formato de llegada a formato de hora
        fechaIN = datetime.strptime(f"{fecha}", "%Y-%m-%d")

        # Descomentar para una fecha especifica
        # fechaIN = datetime.strptime(f"2024-12-01", "%Y-%m-%d")
        # fechaFIN = datetime.strptime(f"2024-12-15", "%Y-%m-%d")

        # fecha_year_less = fechaIN - timedelta(days=365)

        array_fechasAnual = [(fechaIN + timedelta(days=d)).strftime("%d-%m-%y") for d in range((365 + 1))]

        array_fechasDia = [(fechaIN + timedelta(days=d)).strftime("%d-%m-%y") for d in range((fechaIN - fechaIN).days + 1)]

         # Descomentar para una fecha especifica
        # array_fechasDia = [(fechaIN + timedelta(days=d)).strftime("%d-%m-%y") for d in range((fechaFIN - fechaIN).days + 1)]

        # Rescates por dia de las OR sin chiapas y tabasco
        rescates_por_dia = RescatePunto.objects.filter(fecha__in= array_fechasDia).exclude(oficinaRepre__in=["CHIAPAS", "TABASCO"]) \
            .values('nombre', 'apellidos', 'iso3', 'puntoEstra', 'oficinaRepre') \
            .order_by('iso3')

        datosORs = list(rescates_por_dia)

        # Rescates por dia de la OR CHIS
        rescates_por_dia_CHIS = RescatePunto.objects.filter(fecha__in=array_fechasDia, oficinaRepre="CHIAPAS") \
            .values('nombre', 'apellidos', 'iso3', 'puntoEstra', 'oficinaRepre') \
            .order_by('iso3')

        datosCHIS = list(rescates_por_dia_CHIS)

    # Valores duplicados desde un año atras
        valores_duplicados = RescatePunto.objects.all() \
            .values('nombre', 'apellidos', 'iso3') \
            .annotate(veces=Count('idRescate')) \
            .filter(veces__gt=1) \
            .order_by('-veces')
        
        print(valores_duplicados.count())

        valores_duplicados1year = {
            (valor['nombre'], valor['apellidos'], valor['iso3']): valor['veces']
            for valor in valores_duplicados
        }

        # Comparar cada entrada de datos1 con valores_unicos y obtener el valor de veces si existe
        resultados = []
        for dato in datosORs:
            clave = (dato['nombre'], dato['apellidos'], dato['iso3'])
            veces = valores_duplicados1year.get(clave)  # Buscar en el diccionario
            if veces is not None:
                # print(veces)
                resultados.append({**dato, 'veces': veces})
            # else:
            #     resultados.append({**dato, 'veces': 1})  # Si no existe, agregar 'veces': 0 o lo que prefieras

        # Comparar cada entrada de datos1 con valores_unicos y obtener el valor de veces si existe
        for dato in datosCHIS:
            clave = (dato['nombre'], dato['apellidos'], dato['iso3'])
            veces = valores_duplicados1year.get(clave)  # Buscar en el diccionario
            if veces is not None:
                # print(veces)
                resultados.append({**dato, 'veces': veces + 1})
            else:
                resultados.append({**dato, 'veces': 1})  # Si no existe, agregar 'veces': 0 o lo que prefieras

        conteo = len(resultados)
        # # Crear el archivo Excel
        # ruta_archivo_excel = os.path.join(os.getcwd(), f'reincidetes_{fechaIN.day:02}_{fechaIN.month:02}_Pais.xlsx')
        
        print(conteo)

        data = [
            {
                'fecha': fecha,
                'resultados': resultados,
                'conteo': conteo,
            }
        ]
        return JsonResponse({'data': data}, safe=False)
    
    return JsonResponse({'error': 'Petición inválida'}, status=400)
    

@login_required
def buscar_reincidente_ajax(request):
    if request.method == 'GET' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        nombre = request.GET.get('nombre', '')
        apellidos = request.GET.get('apellidos', '')
        nacionalidad = request.GET.get('nacionalidad', '')

        rescates = RescatePunto.objects.all()

        rescates = rescates.filter(nombre__icontains=nombre, apellidos__icontains=apellidos, nacionalidad__icontains=nacionalidad)

        # datetime.strptime(f"{rescate.fecha}", "%Y-%m-%d")

        data = [
            {
                'No': indice,
                'fecha': rescate.fecha,
                'oficina': rescate.oficinaRepre,
                'punto': rescate.puntoEstra,
                'nombre': rescate.nombre,
                'apellidos': rescate.apellidos,
                'nacionalidad': rescate.nacionalidad,
            }
            for indice , rescate in enumerate(rescates, start=1)
        ]
        return JsonResponse({'data': data}, safe=False)
    
    return JsonResponse({'error': 'Petición inválida'}, status=400)