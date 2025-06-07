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
from typing import Dict, Any, List, Optional

# Configuración
PROJECT_ROOT = '/home/jupyter/Zenda_ADK'
SCHEMAS_PATH = f'{PROJECT_ROOT}/schemas'
# -- RUTA DEL DUMP ACTUALIZADA --
CSV_DUMP_PATH = f'{PROJECT_ROOT}/supabase/Supabase Snippet Tablas, Campos, COC.csv'
# ------------------------------

def print_header(title: str):
    """Imprime un header formateado"""
    print(f"\n{'='*60}")
    print(f"🔍 {title}")
    print('='*60)

def print_section(title: str):
    """Imprime una sección"""
    print(f"\n📋 {title}")
    print('-'*40)

def check_environment() -> bool:
    """Verifica el entorno y dependencias"""
    print_header("DIAGNÓSTICO DE ENTORNO")
    
    print(f"Python: {sys.version}")
    print(f"Directorio actual: {os.getcwd()}")
    print(f"Proyecto Zenda: {PROJECT_ROOT}")
    
    # Verificar librerías críticas
    required_libs = ['supabase', 'dotenv', 'uuid']
    optional_libs = ['pandas', 'pydantic']
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

def check_credentials() -> bool:
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

def test_supabase_connection() -> Any | None: # Returns SupabaseClient or None
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

def analyze_schemas() -> Dict[str, Dict[str, Any]]:
    """Analiza schemas Pydantic reales y extrae información detallada de campos."""
    print_header("SCHEMAS PYDANTIC REALES")
    
    if not os.path.exists(SCHEMAS_PATH):
        print(f"❌ Carpeta schemas no encontrada: {SCHEMAS_PATH}")
        return {}
    
    schema_files = glob.glob(f'{SCHEMAS_PATH}/*.py')
    schemas_info = {}
    
    for schema_file in schema_files:
        filename = os.path.basename(schema_file)
        if filename.startswith('__'):
            continue
        print_section(f"Schema: {filename}")
        
        try:
            with open(schema_file, 'r') as f:
                content = f.read()
                
            lines = content.split('\n')
            enums_literals_found_lines = []
            id_fields_names = []
            models_found = []
            
            file_models_fields: Dict[str, Dict[str, Any]] = {}
            current_model_name = None
            
            for i, line in enumerate(lines):
                line_clean = line.strip()
                
                if line_clean.startswith('class ') and 'BaseModel' in line_clean:
                    model_match = line_clean.split('(')[0].replace('class ', '').strip()
                    models_found.append(f"Línea {i+1}: {line_clean}")
                    current_model_name = model_match
                    file_models_fields[current_model_name] = {}
                    
                elif current_model_name and not line_clean.startswith(('import', 'from', '#', '"""', 'class ', '@')) and ':' in line_clean:
                    field_name_part = line_clean.split(':')[0].strip()
                    type_hint_part = line_clean.split(':', 1)[1].split('=')[0].strip() if '=' in line_clean else line_clean.split(':', 1)[1].strip()
                    default_value_part = line_clean.split('=', 1)[1].strip() if '=' in line_clean else None

                    is_optional = 'Optional[' in type_hint_part
                    is_literal = 'Literal[' in type_hint_part
                    
                    file_models_fields[current_model_name][field_name_part] = {
                        'type_hint': type_hint_part,
                        'is_optional': is_optional,
                        'is_literal': is_literal,
                        'default_value': default_value_part,
                        'line_num': i+1
                    }
                    
                    id_keywords = ['id', 'uuid', 'fk_']
                    if any(keyword in field_name_part.lower() for keyword in id_keywords) or \
                       (field_name_part.lower().endswith('id') and len(field_name_part) > 2):
                        id_fields_names.append(field_name_part)
                    
                    if is_literal:
                        enums_literals_found_lines.append(f"Línea {i+1}: {line_clean}")
            
            schemas_info[filename] = {
                'enums_literals_lines': enums_literals_found_lines,
                'models': models_found,
                'id_fields_names': list(set(id_fields_names)),
                'path': schema_file,
                'all_models_fields': file_models_fields
            }
            
            if schemas_info[filename]['id_fields_names']:
                print("  🔍 Campos ID encontrados:")
                for id_field in schemas_info[filename]['id_fields_names']:
                    print(f"    - {id_field}")
            
            if enums_literals_found_lines:
                print("  📋 ENUMs/Literals encontrados:")
                for enum_line in enums_literals_found_lines:
                    print(f"    {enum_line}")
            
            if models_found:
                print("  📋 Modelos Pydantic encontrados en este archivo:")
                for model_line in models_found:
                    print(f"    {model_line}")
                
                for model_name, fields in file_models_fields.items():
                    print(f"  📋 Campos del modelo Pydantic '{model_name}':")
                    for field_name, field_info in fields.items():
                        print(f"    - {field_name}: {field_info['type_hint']} (Línea {field_info['line_num']})")

        except Exception as e:
            print(f"  ❌ Error leyendo {filename}: {e}")
    
    return schemas_info

def analyze_db_dump() -> Dict[str, Any] | None:
    """Analiza el dump CSV de la estructura DB"""
    print_header("ANÁLISIS DEL DUMP CSV")
    
    # Buscar CSV en múltiples ubicaciones
    possible_paths = [
        CSV_DUMP_PATH, # Updated path
        f'{PROJECT_ROOT}/supabase/Supabase Snippet Tablas, Campos, Pydantic.csv', # Keep old name as fallback
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
        return None
    
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
                print(f"  - {row['campo']}: {row['formato_sql']} (Pydantic sugerido: {row.get('tipo_pydantic', 'N/A')}) [Restricciones: {row['restricciones']}] [COC: {row.get('descripcion_coc', 'N/A')}]")
            
            # ENUMs específicos
            enum_fields_db = bitacora_fields[bitacora_fields['formato_sql'].str.contains('USER-DEFINED|enum', na=False)]
            if len(enum_fields_db) > 0:
                print("\n🔍 Campos ENUM en bitacora (definición SQL):")
                for _, row in enum_fields_db.iterrows():
                    print(f"  - {row['campo']}:")
                    print(f"    SQL: {row['formato_sql']}")
                    print(f"    Pydantic (dump): {row.get('tipo_pydantic', 'N/A')}")
                    print(f"    Restricciones: {row['restricciones']}")
                    print(f"    COC: {row.get('descripcion_coc', 'N/A')}")
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
        from io import StringIO
        with open(csv_found, 'r') as f:
            reader = csv.DictReader(f)
            data = list(reader)
        print(f"✅ CSV cargado: {len(data)} filas (usando csv nativo)")
        temp_df = pd.DataFrame(data) if 'pandas' in sys.modules else data
        return {'csv_path': csv_found, 'total_filas': len(data), 'df': temp_df}
            
    except Exception as e:
        print(f"❌ Error analizando CSV: {e}")
        return None

def verificar_inconsistencias_schemas(df_db_dump: Any, schemas_info: Dict[str, Dict[str, Any]]) -> List[Dict[str, str]]:
    """Detecta inconsistencias entre schemas Pydantic y estructura DB"""
    print_header("VERIFICACIÓN DE INCONSISTENCIAS SCHEMA Pydantic vs DB")
    
    inconsistencias = []
    
    if not schemas_info:
        print("⚠️ No se pudieron cargar los schemas Pydantic para la verificación.")
        return inconsistencias
    if df_db_dump is None or (not hasattr(df_db_dump, 'columns') and not isinstance(df_db_dump, list)):
        print("⚠️ No se pudo cargar el dump de la base de datos para la verificación.")
        return inconsistencias
    
    try:
        import pandas as pd
        if not isinstance(df_db_dump, pd.DataFrame):
            if 'df' in df_db_dump and isinstance(df_db_dump['df'], pd.DataFrame):
                db_df = df_db_dump['df']
            elif 'data' in df_db_dump and isinstance(df_db_dump['data'], list):
                db_df = pd.DataFrame(df_db_dump['data'])
            else:
                raise TypeError("df_db_dump is not a DataFrame and cannot be converted.")
        else:
            db_df = df_db_dump
    except Exception as e:
        print(f"❌ Error procesando el dump de DB para verificación: {e}")
        return inconsistencias


    # === 1. Verificar inconsistencias de campos ID ===
    print_section("Verificación de Campos ID")
    for filename, schema_data in schemas_info.items():
        table_name_from_file = filename.replace('.py', '') 
        
        if table_name_from_file in ['session_context', '__init__']:
            continue
        
        db_table_fields = db_df[db_df['tabla'] == table_name_from_file]
        if db_table_fields.empty:
            print(f"⚠️  Tabla '{table_name_from_file}' (derivada de {filename}) no encontrada en el dump de DB. Imposible verificar IDs.")
            continue

        pydantic_id_fields_names = set(schema_data.get('id_fields_names', []))
        
        db_id_fields_names_raw = db_table_fields[db_table_fields['campo'].str.contains('id|fk_', case=False, na=False)]['campo'].tolist()
        
        db_id_fields_names = set(db_id_fields_names_raw)
        
        if pydantic_id_fields_names != db_id_fields_names:
            inconsistencias.append({
                'tabla': table_name_from_file,
                'schema_file': filename,
                'problema': f"Campos ID inconsistentes. Pydantic: {list(pydantic_id_fields_names)}, DB: {list(db_id_fields_names)}.",
                'accion': f"Asegurar que los campos ID en schemas/{filename} coincidan con la DB. Revisar campos 'id', 'uuid' y 'fk_'.",
                'impacto': 'ALTO - Posibles fallas en FunctionTools (identificación/búsqueda de registros).'
            })
        else:
             print(f"✅ ID de '{table_name_from_file}': Consistente. (Pydantic: {list(pydantic_id_fields_names)}, DB: {list(db_id_fields_names)})")
        
    # === 2. Verificar Optional Pydantic vs NOT NULL en DB ===
    print_section("Verificación de Optional Pydantic vs NOT NULL DB")
    for filename, schema_data in schemas_info.items():
        table_name_from_file = filename.replace('.py', '')
        
        if table_name_from_file in ['session_context', '__init__']:
            continue

        db_table_fields = db_df[db_df['tabla'] == table_name_from_file]
        if db_table_fields.empty:
            continue
        
        for model_name, fields_in_model in schema_data.get('all_models_fields', {}).items():
            for field_name, field_info in fields_in_model.items():
                pydantic_is_optional = field_info['is_optional']
                
                db_field_row = db_table_fields[db_table_fields['campo'] == field_name]
                if not db_field_row.empty:
                    db_restrictions = str(db_field_row.iloc[0]['restricciones']).upper()
                    db_is_not_null = 'NOT NULL' in db_restrictions and 'PRIMARY KEY' not in db_restrictions # PK implies NOT NULL
                    
                    if pydantic_is_optional and db_is_not_null:
                        inconsistencias.append({
                            'tabla': table_name_from_file,
                            'campo': field_name,
                            'problema': f"Campo '{field_name}' es Optional en Pydantic pero NOT NULL en la DB.",
                            'accion': f"Hacer el campo NOT NULL en Pydantic (eliminar Optional) o permitir NULL en la DB.",
                            'impacto': 'CRÍTICO - Fallará en inserciones/actualizaciones si se envía NULL.'
                        })
                    else:
                        print(f"✅ '{table_name_from_file}.{field_name}': Consistencia de nulabilidad OK.")
                else:
                    print(f"⚠️  Campo '{field_name}' del schema '{table_name_from_file}' no encontrado en el dump de DB. No se pudo verificar nulabilidad.")

    # === 3. Verificar ENUMs de DB vs Literal/str de Pydantic ===
    print_section("Verificación de ENUMs (DB) vs Literals (Pydantic)")
    for filename, schema_data in schemas_info.items():
        table_name_from_file = filename.replace('.py', '')
        
        if table_name_from_file in ['session_context', '__init__']:
            continue
        
        db_table_fields = db_df[db_df['tabla'] == table_name_from_file]
        if db_table_fields.empty:
            continue

        for model_name, fields_in_model in schema_data.get('all_models_fields', {}).items():
            for field_name, field_info in fields_in_model.items():
                pydantic_is_literal = field_info['is_literal']
                pydantic_type_hint = field_info['type_hint']

                db_field_row = db_table_fields[db_table_fields['campo'] == field_name]
                if not db_field_row.empty:
                    db_sql_format = str(db_field_row.iloc[0]['formato_sql']).lower()
                    db_is_enum = 'user-defined' in db_sql_format or db_sql_format.endswith('_enum')
                    
                    if pydantic_is_literal and not db_is_enum:
                        inconsistencias.append({
                            'tabla': table_name_from_file,
                            'campo': field_name,
                            'problema': f"Campo '{field_name}' es Literal en Pydantic ('{pydantic_type_hint}') pero no un ENUM definido por usuario en la DB ('{db_sql_format}').",
                            'accion': "Asegurar que el tipo de campo en la DB sea un ENUM o cambiar el tipo en Pydantic a str/int.",
                            'impacto': 'ALTO - Inconsistencia de tipo. Puede causar errores ("operator does not exist") o validación débil.'
                        })
                    elif not pydantic_is_literal and db_is_enum:
                        inconsistencias.append({
                            'tabla': table_name_from_file,
                            'campo': field_name,
                            'problema': f"Campo '{field_name}' es un ENUM en la DB ('{db_sql_format}') pero no es Literal en Pydantic ('{pydantic_type_hint}').",
                            'accion': "Usar Literal en el schema Pydantic para este campo o cambiar el tipo en la DB si no es un ENUM.",
                            'impacto': 'ALTO - Puede causar errores de "operator does not exist" o validación.'
                        })
                    elif pydantic_is_literal and db_is_enum:
                         print(f"✅ '{table_name_from_file}.{field_name}': Consistencia ENUM/Literal OK.")
                    else:
                        pass

                else:
                    print(f"⚠️  Campo '{field_name}' del schema '{table_name_from_file}' no encontrado en el dump de DB. No se pudo verificar tipo ENUM.")


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

def test_table_access(client: Any, table_name: str = 'clientes') -> bool:
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

def check_function_tools() -> Dict[str, Dict[str, Any]]:
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
                
                if ('client_id' in line_clean or 'id_cliente' in line_clean or 'user_id' in line_clean) and \
                   any(tbl in filename.lower() for tbl in ['clientes', 'bitacora', 'entidades', 'sesiones', 'tokens']):
                    client_id_usage.append(f"Línea {i+1}: {line_clean}")
            
            tools_info[filename] = {
                'functions': functions,
                'client_id_usage': client_id_usage
            }
            
            print(f"  ✅ Funciones encontradas: {len(functions)}")
            for func in functions:
                print(f"    - {func}")
            
            if client_id_usage:
                print(f"  🔍 Uso de ID de cliente/usuario:")
                for usage in client_id_usage[:5]:
                    print(f"    {usage}")
                if len(client_id_usage) > 5:
                    print(f"    ...y {len(client_id_usage) - 5} más líneas.")
            else:
                 print(f"  ✅ No se encontró uso explícito de IDs de cliente/usuario o es consistente en este archivo.")
                
        except Exception as e:
            print(f"  ❌ Error leyendo {filename}: {e}")
    
    return tools_info

def generate_report():
    """Genera reporte completo de diagnóstico"""
    print_header("REPORTE DE DIAGNÓSTICO ZENDA")
    print(f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    env_ok = check_environment()
    creds_ok = check_credentials()
    client = test_supabase_connection()
    schemas_info = analyze_schemas()
    db_info = analyze_db_dump()
    tools_info = check_function_tools()
    
    all_critical_ok = env_ok and creds_ok and (client is not None) and (db_info is not None)
    
    table_access_ok = False
    if client:
        table_access_ok = test_table_access(client, 'clientes')
        all_critical_ok = all_critical_ok and table_access_ok
    else:
        all_critical_ok = False
    
    inconsistencies_found = False
    if db_info and schemas_info:
        inconsistencies_list = verificar_inconsistencias_schemas(db_info['df'], schemas_info)
        if inconsistencies_list:
            inconsistencies_found = True
            all_critical_ok = False
    else:
        print("⚠️ No se pudo realizar la verificación de inconsistencias Schema vs DB debido a datos faltantes.")
        inconsistencies_found = True
        all_critical_ok = False

    print_header("RESUMEN EJECUTIVO")
    
    status_items = [
        ("Entorno Python", "✅" if env_ok else "❌"),
        ("Credenciales Supabase", "✅" if creds_ok else "❌"),
        ("Conexión DB", "✅" if client else "❌"),
        ("Acceso Tablas (clientes)", "✅" if table_access_ok else "❌"),
        ("Schemas Pydantic Cargados", f"✅ {len(schemas_info)}" if schemas_info else "❌"),
        ("DB Dump (CSV) Cargado", "✅" if db_info else "❌"),
        ("Function Tools Analizadas", f"✅ {len(tools_info)}" if tools_info else "❌"),
        ("Consistencia Schema vs DB", "✅" if not inconsistencies_found else "❌"),
    ]
    
    for item, status in status_items:
        print(f"{status} {item}")
    
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
        elif command == 'all':
            generate_report()
        else:
            print(__doc__)
    else:
        generate_report()