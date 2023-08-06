#!/usr/bin/python3
import json
import signal
import socketserver
import threading
import argparse
import random
from http.server import BaseHTTPRequestHandler,HTTPServer
from os import getcwd
import os
from .crypt import Crypt
from .client import send_client_request

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
# Certificate file is a file that is only used by the coordinator node.
# It consists of all the other node's certificates (ip address + public key).
certificate_file = __location__+"/.certificates.txt"


_server_connected_ips = []              # List to cache ips/addresses of other nodes in the distributed network
_server_auto_shutdown = 60*60*128       # seconds until automatic shutdown
_server_ip = None
_server_port = None
_server_address = None
_server_nodefile = None
_server_iscoordinator = False
_server_coordinator_addr = None
ck = Crypt()
# Latest analysis result stored here
_result_value = None

_analysis_function = None
_request_timeout_sec = 3

# Offset that the coordinator sets on result to make sure no other nodes can read it.
_operations = None


def get_scramble():
    return random.randint(-1000000, 1000000)

def get_machine_info():
    """ Returns machine host name and public ip. If no public ip is found 
        then returns ip as localhost (127.0.0.1)"""

    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.254.254.254', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    
    return socket.gethostname(), ip


class Operation():
    def __init__(self):
        self.operations = {}
        self.id = 0
    def _get_id(self):
        # Returns a new valid operation id > 0
        self.id += 1
        return self.id
    def add(self, scramble_list):
        # Adds new operation
        new_id = self._get_id()
        self.operations[new_id] = [scramble_list, None]
        return new_id
    def get(self, id, remove=True):
        # Return None if id doesn't exist
        # Removes id from dictionary if remove=True
        return self.operations.pop(int(id), None) if remove == True else self.operations.get(int(id), None)
    def set_result(self, id, result):
        # Sets the result for given operation id
        x = self.get(int(id), False)
        x[1] = result
    def get_result(self, id):
        # Returns result or None if result has not been set yet
        x = self.get(int(id), False)
        scramble_list = x[0]
        result = x[1]
        if result == None:
            return None
        for scramble in scramble_list:
            result -= scramble
        
        # Remove result from dict
        self.operations.pop(int(id))
        return result



def analysis(sum_data):
    """ Function to be overridden by user. Param @sum_data gives previous sum data and this function must return the new sum data after the analysis is complete.
        @sum_data will be None if it has not been previously set (first time).
    """
    return 1 if sum_data is None else sum_data + 10



def run_server(coordinator=None, analysis_function=None, nodefile=None, ip=None, 
                port=None, timeout=None, request_timout=None, min_nodes=1):
        """ Main function to run the server """
        global _server_nodefile, _server_ip, _server_port, _server_connected_ips
        global _analysis_function, _server_iscoordinator, _server_address, _request_timeout_sec
        global _server_coordinator_addr, _server_auto_shutdown
        global _operations

        if timeout is not None:
            _server_auto_shutdown = timeout
        if request_timout is not None:
            _request_timeout_sec = request_timout

        if analysis_function is None:
            raise Exception("No analysis function is given")

        host_name, host_ip = get_machine_info()
        if ip is None:
            ip = host_ip
        if port is None:
            # Set random port between 49152->65535
            #port = random.randint(49152, 65535)
            # Default port used
            port = 8985
        
        _operations = Operation()

        _analysis_function = analysis_function
        _server_nodefile = nodefile
        _server_ip = ip
        _server_port = int(port)
        _server_iscoordinator = True if nodefile is not None else False

        if not _server_iscoordinator and coordinator is None:
            raise Exception("Expected coordinator address given (ip:port) for none coordinator nodes")
        else:
            _server_coordinator_addr = coordinator
        
        # Check if nodefile given is a valid file with atleast N amount of nodes.
        if _server_iscoordinator:
            try:
                with open(nodefile, "r") as f:
                    num_nodes = len(f.readlines())
            except:
                raise Exception("Could not find nodefile given at %s" % nodefile)

            if num_nodes < min_nodes:
                raise Exception("Not enough nodes in nodefile given. Found %d but minimum is %d" % (num_nodes, min_nodes))

            # Only coordinator read nodefile
            _server_connected_ips = Smcserver.get_node_ips(ip, int(port))

        server = Smcserver._ThreadingHttpServer((_server_ip, _server_port), Smcserver)
        _server_address = "%s:%s" % (ip, port)

        def server_main():
            if _server_iscoordinator:
                # Requesting the certificates of every node in the distributed network. Hence why all nodes must be run before the coordinator.
                # TODO: when a start smc operation request is made from client, then call this get-certificates..
                Smcserver.request_nodelist_certificates()
            else:
                # Non coordinator server
                pass

            # Start listening to requests
            print("[Host: %s] Running server on %s:%d" % (host_name, ip, int(port)))
            server.serve_forever()
            print("[Host: %s] Server has shut down" % host_name)

        def shutdown_server_on_signal(signum, frame):
            print("Received shutdown signal %d.. shutting down" % signum)
            server.shutdown()
            exit(0) # TODO: need this?


        # Shut down on kill (SIGTERM) and Ctrl-C (SIGINT)
        signal.signal(signal.SIGTERM, shutdown_server_on_signal)
        signal.signal(signal.SIGINT, shutdown_server_on_signal)

        # Start server on a new thread
        thread = threading.Thread(target=server_main)
        thread.daemon = True
        thread.start()

        # Shutdown automatic after _server_auto_shutdown has elapsed
        thread.join(_server_auto_shutdown)
        if thread.is_alive():
            server.shutdown()



class Smcserver(BaseHTTPRequestHandler):
    """ Class to handle all server smc requests. """

    class _ThreadingHttpServer(socketserver.ThreadingMixIn, HTTPServer):
        # Use threading variant of BaseHTTPRequestHandler.
        # It can remain empty.
        pass
    
    def validate_request(self, except_urls_list=None):
        """ Should only be called after a request has been received.
            Ensures that the request is from a valid node, accepted by the system.
            Returns the decrypted message if valid, otherwise changes the path of the request
            to /invalid-certificate to handle errors and returns certificate and the decrypted msg. """
        
        print("Validating request..")

        exception = False
        if except_urls_list is not None:
            for url in except_urls_list:
                if self.path == url:
                    exception = True
                    break

        certificate, decrypted_msg = self.decrypt_msg()
        is_valid = True if exception is True else self.validate_certificate(certificate)
        #is_valid = self.validate_certificate(certificate)
        if is_valid:
            return decrypted_msg

        print("Request invalid..")
        # Set path to invalid url to handle specific invalid certificate case
        self.path = "/invalid-certificate"
        return certificate, decrypted_msg
        

    def validate_certificate(self, certificate):
        # TODO:
        print("Validating ceritificate")
        return True
    
    def handle_invalid_certificate(self, certificate=None, decrypted_msg=None):
        pass

    def get_node_ips(own_ip, own_port):
        """ Reads nodefile which contains all node information in the system and returns a list of their ips ["ip:port", public-key].
            Public-key is null on instantiation. Ignores its own ip:port. 

            Only coordinator will have the nodefile and is able to know about other nodes in the network on initialization.
        """

        r = []
        with open(getcwd()+"/"+_server_nodefile, "r") as f:
            for line in f.readlines():
                line = line.strip("\n") # Remove the new line symbol (only for printing purposes and not technically needed)
                ip, port = line.split(":")

                if ip == own_ip and int(port) == own_port:
                    continue # Skip itself

                r.append((line, None)) # None is just empty space atm but will be the public key
        return r

    def request_certificate(addr):
        """ Request certificate from address given. Returns the certificate on success otherwise None. """
        try:
            status, content = send_client_request(type="GET", url="/certificate", receiver=addr, timeout=_request_timeout_sec)
            if status != 200:
                print("Could not get certificate from %s, status code: %d" % (addr, status))
                return None

            return content

        except Exception as e:
            print(e)
        
        return None

    def request_nodelist_certificates():
        """ Initialize certificate file. 
            Requests the certificate for each node in the nodefile given (whitelist). """

        with open(certificate_file, "w") as f:
            for addr, _ in _server_connected_ips:
                cert = Smcserver.request_certificate(addr)
                if cert is None:
                    # Something went wrong getting this nodes certificate
                    continue
                print(cert)
                f.write(cert+"\n")

    

    def get_certificate(self):
        """ Returns this nodes certificate in string format consisting of ip, port and public-key (ip:port@publickey). """
        key = Crypt.key2string(ck.get_public_key())
        return "%s:%d@%s" % (_server_ip, _server_port, key)

    def send_whole_response(self, code, content, content_type="text/plain"):
        """ Function to easily and correctly sending a response back after having received a request. """

        if isinstance(content, str):
            content = content.encode("utf-8")
            if not content_type:
                content_type = "text/plain"
            if content_type.startswith("text/"):
                content_type += "; charset=utf-8"
        elif isinstance(content, bytes):
            if not content_type:
                content_type = "application/octet-stream"
        elif isinstance(content, object):
            content = json.dumps(content, indent=2)
            content += "\n"
            content = content.encode("utf-8")
            content_type = "application/json"

        self.send_response(code)
        self.send_header('Content-type', content_type)
        self.send_header('Content-length',len(content))
        self.end_headers()
        self.wfile.write(content)
    
    def get_public_key(self, ip):
        """ Checks if the public key from given ip address has already been cached. Otherwise calls init_public_key()
            which eventually returns its public key. """
        for i in range(len(_server_connected_ips)):
            ipx, publickey = _server_connected_ips[i]
            if ipx == ip:
                if publickey == None:
                    publickey = self.init_public_key(ip)
                return publickey
        
        # This ip is not stored previously (typically client), so it should be added
        return self.init_public_key(ip)
                

    def init_public_key(self, ip):
        """ Requests the public key from ip address given. The key is then stored in a list to cache it. """
        status, content = send_client_request(url="/get_public_key", receiver=ip)
        if status != 200 or status == None:
            self.send_whole_response(400, "error")
            raise Exception("Could not get key with status %d" % (status))

        public_key = Crypt.string2key(content)
        print("Received public key: %s from ip: %s" % (str(public_key), ip))
        # Update connected ip list with public key
        for i in range(len(_server_connected_ips)):
            ipx, _ = _server_connected_ips[i]
            if ipx == ip:
                _server_connected_ips[i] = (ip, public_key)
                break

        return public_key
    
    def create_encrypted_msg(self, msg2encrypt, ip):
        """ Encrypts the message to the given ip address (node).
            Attaches this nodes certificate to the message as well. """
        public_key = self.get_public_key(ip)

        encrypted_msg = ck.encrypt(public_key, msg2encrypt)

        # Each message must have a certificate attached
        certificate = self.get_certificate()
        encrypted_cert = ck.encrypt(public_key, certificate)
        cert_length = len(encrypted_cert).to_bytes(4, 'little')
        fullmsg = cert_length+encrypted_cert+encrypted_msg
        return fullmsg
    
    def send_encrypted_msg(self, msg, url="/add", ip=None):
        """ Encrypts the given msg to the given ip (using their public key) and sends the encrypted message. """

        fullmsg = self.create_encrypted_msg(msg, ip)
        status, response = send_client_request(type="POST", url=url, body=fullmsg, receiver=ip)

        if status != 200:
            raise Exception("Status code was not 200 when sending encrypted msg to (%s), status code: %d response: %s" % (ip, status, response))

        return status, response

    def decrypt_msg(self, data=None):
        """ Returns the message decrypted and the senders certificate decrypted. """
        
        if data == None:
            content_length = int(self.headers.get('Content-Length'))
            data = self.rfile.read(content_length)

        cert_size = int.from_bytes(data[:4], 'little')+4
        certificate = data[4:cert_size]
        encrypted_msg = data[cert_size:]

        return ck.decrypt(certificate), ck.decrypt(encrypted_msg)


    def do_PUT(self):
        msg = self.validate_request()
        # TODO: request from coordinator -> nodes to save all node data of other nodes.

        if self.path.startswith("/invalid-certificate"):
            certificate, decrypted_msg = msg
            self.handle_invalid_certificate(certificate, decrypted_msg)

        
        self.send_whole_response(200, "ok")
        
    
    def do_POST(self):
        msg = self.validate_request()
        
        if self.path.startswith("/invalid-certificate"):
            certificate, decrypted_msg = msg
            self.handle_invalid_certificate(certificate, decrypted_msg)

        elif self.path.startswith("/analysis_done"):
            global _result_value, _analysis_offset_value

            print("got analysis done")
            data_dict = json.loads(msg)
            result = data_dict['data']
            operation_id = data_dict['id']
            # Save result
            _operations.set_result(operation_id, result)
            
            self.send_whole_response(200, "ok")
        
        elif self.path.startswith("/analysis"):
            print("Received analysis request")
            self.send_whole_response(200, "ok")

            # The decrypted message will be a dictonary in string format.
            # It must be converted back from string to dictionary.
            dict = json.loads(msg)

            # The dictionary will then contain the next set of instructions (who to further the results to)
            # which the coordinator node has encrypted for this node only.
            send_list = dict['send_list']
            # Pop itself from the send list, as it has been received
            msg = send_list.pop(0)
            # Decrypt this data in order to get the ip address of who to send the remaining list + analysis-result to.
            certificate, msg = self.decrypt_msg(data=msg.encode('latin-1'))
            
            # Convert string back to dictionary
            msg = json.loads(msg)
            scramble = msg['scramble']
            sendto_ip = msg['next']

            # Validate the coordinators certificate before we trust the msg received
            if not self.validate_certificate(certificate):
                self.handle_invalid_certificate(certificate)
                return

            print("msg received: " + sendto_ip)

            # Perform the analysis function on this nodes data and update the analysis value 'data' in the dictionary.
            dict['data'] = _analysis_function(dict['data']) + scramble

            # Dump the dictionary back to string in order to send it over the internet to the next node.
            s = json.dumps(dict)
            print(s)

            # Further the result
            # send /analysis_done url if next node is the coordinator, otherwise send /analysis
            url = "/analysis_done" if sendto_ip == _server_coordinator_addr else "/analysis"
            self.send_encrypted_msg(s, url=url, ip=sendto_ip)



    def do_GET(self):
        global _result_value, _server_iscoordinator

        # Exception list for validating requests. 
        # Some requests might not have/need a valid certificate
        # in order for the request to pass through.
        except_urls = ["/certificate", "/invalid-certificate", "/get_public_key"
                        "/shutdown", "/get_result", "/start_analysis"]
        # Have an exception list for validate requests
        #msg = self.validate_request(except_urls)

        if self.path.startswith("/invalid-certificate"):
            self.handle_invalid_certificate()

        elif self.path.startswith("/get_public_key"):
            s = Crypt.key2string(ck.get_public_key())
            self.send_whole_response(200, s)
        
        elif self.path.startswith("/send_test"):
            #content_len = int(self.headers.get('Content-Length'))
            print(_server_connected_ips)
            self.send_encrypted_msg("0")
            self.send_whole_response(200, "ok")
        

        # Shutdown
        elif self.path.startswith("/shutdown"):
            self.send_whole_response(200, "ok")
            self.server.shutdown()
            exit(0)
        
        elif self.path.startswith("/get_result"):
            """ Client request the result from coordinator. """
            if not _server_iscoordinator:
                raise Exception("Client sent get-result request to a node whose not coordinator.")

            print("Received result request")

            # Read the operation id from client
            content_length = int(self.headers.get('Content-Length'))
            data = self.rfile.read(content_length)
            operation_id = int(data)
            result = _operations.get_result(operation_id)

            if result != None:
                self.send_whole_response(200, result)
            else:
                self.send_whole_response(102, "Not ready yet")

        
        elif self.path.startswith("/certificate"):
            # Only non coordinator node should get this request
            # If this node is the coordinator then raise an exception
            if _server_iscoordinator:
                raise Exception("Coordinator node should not receive a certificate request from other nodes.")
            
            # receive_ip = self.client_address[0]
            # if not ip_whitelisted(receive_ip):
            #     raise Exception("Connected node %s is not whitelisted within nodefile for coordinator" % str(self.client_address))

            self.send_whole_response(200, self.get_certificate())
           
        
        elif self.path.startswith("/start_analysis"):
            """ Start analysis request. Only coordinator will receive this request from a client. """

            if not _server_iscoordinator:
                self.send_whole_response(404, "Only coordinator should get a start_analysis request")
                return


            content_length = int(self.headers.get('content-length', 0))
            value = self.rfile.read(content_length).decode()

            # Send a dictionary containing encrypted list of receivers (send_list)
            # and some analysis data sum (data) which is initialized with a given offset such that no node can know the current data sum.
            enc = []
            scramble_list = []
            operation_id = _operations.add(scramble_list)

            enc_dict = {'send_list': enc, 'data': 0, 'id': operation_id}

            # Create sequence list of nodes to perform analysis of its data
            # This is such that the nodes know which node to forward the data to.

            # Add all nodes from certificate-file into a list with address and their public key
            node_list = []
            with open(certificate_file, "r") as f:
                for line in f.readlines():
                    print(line)
                    addr, strkey = line.split("@")
                    node_list.append((addr, Crypt.string2key(strkey)))
            
            # Shuffle the node list to make the order random
            random.shuffle(node_list)

            

            # Encrypt for each node who they should further their results to. The last node will further it back to the coordinator.
            for i in range(len(node_list)):
                addr, key = node_list[i]
                print(addr)
                # Last node sends back to coordinator again (loops around)
                if i >= len(node_list)-1:
                    scramble = get_scramble()
                    scramble_list.append(scramble)
                    msg = {'next': _server_address, 'scramble': scramble}
                    msg = json.dumps(msg)
                    msg = self.create_encrypted_msg(msg, addr)
                    enc.append(msg.decode('latin-1'))
                    break
                
                # Set it to the next node in the list
                sendto_ip, _ = node_list[i+1]
                scramble = get_scramble()
                scramble_list.append(scramble)
                msg = {'next': sendto_ip, 'scramble': scramble}
                # Convert to string
                msg = json.dumps(msg)
                msg = self.create_encrypted_msg(msg, addr)
                enc.append(msg.decode('latin-1'))

            # Dump the dictionary to string such that it can be sent over http
            order = json.dumps(enc_dict)

            # Send the string dictionary to the first node in the list.
            first_node, first_node_public_key = node_list[0]

            status, content = self.send_encrypted_msg(order, url="/analysis", ip=first_node)

            if status != 200:
                self.send_whole_response(404, "Error occurred: %s" % content)
                raise Exception("Error starting analysis: %s" % content)

            # Send ok response (200) back to client with the created operation id.
            # The client have to ask for the result in a separate request.
            self.send_whole_response(200, str(operation_id))



def arg_parser():
    parser = argparse.ArgumentParser(prog="server", description="http server")

    parser.add_argument("-p", "--port", type=int, required=True,
            help="port number to listen on")

    # Add a required server address argument
    parser.add_argument("-ip", "--server_ip", type=str, required=True,
            help="server ip of this server")
    
    parser.add_argument("-coordinator", "--coordinator", type=str, required=False,
            help="The ip address (ip:port) of coordinator node or empty if this node is the coordinator node.")
    
    parser.add_argument("-nodefile", "--nodefile", type=str, required=False,
            help="file containing all valid node addresses (node white-list). Note: this is required for coordinator node but not for regular nodes")

    parser.add_argument("connect", type=str, nargs="*",
            help="addresses (host:port) of other http servers to connect to")

    return parser


if __name__ == "__main__":
    parser = arg_parser()
    args = parser.parse_args()
    n = args.nodefile
    i = args.server_ip
    p = args.port
    run_server(analysis_function=analysis, nodefile=n, ip=i, port=p, coordinator=args.coordinator)
        

        