# Database PG - Backup e Restore para PostgreSQL

Projeto simples em Python para facilitar backups e restores de bancos de dados PostgreSQL, suportando cenários com Docker e servidores bare-metal.

## Objetivo
- Portátil: pode ser copiado e executado em qualquer máquina com Python 3.
- Suporta 3 cenários principais:
  1. Backup de container Docker → arquivo local → Restore em servidor PostgreSQL sem container.
  2. Backup de container Docker → Restore direto em outro container Docker.
  3. Backup de servidor PostgreSQL sem container → Restore em outro servidor sem container.

## Ferramenta Principal All-in-One (pg_main.py)
O script `pg_main.py` é o entrypoint principal da ferramenta unificada. Ele permite escolher interativamente qual operação executar ou acionar as ações diretamente via argumentos de linha de comando.

Para maior facilidade e rapidez, o projeto conta com suporte a **Make**. Para iniciar o menu interativo de escolha, basta executar:

```bash
make start
```

Ou de forma tradicional:

```bash
python3 pg_main.py
```

### Comandos de Atalho (Makefile):
Se preferir, utilize os comandos simplificados via `make` para agilizar a execução de tarefas comuns:
- `make start` : Inicia o menu interativo (`pg_main.py`).
- `make install-postgres` : Executa o instalador do PostgreSQL (requer sudo).
- `make install-docker` : Executa o instalador do Docker CE (requer sudo).
- `make install-kamal` : Executa o instalador do Kamal (requer sudo).
- `make install-all` : Executa o instalador All-in-One completo (requer sudo).
- `make backup-restore` : Executa a ferramenta de Backup/Restore.
- `make help` : Exibe a lista de comandos do Makefile disponíveis.

### Menu Interativo:
- `1` → **Backup / Restore de PostgreSQL** (`pg_backup_restore.py`)
- `2` → **Instalar PostgreSQL** completo pronto para produção (`pg_install.py`)
- `3` → **Instalar Docker CE** de forma otimizada (`docker_install.py`)
- `4` → **Instalar Kamal** via Ruby/gem (`kamal_install.py`)
- `5` → **Instalação Completa All-in-One (AIO)**: Instala e configura Docker, Kamal e PostgreSQL sequencialmente, realizando testes de conexão e sugerindo reinicialização ao final.
- `0` → **Sair**

### Atalhos via Linha de Comando (CLI):
Para facilitar a automação em servidores limpos (bare-metal ou VPS), você pode chamar as rotinas diretamente passando argumentos:
- `--all` / `--install-all` / `-aio` : Executa o assistente de instalação completo All-in-One.
- `--postgres` / `--install-postgres` : Executa diretamente o instalador do PostgreSQL.
- `--docker` / `--install-docker` : Executa diretamente o instalador do Docker.
- `--kamal` / `--install-kamal` : Executa diretamente o instalador do Kamal.
- `backup` / `restore` / `--backup-restore` : Repassa os argumentos diretamente para a ferramenta de backup e restore.

*Qualquer argumento extra fornecido (ex: `--skip-install`, `--user`, `--password`) será repassado de forma inteligente para os instaladores correspondentes.*

## Instalação do PostgreSQL (Debian/Ubuntu)
O script `pg_install.py` automatiza a instalação completa do PostgreSQL em servidores Debian ou Ubuntu, garantindo que esteja pronto para produção:

```bash
sudo python3 pg_install.py
```

Opções:
- `--user NOME` : nome do usuário (padrão: postgres_app)
- `--database NOME` : nome do banco (padrão: app_db)
- `--password SENHA` : senha customizada (será solicitada interativamente se omitida; gerada aleatória se deixada vazia)
- `--skip-install` : pula instalação (útil para configurar apenas usuário/banco)

Ao final, o script:
- Imprime as credenciais (usuário, senha, host, porta, banco)
- Realiza o teste padrão de conexão com `SELECT 1` para confirmar o funcionamento
- Oferece a opção de executar um **teste de conexão personalizado** (solicitando host, porta, usuário, senha e banco)

**Nota**: Execute sempre com `sudo`. A senha gerada é exibida apenas uma vez.

## Instalação do Docker CE (Debian/Ubuntu)
O script `docker_install.py` instala e configura de forma otimizada para produção o Docker Engine, containerd e plugins do Docker Compose no Debian ou Ubuntu:

```bash
sudo python3 docker_install.py
```

Funcionalidades:
- Detecta a distribuição de forma nativa e adiciona os repositórios oficiais e chaves GPG corretas.
- Solicita interativamente o usuário do sistema (com detecção do usuário que executou o `sudo`) para adicioná-lo aos grupos `docker` e `sudo`, evitando o uso direto do root.
- Gerencia o processo de reboot opcional e amigável.

## Instalação do Kamal (Debian/Ubuntu)
O script `kamal_install.py` automatiza a preparação do ambiente Ruby e instala o Kamal:

```bash
sudo python3 kamal_install.py
```

Funcionalidades:
- Instala a versão completa do Ruby (`ruby-full`) e as ferramentas essenciais de compilação de extensões nativas (`build-essential`, `libssl-dev`, etc.).
- Instala a gem `kamal` de forma global e limpa.

## Instalação Completa All-in-One (AIO)
A ferramenta permite a instalação coordenada e limpa de todos os recursos de uma só vez:

```bash
sudo python3 pg_main.py --all
```
Ou escolhendo a opção `5` no menu principal.

A instalação All-in-One realiza:
1. Instalação e configuração completa do Docker CE sem forçar um reboot imediato.
2. Instalação e configuração do Ruby, pacotes de compilação essenciais e Kamal.
3. Instalação do PostgreSQL completo pronto para produção com criação de usuário/banco e testes de conexão.
4. Sugestão amigável de reinicialização do sistema no fim de todo o fluxo.

## Requisitos
- Python 3.8+
- Ferramentas PostgreSQL instaladas localmente (`pg_dump`, `pg_restore`, `psql`) OU Docker CLI (para cenários com containers)
- Acesso ao Docker daemon (se usar containers)
- Conexão de rede aos servidores de banco (se remotos)

## Instalação em Servidor Limpo
Para instalar e usar a ferramenta `py-db-install` em um servidor limpo (recomendado Debian/Ubuntu):

1. Instale as dependências básicas (Python e git):

```bash
sudo apt update
sudo apt install -y python3 python3-pip git
```

2. Clone o repositório diretamente do GitHub:

```bash
git clone https://github.com/pedropagotto/py-db-install.git
cd py-db-install
```

*(Substitua a URL pelo endereço real do seu repositório. Alternativamente, baixe o ZIP via GitHub e extraia os arquivos.)*

3. Nenhuma instalação via pip é necessária — o projeto usa apenas a biblioteca padrão do Python (sem dependências externas, conforme `requirements.txt`).

4. Execute a ferramenta utilizando o Make (ou diretamente com Python):

```bash
make start
```

Ou de forma tradicional:

```bash
python3 pg_main.py
```

Ou invoque os scripts diretamente:

```bash
python3 pg_install.py --help
python3 pg_backup_restore.py --help
```

**Nota sobre distribuição**: Atualmente o uso é via clone ou download manual. No futuro, será possível instalar com `pip install git+https://github.com/...` após adicionar `pyproject.toml`.

## Estrutura do Projeto
```
py-db-install/
├── README.md              # Documentação unificada do projeto
├── Makefile               # Atalhos para comandos comuns (make start, make install-all, etc.)
├── requirements.txt       # Requisitos (vazio, pois o projeto usa apenas a biblioteca padrão)
├── config.example.json    # Exemplo de configuração para backup/restore
├── docker_install.py      # Instalador de Docker CE otimizado para Debian/Ubuntu
├── kamal_install.py       # Instalador de Ruby e Kamal
├── pg_install.py          # Instalador completo do PostgreSQL para Debian/Ubuntu
├── pg_backup_restore.py   # Script de Backup e Restore (Docker ou Bare-Metal)
├── pg_main.py             # Entrypoint da ferramenta interativa e direta All-in-One
└── .env.example           # Exemplo de variáveis de ambiente para credenciais
```

## Como Usar

### 1. Configuração
Copie `config.example.json` para `config.json` e preencha os dados.

Ou use variáveis de ambiente / argumentos CLI.

### 2. Executar Backup
```bash
python pg_backup_restore.py backup --source-type docker --source-container meu_postgres --source-db minha_db --backup-file backup.sql
```

### 3. Executar Restore
```bash
python pg_backup_restore.py restore --target-type local --target-host localhost --target-db minha_db --backup-file backup.sql
```

### Exemplos de Cenários

**Cenário 1: Docker → Local file → Servidor bare-metal**
```bash
# Backup
python pg_backup_restore.py backup --source-type docker --source-container pg_source --source-db appdb --backup-file /tmp/backup.dump --format custom

# Restore
python pg_backup_restore.py restore --target-type local --target-host 192.168.1.100 --target-port 5432 --target-db appdb --target-user postgres --backup-file /tmp/backup.dump --format custom
```

**Cenário 2: Docker → Docker**
```bash
python pg_backup_restore.py backup-restore \
  --source-type docker --source-container pg_a --source-db db1 \
  --target-type docker --target-container pg_b --target-db db2
```

**Cenário 3: Servidor → Servidor (bare-metal)**
```bash
python pg_backup_restore.py backup-restore \
  --source-type local --source-host db1.example.com --source-db production \
  --target-type local --target-host db2.example.com --target-db staging
```

## Segurança
- Nunca armazene senhas em texto plano. Use variáveis de ambiente (`PGPASSWORD`) ou `.pgpass`.
- O script suporta passagem de senha via variável de ambiente.

## Desenvolvimento
O projeto usa apenas a biblioteca padrão do Python para máxima portabilidade.

## Licença
MIT
