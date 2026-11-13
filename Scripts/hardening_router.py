
import os
import re
import getpass
import pexpect

HOST = "10.8.27.1"
USER = "router"
REPORT_DIR = "reportes"

os.makedirs(REPORT_DIR, exist_ok=True)


def conectar():
    password = getpass.getpass("Contrasena SSH del router: ")
    ssh = pexpect.spawn(
        f"ssh -o StrictHostKeyChecking=accept-new {USER}@{HOST}",
        encoding="utf-8",
        timeout=30
    )

    resultado = ssh.expect([
        r"(?i)password:",
        r"[#>]",
        pexpect.TIMEOUT,
        pexpect.EOF
    ])

    if resultado == 0:
        ssh.sendline(password)
        ssh.expect(r"[#>]")

    elif resultado != 1:
        raise RuntimeError("No se pudo establecer la conexion SSH")

    if ssh.after == ">":
        ssh.sendline("enable")
        ssh.expect([r"(?i)password:", r"#"])
        if "password" in str(ssh.after).lower():
            raise RuntimeError(
                "Se requiere autenticacion enable adicional"
            )

    ssh.sendline("terminal length 0")
    ssh.expect(r"#")
    return ssh


def comando(ssh, cmd):
    ssh.sendline(cmd)
    ssh.expect(r"#", timeout=30)
    return ssh.before


def auditar(ssh):
    config = comando(ssh, "show running-config")
    consola = re.search(
        r"line con(?:sole)? 0\b(.*?)(?=\nline |\Z)",
        config,
        re.S
    )

    bloque = consola.group(1) if consola else ""

    return {
        "Tiempo de espera de 5 minutos":
            bool(re.search(r"exec-timeout 5 0", bloque)),
        "Autenticacion local":
            bool(re.search(r"^\s*login local\s*$", bloque, re.M)),
        "Sin privilegio 15 directo":
            bool(consola) and not bool(
                re.search(r"privilege level 15", bloque)
            )
    }


def guardar(nombre, resultados, fase):
    texto = f"AUDITORIA ROUTER - {fase}\n"
    texto += "-" * 45 + "\n"

    for control, cumple in resultados.items():
        estado = "CUMPLE" if cumple else "NO CUMPLE"
        texto += f"{control}: {estado}\n"

    print(texto)

    ruta = os.path.join(REPORT_DIR, nombre)
    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write(texto)

    print(f"Reporte guardado en: {ruta}")


def remediar(ssh, resultados):
    if all(resultados.values()):
        print("Todos los controles cumplen. No se aplicaron cambios.")
        return

    comandos = ["configure terminal", "line console 0"]

    if not resultados["Tiempo de espera de 5 minutos"]:
        comandos.append("exec-timeout 5 0")

    if not resultados["Autenticacion local"]:
        comandos.append("login local")

    if not resultados["Sin privilegio 15 directo"]:
        comandos.append("no privilege level")

    comandos += ["end", "write memory"]

    for cmd in comandos:
        comando(ssh, cmd)

    print("Correcciones enviadas al router.")


def main():
    print("\nAUTOMATIZACION DE HARDENING - ROUTER")
    print("1. Auditar sin modificar")
    print("2. Aplicar remediacion y verificar")

    opcion = input("Selecciona una opcion: ").strip()

    if opcion not in ("1", "2"):
        print("Opcion no valida")
        return

    ssh = conectar()

    try:
        if opcion == "1":
            resultados = auditar(ssh)
            guardar(
                "hardening_router_auditoria.txt",
                resultados,
                "AUDITORIA"
            )
        else:
            previo = auditar(ssh)
            guardar(
                "hardening_router_previo.txt",
                previo,
                "PREVIO"
            )

            remediar(ssh, previo)

            posterior = auditar(ssh)
            guardar(
                "hardening_router_posterior.txt",
                posterior,
                "POSTERIOR"
            )
    finally:
        ssh.sendline("exit")
        ssh.close()


if __name__ == "__main__":
    main()
