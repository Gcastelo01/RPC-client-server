import grpc
from concurrent import futures
import centralserver_pb2
import centralserver_pb2_grpc

class CentralRegistryServicer(centralserver_pb2_grpc.CentralRegistryServicer):
    def __init__(self):
        self.key_server_mapping = {}

    def Register(self, request, context):
        server_id = request.server_id
        processed_keys = 0

        for key in request.keys:
            self.key_server_mapping[key] = server_id
            processed_keys += 1

        return centralserver_pb2.RegisterResponse(processed_keys=processed_keys)

    def MapKey(self, request, context):
        key = request.key
        
        if key in self.key_server_mapping:
            server_id = self.key_server_mapping[key]
            
            return centralserver_pb2.MappingResponse(server_id=server_id)
        else:
            return centralserver_pb2.MappingResponse()

    def Terminate(self, request, context):
        return centralserver_pb2.TerminationResponse()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    centralserver_pb2_grpc.add_CentralRegistryServicer_to_server(
        CentralRegistryServicer(), server
    )
    
    server.add_insecure_port("localhost:6666")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
