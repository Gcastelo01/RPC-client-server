import grpc
import sys
import peerserver_pb2_grpc, peerserver_pb2


def run(canal, comando):
    stub = peerserver_pb2_grpc.PeerServerStub(canal)
    
    if comando[0] == 'I':
        chave, descricao = comando[2:].split(',', 1)
        response = stub.Insercao(peerserver_pb2.InsertRequest(chave=int(chave), conteudo=descricao))
        print(f"Responsta à inserção: {response}")
        
    elif comando[0] == 'C':
        chave = comando[2:]
        response = stub.Consulta(peerserver_pb2.ConsultaRequest(chave=chave))
        print(f"Responsta à consulta: {response.conteudo}")
    
    elif comando[0] == 'A':
        identificador_servico = (comando[2:].strip())
        
        response = stub.Ativacao(peerserver_pb2.AtivacaoRequest(servico=identificador_servico))
        print(f"Resultado da ativação: {response.mensagem}")

    elif comando[0] == 'T':
        response = stub.Termino( peerserver_pb2.TerminoRequest())
        print(f"Resultado do término: {response.mensagem}")
        return True 
    
    
def main():
    if len(sys.argv) != 2:
        print("Uso: python client.py <endereco_servidor>")
        sys.exit(1)

    endereco_servidor = sys.argv[1]
    with grpc.insecure_channel(endereco_servidor) as channel:
        continuar_execucao = True

        while continuar_execucao:
            comando = input("Digite um comando (I,ch,descricao | C,ch | A,servico | T): ")
            continuar_execucao = not run(channel, comando)
        
        channel.close()

if __name__ == "__main__":
    main()