#!/usr/bin/env python3
"""
Database PG - Ferramenta Principal (Main Tool)
Permite escolher qual operação executar: Backup/Restore ou Instalação do PostgreSQL.
Uso: python pg_main.py
"""

import subprocess
import sys
from pathlib import Path


def print_menu():
    """Exibe o menu principal de opções."""
    print("\n" + "=" * 50)
    print("DATABASE PG - FERRAMENTA PRINCIPAL")
    print("=" * 50)
    print("Escolha a operação que deseja executar:")
    print("  1. Backup / Restore de PostgreSQL")
    print("  2. Instalar PostgreSQL (Debian/Ubuntu)")
    print("  0. Sair")
    print("=" * 50)


def run_backup_restore():
    """Executa o script de backup/restore."""
    script_path = Path(__file__).parent / "pg_backup_restore.py"
    if not script_path.exists():
        print("[ERRO] pg_backup_restore.py não encontrado!")
        return

    print("\n[INFO] Iniciando ferramenta de Backup/Restore...")
    print("[INFO] Use --help para ver as opções de subcomandos (backup, restore, backup-restore)\n")

    # Passa os argumentos extras para o script filho
    cmd = [sys.executable, str(script_path)] + sys.argv[1:]
    try:
        subprocess.run(cmd, check=False)
    except KeyboardInterrupt:
        print("\n[INFO] Operação interrompida pelo usuário.")


def run_install():
    """Executa o script de instalação do PostgreSQL."""
    script_path = Path(__file__).parent / "pg_install.py"
    if not script_path.exists():
        print("[ERRO] pg_install.py não encontrado!")
        return

    print("\n[INFO] Iniciando instalador do PostgreSQL...")
    print("[AVISO] Esta operação geralmente requer sudo/root.\n")

    cmd = [sys.executable, str(script_path)] + sys.argv[1:]
    try:
        subprocess.run(cmd, check=False)
    except KeyboardInterrupt:
        print("\n[INFO] Operação interrompida pelo usuário.")


def main():
    while True:
        print_menu()
        try:
            choice = input("Digite sua escolha [0-2]: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSaindo...")
            break

        if choice == "1":
            run_backup_restore()
        elif choice == "2":
            run_install()
        elif choice == "0":
            print("Saindo da ferramenta principal. Até logo!")
            break
        else:
            print("[ERRO] Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
