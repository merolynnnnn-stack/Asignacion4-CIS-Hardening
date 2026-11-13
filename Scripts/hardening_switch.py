
import os
import re
import getpass
import pexpect

HOST = "10.8.27.2"
USER = "switch"
REPORT_DIR = "reportes"

os.makedirs(REPORT_DIR, exist_ok=True)


def conectar():
    password = getpass.getpass("Contrasena SSH del switch: ")

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
        raise RuntimeError("No se pudo conectar al switch")

    if ssh.after == ">":
        raise RuntimeError(
            "La sesion requiere acceso privilegiado"
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
    ssh_info = comando(ssh, "show ip ssh")

    vty = re.search(
        r"line vty 0 4\b(.*?)(?=\nline |\Z)",
        config,
        re.S
    )

    bloque = vty.group(1) if vty else ""

    return {
        "SSH version 2":
            bool(re.search(
                r"SSH Enabled.*version 2",
                ssh_info,
                re.I
            )),
        "Acceso remoto solo SSH":
            bool(re.search(
                r"^\s*transport input ssh\s*$",
                bloque,
                re.M
            )),
        "Autenticacion local":
            bool(re.search(
                r"^\s*login local\s*$",
                bloque,
                re.M
            )),
        "Servidor HTTP deshabilitado":
            bool(re.search(
                r"^\s*no ip http server\s*$",
                config,
                re.M
            )),
        "Servidor HTTPS deshabilitado":
            bool(re.search(
                r"^\s*no ip http secure-server\s*$",
                config,
                re.M
            ))
    }


def guardar(nombre, resultados, fase):
    texto = f"AUDITORIA SWITCH - {fase}\n"
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

    comandos = ["configure terminal"]

    if not resultados["SSH version 2"]:
        comandos.append("ip ssh version 2")

    if not resultados["Servidor HTTP deshabilitado"]:
        comandos.append("no ip http server")

    if not resultados["Servidor HTTPS deshabilitado"]:
        comandos.append("no ip http secure-server")

    necesita_vty = (
        not resultados["Acceso remoto solo SSH"]
        or not resultados["Autenticacion local"]
    )

    if necesita_vty:
        comandos.append("line vty 0 4")

        if not resultados["Acceso remoto solo SSH"]:
            comandos.append("transport input ssh")

        if not resultados["Autenticacion local"]:
            comandos.append("login local")

        comandos.append("exit")

    comandos += ["end", "write memory"]

    for cmd in comandos:
        comando(ssh, cmd)

    print("Correcciones enviadas al switch.")


def main():
    print("\nAUTOMATIZACION DE HARDENING - SWITCH")
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
                "hardening_switch_auditoria.txt",
                resultados,
                "AUDITORIA"
            )
        else:
            previo = auditar(ssh)
            guardar(
                "hardening_switch_previo.txt",
                previo,
                "PREVIO"
            )

            remediar(ssh, previo)

            posterior = auditar(ssh)
            guardar(
                "hardening_switch_posterior.txt",
                posterior,
                "POSTERIOR"
            )
    finally:
        ssh.sendline("exit")
        ssh.close()


if __name__ == "__main__":
    main()
