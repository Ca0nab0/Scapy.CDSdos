# Objetivo del script:
- Inundar el registro de vecinos en la red por medio de CDP. Esto puede agotar la memoria ram y/o saturar la CPU de un switch Cisco causando latencia y/o interrupcion de los servicios. Con este script tambien se puede causar ruido, dificultando la visibildad de dispositivos legitimos. 

Video ilustrativo: https://youtu.be/jEswLxYMfo4

**Capturas de pantalla.**

- Ejecucion

<img width="314" height="149" alt="image" src="https://github.com/user-attachments/assets/4c4a7146-4667-4352-b1a5-56a3a895c6de" />


- Impacto en el objetivo


<img width="496" height="558" alt="image" src="https://github.com/user-attachments/assets/3f034797-91ae-4454-83f7-065ba9506e40" />


- Trafico generado

<img width="780" height="449" alt="image" src="https://github.com/user-attachments/assets/9c88eb6b-50c2-4d5b-869f-40d879058154" />



<img width="480" height="308" alt="image" src="https://github.com/user-attachments/assets/b4d3cb65-292f-49d4-bbc1-3ab2502e3d9f" />



**Topología (interfaces, VLANs, direccionamiento IP), etc..**


<img width="428" height="240" alt="image" src="https://github.com/user-attachments/assets/a0cdd55d-aeee-46f5-9a5a-fc73742d48e2" />




<img width="865" height="97" alt="image" src="https://github.com/user-attachments/assets/ac2ecb97-ef46-43f9-a8bb-a06085ac1174" />



**Parámetros usados:**
- Interfaz eth0 (estatica).
- Cantidad de dispositivos a generar.
- Nombre del dispositivo falso SRV-VULN (estatico)
- Direccion MAC utilizada para el protocolo CDP 01:00:0c:cc:cc:cc (estatica)
- Payload para aumentar el tamaño del paquete (estatico)

**Requisitos para utilizar la herramienta:**
- Permisos root o sudo
- Sistema operativo basados en Debian (Kali, Parrot, Ubuntu)
- Conexion por medio de la interfaz eth0 al Switch
- Python3
- Scapy
  
**Medidas de mitigación**
- Deshabilitar CDP globalmente:
   enable
  
   configure terminal

   _no cdp run_

-  Deshebilitar CDP en las interfaces de acceso 
  
   enable
  
   configure terminal
  
   interface <interfaz>
   
   no cdp enable
  
-  Control de tormentas: 
  
   enable
  
   configure terminal
  
   interface <interfaz>
   
   para bradcast
  
   storm-control broadcast level 30.5
  
   Para multicast
  
   storm-control multicast level 30.5
  
   Para unicast
  
   storm-control unicast level 30.5
  
   Acciones a tomar en caso de violacion
  
   storm-control action shutdown <- apagar
  
   storm-control action trap     <- solo enviar SNMP
  
   storm-control action block    <- bloquear el trafico excesivo
  
   storm-control broadcast level rising-threshold 80 falling-threshold 70 <- se coloca un bloqueo al superar 80% y lo restaura al bajar a 70% de ancho de banda
  
-  Port security: 
  
   enable
  
   configure terminal
  
   interface <interfaz>
   
    Dinamico
  
   switchport port-security mac-address sticky
  
    Estatico
  
   switchport port-security mac-address 0000.1111.2222
  
    Limite de MACs
  
   switchport port-security maximum 3
  
   Accion
  
   switchport port-security violation protect <- descarta los paquetes de direcciones no autorizadas
  
   switchport port-security violation restrict <- descarta los paquetes y genera logs
  
   switchport port-security violation shutdown <- apaga el puerto y genera logs

-  Implementacion de LLDP 
