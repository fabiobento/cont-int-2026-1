# Docker com X11 Forwarding via SSH

Como rodar containers com interface gráfica em máquinas remotas acessadas por `ssh -X`.

---

## Como funciona

Quando você faz `ssh -X usuario@servidor`, o SSH cria um display virtual (ex: `localhost:12.0`) na máquina remota. Esse display encaminha janelas gráficas de volta para sua máquina local. Containers Docker não herdam esse display automaticamente — você precisa passar as credenciais X11 explicitamente.

> **Atenção:** `xhost +` falha em sessões SSH porque o X server não é local. Use o método de cookie descrito abaixo.

---

## Passo 1 — Build da imagem

```bash
docker build \
  --build-arg USER_UID=$(id -u) \
  --build-arg USER_GID=$(id -g) \
  -t minha_imagem .
```

---

## Passo 2 — Verificar o display e o cookie

Na máquina remota, antes de iniciar o container:

```bash
# Ver o display criado pela sessão SSH
echo $DISPLAY
# Saída esperada: localhost:12.0

# Ver os cookies de autenticação X11
xauth list
# Saída esperada:
# odin/unix:12  MIT-MAGIC-COOKIE-1  f2aa9349d6ed7b8948bc61c3c5478bd7
```

Identifique o cookie cujo número bate com o do seu `$DISPLAY` (ex: `unix:12` → `localhost:12.0`).

---

## Passo 3 — Exportar o cookie para um arquivo

```bash
# Extrair o cookie do display correto para um arquivo temporário
xauth extract ~/tmp/xauth_docker localhost:12

# Garantir que o container consiga ler o arquivo
chmod 644 ~/tmp/xauth_docker
```

> Ajuste o número `:12` conforme o seu `$DISPLAY`.

---

## Passo 4 — Iniciar o container

```bash
docker run -it --rm \
  --name meu_container \
  --net=host \
  --ipc=host \
  -e DISPLAY=$DISPLAY \
  -v ~/tmp/.X11-unix:/tmp/.X11-unix:rw \
  -v ~/tmp/xauth_docker:/tmp/.xauth_docker:ro \
  -e XAUTHORITY=/tmp/.xauth_docker \
  minha_imagem
```

O que cada flag faz:

| Flag | Função |
|------|--------|
| `--net=host` | Usa a rede do host — necessário para `localhost:N` funcionar dentro do container |
| `-e DISPLAY` | Passa o display SSH para dentro do container |
| `-v ~/tmp/.X11-unix` | Monta o socket X11 no container |
| `-v ~/tmp/xauth_docker` | Monta o arquivo de cookie de autenticação |
| `-e XAUTHORITY` | Aponta para o cookie dentro do container |

---

## Passo 5 — Verificar dentro do container

```bash
# Confirmar que o display está correto
echo $DISPLAY
# deve ser localhost:12.0

# Confirmar que o cookie está acessível
cat ~/tmp/.xauth_docker | od -An -tx1 | head
# deve mostrar bytes, não um erro de permissão

# Teste rápido — deve abrir uma janelinha de relógio
xclock
```

Se o `xclock` abrir, o X11 está funcionando e qualquer aplicação gráfica (Gazebo, RViz, etc.) vai carregar normalmente.

---

## Solução de problemas

**`X11 connection rejected because of wrong authentication`**

O cookie não chegou corretamente ao container. Verifique:
- Se o `chmod 644 /tmp/xauth_docker` foi executado antes de subir o container.
- Se o arquivo montado não está vazio (`cat /tmp/.xauth_docker` deve retornar bytes).

**`Can't open display: localhost:12.0`**

O socket X11 não está montado ou falta o `--net=host`. Sem `--net=host`, o container não consegue rotear para o display `localhost:N` criado pelo SSH.

**`must be on local machine` ao rodar `xhost`**

`xhost` só funciona no X server local. Em sessões SSH, use sempre o método de cookie (`xauth extract`) descrito neste tutorial.

**`xauth: command not found` dentro do container**

Nem todo container tem `xauth` instalado. Por isso usamos `xauth extract` fora e montamos o arquivo diretamente — não é necessário ter `xauth` dentro do container.

---

## Referência rápida — comandos essenciais

```bash
# Na máquina remota (fora do container)
echo $DISPLAY                                          # ver display atual
xauth list                                             # listar cookies
xauth extract /tmp/xauth_docker localhost:<N>          # exportar cookie
chmod 644 /tmp/xauth_docker                            # liberar leitura

# Subir o container
docker run -it --rm \
  --net=host --ipc=host \
  -e DISPLAY=$DISPLAY \
  -v ~/tmp/.X11-unix:/tmp/.X11-unix:rw \
  -v ~/tmp/xauth_docker:/tmp/.xauth_docker:ro \
  -e XAUTHORITY=/tmp/.xauth_docker \
  minha_imagem

# Dentro do container
echo $DISPLAY && echo $XAUTHORITY   # verificar variáveis
xclock                               # testar X11
```