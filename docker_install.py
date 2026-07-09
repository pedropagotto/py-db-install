#!/usr/bin/env python3
"""
Database PG - Instalador de Docker para Debian/Ubuntu
Instala e configura o Docker CE e adiciona o usuário informado aos grupos apropriados.
Uso: sudo python docker_install.py --help
"""

import argparse
import getpass
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


def get_codename():
    """Obtém o codinome da distribuição."""
    try:
        with open("/etc/os-release") as f:
            for line in f:
                if line.startswith("VERSION_CODENAME="):
                    return line.split("=")[1].strip().strip('"').strip("'")
    except Exception:
        pass
    
    # Fallback para lsb_release
    try:
        result = subprocess.run(
            ["lsb_release", "-cs"],
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except FileNotFoundError:
        pass
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


def install_docker(real_user, skip_install=False, skip_reboot=False):
    """Instala o Docker no Debian/Ubuntu."""
    if skip_install:
        print("[INFO] Pulando instalação física do Docker (--skip-install).")
        return True

    os_type = detect_os()
    if os_type is None:
        print("[ERRO] Sistema operacional não suportado. Apenas Debian e Ubuntu são suportados.")
        return False

    codename = get_codename()
    if not codename:
        print("[ERRO] Não foi possível determinar o codinome da distribuição.")
        return False

    print(f"[INFO] Sistema detectado: {os_type} ({codename})")
    print(f"[INFO] Configurando Docker para o usuário: {real_user}")

    # Atualiza pacotes e instala dependências básicas
    run_cmd(["apt-get", "update", "-y"])
    run_cmd(["apt-get", "install", "-y", "sudo", "ca-certificates", "curl", "gnupg", "lsb-release"])

    # Adiciona usuário ao grupo sudo se não for root
    if real_user and real_user != "root":
        run_cmd(["/usr/sbin/usermod", "-aG", "sudo", real_user], check=False)

    # Cria diretório de chaves do apt
    run_cmd(["mkdir", "-p", "/etc/apt/keyrings"])

    # Baixa e adiciona chave GPG do Docker
    gpg_url = f"https://download.docker.com/linux/{os_type}/gpg"
    gpg_file = "/etc/apt/keyrings/docker.gpg"
    
    # Remove arquivo de chave existente se houver para evitar conflitos de permissão/formato
    if os.path.exists(gpg_file):
        try:
            os.remove(gpg_file)
        except OSError:
            pass

    # Baixa a chave GPG usando curl e dearmora usando gpg
    print(f"[INFO] Baixando chave GPG do Docker de {gpg_url}...")
    curl_proc = subprocess.Popen(["curl", "-fsSL", gpg_url], stdout=subprocess.PIPE)
    gpg_proc = subprocess.Popen(["gpg", "--dearmor", "--yes", "-o", gpg_file], stdin=curl_proc.stdout)
    curl_proc.stdout.close()
    gpg_proc.communicate()

    if gpg_proc.returncode != 0:
        print("[ERRO] Falha ao adicionar chave GPG do Docker.")
        return False

    # Adiciona o repositório
    arch_result = subprocess.run(["dpkg", "--print-architecture"], capture_output=True, text=True, check=True)
    arch = arch_result.stdout.strip()
    
    repo_entry = f"deb [arch={arch} signed-by={gpg_file}] https://download.docker.com/linux/{os_type} {codename} stable"
    repo_file = "/etc/apt/sources.list.d/docker.list"
    
    print(f"[INFO] Adicionando repositório do Docker: {repo_entry}")
    with open(repo_file, "w") as f:
        f.write(repo_entry + "\n")

    # Atualiza lista de pacotes com o novo repositório
    run_cmd(["apt-get", "update", "-y"])

    # Instala o Docker CE e plugins
    run_cmd([
        "apt-get", "install", "-y",
        "docker-ce", "docker-ce-cli", "containerd.io",
        "docker-buildx-plugin", "docker-compose-plugin"
    ])

    # Habilita e inicia os serviços do Docker
    run_cmd(["/bin/systemctl", "daemon-reload"])
    run_cmd(["/bin/systemctl", "enable", "docker.service"])
    run_cmd(["/bin/systemctl", "enable", "containerd.service"])
    run_cmd(["/bin/systemctl", "start", "docker.service"])
    run_cmd(["/bin/systemctl", "start", "containerd.service"])

    # Adiciona o usuário ao grupo docker
    if real_user and real_user != "root":
        # Garante que o grupo docker existe
        run_cmd(["groupadd", "-f", "docker"])
        run_cmd(["/usr/sbin/usermod", "-aG", "docker", real_user])

    print("[SUCCESS] Instalação do Docker concluída com sucesso!")
    
    if not skip_reboot:
        print("\n==================================================")
        print("A instalação foi concluída! O sistema precisa ser reiniciado")
        print("para aplicar as novas permissões de grupo do Docker.")
        print("==================================================")
        try:
            confirm = input("Deseja reiniciar o sistema agora? (s/N): ").strip().lower()
            if confirm in ("s", "sim", "y", "yes"):
                print("[INFO] Reiniciando em 5 segundos...")
                import time
                time.sleep(5)
                run_cmd(["/bin/systemctl", "reboot"])
            else:
                print("[INFO] Reinicialização ignorada. Lembre-se de reiniciar manualmente antes de usar o Docker.")
        except (EOFError, KeyboardInterrupt):
            print("\n[INFO] Reinicialização ignorada.")
    else:
        print("[INFO] Lembre-se de reiniciar o sistema posteriormente para aplicar as permissões de grupo.")
        
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Instalador de Docker para Debian/Ubuntu"
    )
    parser.add_argument("--user", default=None, help="Nome do usuário para configurar permissões")
    parser.add_argument("--skip-install", action="store_true", help="Pula a instalação real do Docker")
    parser.add_argument("--no-reboot", action="store_true", help="Não solicita nem realiza reinicialização imediata")
    args, unknown = parser.parse_known_args()

    if os.geteuid() != 0 and not args.skip_install:
        print("[ERRO] Execute como root ou com sudo para instalar pacotes.")
        sys.exit(1)

    real_user = args.user
    if not real_user:
        default_user = os.environ.get("SUDO_USER") or getpass.getuser()
        if default_user == "root":
            default_user = ""
        
        try:
            real_user = input(f"Digite o nome do usuário para habilitar o Docker (padrão: {default_user}): ").strip()
            if not real_user:
                real_user = default_user
        except (EOFError, KeyboardInterrupt):
            print("\n[INFO] Instalação cancelada.")
            sys.exit(1)

    if not real_user:
        print("[ERRO] Nome de usuário não pode ser vazio.")
        sys.exit(1)

    success = install_docker(real_user, skip_install=args.skip_install, skip_reboot=args.no_reboot)
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
