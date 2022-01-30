from flask import make_response


def build_404(message):
    return make_response('','404', {'error' : "Not Found", "message" : message})
