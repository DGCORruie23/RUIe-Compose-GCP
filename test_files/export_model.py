from django.apps import apps                                                                                                                                     
from django.core import serializers                                                                                                                              
                                                                                                                                                                    
# 1. Obtener todos los modelos de la aplicación 'usuario'                                                                                                        
try:                                                                                                                                                             
    usuario_app = apps.get_app_config('usuario')                                                                                                                 
    models = list(usuario_app.get_models())                                                                                                                      
except LookupError:                                                                                                                                              
    print("No se encontró la aplicación 'usuario'. Asegúrate de que está en INSTALLED_APPS.")                                                                    
    models = []                                                                                                                                                  
                                                                                                                                                                    
if models:                                                                                                                                                       
    print("\n--- Modelos disponibles en la aplicación 'usuario' ---")                                                                                            
    for idx, model in enumerate(models):                                                                                                                         
        try:                                                                                                                                                     
            count = model.objects.count()                                                                                                                        
        except Exception:                                                                                                                                        
            count = "N/A"                                                                                                                                        
        print(f"[{idx + 1}] {model.__name__} ({count} registros)")                                                                                               
                                                                                                                                                                    
    # 2. Selección del usuario                                                                                                                                   
    try:                                                                                                                                                         
        seleccion = int(input("\nSelecciona el número del modelo que deseas exportar: ")) - 1                                                                    
        if seleccion < 0 or seleccion >= len(models):                                                                                                            
            raise ValueError                                                                                                                                     
                                                                                                                                                                    
        selected_model = models[seleccion]                                                                                                                       
        model_name = selected_model.__name__                                                                                                                     
        total_records = selected_model.objects.count()                                                                                                           
                                                                                                                                                                    
        print(f"\nHas seleccionado: {model_name} ({total_records} registros)")                                                                                   
                                                                                                                                                                    
        # 3. Configuración del tamaño del bloque                                                                                                                 
        batch_input = input("Ingresa el tamaño del lote (por defecto 50000): ")                                                                                 
        BATCH_SIZE = int(batch_input) if batch_input.strip() else 50000                                                                                         
                                                                                                                                                                    
        # 4. Proceso de exportación                                                                                                                              
        part = 1                                                                                                                                                 
        last_pk = 0                                                                                                                                              
                                                                                                                                                                    
        print(f"\nIniciando exportación segmentada de {model_name}...")                                                                                          
                                                                                                                                                                    
        while True:                                                                                                                                              
            # Consultamos el bloque por clave primaria                                                                                                           
            batch = list(selected_model.objects.filter(pk__gt=last_pk).order_by('pk')[:BATCH_SIZE])                                                              
                                                                                                                                                                    
            if not batch:                                                                                                                                        
                break                                                                                                                                            
                                                                                                                                                                    
            # Nombre de archivo dinámico basado en el nombre del modelo                                                                                          
            filename = f"dbRUIeexport_{model_name.lower()}_part{part}.json"                                                                                      
            print(f" -> Exportando parte {part} ({len(batch)} registros)...")                                                                                    
                                                                                                                                                                    
            with open(filename, 'w', encoding='utf-8') as f:                                                                                                     
                serializers.serialize('json', batch, stream=f)                                                                                                   
                                                                                                                                                                    
            print(f"    Guardado: {filename}")
            
            last_pk = batch[-1].pk
            part += 1
            
        print(f"\n¡Completado! Se generaron {part - 1} archivos para {model_name}.")
        
    except ValueError:
        print("Selección o formato inválido. Operación cancelada.")
    except KeyboardInterrupt:
        print("\nOperación cancelada por el usuario.")