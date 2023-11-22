import grpc
import centralserver_pb2_grpc, centralserver_pb2
import peerserver_pb2_grpc, peerserver_pb2
import sys


def run(canal, comando: str) -> bool:
    """Código do cliente responsável por enviar comandos para o servidor central. Recebe dois parâmetros 
    
    Parâmetro canal: Canal gRPC para o servidor central
    Parâmetro comando(str): Comando recebido pela entrada padrão do programa
    """
    
    stub = centralserver_pb2_grpc.CentralRegistryStub(canal)
    
    #  Comando de Término do servidor central. Termina a execução dele e do Cliente
    if comando[0] == 'T':
        response = stub.Terminate(centralserver_pb2.TerminateRequest())
        print(response.processed_keys)
        return True
    
    # Comando para buscar uma chave no servidor central 
    elif comando[0] == 'C':
        key = int(comando.split(",")[1])
        response = stub.MapKey(centralserver_pb2.KeyRequest(key=key))
        addr = response.server_id
        
        if addr != "":
            c2 = grpc.insecure_channel(addr)
            stub2 = peerserver_pb2_grpc.PeerServerStub(c2)
            
            res = stub2.Consulta(peerserver_pb2.ConsultaRequest(chave=key))
            
            print(f"{addr}:{res.conteudo}")
        
        return False
    
    else:
        return False


def main():
    """Corpo principal do cliente central. Aqui é processado o argumento de entrada e é criado o canal com o servidor central
    Enquanto são recebidos comandos via linha de comando ou stdin, o clienten continua rodando. Se acabarem os comandos do arquivo de input ou se o comando T for emitido, o sistema encerra a execução;
    """
    # MEnsagem de erro caso argumentos não tenham sido passados corretamente
    if len(sys.argv) != 2:
        print("Uso: python centralClient.py <canal>")
        sys.exit(1)
    
    # Recuperação de endereço do servidor central, que é inserido como argumento posicional 1
    addr_central = sys.argv[1]
    continuar = True 
    channel = grpc.insecure_channel(addr_central)
    
    #  Lê comandos da entrada padrão, até o usuário indicar término ou EOF
    while continuar:
        comando = input()
        continuar = not run(channel, comando)
    
    # Encerra canal de comunicação
    channel.close()
    
if __name__ == '__main__':
    main()