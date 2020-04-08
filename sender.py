# Author Raffaele Perini
#
# Simple process which wait to be notify by crypto and send the info to an endpoint
#

from multiprocessing import Process,Pipe

def send(child_conn):
    

    msg = "Everything sent to the endpoint"
    child_conn.send(msg)
    child_conn.close()