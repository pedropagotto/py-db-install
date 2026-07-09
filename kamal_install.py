#!/usr/bin/env python3
"""
Database PG - Instalador de Kamal para Debian/Ubuntu
Instala o Ruby, dependências de compilação e a gem Kamal.
Uso: sudo python kamal_install.py --help
"""

import argparse
import os
import subprocess
import sys


def detect_os():
    """Detecta se é Debian ou Ubuntu."""
    try:
        with open("/etc/os-release") as f:
            content = f.read().lower()
        if "ubuntu" in content:
            return "ubuntu"
        elif "debian" in content:
            return "debian"
        else:
            return None
    except FileNotFoundError:
        return None


def run_cmd(cmd, check=True, capture_output=False, env=None):
    """Executa comando com output amigável."""
    print(f"[INFO] Executando: {' '.join(cmd)}")
    result = subprocess.run(
        cmd,
        check=check,
        capture_output=capture_output,
        text=True,
        env=env or os.environ.copy()
    )
    if capture_output:
        return result.stdout.strip()
    return None


def install_kamal(skip_install=False):
    """Instala o Ruby e a gem Kamal."""
    if skip_install:
        print("[INFO] Pulando instalação física do Kamal (--skip-install).")
        return True

    os_type = detect_os()
    if os_type is None:
        print("[ERRO] Sistema operacional não suportado. Apenas Debian e Ubuntu são suportados.")
        return False

    print(f"[INFO] Sistema detectado: {os_type}")
    print("[INFO] Iniciando instalação do Kamal...")

    # Atualiza pacotes
    run_cmd(["apt-get", "update", "-y"])

    # Instala Ruby e dependências de compilação
    print("[INFO] Instalando ruby-full e dependências de compilação...")
    run_cmd([
        "apt-get", "install", "-y",
        "ruby-full", "build-essential", "libssl-dev", "libreadline-dev", "zlib1g-dev"
    ])

    # Verifica versões instaladas
    try:
        ruby_ver = run_cmd(["ruby", "-v"], capture_output=True)
        print(f"[INFO] Versão do Ruby: {ruby_ver}")
        gem_ver = run_cmd(["gem", "-v"], capture_output=True)
        print(f"[INFO] Versão do Gem: {gem_ver}")
    except Exception as e:
        print(f"[AVISO] Não foi possível verificar as versões do Ruby/Gem: {e}")

    # Instala Kamal via gem
    print("[INFO] Instalando a gem Kamal...")
    run_cmd(["gem", "install", "kamal"])

    print("[SUCCESS] Kamal instalado com sucesso via gem!")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Instalador de Kamal para Debian/Ubuntu"
    )
    parser.add_argument("--skip-install", action="store_true", help="Pula a instalação real do Kamal")
    args, unknown = parser.parse_known_args()

    if os.geteuid() != 0 and not args.skip_install:
        print("[ERRO] Execute como root ou com sudo para instalar pacotes.")
        sys.exit(1)

    success = install_kamal(skip_install=args.skip_install)
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
