
import os
import re
import getpass
import pexpect

HOST = "10.8.27.129"
USER = "admin"
REPORT_DIR = "reportes"
VALOR_REQUERIDO = 15

os.makedirs(REPORT_DIR, exist_ok=True)


def conectar():
    password = getpass.getpass(
        "Contrasena SSH de FortiGate: "
    )

    ssh = pexpect.spawn(
        f"ssh -o StrictHostKeyChecking=accept-new {USER}@{HOST}",
        encoding="utf-8",
        timeout=30
    )

    resultado = ssh.expect([
        r"(?i)password:",
        r"#\s*",
        pexpect.TIMEOUT,
        pexpect.EOF
    ])

    if resultado == 0:
        ssh.sendline(password)
        ssh.expect(r"#\s*")
    elif resultado != 1:
        raise RuntimeError("No se pudo conectar a FortiGate")

    return ssh


def comando(ssh, cmd):
    ssh.sendline(cmd)
    ssh.expect(r"#\s*", timeout=30)
    return ssh.before


def auditar(ssh):
    salida = comando(
        ssh,
        "show full-configuration system global "
        "| grep admin-console-timeout"
    )

    encontrado = re.search(
        r"set admin-console-timeout\s+(\d+)",
        salida
    )

    valor = int(encontrado.group(1)) if encontrado else None

    return {
        "Tiempo de espera de consola":
            valor == VALOR_REQUERIDO
    }


def guardar(nombre, resultados, fase):
    texto = f"FORTIGATE - {fase}\n"

    for control, cumple in resultados.items():
        estado = "CUMPLE" if cumple else "NO CUMPLE"
        texto += f"{control}: {estado}\n"

    texto += (
        f"Valor requerido para este laboratorio: "
        f"{VALOR_REQUERIDO} minutos\n"
    )

    print(texto)

    ruta = os.path.join(REPORT_DIR, nombre)

    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write(texto)

    print(f"Reporte guardado en: {ruta}")


def remediar(ssh, resultados):
    if all(resultados.values()):
        print("El control ya cumple. No se aplicaron cambios.")
        return

    comandos = [
        "config system global",
        f"set admin-console-timeout {VALOR_REQUERIDO}",
        "end"
    ]

    for cmd in comandos:
        comando(ssh, cmd)

    print("Correccion enviada a FortiGate.")


def main():
    print("\nAUTOMATIZACION DE HARDENING - FORTIGATE")
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
                "hardening_fortigate_auditoria.txt",
                resultados,
                "AUDITORIA"
            )
        else:
            previo = auditar(ssh)
            guardar(
                "hardening_fortigate_previo.txt",
                previo,
                "PREVIO"
            )

            remediar(ssh, previo)

            posterior = auditar(ssh)
            guardar(
                "hardening_fortigate_posterior.txt",
                posterior,
                "POSTERIOR"
            )
    finally:
        ssh.sendline("exit")
        ssh.close()


if __name__ == "__main__":
    main()
