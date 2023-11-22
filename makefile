# Defina os nomes dos programas
CLIENT_PARES = client
SERV_PARES = server
SERV_CENTRAL = central_server
CLIENT_CENTRAL = central_client

# Defina as portas padrão
PORT_SERV_PARES = 5555
PORT_SERV_CENTRAL = 6666

# Regras
all: $(CLIENT_PARES) $(SERV_PARES) $(SERV_CENTRAL) $(CLIENT_CENTRAL)


run_cli_pares:
    ./$(CLIENT_PARES) $(arg)

run_serv_pares_1:
    ./$(SERV_PARES) $(PORT_SERV_PARES)

run_serv_pares_2:
    ./$(SERV_PARES) $(PORT_SERV_PARES) qqcoisa

run_serv_central:
    ./$(SERV_CENTRAL) $(PORT_SERV_CENTRAL)

run_cli_central:
    ./$(CLIENT_CENTRAL) $(arg)