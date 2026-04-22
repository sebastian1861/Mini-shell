import os
import datetime
import platform
import psutil
import time
import subprocess
import socket
import shutil
from tabulate import tabulate


def obtener_fecha_hora():
    """Obtiene la fecha y hora del sistema (simulando acceso a BIOS)."""
    print("\n=== FECHA Y HORA DEL SISTEMA ===")
    ahora = datetime.datetime.now()
    print(f"Fecha: {ahora.strftime('%d/%m/%Y')}")
    print(f"Hora: {ahora.strftime('%H:%M:%S')}")
    print(f"Timestamp UNIX: {time.time()}")
    print("===============================\n")

def listar_procesos():
    """Lista los procesos en ejecución."""
    print("\n=== PROCESOS EN EJECUCIÓN ===")
    procesos = []
    for proc in psutil.process_iter(['pid', 'name', 'username', 'memory_percent']):
        try:
            procesos.append([
                proc.info['pid'],
                proc.info['name'],
                proc.info['username'],
                f"{proc.info['memory_percent']:.2f}%"
            ])
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    headers = ["PID", "Nombre", "Usuario", "Memoria"]
    print(tabulate(procesos[:15], headers=headers, tablefmt="grid"))
    print(f"Mostrando 15 de {len(procesos)} procesos")
    print("==============================\n")

def terminar_proceso():
    """Termina un proceso por su PID."""
    try:
        pid = int(input("Ingrese el PID del proceso a terminar: "))
        if psutil.pid_exists(pid):
            proceso = psutil.Process(pid)
            nombre = proceso.name()
            proceso.terminate()
            print(f"Proceso {nombre} (PID: {pid}) terminado correctamente.")
        else:
            print(f"No existe un proceso con PID {pid}")
    except ValueError:
        print("El PID debe ser un número entero.")
    except psutil.AccessDenied:
        print("No tiene permisos para terminar este proceso.")
    except Exception as e:
        print(f"Error: {e}")

def mostrar_ayuda():
    """Muestra la lista de comandos disponibles."""
    print("\n=== COMANDOS DISPONIBLES ===")
    comandos = [
        ["mihorario", "Muestra la fecha y hora actual del sistema"],
        ["misprocesos", "Lista los procesos en ejecución"],
        ["matarproceso", "Termina un proceso por su PID"],
        ["ayudame", "Muestra esta lista de comandos"],
        ["infopc", "Muestra información del sistema"],
        ["misarchivos", "Lista archivos en el directorio actual"],
        ["mired", "Muestra información de red"],
        ["miespacio", "Muestra espacio en disco"],
        ["limpiar", "Limpia la pantalla"],
        ["salir", "Sale del shell"]
    ]
    headers = ["Comando", "Descripción"]
    print(tabulate(comandos, headers=headers, tablefmt="grid"))
    print("===========================\n")

def mostrar_info_sistema():
    """Muestra información del sistema."""
    print("\n=== INFORMACIÓN DEL SISTEMA ===")
    print(f"Sistema operativo: {platform.system()} {platform.version()}")
    print(f"Nombre del equipo: {platform.node()}")
    print(f"Procesador: {platform.processor()}")
    print(f"Arquitectura: {platform.architecture()[0]}")
    
    # Información de memoria
    mem = psutil.virtual_memory()
    print(f"Memoria total: {mem.total / (1024 ** 3):.2f} GB")
    print(f"Memoria usada: {mem.used / (1024 ** 3):.2f} GB ({mem.percent}%)")
    
    # Información de CPU
    print(f"Núcleos físicos: {psutil.cpu_count(logical=False)}")
    print(f"Núcleos lógicos: {psutil.cpu_count()}")
    print(f"Uso de CPU: {psutil.cpu_percent(interval=1)}%")
    print("==============================\n")

def listar_archivos():
    """Lista los archivos en el directorio actual."""
    print(f"\n=== ARCHIVOS EN {os.getcwd()} ===")
    archivos = []
    for item in os.listdir():
        try:
            stats = os.stat(item)
            es_directorio = os.path.isdir(item)
            tipo = "Directorio" if es_directorio else "Archivo"
            tamaño = "-" if es_directorio else f"{stats.st_size / 1024:.2f} KB"
            fecha_mod = datetime.datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M')
            
            archivos.append([
                item,
                tipo,
                tamaño,
                fecha_mod
            ])
        except Exception as e:
            archivos.append([item, "Error", "-", str(e)])
    
    headers = ["Nombre", "Tipo", "Tamaño", "Modificado"]
    print(tabulate(archivos, headers=headers, tablefmt="grid"))
    print("================================\n")

def info_red():
    """Muestra información de red."""
    print("\n=== INFORMACIÓN DE RED ===")
    try:
        # Nombre del host
        print(f"Nombre del host: {socket.gethostname()}")
        
        # Dirección IP
        print(f"Dirección IP: {socket.gethostbyname(socket.gethostname())}")
        
        # Interfaces de red
        print("\nInterfaces de red:")
        if_addrs = psutil.net_if_addrs()
        for interface_name, interface_addresses in if_addrs.items():
            for address in interface_addresses:
                if str(address.family) == 'AddressFamily.AF_INET':
                    print(f"  {interface_name}:")
                    print(f"    IP: {address.address}")
                    print(f"    Máscara de red: {address.netmask}")
                    break
        
        # Estadísticas de red
        net_io = psutil.net_io_counters()
        print("\nEstadísticas:")
        print(f"  Bytes enviados: {net_io.bytes_sent / (1024 ** 2):.2f} MB")
        print(f"  Bytes recibidos: {net_io.bytes_recv / (1024 ** 2):.2f} MB")
    except Exception as e:
        print(f"Error al obtener información de red: {e}")
    print("==========================\n")

def espacio_disco():
    """Muestra información de espacio en disco."""
    print("\n=== ESPACIO EN DISCO ===")
    try:
        if platform.system() == 'Windows':
            particiones = psutil.disk_partitions()
            for particion in particiones:
                try:
                    uso = psutil.disk_usage(particion.mountpoint)
                    print(f"Unidad: {particion.device}")
                    print(f"  Punto de montaje: {particion.mountpoint}")
                    print(f"  Sistema de archivos: {particion.fstype}")
                    print(f"  Espacio total: {uso.total / (1024 ** 3):.2f} GB")
                    print(f"  Espacio usado: {uso.used / (1024 ** 3):.2f} GB ({uso.percent}%)")
                    print(f"  Espacio libre: {uso.free / (1024 ** 3):.2f} GB")
                    print()
                except PermissionError:
                    continue
        else:
            # Para Linux/Mac
            uso = psutil.disk_usage('/')
            print(f"Espacio total: {uso.total / (1024 ** 3):.2f} GB")
            print(f"Espacio usado: {uso.used / (1024 ** 3):.2f} GB ({uso.percent}%)")
            print(f"Espacio libre: {uso.free / (1024 ** 3):.2f} GB")
    except Exception as e:
        print(f"Error al obtener información de disco: {e}")
    print("=======================\n")

def limpiar_pantalla():
    """Limpia la pantalla."""
    os.system('cls' if platform.system() == 'Windows' else 'clear')
    print("Pantalla limpiada.\n")

def main():
    """Función principal del shell."""
    print("=========================================")
    print("  SHELL PERSONALIZADO - VERSIÓN 1.0")
    print("  Escriba 'ayudame' para ver los comandos")
    print("=========================================")
    
    while True:
        # Mostrar prompt
        comando = input("\n$ ").strip().lower()
        
        # Procesar comando
        if comando == "mihorario":
            obtener_fecha_hora()
        elif comando == "misprocesos":
            listar_procesos()
        elif comando == "matarproceso":
            terminar_proceso()
        elif comando == "ayudame":
            mostrar_ayuda()
        elif comando == "infopc":
            mostrar_info_sistema()
        elif comando == "misarchivos":
            listar_archivos()
        elif comando == "mired":
            info_red()
        elif comando == "miespacio":
            espacio_disco()
        elif comando == "limpiar":
            limpiar_pantalla()
        elif comando == "salir":
            print("Saliendo del shell. ¡Hasta pronto!")
            break
        elif comando == "":
            continue
        else:
            print(f"Comando '{comando}' no reconocido. Use 'ayudame' para ver la lista de comandos.")

if __name__ == "__main__":
    main()
