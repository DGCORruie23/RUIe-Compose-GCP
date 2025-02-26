from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.db.models import Count, Q
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from collections import Counter

from usuarioL.models import usuarioL
from usuario.models import RescatePunto, EstadoFuerza, PuntosInternacion, Municipios, Paises, Usuario

from openpyxl import Workbook
from openpyxl import load_workbook


from weasyprint import HTML
from datetime import *
import os


# Create your views here.
@login_required
def estadistica(request):
    if request.method == 'GET':
        contex = {
            'hoy': date.today().isoformat(),
        }
        return render(request, "estadistica/indexE.html", contex)
    
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
        rescates_por_dia = RescatePunto.objects.filter(fecha__in= array_fechasDia).exclude(oficinaRepre__in=["CHIAPAS"]) \
            .values('nombre', 'apellidos', 'iso3', 'puntoEstra', 'oficinaRepre', 'fecha', 'sexo', 'fechaNacimiento') \
            .order_by('iso3')

        datosORs = list(rescates_por_dia)

        # Rescates por dia de la OR CHIS
        rescates_por_dia_CHIS = RescatePunto.objects.filter(fecha__in=array_fechasDia, oficinaRepre="CHIAPAS") \
            .values('nombre', 'apellidos', 'iso3', 'puntoEstra', 'oficinaRepre', 'fecha', 'sexo', 'fechaNacimiento') \
            .order_by('iso3')
        
        total_dia = rescates_por_dia.count() + rescates_por_dia_CHIS.count()

        datosCHIS = list(rescates_por_dia_CHIS)

    # Valores duplicados desde un año atras
        valores_duplicados = RescatePunto.objects.all() \
            .values('nombre', 'apellidos', 'iso3') \
            .annotate(veces=Count('idRescate')) \
            .filter(veces__gt=1) \
            .order_by('-veces')
        
        # print(valores_duplicados.count())

        valores_duplicados1year = {
            (valor['nombre'], valor['apellidos'], valor['iso3']): valor['veces']
            for valor in valores_duplicados
        }

        # Comparar cada entrada de datos1 con valores_unicos y obtener el valor de veces si existe
        resultados = []
        rescatesNuevos = []
        for dato in datosORs:
            clave = (dato['nombre'], dato['apellidos'], dato['iso3'])
            veces = valores_duplicados1year.get(clave)  # Buscar en el diccionario
            if veces is not None:
                # print(veces)
                resultados.append({**dato, 'veces': veces})
            else:
                rescatesNuevos.append({**dato, 'veces': 0})
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
        
        # print(conteo)

        data = [
            {
                'fecha': fecha,
                'resultados': resultados,
                'total_r': total_dia,
                'conteo': conteo,
                'rescatesNuevos': rescatesNuevos,
            }
        ]
        return JsonResponse({'data': data}, safe=False)
    
    return JsonResponse({'error': 'Petición inválida'}, status=400)
    
@login_required
def reincidentes_xfechas_ajax(request):
    if request.method == 'GET' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':

        fecha1 = request.GET.get('fechaI', '')
        fecha2 = request.GET.get('fechaF', '')

        # Convertir el formato de llegada a formato de hora
        fechaIN = datetime.strptime(f"{fecha1}", "%Y-%m-%d")
        fechaFIN = datetime.strptime(f"{fecha2}", "%Y-%m-%d")

        fechas = f"{fecha1}--{fecha2}"

         # Descomentar para una fecha especifica
        array_fechasDia = [(fechaIN + timedelta(days=d)).strftime("%d-%m-%y") for d in range((fechaFIN - fechaIN).days + 1)]

        # Rescates por dia de las OR sin chiapas y tabasco
        rescates_por_dia = RescatePunto.objects.filter(fecha__in= array_fechasDia).exclude(oficinaRepre__in=["CHIAPAS"]) \
            .values('nombre', 'apellidos', 'iso3', 'puntoEstra', 'oficinaRepre', 'fecha', 'sexo', 'fechaNacimiento') \
            .order_by('iso3')

        datosORs = list(rescates_por_dia)

        # Rescates por dia de la OR CHIS
        rescates_por_dia_CHIS = RescatePunto.objects.filter(fecha__in=array_fechasDia, oficinaRepre="CHIAPAS") \
            .values('nombre', 'apellidos', 'iso3', 'puntoEstra', 'oficinaRepre', 'fecha', 'sexo', 'fechaNacimiento') \
            .order_by('iso3')
        
        total_dia = rescates_por_dia.count() + rescates_por_dia_CHIS.count()

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
        rescatesNuevos = []
        for dato in datosORs:
            clave = (dato['nombre'], dato['apellidos'], dato['iso3'])
            veces = valores_duplicados1year.get(clave)  # Buscar en el diccionario
            if veces is not None:
                # print(veces)
                resultados.append({**dato, 'veces': veces})
            else:
                rescatesNuevos.append({**dato, 'veces': 0})
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
        
        # print(conteo)

        data = [
            {
                'fecha': fechas,
                'resultados': resultados,
                'conteo': conteo,
                'total_r1': total_dia,
                'rescatesNuevos1': rescatesNuevos,
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


@login_required
def generar_pdf(request):

    fecha1 = request.GET.get('fechaI', '')

    datoRetorno = request.GET.get('retornos', '')
    # print(fecha1)
    # fecha a elegir
    fechaB = datetime.strptime(f"{fecha1}", "%Y-%m-%d")

    # estadoF = EstadoFuerza.objects.all().order_by('oficinaR')
    # Obtener los datos de la base de datos
    oficinas = EstadoFuerza.objects.values_list("oficinaR", flat=True).distinct().order_by('oficinaR')
    fecha = fechaB.strftime("%d/%m/%Y")
    fechaIN = fechaB.strftime("%d-%m-%y")

    rescates_por_dia = RescatePunto.objects.filter(fecha=fechaIN)\
        .values("oficinaRepre")\
        .annotate(
            total=Count('idRescate'),
            total_aereos=Count('idRescate', filter=Q(aeropuerto=True)),
            total_carreteros=Count('idRescate', filter=Q(carretero=True)),
            total_central=Count('idRescate', filter=Q(centralAutobus=True)),
            total_ferro=Count('idRescate', filter=Q(ferrocarril=True)),
            total_puestos=Count('idRescate', filter=Q(puestosADispo=True)),
            total_otros=Count('idRescate', Q(voluntarios=True)) + Count('idRescate', Q(otro=True)) + Count('idRescate', filter=Q(aeropuerto=False, carretero=False, centralAutobus=False, ferrocarril=False ,casaSeguridad=False, hotel=False, puestosADispo=False, voluntarios=False, otro=False)),
            ) \
        .order_by('oficinaRepre')
    
    # total_otros=Count('idRescate', filter=Q(casaSeguridad=True)) + Count('idRescate', Q(hotel=True)) + Count('idRescate', Q(puestosADispo=True)) + Count('idRescate', Q(voluntarios=True)) + Count('idRescate', Q(otro=True)),
    
    conteo_rescates = {
        nombre: {
            "total": 0,
            "total_aereos": 0,
            "total_carreteros": 0,
            "total_central": 0,
            "total_ferro": 0,
            "total_puestos": 0,
            "total_otros": 0
        }
        for nombre in oficinas
    }

    conteo_rescates["Total"] = {
            "total": 0,
            "total_aereos": 0,
            "total_carreteros": 0,
            "total_central": 0,
            "total_ferro": 0,
            "total_puestos": 0,
            "total_otros": 0
        }


    # print(conteo_rescates)

    for dato in rescates_por_dia:
        oficina = dato["oficinaRepre"]
        if oficina in conteo_rescates:
            a_aux = dato.get("total", 0)
            b_aux = dato.get("total_aereos", 0)
            c_aux = dato.get("total_carreteros", 0)
            d_aux = dato.get("total_central", 0)
            e_aux = dato.get("total_ferro", 0)
            f_aux = dato.get("total_puestos", 0)
            g_aux = dato.get("total_otros", 0)

            conteo_rescates[oficina]["total"] = a_aux
            conteo_rescates[oficina]["total_aereos"] = b_aux
            conteo_rescates[oficina]["total_carreteros"] = c_aux
            conteo_rescates[oficina]["total_central"] = d_aux
            conteo_rescates[oficina]["total_ferro"] = e_aux
            conteo_rescates[oficina]["total_puestos"] = f_aux
            conteo_rescates[oficina]["total_otros"] = g_aux

            conteo_rescates["Total"]["total"] += a_aux
            conteo_rescates["Total"]["total_aereos"] += b_aux
            conteo_rescates["Total"]["total_carreteros"] += c_aux
            conteo_rescates["Total"]["total_central"] += d_aux
            conteo_rescates["Total"]["total_ferro"] += e_aux
            conteo_rescates["Total"]["total_puestos"] += f_aux
            conteo_rescates["Total"]["total_otros"] += g_aux



    # -------------- Datos segunda tabla ------------------

    fechaIN = fechaB
    array_fechasDia = [(fechaIN + timedelta(days=d)).strftime("%d-%m-%y") for d in range((fechaIN - fechaIN).days + 1)]

    # Rescates por dia de las OR sin chiapas y tabasco
    rescates_por_dia = RescatePunto.objects.filter(fecha__in= array_fechasDia).exclude(oficinaRepre__in=["CHIAPAS"]) \
        .values('nombre', 'apellidos', 'nacionalidad', 'oficinaRepre','fecha', 'sexo', 'edad', 'numFamilia') \
        .order_by('nacionalidad')

    datosORs = list(rescates_por_dia)

    # Rescates por dia de la OR CHIS
    rescates_por_dia_CHIS = RescatePunto.objects.filter(fecha__in=array_fechasDia, oficinaRepre="CHIAPAS") \
        .values('nombre', 'apellidos', 'nacionalidad', 'oficinaRepre','fecha', 'sexo', 'edad', 'numFamilia') \
        .order_by('nacionalidad')
    
    total_dia = rescates_por_dia.count() + rescates_por_dia_CHIS.count()

    datosCHIS = list(rescates_por_dia_CHIS)

    # Valores duplicados desde un año atras
    valores_duplicados = RescatePunto.objects.all() \
        .values('nombre', 'apellidos', 'nacionalidad') \
        .annotate(veces=Count('idRescate')) \
        .filter(veces__gt=1) \
        .order_by('-veces')
    
    # print(valores_duplicados.count())

    valores_duplicados1year = {
        (valor['nombre'], valor['apellidos'], valor['nacionalidad']): valor['veces']
        for valor in valores_duplicados
    }

    # Comparar cada entrada de datos1 con valores_unicos y obtener el valor de veces si existe
    resultados = []
    rescatesNuevos = []
    for dato in datosORs:
        clave = (dato['nombre'], dato['apellidos'], dato['nacionalidad'])
        veces = valores_duplicados1year.get(clave)  # Buscar en el diccionario
        if veces is not None:
            # print(veces)
            resultados.append({**dato, 'veces': veces})
        else:
            rescatesNuevos.append({**dato, 'veces': 0})
        # else:
        #     resultados.append({**dato, 'veces': 1})  # Si no existe, agregar 'veces': 0 o lo que prefieras

    # Comparar cada entrada de datos1 con valores_unicos y obtener el valor de veces si existe
    for dato in datosCHIS:
        clave = (dato['nombre'], dato['apellidos'], dato['nacionalidad'])
        veces = valores_duplicados1year.get(clave)  # Buscar en el diccionario
        if veces is not None:
            # print(veces)
            resultados.append({**dato, 'veces': veces + 1})
        else:
            resultados.append({**dato, 'veces': 1})  # Si no existe, agregar 'veces': 0 o lo que prefieras

    #  Se generan los tablas de las oficinas para agrupar
    reincidentes_oficina = Counter(d["oficinaRepre"] for d in resultados)
    nuevos_oficina = Counter(d["oficinaRepre"] for d in rescatesNuevos)

    conteo_reincidentes = {
        nombre: {
            "total": 0,
            "total_reincidentes": 0,
            "total_nuevos": 0,
        }
        for nombre in oficinas
    }

    conteo_reincidentes["Total"] = {
            "total": 0,
            "total_reincidentes": 0,
            "total_nuevos": 0,
        }

    for oficina, count in reincidentes_oficina.items():
        if oficina in conteo_reincidentes:
            conteo_reincidentes[oficina]["total_reincidentes"] = count
            conteo_reincidentes['Total']["total_reincidentes"] += count

    for oficina, count in nuevos_oficina.items():
        if oficina in conteo_reincidentes:
            conteo_reincidentes[oficina]["total_nuevos"] = count
            conteo_reincidentes['Total']["total_nuevos"] += count

    for nombre in conteo_reincidentes:
        total_aux = conteo_reincidentes[nombre]['total_reincidentes'] + conteo_reincidentes[nombre]['total_nuevos']
        conteo_reincidentes[nombre]["total"] = total_aux
        conteo_reincidentes['Total']["total"] = total_aux

    # print(conteo_por_oficina)
    # conteo = len(resultados)

    # print(resultados)

    # -------------- Datos 3: Tercera tabla ------------------
    # print("llego 3ra tabla")

    nacionalidades_nuevos = {d["nacionalidad"] for d in rescatesNuevos}

    nuevos_datos_nacio = {nacionalidad: {"H_AS": 0, "M_AS": 0, "H_mS": 0, "M_mS": 0, "H_AA": 0, "M_AA": 0, "H_mA": 0, "M_mA": 0, 'total':0 } for nacionalidad in nacionalidades_nuevos}

    for d in rescatesNuevos:
        nuevos_datos_nacio[d["nacionalidad"]]["total"] += 1

        if d['sexo'] == True and d['edad'] >= 18 and (d['numFamilia'] is None or d['numFamilia'] == 0):
            nuevos_datos_nacio[d["nacionalidad"]]["H_AS"] += 1
        elif d['sexo'] == False and d['edad'] >= 18 and (d['numFamilia'] is None or d['numFamilia'] == 0):
            nuevos_datos_nacio[d["nacionalidad"]]["M_AS"] += 1
        elif d['sexo'] == True and d['edad'] < 18 and (d['numFamilia'] is None or d['numFamilia'] == 0):
            nuevos_datos_nacio[d["nacionalidad"]]["H_mS"] += 1
        elif d['sexo'] == False and d['edad'] < 18 and (d['numFamilia'] is None or d['numFamilia'] == 0):
            nuevos_datos_nacio[d["nacionalidad"]]["M_mS"] += 1
        elif d['sexo'] == True and d['edad'] >= 18 and (d['numFamilia'] > 0):
            nuevos_datos_nacio[d["nacionalidad"]]["H_AA"] += 1
        elif d['sexo'] == False and d['edad'] >= 18 and (d['numFamilia'] > 0):
            nuevos_datos_nacio[d["nacionalidad"]]["M_AA"] += 1
        elif d['sexo'] == True and d['edad'] < 18 and (d['numFamilia'] > 0):
            nuevos_datos_nacio[d["nacionalidad"]]["H_mA"] += 1
        elif d['sexo'] == False and d['edad'] < 18 and (d['numFamilia'] > 0):
            nuevos_datos_nacio[d["nacionalidad"]]["M_mA"] += 1
        else:
            print(d)


    # -------------- Datos 4: Cuarta tabla ------------------

    nacionalidades_reinc = {d["nacionalidad"] for d in resultados}

    reincidentes_datos_nacio = {nacionalidad: {"H_AS": 0, "M_AS": 0, "H_mS": 0, "M_mS": 0, "H_AA": 0, "M_AA": 0, "H_mA": 0, "M_mA": 0, 'total':0 } for nacionalidad in nacionalidades_reinc}

    for d in resultados:
        reincidentes_datos_nacio[d["nacionalidad"]]["total"] += 1

        if d['sexo'] == True and d['edad'] >= 18 and (d['numFamilia'] is None or d['numFamilia'] == 0):
            reincidentes_datos_nacio[d["nacionalidad"]]["H_AS"] += 1
        elif d['sexo'] == False and d['edad'] >= 18 and (d['numFamilia'] is None or d['numFamilia'] == 0):
            reincidentes_datos_nacio[d["nacionalidad"]]["M_AS"] += 1
        elif d['sexo'] == True and d['edad'] < 18 and (d['numFamilia'] is None or d['numFamilia'] == 0):
            reincidentes_datos_nacio[d["nacionalidad"]]["H_mS"] += 1
        elif d['sexo'] == False and d['edad'] < 18 and (d['numFamilia'] is None or d['numFamilia'] == 0):
            reincidentes_datos_nacio[d["nacionalidad"]]["M_mS"] += 1
        elif d['sexo'] == True and d['edad'] >= 18 and (d['numFamilia'] > 0):
            reincidentes_datos_nacio[d["nacionalidad"]]["H_AA"] += 1
        elif d['sexo'] == False and d['edad'] >= 18 and (d['numFamilia'] > 0):
            reincidentes_datos_nacio[d["nacionalidad"]]["M_AA"] += 1
        elif d['sexo'] == True and d['edad'] < 18 and (d['numFamilia'] > 0):
            reincidentes_datos_nacio[d["nacionalidad"]]["H_mA"] += 1
        elif d['sexo'] == False and d['edad'] < 18 and (d['numFamilia'] > 0):
            reincidentes_datos_nacio[d["nacionalidad"]]["M_mA"] += 1
        else:
            print(d)

    # nuevos_nacionalidades = Counter(d["nacionalidad"] for d in rescatesNuevos)

    # rescates_por_nacionalidad = RescatePunto.objects.filter(fecha__in= array_fechasDia)\
    #     .values("nacionalidad")\
    #     .annotate(
    #         total=Count('idRescate'),
    #         H_S=Count('idRescate', filter=Q(edad__gte=18, sexo=True)),
    #         M_S=Count('idRescate', filter=Q(edad__gte=18, sexo=False)),
    #         H_mS=Count('idRescate', filter=Q(edad__lt=18, sexo=True)),
    #         M_mS=Count('idRescate', filter=Q(edad__lt=18, sexo=False)),
    #         ) \
    #     .order_by('nacionalidad')
    
    # print(rescates_por_nacionalidad)

    # rescates_aereos = rescates_por_dia.filter(aeropuerto=True)\
    #     .values("oficinaRepre")\
    #     .annotate(conteo=Count('idRescate'))\
    #     .order_by('oficinaRepre')

    # for dato in rescates_aereos:
    #     conteo_rescates_aero[dato["oficinaRepre"]]["conteo"] = dato["conteo"]
    
    # rescates_aereos = [[clave, valor['conteo']] for clave, valor in conteo_rescates_aero.items()]

    
    # Crear el contexto con los datos
    context = {
        "fecha_actual": fecha,
        "dato": datoRetorno,
        "rescates": conteo_rescates,
        "reincidentes": conteo_reincidentes,
        "nacionalidades": dict(sorted(nuevos_datos_nacio.items(), key=lambda x: x[1]["total"], reverse=True)),
        "nacionalidades_re": dict(sorted(reincidentes_datos_nacio.items(), key=lambda x: x[1]["total"], reverse=True)),
    }

    # Renderizar el template HTML con los datos
    template = get_template("estadistica/reporteA.html")
    html_string = template.render(context)

    # Crear el PDF con WeasyPrint
    pdf_file = HTML(string=html_string).write_pdf()

    # Devolver el PDF como respuesta HTTP
    response = HttpResponse(pdf_file, content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="reporte.pdf"'
    return response