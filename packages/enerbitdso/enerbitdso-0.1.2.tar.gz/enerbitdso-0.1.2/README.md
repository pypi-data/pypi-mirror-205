```txt
███████╗██████╗     ██████╗ ███████╗ ██████╗ 
██╔════╝██╔══██╗    ██╔══██╗██╔════╝██╔═══██╗
█████╗  ██████╔╝    ██║  ██║███████╗██║   ██║
██╔══╝  ██╔══██╗    ██║  ██║╚════██║██║   ██║
███████╗██████╔╝    ██████╔╝███████║╚██████╔╝
╚══════╝╚═════╝     ╚═════╝ ╚══════╝ ╚═════╝ 
                                             
```

# Introducción

Un programa de línea de comandos para preparar y empujar reportes de lectura desde el api de enerBit al MDM.

Se distribuye como un paquete de Python ejecutable.

# Como empezar

## Instalación

1. Crear un ambiente virtual de Python para aislar la instalación del paquete de otros paquetes.

```sh
python3 -m venv venv
source ./venv/bin/activate
```

1. Instalar paquete usando pip (asegurarse de tener activo el ambiente virtual).

```sh
python -m pip install .
```

1. Comprobar la instalación con el comando de ayuda

```sh
enerbitdso --help
```

# Uso

El comando es `enerbitdso`.

Se tiene una ayuda usando la opción `--help`.
Esta explica los sub-comandos y las opciones disponibles de cada uno.

Esta herramienta usa las variables de entorno para configurar su ejecución.

## Sub-comandos

### `enerbitdso usages fetch`

Consulta los consumos usando el API para DSO de enerBit para un conjunto de fronteras.

#### Variables de entorno **requeridas**

Para ejecutar este sub-comando se requieren tres variables de entorno configuradas con sus respectivos valores.

- ENERBIT_API_BASE_URL: La URL base del API del DSO, su valor debe ser `https://dso.enerbit.me/`
- ENERBIT_API_USERNAME: El nombre de usuario para autenticarse contra el API, ejemplo: `pedro.perez@example.com`
- ENERBIT_API_PASSWORD: La contraseña del usuario para autenticarse, ejemplo: `mIClaVeSUperseCRETa`

Para configurar estas variables de entorno se pueden ejecutar los siguientes comandos en la terminal:

```powershell
$env:ENERBIT_API_BASE_URL = 'https://dso.enerbit.me/'
$env:ENERBIT_API_BASE_URL = 'NOMBRE DE USUARIO'
$env:ENERBIT_API_BASE_URL = 'CONTRASEÑA DE USUARIO'
```

#### Especificación de fronteras a consultar

Las fronteras a consultar se pueden especificar como una lista al final del comando separadas por espacios:

```
> enerbitdso usages fetch Frt00000 Frt00001
```

También se puede usar un archivo de texto con un código de frontera por línea usando la opción `--frt-file` y pasando la ubicación de dicho archivo.

```powershell
> enerbitdso usages fetch --frt-file "D://Mi CGM/misfronteras.txt"
```

#### Especificación de intervalo de tiempo para la consulta

El intervalo de tiempo se define a través de los parámetros de tipo fecha `--since` y `--until` (desde y hasta, respectivamente).
*Por defecto*, se consultan los 24 periodos del día de ayer.

Para consultar los periodos entre 2023-04-01 a las 09:00 y el 2023-04-05 a las 17:00:

```
> enerbitdso usages fetch Frt00000 Frt00001
```

#### Opción de ayuda

También tiene opción `--help` que muestra la ayuda particular de este sub-comando.

```powershell
> enerbitdso usages fetch --help

 Usage: enerbitdso usages fetch [OPTIONS] [FRTS]...

╭─ Arguments ────────────────────────────────────────────────────────────────────────────────────────────────────╮
│   frts      [FRTS]...  List of frt codes separated by ' ' [default: None]                                      │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --api-base-url        TEXT               [env var: ENERBIT_API_BASE_URL] [default: None] [required]         │
│ *  --api-username        TEXT               [env var: ENERBIT_API_USERNAME] [default: None] [required]         │
│ *  --api-password        TEXT               [env var: ENERBIT_API_PASSWORD] [default: None] [required]         │
│    --since               [%Y-%m-%d|%Y%m%d]  [default: (yesterday)]                                             │
│    --until               [%Y-%m-%d|%Y%m%d]  [default: (today)]                                                 │
│    --timezone            TEXT               [default: America/Bogota]                                          │
│    --out-format          [csv|jsonl]        Output file format [default: jsonl]                                │
│    --frt-file            PATH               Path file with one frt code per line [default: None]               │
│    --help                                   Show this message and exit.                                        │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```