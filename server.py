import grpc
import centralserver_pb2_grpc, centralserver_pb2
import peerserver_pb2
import peerserver_pb2_grpc
import sys
import socket

from concurrent import futures
import threading

class PeerServer(peerserver_pb2_grpc.PeerServerServicer):
    
    def __init__(self, server, event_exit, runCentral, port) -> None:
        self.chavesEValores = {}
        self.server = server
        self.runActivate = runCentral
        self.stop_event = event_exit
        self.central = 0
        self.__activated = False
        self.__port = port
    
    def Insercao(self, request, context):
        chave = (request.chave)
        valor = request.conteudo
        
        if chave in self.chavesEValores:
            return peerserver_pb2.InsertResponse(resultado=-1)
        
        else:
            self.chavesEValores[chave] = valor
            return peerserver_pb2.InsertResponse(resultado=0)
    
    
    def Consulta(self, request, context):
        chave = request.chave
        conteudo = self.chavesEValores.get(chave, "")
        
        return peerserver_pb2.ConsultaResponse(conteudo=conteudo)
    
    
    def Ativacao(self, request, context):
        if self.runActivate and not self.__activated:
            self.__activated = True
            
            servico = request.servico
            trem  = grpc.insecure_channel(servico)
            
            self.central = centralserver_pb2_grpc.CentralRegistryStub(trem)
            
            keys_to_register = list(self.chavesEValores.keys())
            
            id_server = f"localhost:{self.__port}"
            
            response = self.central.Register(centralserver_pb2.ServerInfo(server_id=id_server, keys=keys_to_register))

            return peerserver_pb2.AtivacaoResponse(mensagem=response.processed_keys)
        else:
            return peerserver_pb2.AtivacaoResponse(mensagem=0)


    def Termino(self, request, context):
        response = peerserver_pb2.TerminoResponse(mensagem=0)
        
        self.stop_event.set()
        return response


def serve():
    if len(sys.argv) < 2 or len(sys.argv) > 4:
        print("Uso: python3 server.py <port> <flag>")
        sys.exit(1)
    
    elif len(sys.argv) == 2:
        address = sys.argv[1]
        activate = False
    
    else:
        address = sys.argv[1]
        activate = True
        
    stop_event = threading.Event()
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    peer_server = PeerServer(server, stop_event, activate, address)
    
    peerserver_pb2_grpc.add_PeerServerServicer_to_server(peer_server, server)
    
    server.add_insecure_port(f'localhost:{address}')
    
    server.start()
    stop_event.wait()
    server.stop(0)

    
if __name__ == '__main__':
    serve()
