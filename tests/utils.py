'''
Various tests related utilities.
'''

def m(kind, body=None, sender=None):
    '''
    Quickly make a message object.
    '''

    return {
        "kind": kind,
        "body": body,
        "sender": sender
    }
