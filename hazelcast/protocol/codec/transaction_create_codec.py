from hazelcast.serialization.bits import *
from hazelcast.protocol.client_message import ClientMessage
from hazelcast.protocol.custom_codec import *
from hazelcast.util import ImmutableLazyDataList
from hazelcast.protocol.codec.transaction_message_type import *

REQUEST_TYPE = TRANSACTION_CREATE
RESPONSE_TYPE = 104
RETRYABLE = False


def calculate_size(timeout, durability, transaction_type, thread_id):
    """ Calculates the request payload size"""
    data_size = 0
    data_size += LONG_SIZE_IN_BYTES
    data_size += INT_SIZE_IN_BYTES
    data_size += INT_SIZE_IN_BYTES
    data_size += LONG_SIZE_IN_BYTES
    return data_size


def encode_request(timeout, durability, transaction_type, thread_id):
    """ Encode request into client_message"""
    client_message = ClientMessage(payload_size=calculate_size(timeout, durability, transaction_type, thread_id))
    client_message.set_message_type(REQUEST_TYPE)
    client_message.set_retryable(RETRYABLE)
    client_message.append_long(timeout)
    client_message.append_int(durability)
    client_message.append_int(transaction_type)
    client_message.append_long(thread_id)
    client_message.update_frame_length()
    return client_message


def decode_response(client_message, to_object=None):
    """ Decode response from client message"""
    parameters = dict(response=None)
    parameters['response'] = client_message.read_str()
    return parameters


