
# ASIGNACIÓN 4 – AUDITORÍA Y HARDENING DE DISPOSITIVOS DE RED

**Instituto Tecnológico de Las Américas (ITLA)**  
**Asignatura:** Seguridad de Redes  
**Estudiante:** Merolyn Mejía Abreu  
**Matrícula:** 2025-0827  
**Herramientas:** GNS3, Cisco IOS, FortiGate, Ubuntu, Python y SSH

---

# 🎥 VIDEO DEMOSTRATIVO

**Enlace de YouTube:** [AGREGAR ENLACE DEL VIDEO AQUÍ]

El video presenta el funcionamiento de la topología, las auditorías realizadas, los controles de seguridad implementados y las pruebas de remediación automática.

---

# ÍNDICE

1. Introducción
2. Propósito del laboratorio
3. Objetivos
4. Herramientas utilizadas
5. Descripción de la topología
6. Tabla de direccionamiento IP
7. Configuración inicial de los dispositivos
8. Metodología de auditoría basada en CIS Benchmarks
9. Hardening del router Cisco
10. Hardening del switch Cisco
11. Hardening del firewall FortiGate
12. Scripts de automatización
13. Pruebas de funcionamiento
14. Prueba de remediación automática
15. Resultados de las auditorías
16. Evidencias del laboratorio
17. Estructura del repositorio
18. Observaciones y limitaciones
19. Conclusión

---

# 1. INTRODUCCIÓN

La seguridad de los dispositivos de red es fundamental para proteger la información y garantizar el funcionamiento de los servicios tecnológicos de una organización.

Los routers, switches y firewalls permiten establecer comunicaciones, administrar el tráfico y controlar el acceso a diferentes recursos. 
Sin embargo, cuando estos dispositivos no están configurados correctamente, pueden presentar vulnerabilidades que faciliten accesos no autorizados.

En esta práctica se desarrolló una topología de red utilizando GNS3, integrada por un router Cisco, un switch Cisco y un firewall FortiGate.

Sobre estos dispositivos se realizaron auditorías de seguridad tomando como referencia recomendaciones de hardening relacionadas con los CIS Benchmarks.

También se implementaron scripts en Python para automatizar la revisión de configuraciones, identificar controles que no cumplen y aplicar determinadas correcciones.

Finalmente, se realizaron pruebas para comprobar el funcionamiento de las medidas de seguridad implementadas.

---

# 2. PROPÓSITO DEL LABORATORIO

El propósito principal de este laboratorio es fortalecer la seguridad de una infraestructura de red mediante la identificación, aplicación y verificación de controles de hardening.

Se busca demostrar cómo una herramienta automatizada puede analizar las configuraciones de los dispositivos, generar reportes de cumplimiento y corregir determinados parámetros inseguros.

De esta manera, se reduce la necesidad de realizar todas las verificaciones manualmente y se facilita el proceso de administración de seguridad.

---

# 3. OBJETIVOS

## 3.1. Objetivo general

Implementar y evaluar medidas de hardening en dispositivos de red mediante auditorías automatizadas basadas en controles de seguridad seleccionados, utilizando Python y una topología virtual en GNS3.

## 3.2. Objetivos específicos

- Diseñar una topología con un router, un switch y un firewall.
- Configurar el direccionamiento IP de la infraestructura.
- Establecer comunicación mediante SSH.
- Identificar configuraciones que representen riesgos de seguridad.
- Aplicar medidas de hardening.
- Desarrollar scripts automatizados en Python.
- Realizar auditorías sin modificar los dispositivos.
- Implementar una opción de remediación automática.
- Generar informes antes y después de aplicar las correcciones.
- Verificar el funcionamiento de los controles implementados.
- Documentar las pruebas y sus resultados en GitHub.

---

# 4. HERRAMIENTAS UTILIZADAS

| Herramienta | Función |
|---|---|
| GNS3 | Creación de la topología virtual |
| Cisco IOS | Configuración del router y switch |
| FortiGate VM | Implementación y administración del firewall |
| Ubuntu | Estación utilizada para ejecutar las auditorías |
| Python 3 | Desarrollo de scripts de automatización |
| Pexpect | Automatización de conexiones SSH |
| SSH | Administración remota segura |
| GitHub | Publicación de la documentación y evidencias |
| CIS Benchmarks | Referencia para seleccionar controles de seguridad |

---

# 5. DESCRIPCIÓN DE LA TOPOLOGÍA

La infraestructura fue implementada en GNS3 utilizando los siguientes dispositivos:

### R1-HARDINING

Router Cisco encargado de proporcionar conectividad a la red del laboratorio.

### SW1-HARDENING

Switch Cisco utilizado para interconectar los dispositivos y evaluar controles de administración segura.

### FortiGate-VM64-KVM

Firewall utilizado para verificar y fortalecer los parámetros relacionados con la autenticación y las sesiones administrativas.

### Ubuntu-AUDITOR

Equipo desde el cual se ejecutaron los scripts desarrollados en Python.

### NAT1

Dispositivo utilizado para proporcionar conectividad externa al entorno virtual.

## 5.1. Diagrama de la topología

```text
                  RED EXTERNA
                      |
                     NAT1
                      |
                R1-HARDINING
                      |
                SW1-HARDENING
                 /          \
                /            \
       Ubuntu-AUDITOR      FortiGate
         10.8.27.10       10.8.27.129
```

**Figura 1. Diagrama lógico simplificado de la infraestructura.**

### Captura de la topología

![Topología del laboratorio](evidencias/imagenes/topologia.png)

---

# 6. TABLA DE DIRECCIONAMIENTO IP

Se utilizó la red `10.8.27.0/24`, tomando como referencia los últimos dígitos de la matrícula 2025-0827.

| Dispositivo | Dirección IP | Máscara | Función |
|---|---|---|---|
| R1-HARDINING | 10.8.27.1 | 255.255.255.0 | Router principal |
| SW1-HARDENING | 10.8.27.2 | Por verificar | Administración del switch |
| Ubuntu-AUDITOR | 10.8.27.10 | 255.255.255.0 | Equipo auditor |
| FortiGate | 10.8.27.129 | 255.255.255.128 | Firewall |
| NAT1 | DHCP | Según red NAT | Conectividad externa |

**Nota:** El direccionamiento corresponde al esquema utilizado durante el laboratorio. Antes de entregar, se debe confirmar la máscara y dirección de administración del switch y comprobar que la tabla coincida con las configuraciones finales.

---

# 7. CONFIGURACIÓN INICIAL DE LOS DISPOSITIVOS

Antes de realizar las auditorías, se preparó la conectividad y el acceso administrativo de los dispositivos.

## 7.1. Configuración del router

Se configuró la interfaz LAN y se habilitó la administración mediante SSH.

Comandos utilizados para verificar la configuración:

```cisco
show ip interface brief
show running-config
show ip ssh
show running-config | section line con
show running-config | section line vty
```

Estos comandos permitieron comprobar el direccionamiento IP, las interfaces activas y los parámetros de administración.

![Configuración del router](evidencias/imagenes/router.png)

## 7.2. Configuración del switch

El switch fue configurado con una dirección de administración y acceso mediante SSH.

Comandos de verificación:

```cisco
show running-config
show ip ssh
show running-config | section line vty
show running-config | include ip http
```

![Configuración del switch](evidencias/imagenes/switch.png)

## 7.3. Configuración del firewall FortiGate

El firewall fue preparado para permitir conexiones administrativas mediante SSH.

Se utilizó el siguiente comando para revisar sus parámetros:

```text
show full-configuration system global
```

Esto permitió consultar los tiempos de espera administrativos, los parámetros de bloqueo y las versiones SSH permitidas.

![Configuración de FortiGate](evidencias/imagenes/fortigate.png)

---

# 8. METODOLOGÍA DE AUDITORÍA BASADA EN CIS BENCHMARKS

Los CIS Benchmarks son guías que contienen recomendaciones para configurar sistemas y dispositivos de manera segura.

En esta práctica se seleccionaron controles relacionados con la administración de los dispositivos y la reducción de configuraciones inseguras.

El procedimiento utilizado fue el siguiente:

1. Obtener las configuraciones de los dispositivos.
2. Identificar los parámetros de seguridad seleccionados.
3. Comparar sus valores con los criterios esperados.
4. Generar un informe de auditoría.
5. Identificar controles que no cumplen.
6. Aplicar las correcciones correspondientes.
7. Ejecutar una auditoría posterior.
8. Guardar los reportes y evidencias.

Los scripts clasifican los resultados utilizando dos estados:

- **CUMPLE:** el parámetro evaluado coincide con el criterio definido.
- **NO CUMPLE:** el parámetro necesita una corrección.

**Alcance:** La práctica utiliza controles de hardening seleccionados como referencia. No constituye una auditoría integral ni una certificación oficial de cumplimiento CIS.

---

# 9. HARDENING DEL ROUTER CISCO

En el router se aplicaron medidas para fortalecer la autenticación y el acceso administrativo.

## 9.1. Tiempo de espera de consola

Configuración:

```cisco
line console 0
 exec-timeout 5 0
```

**Justificación:**

Esta configuración establece un tiempo de espera de cinco minutos para las sesiones inactivas.

Su propósito es evitar que una sesión administrativa permanezca abierta indefinidamente.

## 9.2. Autenticación local

Configuración:

```cisco
line console 0
 login local
```

**Justificación:**

Permite solicitar las credenciales de un usuario local antes de conceder acceso a la consola.

## 9.3. Eliminación de privilegios directos

Configuración:

```cisco
line console 0
 no privilege level
```

**Justificación:**

Evita asignar directamente el nivel de privilegio 15 a la consola.

## 9.4. Acceso remoto mediante SSH

Configuración:

```cisco
line vty 0 4
 exec-timeout 5 0
 login local
 transport input ssh
```

**Justificación:**

SSH permite administrar los dispositivos mediante conexiones cifradas y evita utilizar Telnet.

## 9.5. Resultados del router

| Control | Resultado |
|---|---|
| Tiempo de espera de consola | CUMPLE |
| Autenticación local | CUMPLE |
| Sin privilegio 15 directo | CUMPLE |

**Resultado final: 3 de 3 controles automatizados cumplen.**

---

# 10. HARDENING DEL SWITCH CISCO

En el switch se evaluaron cinco controles relacionados con la administración segura.

## 10.1. SSH versión 2

```cisco
ip ssh version 2
```

**Justificación:**

Permite utilizar una versión segura del protocolo SSH para la administración remota.

## 10.2. Acceso remoto exclusivamente mediante SSH

```cisco
line vty 0 4
 transport input ssh
```

**Justificación:**

Evita utilizar protocolos de administración remota sin cifrado.

## 10.3. Autenticación local

```cisco
line vty 0 4
 login local
```

**Justificación:**

Exige autenticación mediante los usuarios locales del dispositivo.

## 10.4. Deshabilitación de HTTP

```cisco
no ip http server
```

**Justificación:**

Deshabilita el servicio HTTP que no es necesario para administrar el switch en este laboratorio.

## 10.5. Deshabilitación de HTTPS

```cisco
no ip http secure-server
```

**Justificación:**

Reduce los servicios de administración disponibles cuando no se necesita acceso web.

## 10.6. Resultados del switch

| Control | Resultado |
|---|---|
| SSH versión 2 | CUMPLE |
| Acceso remoto solo SSH | CUMPLE |
| Autenticación local | CUMPLE |
| HTTP deshabilitado | CUMPLE |
| HTTPS deshabilitado | CUMPLE |

**Resultado final: 5 de 5 controles automatizados cumplen.**

---

# 11. HARDENING DEL FIREWALL FORTIGATE

En FortiGate se evaluaron controles relacionados con la seguridad de las sesiones administrativas.

## 11.1. Tiempo de espera administrativo

Se verificó que las sesiones administrativas tuvieran un límite de inactividad.

**Justificación:**

Evitar que una sesión permanezca abierta cuando no está siendo utilizada.

## 11.2. Deshabilitación de SSH versión 1

```text
config system global
    set admin-ssh-v1 disable
end
```

**Justificación:**

Evitar el uso de una versión antigua del protocolo SSH.

## 11.3. Bloqueo después de intentos fallidos

```text
config system global
    set admin-lockout-threshold 3
end
```

**Justificación:**

Limitar la cantidad de intentos fallidos de autenticación administrativa.

## 11.4. Duración del bloqueo

```text
config system global
    set admin-lockout-duration 60
end
```

**Justificación:**

Establecer un período de bloqueo temporal después de alcanzar el límite de intentos fallidos.

## 11.5. Tiempo de espera de consola

Durante las pruebas se identificó inicialmente:

```text
set admin-console-timeout 0
```

Se intentó configurar un tiempo de espera de cinco minutos.

Sin embargo, FortiGate indicó que el valor permitido debía encontrarse entre 15 y 300 minutos, además del valor 0.

Por esta razón se aplicó:

```text
config system global
    set admin-console-timeout 15
end
```

La verificación posterior mostró:

```text
set admin-console-timeout 15
```

**Justificación:**

Evitar que una sesión administrativa de consola permanezca abierta indefinidamente.

## 11.6. Resultados de FortiGate

| Control | Antes | Después |
|---|---|---|
| Tiempo de espera administrativo | CUMPLE | CUMPLE |
| SSH versión 1 deshabilitado | CUMPLE | CUMPLE |
| Bloqueo tras tres intentos | CUMPLE | CUMPLE |
| Duración del bloqueo | CUMPLE | CUMPLE |
| Tiempo de espera de consola | NO CUMPLE | CUMPLE |

**Resultado final: 5 de 5 controles cumplen.**

---

# 12. SCRIPTS DE AUTOMATIZACIÓN

Para automatizar las auditorías y las correcciones se desarrollaron scripts en Python utilizando Pexpect.

Esta biblioteca permite interactuar con las sesiones SSH de los dispositivos y analizar las respuestas obtenidas.

## 12.1. Scripts principales

| Script | Función |
|---|---|
| `hardening_router.py` | Auditoría y remediación del router |
| `hardening_switch.py` | Auditoría y remediación del switch |
| `hardening_fortigate.py` | Auditoría y remediación del control automatizado de FortiGate |
| `auditoria_router.py` | Auditoría complementaria del router |
| `auditoria_switch.py` | Auditoría complementaria del switch |
| `auditoria_fortigate.py` | Auditoría de FortiGate |
| `auditoria_fortigate_despues.py` | Auditoría posterior de FortiGate |

## 12.2. Modo 1: auditoría sin modificar

Los scripts presentan un menú con dos opciones:

```text
1. Auditar sin modificar
2. Aplicar remediacion y verificar
```

Al seleccionar la opción 1, el programa:

1. Establece una conexión SSH.
2. Consulta los parámetros de seguridad.
3. Evalúa los controles seleccionados.
4. Genera un informe de cumplimiento.
5. Finaliza sin modificar la configuración.

## 12.3. Modo 2: remediación automática

Al seleccionar la opción 2, el programa:

1. Ejecuta una auditoría inicial.
2. Identifica los controles que no cumplen.
3. Aplica las correcciones definidas.
4. Ejecuta una auditoría posterior.
5. Guarda los resultados.

## 12.4. Ejecución de los scripts

Desde la carpeta principal del proyecto en Ubuntu:

**Router:**

```bash
python scripts/hardening_router.py
```

**Switch:**

```bash
python scripts/hardening_switch.py
```

**FortiGate:**

```bash
python scripts/hardening_fortigate.py
```

Las credenciales administrativas se solicitan durante la ejecución para evitar incluir contraseñas directamente en el código.

---

# 13. PRUEBAS DE FUNCIONAMIENTO

Se realizaron diferentes pruebas para comprobar la conectividad y el funcionamiento de la automatización.

## 13.1. Prueba de conectividad

Desde Ubuntu se comprobó la comunicación con el router:

```bash
ping 10.8.27.1
```

**Resultado:** Comunicación exitosa.

## 13.2. Prueba de acceso SSH

Se verificó que Ubuntu pudiera establecer sesiones SSH con los dispositivos de administración.

**Resultado:** Conexiones realizadas correctamente durante las auditorías.

## 13.3. Prueba de auditoría del router

Se ejecutó:

```bash
python scripts/hardening_router.py
```

Se seleccionó la opción 1.

**Resultado:** Los tres controles automatizados aparecieron como `CUMPLE`.

## 13.4. Prueba de auditoría del switch

Se ejecutó:

```bash
python scripts/hardening_switch.py
```

Se seleccionó la opción 1.

**Resultado:** Los cinco controles aparecieron como `CUMPLE` en la auditoría final.

## 13.5. Prueba de auditoría de FortiGate

Se ejecutó:

```bash
python scripts/hardening_fortigate.py
```

Se seleccionó la opción 1.

**Resultado:** El control automatizado del tiempo de espera de consola apareció como `CUMPLE`.

Adicionalmente, la auditoría posterior de FortiGate verificó cinco controles de seguridad.

---

# 14. PRUEBA DE REMEDIACIÓN AUTOMÁTICA

Esta fue una de las pruebas más importantes del laboratorio, porque permitió comprobar que el script podía detectar y corregir una configuración insegura.

## 14.1. Generación de un incumplimiento

Para realizar la prueba, se habilitó temporalmente el servidor HTTP del switch:

```cisco
configure terminal
ip http server
end
```

Al verificar la configuración se obtuvo:

```text
ip http server
no ip http secure-server
```

Esto permitió crear un escenario controlado en el que el servidor HTTP estaba habilitado.

## 14.2. Auditoría inicial

Se ejecutó el script:

```bash
python scripts/hardening_switch.py
```

Se seleccionó la opción 1.

El programa detectó:

```text
SSH version 2: CUMPLE
Acceso remoto solo SSH: CUMPLE
Autenticacion local: CUMPLE
Servidor HTTP deshabilitado: NO CUMPLE
Servidor HTTPS deshabilitado: CUMPLE
```

### Evidencia del incumplimiento

![HTTP no cumple](evidencias/imagenes/http_no_cumple.png)

## 14.3. Aplicación de la remediación

Se ejecutó nuevamente el script, esta vez seleccionando la opción 2.

El programa identificó el incumplimiento y aplicó la corrección:

```cisco
no ip http server
```

## 14.4. Auditoría posterior

Después de aplicar la corrección, el script realizó una nueva auditoría.

Resultado:

```text
SSH version 2: CUMPLE
Acceso remoto solo SSH: CUMPLE
Autenticacion local: CUMPLE
Servidor HTTP deshabilitado: CUMPLE
Servidor HTTPS deshabilitado: CUMPLE
```

### Evidencia de la remediación

![Remediación del switch](evidencias/imagenes/remediacion_switch.png)

## 14.5. Verificación directa en el switch

Para confirmar la corrección, se ejecutó:

```cisco
show running-config | include ip http
```

El dispositivo mostró:

```text
no ip http server
no ip http secure-server
```

Finalmente, se guardó la configuración:

```cisco
copy running-config startup-config
```

**Resultado de la prueba:**

El script detectó correctamente una configuración que no cumplía, aplicó la remediación y confirmó que el control pasó a `CUMPLE`.

---

# 15. RESULTADOS DE LAS AUDITORÍAS

Después de aplicar las medidas de hardening, los resultados finales fueron:

| Dispositivo | Controles evaluados | Controles cumplidos |
|---|---:|---:|
| Router Cisco | 3 | 3 |
| Switch Cisco | 5 | 5 |
| FortiGate | 5 | 5 |
| **TOTAL** | **13** | **13** |

## 15.1. Porcentaje de cumplimiento

```text
Cumplimiento = (Controles cumplidos / Controles evaluados) × 100

Cumplimiento = (13 / 13) × 100

Cumplimiento = 100 %
```

**Resultado final: 100 % de cumplimiento de los controles seleccionados.**

Este resultado corresponde únicamente a los 13 controles evaluados y no representa un cumplimiento integral de todos los CIS Benchmarks.

---

# 16. EVIDENCIAS DEL LABORATORIO

En esta sección se presentan las capturas que demuestran la implementación y el funcionamiento de la infraestructura.

## Evidencia 1. Topología de GNS3

![Topología](evidencias/imagenes/topologia.png)

## Evidencia 2. Configuración del router

![Router](evidencias/imagenes/router.png)

## Evidencia 3. Configuración del switch

![Switch](evidencias/imagenes/switch.png)

## Evidencia 4. Configuración de FortiGate

![FortiGate](evidencias/imagenes/fortigate.png)

## Evidencia 5. Auditoría del router

![Auditoría router](evidencias/imagenes/auditoria_router.png)

## Evidencia 6. Auditoría del switch

![Auditoría switch](evidencias/imagenes/auditoria_switch.png)

## Evidencia 7. Auditoría de FortiGate

![Auditoría FortiGate](evidencias/imagenes/auditoria_fortigate.png)

## Evidencia 8. Incumplimiento HTTP

![HTTP no cumple](evidencias/imagenes/http_no_cumple.png)

## Evidencia 9. Remediación automática

![Remediación](evidencias/imagenes/remediacion_switch.png)

## Evidencia 10. Verificación posterior

![Resultado final](evidencias/imagenes/resultado_final.png)

---

# 17. ESTRUCTURA DEL REPOSITORIO

La siguiente estructura organiza los archivos de documentación y evidencias.

```text
Asignacion4-CIS-Hardening/
|
|-- README.md
|
|-- scripts/
|   |-- hardening_router.py
|   |-- hardening_switch.py
|   |-- hardening_fortigate.py
|   |-- auditoria_router.py
|   |-- auditoria_switch.py
|   |-- auditoria_fortigate.py
|   |-- auditoria_fortigate_despues.py
|
|-- reportes/
|   |-- auditoria_router_antes.txt
|   |-- auditoria_switch_antes.txt
|   |-- auditoria_switch_despues.txt
|   |-- auditoria_fortigate_antes.txt
|   |-- auditoria_fortigate_despues.txt
|
|-- configuraciones_publicas/
|   |-- router_running_config.txt
|   |-- switch_running_config.txt
|   |-- fortigate_running_config_publica.txt
|
|-- evidencias/
|   |-- prueba_remediacion/
|   |   |-- switch_http_no_cumple.txt
|   |   |-- switch_antes_remediacion.txt
|   |   |-- switch_despues_remediacion.txt
|   |
|   |-- imagenes/
|       |-- topologia.png
|       |-- router.png
|       |-- switch.png
|       |-- fortigate.png
|       |-- auditoria_router.png
|       |-- auditoria_switch.png
|       |-- auditoria_fortigate.png
|       |-- http_no_cumple.png
|       |-- remediacion_switch.png
|       |-- resultado_final.png
```

**Nota:** Las imágenes indicadas son nombres propuestos. Deben subirse a esas rutas para que aparezcan correctamente en el README. Las configuraciones públicas deben revisarse para evitar publicar credenciales, claves o información sensible.

---

# 18. OBSERVACIONES Y LIMITACIONES

Durante el desarrollo del laboratorio se identificaron las siguientes situaciones:

### Compatibilidad de FortiGate

La versión utilizada no permitió establecer un tiempo de espera de consola de cinco minutos.

Por esta razón se configuró el valor mínimo admitido de 15 minutos.

### Automatización

La prueba de remediación automática del switch demostró que el script podía identificar y corregir un incumplimiento real.

En otros casos, los scripts comprobaron que los controles ya cumplían y no necesitaban modificaciones adicionales.

### Respaldo inicial de FortiGate

Durante las pruebas, el archivo original de configuración inicial fue sobrescrito.

Sin embargo, se conservó el reporte inicial de auditoría, que permite documentar el incumplimiento detectado antes de la corrección.

### Protección de credenciales

Para publicar las configuraciones en GitHub se deben utilizar versiones revisadas y sanitizadas.

No deben publicarse contraseñas, hashes de autenticación, claves privadas ni otros secretos.

### Alcance del análisis CIS

La práctica evaluó controles seleccionados de hardening. No se realizó una auditoría integral de todos los controles de los CIS Benchmarks.

---

# 19. CONCLUSIÓN

Durante esta práctica se pudo comprobar la importancia de mantener los dispositivos de red con configuraciones seguras. A través de GNS3 se implementó una infraestructura con un router, un switch y un firewall, en la cual se revisaron diferentes parámetros relacionados con la administración, la autenticación y los servicios habilitados.

Uno de los aspectos más importantes fue el desarrollo de los scripts en Python, ya que permitieron automatizar las auditorías y generar reportes de cumplimiento. Además, mediante una prueba controlada en el switch, se demostró que el programa podía identificar una configuración insegura y aplicar una corrección automáticamente.

En general, el laboratorio permitió poner en práctica conocimientos de seguridad de redes y comprender cómo el hardening y la automatización ayudan a reducir riesgos y facilitar la administración de los dispositivos.

---

**Asignación 4 – Auditoría y Hardening de Dispositivos de Red**  
**Merolyn Mejía Abreu – 2025-0827**  
**Instituto Tecnológico de Las Américas (ITLA)**
