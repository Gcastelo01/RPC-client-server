import grpc
import sys

import centralserver_pb2
import centralserver_pb2_grpc

from concurrent import futures
import threading

class CentralRegistryServicer(centralserver_pb2_grpc.CentralRegistryServicer):
    """Classe de serviço do servidor central. 
    
    Parâmetro stop_serv: Evento que é utilizado para demarcar a parada do servidor centralizador
    """
    
    def __init__(self, stop_serv):
        self.stop_service = stop_serv  # Serviço de parada
        self.key_server_mapping = {}  # Mapa de Chaves

    def Register(self, request, context):
        """Serviço chamado por um servidor de pares para inscrever suas chaves no servidor principal
        
        Parâmetro server_id: ID do servidor que está se registrando
        Parâmetro keys: Chaves cadastradas no servidor
        """
        
        server_id = request.server_id
        processed_keys = 0
        
        # Inscrevendo as chaves no servidor central
        for key in request.keys:
            self.key_server_mapping[key] = server_id
            processed_keys += 1

        return centralserver_pb2.RegisterResponse(processed_keys=processed_keys)

    def MapKey(self, request, context):
        """Chamada para mapear uma chave para seu servidor de pares origem, Função chamada pelo cliente do servidor central
        
        Parâmetro key: Chave a ser buscada
        """
        
        key = request.key
        
        #  Verifica se uma chave está no servidor
        if key in self.key_server_mapping:
            server_id = self.key_server_mapping[key]
            
            return centralserver_pb2.MappingResponse(server_id=server_id)
        else:
            return centralserver_pb2.MappingResponse(server_id="\n")  # Retorna quebra de linha se ela não estiver


    def Terminate(self, request, context):
        """Termina a execução do servidor Central, chamando o método de stop_service e retornando o número de chaves mapeadas para o cliente que chamou a função de término.
        """
        
        key_count = len(self.key_server_mapping)
            
        self.stop_service.set()
        return centralserver_pb2.TerminationResponse(processed_keys=key_count)


def serve():
    """Corpo principal, responsável por preparar o servidor centralizador de acordo com os parâmetros da linha de comando
    """
    
    # Verificação da quantidade correta de argumentos de entrada
    if len(sys.argv) < 2:
        print("Uso: python3 <port>")
        sys.exit(1)
    
    # Criaçaõ de servidor gRPC e thread responsável por gerir o evento de parada
    address = sys.argv[1]
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    stop_event = threading.Event()
    
    # Adicionando a classe ao servidor
    centralserver_pb2_grpc.add_CentralRegistryServicer_to_server(
        CentralRegistryServicer(stop_event), server
    )
    
    # Criando o canal e iniciando a execução
    server.add_insecure_port(f"0.0.0.0:{address}")
    
    server.start()
    stop_event.wait()
    server.stop(0)
    
if __name__ == "__main__":
    serve()
