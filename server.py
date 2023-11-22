import sys
import socket
import grpc

import centralserver_pb2_grpc, centralserver_pb2
import peerserver_pb2
import peerserver_pb2_grpc

from concurrent import futures
import threading


class PeerServer(peerserver_pb2_grpc.PeerServerServicer):
    """Classe de serviço do servidor central. 
    
    Parâmetro stop_serv: Evento que é utilizado para demarcar a parada do servidor centralizador
    """
    
    def __init__(self, event_exit, runCentral, port) -> None:
        self.chavesEValores = {}  # Relação de Chaves e valores
        self.runActivate = runCentral  # Existência de Flag de ativação
        self.stop_event = event_exit  # Evento de parada da thread
        self.__port = port  # Porta na qual o servidor de pares está rodando
    
    def Insercao(self, request, context):
        """Insere uma chave e seu valor associado no servidor
        
        Parâmetro chave: Valor inteiro positivo 
        Parâmetro conteudo: String contendo conteudo a ser armazenado
        """
        chave = (request.chave)
        valor = request.conteudo
        
        # Se a chave já estiver registrada, não sobrescreve o valor e retorna -1
        if chave in self.chavesEValores:
            return peerserver_pb2.InsertResponse(resultado=-1)
        
        # Se a chave não estiver inscrita, retorna 0 e inscreve a chave
        else:
            self.chavesEValores[chave] = valor
            return peerserver_pb2.InsertResponse(resultado=0)
    
    
    def Consulta(self, request, context):
        """Consulta se uma chave existe no servidor. Caso exista, retorna o valor associado
        
        Parâmetro chave: Inteiro positivo a ser consultado
        """
        
        chave = request.chave  # Chave a ser buscada
        conteudo = self.chavesEValores.get(chave, "")  # Caso não encontre, valor associado será ""
        
        return peerserver_pb2.ConsultaResponse(conteudo=conteudo)
    
    
    def Ativacao(self, request, context):
        """Caso a flag de ativação tenha sido passada, o sistema se conecta ao servidor central e passa a relação de cahves
        
        Parâmetro servico: Endereço do servidor central
        """
        if self.runActivate:
            self.__activated = True
            
            servico = request.servico
            trem  = grpc.insecure_channel(servico)
            
            # Estabelece conexão com servidor central
            central = centralserver_pb2_grpc.CentralRegistryStub(trem)
            
            # Lista chaves a serem enviadas
            keys_to_register = list(self.chavesEValores.keys())
            
            id_server = f"{socket.getfqdn()}:{self.__port}"
            
            # Envia chaves e o prórprio endereço
            response = central.Register(centralserver_pb2.ServerInfo(server_id=id_server, keys=keys_to_register))

            return peerserver_pb2.AtivacaoResponse(mensagem=response.processed_keys)
        
        else:
            return peerserver_pb2.AtivacaoResponse(mensagem=0)


    def Termino(self, request, context):
        """Termina a execuçaõ do servidor e retorna 0
        """
        response = peerserver_pb2.TerminoResponse(mensagem=0)
        
        self.stop_event.set()
        return response


def serve():
    """Corpo principal, responsável por preparar o servidor de pares de acordo com os parâmetros da linha de comando
    """
    
    # verifica se quantidade correta de args foi passada 
    if len(sys.argv) < 2 or len(sys.argv) > 4:
        print("Uso: python3 server.py <port> <flag>")
        sys.exit(1)
    
    # Preparação caso não haja flag
    elif len(sys.argv) == 2:
        address = sys.argv[1]
        activate = False
    
    # Preparação caso haja flag
    else:
        address = sys.argv[1]
        activate = True
        
    stop_event = threading.Event()
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    peer_server = PeerServer(stop_event, activate, address)
    
    peerserver_pb2_grpc.add_PeerServerServicer_to_server(peer_server, server)
    
    server.add_insecure_port(f'0.0.0.0:{address}')
    
    server.start()
    stop_event.wait()
    server.stop(0)

    
if __name__ == '__main__':
    serve()
