#!/usr/bin/env python3
"""
xDiagnostico.py
Script de diagnóstico completo para el sistema Zenda.

USO:

- TERMINAL: 
python xDiagnostico.py [env|creds|db|schemas|dump|tools]

- JUPYTERLAB: 
import sys
sys.argv = ['xDiagnostico.py']  # Para reporte completo
exec(open('/home/jupyter/Zenda_ADK/xDiagnostico.py').read())

- JUPYTERLAB SECCIÓN ESPECÍFICA:
import sys
sys.argv = ['xDiagnostico.py', 'schemas']  # o env, creds, db, dump, tools
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
    optional_libs = ['pandas']
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
            print(f"⚠️  {lib}: NO INSTALADA (opcional)")
    
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
        print_section(f"Schema: {filename}")
        
        try:
            with open(schema_file, 'r') as f:
                content = f.read()
                
            lines = content.split('\n')
            enums_found = []
            models_found = []
            
            for i, line in enumerate(lines):
                line_clean = line.strip()
                
                # Buscar Enums y Literals
                if any(keyword in line_clean for keyword in ['Literal[', 'Enum', 'class.*Enum']):
                    enums_found.append(f"Línea {i+1}: {line_clean}")
                
                # Buscar modelos
                if line_clean.startswith('class ') and 'BaseModel' in line_clean:
                    models_found.append(f"Línea {i+1}: {line_clean}")
                
                # Buscar campos específicos
                if any(field in line_clean.lower() for field in ['event_type', 'actor', 'client_id', 'user_id']):
                    print(f"  🔍 Línea {i+1}: {line_clean}")
            
            schemas_info[filename] = {
                'enums': enums_found,
                'models': models_found,
                'path': schema_file
            }
            
            if enums_found:
                print("  📋 ENUMs encontrados:")
                for enum in enums_found:
                    print(f"    {enum}")
            
            if models_found:
                print("  📋 Modelos encontrados:")
                for model in models_found:
                    print(f"    {model}")
                    
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
        return {}
    
    try:
        # Intentar con pandas primero, si no está usar csv
        try:
            import pandas as pd
            df = pd.read_csv(csv_found)
            print(f"✅ CSV cargado: {len(df)} filas (usando pandas)")
            
            # Analizar tabla bitacora específicamente
            print_section("Tabla BITACORA")
            bitacora_fields = df[df['tabla'] == 'bitacora']
            
            if len(bitacora_fields) > 0:
                print("📋 Campos de bitacora:")
                for _, row in bitacora_fields.iterrows():
                    print(f"  - {row['campo']}: {row['formato_sql']} ({row['tipo_pydantic']})")
                
                # ENUMs específicos
                enum_fields = bitacora_fields[bitacora_fields['formato_sql'].str.contains('USER-DEFINED|enum', na=False)]
                if len(enum_fields) > 0:
                    print("\n🔍 Campos ENUM en bitacora:")
                    for _, row in enum_fields.iterrows():
                        print(f"  - {row['campo']}:")
                        print(f"    SQL: {row['formato_sql']}")
                        print(f"    Pydantic: {row['tipo_pydantic']}")
                        print(f"    Restricciones: {row['restricciones']}")
            else:
                print("❌ No se encontraron campos para tabla 'bitacora'")
            
            # Todas las tablas disponibles
            print_section("Tablas Disponibles")
            tablas = df['tabla'].unique()
            print(f"Total tablas: {len(tablas)}")
            for tabla in sorted(tablas):
                count = len(df[df['tabla'] == tabla])
                print(f"  - {tabla}: {count} campos")
                
        except ImportError:
            # Fallback sin pandas
            import csv
            with open(csv_found, 'r') as f:
                reader = csv.DictReader(f)
                data = list(reader)
            print(f"✅ CSV cargado: {len(data)} filas (usando csv)")
            
            bitacora_fields = [row for row in data if row['tabla'] == 'bitacora']
            if bitacora_fields:
                print_section("Tabla BITACORA")
                for row in bitacora_fields:
                    print(f"  - {row['campo']}: {row['formato_sql']} ({row['tipo_pydantic']})")
        
        return {'csv_path': csv_found, 'total_filas': len(data) if 'data' in locals() else len(df)}
        
    except Exception as e:
        print(f"❌ Error analizando CSV: {e}")
        return {}

def test_table_access(client, table_name='bitacora'):
    """Prueba acceso a tabla específica"""
    print_header(f"PRUEBA DE ACCESO - TABLA {table_name.upper()}")
    
    if not client:
        print("❌ Cliente Supabase no disponible")
        return False
    
    try:
        response = client.table(table_name).select('*').limit(1).execute()
        print(f"✅ SELECT en {table_name}: OK")
        
        if response.data:
            print("📋 Estructura real de la tabla:")
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
            
            for line in lines:
                line_clean = line.strip()
                if line_clean.startswith('def ') and not line_clean.startswith('def __'):
                    functions.append(line_clean)
            
            tools_info[filename] = {'functions': functions}
            
            print(f"  ✅ Funciones encontradas: {len(functions)}")
            for func in functions:
                print(f"    - {func}")
                
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
    schemas_info = analyze_schemas()
    db_info = analyze_db_dump()
    tools_info = check_function_tools()
    
    if client:
        table_ok = test_table_access(client, 'bitacora')
    else:
        table_ok = False
    
    # Resumen final
    print_header("RESUMEN EJECUTIVO")
    
    status_items = [
        ("Entorno Python", "✅" if env_ok else "❌"),
        ("Credenciales Supabase", "✅" if creds_ok else "❌"),
        ("Conexión DB", "✅" if client else "❌"),
        ("Acceso Tablas", "✅" if table_ok else "❌"),
        ("Schemas Encontrados", f"✅ {len(schemas_info)}" if schemas_info else "❌"),
        ("DB Dump", "✅" if db_info else "❌"),
        ("Function Tools", f"✅ {len(tools_info)}" if tools_info else "❌"),
    ]
    
    for item, status in status_items:
        print(f"{status} {item}")
    
    all_critical_ok = env_ok and creds_ok and client and table_ok
    print(f"\n🎯 ESTADO GENERAL: {'✅ LISTO PARA DESARROLLO' if all_critical_ok else '⚠️ REQUIERE ATENCIÓN'}")

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
        else:
            print(__doc__)
    else:
        generate_report()