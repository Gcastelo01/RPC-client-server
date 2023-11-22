import grpc
import centralserver_pb2_grpc, centralserver_pb2
import peerserver_pb2_grpc, peerserver_pb2
import sys

def run(canal, comando: str):
    stub = centralserver_pb2_grpc.CentralRegistryStub(canal)
    
    if comando[0] == 'T':
        response = stub.Terminate(centralserver_pb2.TerminateRequest())
        print(response.processed_keys)
        return True
    
    elif comando[0] == 'C':
        key = int(comando.split(",")[1])
        response = stub.MapKey(centralserver_pb2.KeyRequest(key=key))
        addr = response.server_id
        
        if addr != "":
            c2 = grpc.insecure_channel(addr)
            stub2 = peerserver_pb2_grpc.PeerServerStub(c2)
            
            res = stub2.Consulta(peerserver_pb2.ConsultaRequest(chave=key))
            
            print(f"{addr}:{res.conteudo}")
                
    else:
        pass

def main():
    if len(sys.argv) != 2:
        print("Uso: python centralClient.py <canal>")
        sys.exit(1)
    
    addr_central = sys.argv[1]
    continuar = True
    channel = grpc.insecure_channel(addr_central)
    
    while continuar:
        comando = input("Digite um comando (T | C,ch): ")
        continuar = not run(channel, comando)
    
    channel.close()
    
if __name__ == '__main__':
    main()