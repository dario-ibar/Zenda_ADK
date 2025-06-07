#!/usr/bin/env python3
"""
xDiagnostico.py
Script de diagnóstico completo para el sistema Zenda.

USO:
- TERMINAL:
python xDiagnostico.py [env|creds|db|schemas|dump|tools|all]

- JUPYTERLAB:
import sys
sys.argv = ['xDiagnostico.py', 'all'] # o el comando específico
exec(open('/home/jupyter/Zenda_ADK/xDiagnostico.py').read())

- JUPYTERLAB SECCIÓN ESPECÍFICA:
import sys
sys.argv = ['xDiagnostico.py', 'schemas']
exec(open('/home/jupyter/Zenda_ADK/xDiagnostico.py').read())
"""

import os
import sys
import glob
import json
from datetime import datetime
from pathlib import Path

# Configuración
PROJECT_ROOT = '/home/jupyter/Zenda_ADK'
SCHEMAS_PATH = f'{PROJECT_ROOT}/schemas'
CSV_DUMP_PATH = f'{PROJECT_ROOT}/supabase/Supabase Snippet Tablas, Campos, Pydantic.csv'

def print_header(title):
    """Imprime un header formateado"""
    print(f"\n{'='*60}")
    print(f"🔍 {title}")
    print('='*60)

def print_section(title):
    """Imprime una sección"""
    print(f"\n📋 {title}")
    print('-'*40)

def check_environment():
    """Verifica el entorno y dependencias"""
    print_header("DIAGNÓSTICO DE ENTORNO")
    
    print(f"Python: {sys.version}")
    print(f"Directorio actual: {os.getcwd()}")
    print(f"Proyecto Zenda: {PROJECT_ROOT}")
    
    # Verificar librerías críticas
    required_libs = ['supabase', 'dotenv', 'uuid']
    optional_libs = ['pandas', 'pydantic'] # Agregado pydantic para validación de schemas
    missing_libs = []
    
    for lib in required_libs:
        try:
            __import__(lib)
            print(f"✅ {lib}: Instalada")
        except ImportError:
            print(f"❌ {lib}: NO INSTALADA")
            missing_libs.append(lib)
    
    for lib in optional_libs:
        try:
            __import__(lib)
            print(f"✅ {lib}: Instalada")
        except ImportError:
            print(f"⚠️  {lib}: NO INSTALADA (opcional o para funcionalidades avanzadas)")
    
    if missing_libs:
        print(f"\n⚠️  Instalar: pip install {' '.join(missing_libs)}")
    
    return len(missing_libs) == 0

def check_credentials():
    """Verifica credenciales de Supabase"""
    print_header("CREDENCIALES SUPABASE")
    
    env_path = f'{PROJECT_ROOT}/.env'
    if not os.path.exists(env_path):
        print("❌ Archivo .env NO ENCONTRADO")
        return False
    
    print(f"✅ Archivo .env encontrado: {env_path}")
    
    try:
        from dotenv import load_dotenv
        load_dotenv(env_path)
        
        url = os.getenv('SUPABASE_URL')
        key = os.getenv('SUPABASE_KEY')
        
        if url and key:
            print(f"✅ SUPABASE_URL: {url[:30]}...")
            print(f"✅ SUPABASE_KEY: {key[:30]}...")
            return True
        else:
            print("❌ Variables SUPABASE_URL o SUPABASE_KEY no encontradas")
            return False
            
    except Exception as e:
        print(f"❌ Error cargando .env: {e}")
        return False

def test_supabase_connection():
    """Prueba conexión a Supabase"""
    print_header("CONEXIÓN SUPABASE")
    
    try:
        from supabase import create_client
        from dotenv import load_dotenv
        
        load_dotenv(f'{PROJECT_ROOT}/.env')
        url = os.getenv('SUPABASE_URL')
        key = os.getenv('SUPABASE_KEY')
        
        if not url or not key:
            print("❌ Credenciales no disponibles")
            return None
        
        client = create_client(url, key)
        
        # Test básico de conexión
        response = client.table('clientes').select('count', count='exact').execute()
        print("✅ Conexión a Supabase exitosa")
        print(f"✅ Acceso a tablas verificado")
        
        return client
        
    except Exception as e:
        print(f"❌ Error conectando a Supabase: {e}")
        return None

def analyze_schemas():
    """Analiza schemas Pydantic reales"""
    print_header("SCHEMAS PYDANTIC REALES")
    
    if not os.path.exists(SCHEMAS_PATH):
        print(f"❌ Carpeta schemas no encontrada: {SCHEMAS_PATH}")
        return {}
    
    schema_files = glob.glob(f'{SCHEMAS_PATH}/*.py')
    schemas_info = {}
    
    for schema_file in schema_files:
        filename = os.path.basename(schema_file)
        if filename.startswith('__'): # Ignorar __init__.py
            continue
        print_section(f"Schema: {filename}")
        
        try:
            with open(schema_file, 'r') as f:
                content = f.read()
                
            lines = content.split('\n')
            enums_found = []
            models_found = []
            id_fields = []
            
            # Extract models and their fields for more detailed schema info
            current_model_name = None
            current_model_fields = {}
            
            for i, line in enumerate(lines):
                line_clean = line.strip()
                
                # Detect Pydantic Models
                if line_clean.startswith('class ') and 'BaseModel' in line_clean:
                    model_match = line_clean.split('(')[0].replace('class ', '').strip()
                    models_found.append(f"Línea {i+1}: {line_clean}")
                    current_model_name = model_match
                    current_model_fields = {} # Reset for new model
                    
                elif current_model_name and not line_clean.startswith(('import', 'from', '#', '"""', 'class ')) and ':' in line_clean:
                    # Detect fields within the current model
                    field_name_part = line_clean.split(':')[0].strip()
                    type_hint_part = line_clean.split(':', 1)[1].split('=')[0].strip()

                    is_optional = 'Optional[' in type_hint_part
                    is_literal = 'Literal[' in type_hint_part
                    
                    current_model_fields[field_name_part] = {
                        'type_hint': type_hint_part,
                        'is_optional': is_optional,
                        'is_literal': is_literal,
                        'line_num': i+1
                    }
                    
                    # Buscar campos ID
                    if any(id_pattern in field_name_part.lower() for id_pattern in ['id', 'id_cliente', 'client_id', 'user_id']):
                        id_fields.append(f"Línea {i+1}: {line_clean}")
                    
                    # Buscar Enums y Literals
                    if is_literal:
                        enums_found.append(f"Línea {i+1}: {line_clean}")
            
            schemas_info[filename] = {
                'enums': enums_found,
                'models': models_found,
                'id_fields': id_fields,
                'path': schema_file,
                'fields': current_model_fields # Store fields for the *last* model found in the file
            }
            
            if id_fields:
                print("  🔍 Campos ID encontrados:")
                for id_field in id_fields:
                    print(f"    {id_field}")
            
            if enums_found:
                print("  📋 ENUMs/Literals encontrados:")
                for enum in enums_found:
                    print(f"    {enum}")
            
            if models_found:
                print("  📋 Modelos Pydantic encontrados:")
                for model in models_found:
                    print(f"    {model}")
                if current_model_fields:
                    print("  📋 Campos del último modelo Pydantic:")
                    for field_name, field_info in current_model_fields.items():
                        print(f"    - {field_name}: {field_info['type_hint']} (Línea {field_info['line_num']})")

        except Exception as e:
            print(f"  ❌ Error leyendo {filename}: {e}")
    
    return schemas_info

def analyze_db_dump():
    """Analiza el dump CSV de la estructura DB"""
    print_header("ANÁLISIS DEL DUMP CSV")
    
    # Buscar CSV en múltiples ubicaciones
    possible_paths = [
        CSV_DUMP_PATH,
        f'{PROJECT_ROOT}/supabase/Supabase Snippet Tablas, Campos, Pydantic.csv',
        f'{PROJECT_ROOT}/supabase/Supabase*.csv'
    ]
    
    csv_found = None
    for path in possible_paths:
        if '*' in path:
            matches = glob.glob(path)
            if matches:
                csv_found = matches[0]
                break
        elif os.path.exists(path):
            csv_found = path
            break
    
    if not csv_found:
        print(f"❌ CSV dump no encontrado en ubicaciones:")
        for path in possible_paths:
            print(f"  - {path}")
        return None # Devuelve None para indicar que no se encontró el CSV
    
    try:
        import pandas as pd
        df = pd.read_csv(csv_found)
        print(f"✅ CSV cargado: {len(df)} filas (usando pandas)")
        
        # Analizar inconsistencias schema vs DB
        verificar_inconsistencias_schemas(df)
        
        # Analizar tabla bitacora específicamente
        print_section("Tabla BITACORA")
        bitacora_fields = df[df['tabla'] == 'bitacora']
        
        if len(bitacora_fields) > 0:
            print("📋 Campos de bitacora:")
            for _, row in bitacora_fields.iterrows():
                print(f"  - {row['campo']}: {row['formato_sql']} ({row['tipo_pydantic']})")
            
            # ENUMs específicos
            enum_fields_db = bitacora_fields[bitacora_fields['formato_sql'].str.contains('USER-DEFINED|enum', na=False)]
            if len(enum_fields_db) > 0:
                print("\n🔍 Campos ENUM en bitacora (definición SQL):")
                for _, row in enum_fields_db.iterrows():
                    print(f"  - {row['campo']}:")
                    print(f"    SQL: {row['formato_sql']}")
                    print(f"    Pydantic (dump): {row['tipo_pydantic']}")
                    print(f"    Restricciones: {row['restricciones']}")
            else:
                print("❌ No se encontraron campos ENUM definidos por usuario para tabla 'bitacora'")
        else:
            print("❌ No se encontraron campos para tabla 'bitacora'")
        
        # Todas las tablas disponibles
        print_section("Tablas Disponibles")
        tablas = df['tabla'].unique()
        print(f"Total tablas: {len(tablas)}")
        for tabla in sorted(tablas):
            count = len(df[df['tabla'] == tabla])
            print(f"  - {tabla}: {count} campos")
            
        return {'csv_path': csv_found, 'total_filas': len(df), 'df': df}
            
    except ImportError:
        print("⚠️  Pandas no está instalado. Análisis de CSV limitado.")
        import csv
        with open(csv_found, 'r') as f:
            reader = csv.DictReader(f)
            data = list(reader)
        print(f"✅ CSV cargado: {len(data)} filas (usando csv nativo)")
        return {'csv_path': csv_found, 'total_filas': len(data), 'data': data}
            
    except Exception as e:
        print(f"❌ Error analizando CSV: {e}")
        return None

def verificar_inconsistencias_schemas(df_db_dump):
    """Detecta inconsistencias entre schemas Pydantic y estructura DB"""
    print_header("VERIFICACIÓN DE INCONSISTENCIAS SCHEMA Pydantic vs DB")
    
    inconsistencias = []
    schemas_info = analyze_schemas() # Vuelve a obtener la info de los schemas
    
    if not schemas_info:
        print("⚠️ No se pudieron cargar los schemas Pydantic para la verificación.")
        return
    
    # === 1. Verificar inconsistencias de campos ID (Revisado) ===
    print_section("Verificación de campos ID")
    for filename, schema_data in schemas_info.items():
        table_name = filename.replace('.py', '') # Asume que el nombre del archivo es el nombre de la tabla
        
        # Excepciones donde el nombre del archivo no es el nombre de la tabla directamente
        if table_name == 'session_context': # No es una tabla de DB directa
            continue
        
        db_table_fields = df_db_dump[df_db_dump['tabla'] == table_name]
        if db_table_fields.empty:
            # print(f"⚠️  Tabla '{table_name}' del schema no encontrada en el dump de DB.")
            continue

        pydantic_id_fields = [f.split(':')[0].strip() for f in schema_data.get('id_fields', [])]
        db_id_fields = db_table_fields[db_table_fields['campo'].str.contains('id', case=False, na=False)]['campo'].tolist()

        if pydantic_id_fields and db_id_fields:
            # Para la tabla clientes, el id_cliente ya es correcto en el schema
            # Si el schema tiene 'id_cliente' y la DB tiene 'id_cliente', es consistente
            if 'clientes.py' in filename:
                if 'id_cliente' in pydantic_id_fields and 'id_cliente' in db_id_fields:
                    print(f"✅ ID de cliente en '{table_name}': Consistente (id_cliente)")
                elif 'id' in pydantic_id_fields and 'id_cliente' in db_id_fields:
                    inconsistencias.append({
                        'tabla': table_name,
                        'problema': f"El schema Pydantic usa 'id' pero la DB usa 'id_cliente'.",
                        'accion': f"Cambiar campo 'id' por 'id_cliente' en schemas/{filename}.",
                        'impacto': 'CRÍTICO - Fallas en FunctionTools.'
                    })
                else:
                    # Otros casos de ID que pueden ser inconsistentes
                    for p_id in pydantic_id_fields:
                        if p_id not in db_id_fields and f"id_{table_name}" not in db_id_fields: # Más general
                            inconsistencias.append({
                                'tabla': table_name,
                                'problema': f"Campo ID '{p_id}' en schema Pydantic no coincide con los campos ID en la DB: {db_id_fields}.",
                                'accion': f"Asegurar que los campos ID del schema Pydantic ({p_id}) coincidan con la DB o viceversa.",
                                'impacto': 'ALTO - Posibles fallas en inserciones/consultas.'
                            })

            elif set(pydantic_id_fields) != set(db_id_fields):
                inconsistencias.append({
                    'tabla': table_name,
                    'problema': f"Campos ID inconsistentes. Pydantic: {pydantic_id_fields}, DB: {db_id_fields}.",
                    'accion': f"Asegurar que los campos ID en schemas/{filename} coincidan con la DB.",
                    'impacto': 'ALTO - Posibles fallas en FunctionTools.'
                })
            else:
                 print(f"✅ ID de '{table_name}': Consistente. (Pydantic: {pydantic_id_fields}, DB: {db_id_fields})")
        
        elif pydantic_id_fields and not db_id_fields:
             inconsistencias.append({
                'tabla': table_name,
                'problema': f"Schema Pydantic tiene campos ID ({pydantic_id_fields}), pero la DB no los tiene o no fueron detectados.",
                'accion': f"Verificar que la tabla '{table_name}' en DB tenga campos ID y sean detectados en el dump.",
                'impacto': 'ALTO - Posibles fallas en FunctionTools.'
            })
        elif not pydantic_id_fields and db_id_fields:
            print(f"⚠️  Schema Pydantic de '{table_name}' no tiene campos ID detectados, pero la DB sí: {db_id_fields}.")
            # No se agrega como inconsistencia crítica a menos que cause un error conocido
        else:
             print(f"ℹ️  Tabla '{table_name}': No se detectaron campos ID críticos.")
    
    # === 2. Verificar Optional Pydantic vs NOT NULL en DB ===
    print_section("Verificación de Optional Pydantic vs NOT NULL DB")
    for filename, schema_data in schemas_info.items():
        table_name = filename.replace('.py', '')
        
        if table_name == 'session_context':
            continue

        db_table_fields = df_db_dump[df_db_dump['tabla'] == table_name]
        if db_table_fields.empty:
            continue
        
        if 'fields' in schema_data:
            for field_name, field_info in schema_data['fields'].items():
                pydantic_is_optional = field_info['is_optional']
                
                db_field_row = db_table_fields[db_table_fields['campo'] == field_name]
                if not db_field_row.empty:
                    db_is_not_null = 'NOT NULL' in str(db_field_row.iloc[0]['restricciones']).upper()
                    
                    if pydantic_is_optional and db_is_not_null:
                        inconsistencias.append({
                            'tabla': table_name,
                            'campo': field_name,
                            'problema': f"Campo '{field_name}' es Optional en Pydantic pero NOT NULL en la DB.",
                            'accion': f"Hacer el campo NOT NULL en Pydantic o permitir NULL en la DB.",
                            'impacto': 'CRÍTICO - Fallará en inserciones/actualizaciones.'
                        })
                    elif not pydantic_is_optional and not db_is_not_null and field_name != 'id': # 'id' es autoincremental/nullable usualmente
                         # Esto es solo un warning si un campo NO es opcional en Pydantic pero es NULLABLE en DB
                         # print(f"ℹ️  '{table_name}.{field_name}': Pydantic no opcional, DB NULLABLE. Puede ser intencional.")
                         pass
                    else:
                        print(f"✅ '{table_name}.{field_name}': Consistencia de nulabilidad OK.")
                else:
                    print(f"⚠️  Campo '{field_name}' del schema '{table_name}' no encontrado en el dump de DB. No se pudo verificar nulabilidad.")

    # === 3. Verificar ENUMs de DB vs Literal/str de Pydantic ===
    print_section("Verificación de ENUMs (DB) vs Literals (Pydantic)")
    for filename, schema_data in schemas_info.items():
        table_name = filename.replace('.py', '')
        
        if table_name == 'session_context':
            continue
        
        db_table_fields = df_db_dump[df_db_dump['tabla'] == table_name]
        if db_table_fields.empty:
            continue

        if 'fields' in schema_data:
            for field_name, field_info in schema_data['fields'].items():
                pydantic_is_literal = field_info['is_literal']
                pydantic_type_hint = field_info['type_hint']

                db_field_row = db_table_fields[db_table_fields['campo'] == field_name]
                if not db_field_row.empty:
                    db_sql_format = str(db_field_row.iloc[0]['formato_sql']).lower()
                    db_is_enum = 'user-defined' in db_sql_format or 'enum' in db_sql_format
                    
                    if pydantic_is_literal and not db_is_enum:
                        inconsistencias.append({
                            'tabla': table_name,
                            'campo': field_name,
                            'problema': f"Campo '{field_name}' es Literal en Pydantic pero no un ENUM definido por usuario en la DB ('{db_sql_format}').",
                            'accion': "Asegurar que el tipo de campo en la DB sea un ENUM o cambiar el tipo en Pydantic.",
                            'impacto': 'ALTO - Inconsistencia de tipo. Puede causar errores.'
                        })
                    elif not pydantic_is_literal and db_is_enum:
                        inconsistencias.append({
                            'tabla': table_name,
                            'campo': field_name,
                            'problema': f"Campo '{field_name}' es un ENUM en la DB ('{db_sql_format}') pero no es Literal en Pydantic ('{pydantic_type_hint}').",
                            'accion': "Usar Literal en el schema Pydantic para este campo o cambiar el tipo en la DB.",
                            'impacto': 'ALTO - Puede causar errores de "operator does not exist" o validación.'
                        })
                    elif pydantic_is_literal and db_is_enum:
                         print(f"✅ '{table_name}.{field_name}': Consistencia ENUM/Literal OK.")
                    else:
                        # print(f"ℹ️ '{table_name}.{field_name}': No es ENUM/Literal o consistencia de tipo OK.")
                        pass # No es un caso de ENUM/Literal o son consistentes

                else:
                    print(f"⚠️  Campo '{field_name}' del schema '{table_name}' no encontrado en el dump de DB. No se pudo verificar tipo ENUM.")


    # Reportar inconsistencias
    if inconsistencias:
        print("\n🚨 INCONSISTENCIAS CRÍTICAS DETECTADAS:")
        for inc in inconsistencias:
            print(f"\n  ❌ TABLA: {inc.get('tabla', 'N/A')}")
            if 'campo' in inc:
                print(f"     CAMPO: {inc['campo']}")
            print(f"     PROBLEMA: {inc['problema']}")
            print(f"     ACCIÓN: {inc['accion']}")
            print(f"     IMPACTO: {inc['impacto']}")
    else:
        print("✅ No se detectaron inconsistencias críticas en el mapeo Schema vs DB.")
    
    return inconsistencias

def test_table_access(client, table_name='clientes'):
    """Prueba acceso a tabla específica"""
    print_header(f"PRUEBA DE ACCESO - TABLA {table_name.upper()}")
    
    if not client:
        print("❌ Cliente Supabase no disponible")
        return False
    
    try:
        response = client.table(table_name).select('*').limit(1).execute()
        print(f"✅ SELECT en {table_name}: OK")
        
        if response.data:
            print("📋 Estructura real de la tabla (primer registro):")
            sample_record = response.data[0]
            for field, value in sample_record.items():
                print(f"  - {field}: {type(value).__name__}")
        else:
            print("📋 Tabla vacía - no hay datos de muestra")
        
        return True
        
    except Exception as e:
        print(f"❌ Error accediendo {table_name}: {e}")
        return False

def check_function_tools():
    """Verifica FunctionTools implementadas"""
    print_header("FUNCTION TOOLS")
    
    tools_path = f'{PROJECT_ROOT}/tools'
    if not os.path.exists(tools_path):
        print(f"❌ Carpeta tools no encontrada: {tools_path}")
        return {}
    
    tool_files = glob.glob(f'{tools_path}/*.py')
    tools_info = {}
    
    for tool_file in tool_files:
        filename = os.path.basename(tool_file)
        if filename.startswith('__'):
            continue
            
        print(f"📄 {filename}")
        
        try:
            with open(tool_file, 'r') as f:
                content = f.read()
            
            lines = content.split('\n')
            functions = []
            client_id_usage = []
            
            for i, line in enumerate(lines):
                line_clean = line.strip()
                if line_clean.startswith('def ') and not line_clean.startswith('def __'):
                    functions.append(line_clean)
                
                # Buscar uso problemático de client_id vs id_cliente (ahora más informativo)
                if ('client_id' in line_clean or 'id_cliente' in line_clean) and \
                   ('clientes' in filename or 'bitacora' in filename or 'entidades' in filename or 'sesiones' in filename): # Solo si es relevante para esas tablas
                    client_id_usage.append(f"Línea {i+1}: {line_clean}")
            
            tools_info[filename] = {
                'functions': functions,
                'client_id_usage': client_id_usage
            }
            
            print(f"  ✅ Funciones encontradas: {len(functions)}")
            for func in functions:
                print(f"    - {func}")
            
            if client_id_usage:
                print(f"  🔍 Uso de client_id/id_cliente (posible inconsistencia):")
                for usage in client_id_usage[:5]:  # Solo mostrar primeros 5
                    print(f"    {usage}")
                if len(client_id_usage) > 5:
                    print(f"    ...y {len(client_id_usage) - 5} más líneas.")
            else:
                 print(f"  ✅ Uso de 'client_id'/'id_cliente' parece consistente en este archivo.")
                
        except Exception as e:
            print(f"  ❌ Error leyendo {filename}: {e}")
    
    return tools_info

def generate_report():
    """Genera reporte completo de diagnóstico"""
    print_header("REPORTE DE DIAGNÓSTICO ZENDA")
    print(f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Ejecutar todas las verificaciones
    env_ok = check_environment()
    creds_ok = check_credentials()
    client = test_supabase_connection()
    schemas_info = analyze_schemas() # Se usa internamente en verificar_inconsistencias_schemas
    db_info = analyze_db_dump() # Se usa internamente en verificar_inconsistencias_schemas
    tools_info = check_function_tools()
    
    all_critical_ok = env_ok and creds_ok and (client is not None) and (db_info is not None)
    
    if client:
        table_ok = test_table_access(client, 'clientes')
        all_critical_ok = all_critical_ok and table_ok
    else:
        table_ok = False
        all_critical_ok = False # Si no hay cliente, no puede estar todo crítico OK
    
    # Resumen final
    print_header("RESUMEN EJECUTIVO")
    
    status_items = [
        ("Entorno Python", "✅" if env_ok else "❌"),
        ("Credenciales Supabase", "✅" if creds_ok else "❌"),
        ("Conexión DB", "✅" if client else "❌"),
        ("Acceso Tablas (clientes)", "✅" if table_ok else "❌"),
        ("Schemas Pydantic", f"✅ {len(schemas_info)}" if schemas_info else "❌"),
        ("DB Dump (CSV)", "✅" if db_info else "❌"),
        ("Function Tools", f"✅ {len(tools_info)}" if tools_info else "❌"),
    ]
    
    for item, status in status_items:
        print(f"{status} {item}")
    
    print(f"\n🎯 ESTADO GENERAL: {'✅ LISTO PARA DESARROLLO' if all_critical_ok and not verificar_inconsistencias_schemas(db_info['df']) else '⚠️ REQUIERE ATENCIÓN'}")
    # Nota: Se llama verificar_inconsistencias_schemas de nuevo para el reporte final.
    # Se pasa df_info['df'] si db_info no es None.

if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'env':
            check_environment()
        elif command == 'creds':
            check_credentials()
        elif command == 'db':
            client = test_supabase_connection()
            if client:
                test_table_access(client)
        elif command == 'schemas':
            analyze_schemas()
        elif command == 'dump':
            analyze_db_dump()
        elif command == 'tools':
            check_function_tools()
        elif command == 'all': # Nuevo comando para ejecutar todo
            generate_report()
        else:
            print(__doc__)
    else:
        generate_report()