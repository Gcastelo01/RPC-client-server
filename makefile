# Makefile para o projeto

# Comandos para compilar os arquivos .proto
proto:
	python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. peerserver.proto
	python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=.  centralserver.proto

# Comandos para limpar arquivos intermediários
clean:
	rm *_pb2*.py

# Comando para executar o cliente de pares
run_cli_pares: proto
	python3 client.py $(arg)

# Comando para executar o servidor de pares (parte 1)
run_serv_pares_1: proto
	python3 server.py $(arg)

# Comando para executar o servidor de pares (parte 2)
run_serv_pares_2: proto
	python3 server.py $(arg) qqcoisa

# Comando para executar o servidor centralizador
run_serv_central: proto
	python3 centralizador.py $(arg)

# Comando para executar o cliente centralizador
run_cli_central: proto
	python3 centralClient.py $(arg)
