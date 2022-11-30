# Práctica 4 - Seguridad en Redes
URL del proyecto: https://github.com/PilotoEspacial/SegRed-P4

# Contenido
- [Integrantes](#integrantes)
- [Requisitos](#requisitos)
- [Setup del entorno](#setup-del-entorno)
- [Explicación](#explicación)
    - [Configuración y despliegue de la API](#configuración-y-despliegue-de-la-api)
    - [SSH](#ssh)
    - [Reglas iptables](#reglas-iptables)
    - [Rsyslog](#rsyslog)
    - [Fail2ban](#fail2ban)
- [Lanzamiento de pruebas automáticas](#lanzamiento-de-pruebas-automáticas)

## Integrantes

- Alberto Vázquez Martínez - Alberto.Vazquez1@alu.uclm.es
- Paulino de la Fuente Lizcano - Paulino.Lafuente@alu.uclm.es

## Requisitos

Para poder lanzar el entorno es necesario tener instalado `docker`. Ejecuta los siguientes comandos para instalar `docker` en distribuciones Ubuntu/Debian:

```bash
sudo apt update
sudo apt-get install docker.io
```

Si quieres evitar escribir `sudo` cada vez que ejecutes el comando `docker`, añade tu nombre de usuario al grupo docker:

```bash
sudo usermod -aG docker ${USER}
```

## Setup del entorno

Para automatizar el despliege del entorno, se ha utilizado un archivo `Makefile` con diferentes instrucciones que automatizan las tareas. El órden de ejecución de las instrucciones es el que se muestra a continuación:

1. **build** → construye las imágenes de los diferentes nodos que componen el sistema distribuido.
2. **network** → crea las redes donde se desplegarán los nodos.
3. **containers** → ejecuta los diferentes nodos y les asigna la red a la que pertenecen.
4. **run-tests** → ejecuta tests para comprobar el correcto funcionamiento de la API.
5. **remove** → elimina los contenedores (nodos) y las redes creadas.
6. **clean** → elimina archivos temporales.

## Explicación

**Todas estas configuraciones se realizan de manera automática usando `Makefile` y los scripts `entrypoint.sh` de cada contenedor.**

### Configuración y despliegue de la API

### SSH

### Reglas iptables

### Rsyslog

Se ha configurado un nodo específico llamado **logs** que será utilizado para almacenar los logs de todos los nodos del sistema, para así tener un sistema centralizado de logs.

Primero tenemos que configurar el servidor **logs** para usarlo como servidor central. Para ello se utiliza un módulo de `rsyslog` llamado `imupd` que proporciona la capacidad para que el servidor central-rsyslog reciba mensajes Syslog a través del protocolo UDP. Descomentamos las del archivo de configuración **/etc/rsyslog.conf** lineas para activar el módulo:

```ini
#################
#### MODULES ####
#################
...

# provides UDP syslog reception
module(load="imudp")
input(type="imudp" port="514")

...
```
Además, añadimos una plantilla ([50-remote-logs.conf](/docker/logs/assets/50-remote-logs.conf)), para especificar la ruta donde se almacenarán los logs de manera centralizada.

En los clientes añadiremos dos plantillas, una para reenviar los logs al servidor de logs y además almacenarlos en manera local ([20-forward-logs.conf](/docker/assets/rsyslog/20-forward-logs.conf)) y uno específico para el servicio de ssh ([50-sshd.conf](/docker/assets/rsyslog/50-sshd.conf)).

### Fail2ban

Para evitar ataques de fuerza bruta, se utiliza el servicio de `fail2ban` para banear IPs si exceden un número de intentos a la hora de logear en cualquiera de los nodos mediante SSH. Para ello es necesario tener al menos el un log local monitorize los intentos de autenticación (auth.log). Por eso en la configuración de `rsyslog` se almacenan los logs en un servidor centralizado, pero además, se almacenan de manera local.

La configuración que se realiza en cada nodo es añadir una "jaula" para el servicio de ssh, para que banee una IP que intente autenticarse en cualquiera de los nodos y falle más de 3 veces. El archivo [defaults-debian.conf](docker/assets/fail2ban/defaults-debian.conf) contiene dicha configuración y deberá ser almacenado en la ruta **/etc/fail2ban/jail.d/defaults-debian.conf**.

Hay un excepción en la configuración para el servidor de **logs**, ya que el log que tiene que monitorizar se encuentra en un ruta diferente. Su configuración es la siguiente:

```ini
[sshd]
enabled = true
port = ssh
mode = aggressive
logpath = /var/log/remotelogs/logs/sshd.log
maxretry = 3
bantime = 120
```


## Lanzamiento de pruebas automáticas
