import http.client
import time
from .crypt import Crypt


def send_client_request(type="GET", url="empty", body="", receiver="", timeout=3.0):
    """ Sends a request to another node/server.
        Params:
            @type       - The restful api type (get/put/post..).
            @url        - The url that should correspond to this request.
            @body       - The message body to send.
            @receiver   - The server address which will receive this request.
            @timeout    - The request timeout in seconds 
                        (should be applied in case server can't be reached).
        Returns the status code and message reply as a tuple (code, msg),
         or (None, None) on error. """
    try:
        conn = http.client.HTTPConnection(receiver, timeout=timeout)
        conn.request(type, url, body)
        resp = conn.getresponse()
        conn.close()
        content = resp.read().decode()

        return resp.status, content

    except Exception as e:
        print(e)
    
    return None, None


class Client():
    """ Client class to request and communicate with a sneaksmc coordinator. """
    def __init__(self) -> None:
        self.ck = Crypt()
        self.coordinator_node = None
    
    def request_analysis(self, coordinator_node):
        """ Sends a request to start an analysis operation to the given coordinator address node.
            Returns (response-code, response-msg) tuple from coordinator node. Raises exception on error. """
        self.coordinator_node = coordinator_node
        pub_key = Crypt.key2string(self.ck.get_public_key())

        # Send start analysis request to the coordinator node.
        # If the node is not coordinator then the request is dropped.
        # Sends its public key as the result will be encrypted
        r = send_client_request(type="GET", url="/start_analysis", body=pub_key, 
                                    receiver=self.coordinator_node, timeout=3.0)
        return r
        
    
    def get_result(self, id, tries=100, ms=50):
        """ Sends http request to coordinator node for the result of a requested analysis operation.
            Returns the result (if received) (response-code, response-msg) tuple, otherwise if not received, 
            returns from last message sent. Raises exception on error.
            Returns immediately if given operation_id is not valid.
            Params:
                @tries  : Max number of get-requests sent until giving up
                @ms     : Sleep in ms between each request try. """

        if self.coordinator_node == None:
            raise Exception("No SMC request has been sent to coordinator.")
        if tries <= 0 or ms < 0:
            raise Exception("Invalid arguments tries=%d, ms=%d given." % (tries, ms))
        if id <= 0:
            raise Exception("Invalid id (%d) given." % id)

        #pub_key = Crypt.key2string(self.ck.get_public_key())
        response_code = 408
        response_msg = "Response timeout"

        # Request the result from coordinator. Asks every @ms until it receives the result.
        for i in range(0, tries):
            r = send_client_request(type="GET", url="/get_result", body=str(id), 
                                    receiver=self.coordinator_node, timeout=3.0)
            response_code = r[0]
            response_msg = r[1]
            if response_code  != 102:
                # Server done processing request
                break
            
            time.sleep(0.001*ms)
        
        return (response_code, response_msg)
    
    def shutdown(self):
        # TODO: ask to shutdown all smc servers
        pass
