import grpc
import peerserver_pb2
import peerserver_pb2_grpc

from concurrent import futures

class PeerServer(peerserver_pb2_grpc.PeerServerServicer):
    
    def __init__(self) -> None:
        self.chavesEValores = {}
        
    def Insercao(self, request, context):
        chave = request.chave
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
        servico = request.servico
        return peerserver_pb2.AtivacaoResponse(mensagem=f"Serviço {servico} ativado!")


    def Termino(self, request, context):
        
        return peerserver_pb2.TerminoResponse(mensagem="Servidor encerrado.")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    peerserver_pb2_grpc.add_PeerServerServicer_to_server(PeerServer(), server)
    
    server.add_insecure_port('localhost:8888')
    server.start()
    server.wait_for_termination()
    
if __name__ == '__main__':
    serve()
        