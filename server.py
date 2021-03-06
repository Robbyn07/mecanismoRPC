from concurrent import futures

import grpc
import time

import proto.chat_pb2 as chat
import proto.chat_pb2_grpc as rpc

class ChatServer(rpc.ChatServerServicer):  

    def __init__(self):
        self.chats = []

    def ChatStream(self, request_iterator, context):
        """
        This is a response-stream type call. This means the server can keep sending messages
        Every client opens this connection and waits for server to send new messages

        :param request_iterator:
        :param context:
        :return:
        """
        lastindex = 0
       
        while True:
            
            while len(self.chats) > lastindex:
                n = self.chats[lastindex]
                lastindex += 1
                yield n

    def SendNote(self, request: chat.Note, context):
        """
        This method is called when a clients sends a Note to the server.

        :param request:
        :param context:
        :return:
        """
        print("[{}] {}".format(request.name, request.message))
        
        self.chats.append(request)
        return chat.Empty()  


if __name__ == '__main__':
    port = 11912  
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))  
    rpc.add_ChatServerServicer_to_server(ChatServer(), server)  
    
    print('Starting server. Listening...')
    server.add_insecure_port('[::]:' + str(port))
    server.start()
    
    while True:
        time.sleep(64 * 64 * 100)
