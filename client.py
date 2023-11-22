import grpc
import sys
import peerserver_pb2_grpc, peerserver_pb2


def run(canal, comando) -> bool:
    """Código do cliente responsável por enviar comandos para o servidor de pares. Recebe dois parâmetros 
    
    Parâmetro canal: Canal gRPC para o servidor de pares
    Parâmetro comando(str): Comando recebido pela entrada padrão do programa
    """
    
    # Estabelece conexão com o Servidor de pares
    stub = peerserver_pb2_grpc.PeerServerStub(canal)
    
    # Comando para inscrição de chave no servidor de pares
    # Possui 2 parâmetros: ch - Chave inteira positiva; desc - String de descriçao
    if comando[0] == 'I':
        chave, descricao = comando[2:].split(',', 1)
        response = stub.Insercao(peerserver_pb2.InsertRequest(chave=int(chave), conteudo=descricao))
        print(f"{response}")
        return False
    
    # Comando para a busca de uma chave no servidor de pares
    # Possui 2 parâmetro: ch - Chave inteira positiva;
    elif comando[0] == 'C':
        chave = comando[2:]
        
        response = stub.Consulta(peerserver_pb2.ConsultaRequest(chave=int(chave)))
        print(f"{response.conteudo}")
        return False
    
    # Comando de Ativação - Caso a flag de ativação tenha sido passada para o servidor de pares, indica para esse o endereço do servidor central ao qual ele deve se conectar. O servidor central guarda as chaves associadas ao endereço do servidor de pares
    elif comando[0] == 'A':
        identificador_servico = (comando[2:].strip())
        
        response = stub.Ativacao(peerserver_pb2.AtivacaoRequest(servico=identificador_servico))
        print(f"{response.mensagem}")
        return False

    # Comando para encerrar a execução do servidor principal
    elif comando[0] == 'T':
        response = stub.Termino( peerserver_pb2.TerminoRequest())
        print(f"{response.mensagem}")
        return True 
    
    
def main():
    """Corpo principal do cliente central. Aqui é processado o argumento de entrada e é criado o canal com o servidor central
    Enquanto são recebidos comandos via linha de comando ou stdin, o clienten continua rodando. Se acabarem os comandos do arquivo de input ou se o comando T for emitido, o sistema encerra a execução;
    """
    
    # MEnsagem de erro caso argumentos não tenham sido passados corretamente
    if len(sys.argv) != 2:
        print("Uso: python client.py <endereco_servidor>")
        sys.exit(1)

    # Recuperação de endereço do servidor central, que é inserido como argumento posicional 1
    endereco_servidor = sys.argv[1]
    with grpc.insecure_channel(endereco_servidor) as channel:
        continuar_execucao = True

        #  Lê comandos da entrada padrão, até o usuário indicar término ou EOF
        while continuar_execucao:
            comando = input()
            continuar_execucao = not run(channel, comando)
            
        # Encerra canal de comunicação
        channel.close()

if __name__ == "__main__":
    main()