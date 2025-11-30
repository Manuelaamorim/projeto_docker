O projeto é uma coleção de 5 desafios progressivos que mostram conceitos de containerização e arquitetura distribuída. 

Desafio 1 — Rede entre containers: comunicação básica entre dois containers (servidor + cliente).

Desafio 2 — Volumes e persistência: persistir dados com volumes Docker usando SQLite.

Desafio 3 — Docker Compose: orquestração de web + DB + cache (Postgres + Redis) com docker compose.

Desafio 4 — Microsserviços independentes: dois serviços que se comunicam via HTTP (sem gateway).

Desafio 5 — Microsserviços + API Gateway: dois microsserviços (users, orders) e um gateway como ponto único de entrada.

A solução foi implementada com Python + Flask para APIs, Docker / Docker Compose para empacotamento e orquestração, SQLite/Postgres para persistência e Redis para cache (no Desafio 3). Cada serviço tem seu próprio Dockerfile para garantir isolamento.

Obs: é necessário entrar na pasta "docker" para conseguir entrar nas pastas do desafio.


# Desafio 1 — Containers em Rede


- **server/server.py**: Servidor Flask que responde a requisições HTTP.
- **client/client.sh**: Script que realiza requisições HTTP para o servidor em loop.
- **Dockerfile (server)**: Configura a imagem do servidor com Python e Flask.
- **Dockerfile (client)**: Configura a imagem do cliente com Alpine e `curl`.

## Fluxo
server (Flask) roda em porta 8080 no container server.

client é um container Alpine que executa client.sh (loop com curl http://server:8080).

Ambos são conectados a desafio1-net.

client lê a resposta e escreve no stdout, que é visível via docker logs client.

O que demonstra: resolução de nome do container na rede Docker, comunicação HTTP entre containers e visualização de logs.

## Decisões Técnicas  
Flask no servidor: escolha leve e simples para expor um endpoint HTTP.

Alpine no cliente: garante uma imagem mínima, rápida e com curl pré-instalado.

Rede Docker customizada (desafio1-net): permite comunicação via hostname (server), simulando um ambiente distribuído.

Dois Dockerfiles separados: reforça o conceito de isolamento por serviço.

Uso de docker logs client: demonstra saída contínua do cliente consumindo o servidor.

---

## Como Rodar

```bash
# 1. Entre na pasta desafio1 para criar a rede Docker customizada
docker network create desafio1-net

# 2. Build da imagem do servidor
docker build -t d1-server -f Dockerfile.server .

# 3. Build da imagem do cliente
docker build -t d1-client -f Dockerfile.client .

# 4. Rodar o container do servidor
docker run -d --network desafio1-net --name server d1-server

# 5. Rodar o container do cliente
docker run -d --network desafio1-net --name client d1-client

# 6. Verificar logs do cliente
docker logs client
````



# Desafio 2 — Volumes e Persistência


- **app.py**: Script Python que cria um banco SQLite, insere dados aleatórios e imprime os registros.
- **Dockerfile**: Imagem Python configurada para rodar o `app.py`.

## Fluxo
Imagem d2-image roda app.py que cria data.db em /data.

Container montado com -v desafio2-volume:/data grava data.db no volume.

Insere um novo aluno a cada execução

Lê e exibe os registros persistidos

docker rm d2-db remove container

Rodando novo container com o mesmo volume lê/insere novos registros no mesmo data.db.

Resultado mostra crescimento da tabela a cada execução, provando persistência.

## Decisões Técnicas  
SQLite: banco de arquivo simples, ideal para demonstrar persistência via volume.

Criação automática da tabela: evita necessidade de comandos manuais.

Cada execução mostra o aumento da tabela → prova visual de persistência.

---

## Como Rodar

```bash
# 1. Entre na pasta desafio 2 para criar um volume Docker para persistência
docker volume create desafio2-volume

# 2. Build da imagem do container
docker build -t d2-image .

# 3. Rodar o container com volume montado
docker run --name d2-db -v desafio2-volume:/data d2-image

# 4. Apagar o container
docker rm d2-db

# 4. Rodar novamente o container (mesmo volume)
docker run --name d2-db -v desafio2-volume:/data d2-image

````



# Desafio 3 — Docker Compose Orquestrando Serviços


- **web/app.py**: API Flask que consulta dados no PostgreSQL e usa Redis como cache.
- **web/requirements.txt**: Dependências do Python (`Flask`, `psycopg2-binary`, `redis`).
- **web/Dockerfile**: Imagem do serviço web.
- **docker-compose.yml**: Orquestração dos 3 serviços com rede interna e volumes.

## Fluxo
docker compose up --build cria serviços: web, db (Postgres), cache (Redis).

Ao inicializar, web espera alguns segundos (time.sleep) para o DB disponibilizar.

Requisição GET / ao web:

tenta ler contador do Redis (cache.get("contador")).

se ausente, assume 0.

incrementa contador e grava novamente no Redis.

registra no Postgres uma linha em logs com a mensagem do acesso.

Endpoint /log consulta Postgres e retorna histórico.

## Decisões Técnicas
Docker Compose escolhido para orquestrar serviços dependentes (web, DB e cache).

PostgreSQL usado por ser um banco real e robusto.

Redis utilizado como cache simples demonstrando camadas de arquitetura.

depends_on garante ordem básica de inicialização.

Espera ativa no web (time.sleep) contorna tempo de inicialização do banco.

Volumização do Postgres mantém dados após recriação.

---

## Como Rodar

```bash
# 1. Entre na pasta desafio3 e execute:
docker-compose up --build -d

# 2. Verificar logs do serviço web
docker compose logs -f web

# 3. Testar endpoints da API
# Listar todos os alunos
http://localhost:5000/todos

# Consultar aluno específico
http://localhost:5000/aluno/1 (trocar o id (2,3) para consultar outros alunos)

````



# Desafio 4 - Microsserviços Independentes


- **Service A — Fornece lista de usuários**
  
  Porta: 5001  
  
  Endpoint principal: /usuarios  
  
  Retorna JSON com usuários  

- **Service B — Consume Service A**
  Porta: 7000
  
  Endpoint principal: /info  
  
  Faz requisição HTTP para Service A usando:  
  
  http://service_a:5001/usuarios  

## Fluxo
service_a expõe /usuarios (porta 5001).

service_b expõe /info (porta 7000) e faz requests.get("http://service_a:5001/usuarios").

Compose garante service_b consegue resolver o hostname service_a.

service_b transforma a lista retornada em frases “Usuário X (Y anos) - ativo desde 2023”.

## Decisões Técnicas  
Dois serviços independentes, cada um com seu Dockerfile.

Comunicação via HTTP usando requests.

Hostnames resolvidos via Compose (service_a).

---

## Como rodar

```bash
# 1. Entre na pasta desafio4 e execute:
docker compose up --build

# 2. Testar service A
http://localhost:5001/usuarios

# 3. Testar service B
http://localhost:7000/info


````



# Desafio 5 - Microsserviços com API Gateway

- **Users Service (fornece usuários)**

- **Orders Service (fornece pedidos)**

- **Gateway**

## Fluxo
users_service em 5003 fornece /users.

orders_service em 5002 fornece /orders.

gateway em 5004 tem endpoints /users e /orders e:

repassa as chamadas internamente para http://users_service:5003/users e http://orders_service:5002/orders.

retorna resultados

Gateway atua como ponto único de entrada

## Decisões Técnicas  
Gateway centraliza o acesso

Comunicação interna via hostnames:

users_service

orders_service

Cada microsserviço é completamente isolado (Dockerfile próprio).

---

# Como rodar

```bash
# 1. Entre na pasta desafio5 e execute:
docker compose up --build

# 2. Testando Endpoints:
http://localhost:5003/users
http://localhost:5002/orders

# 3. Gateways
http://localhost:5004/users
http://localhost:5004/orders


````

# Tecnologias Utilizadas
Docker	

Docker Compose	

Python 3.10	 

Flask	 

Requests	

SQLite / Postgres	 

Redis


