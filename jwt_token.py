from flask import Flask, request
from flask_restful import Api, Resource
import hashlib, hmac, json, os, base64
from datetime import datetime, timezone, date

flaskapp = Flask(__name__)
apiManager = Api(flaskapp)
# Class jwtgen:
# Allowed methods = POST
# POST = Create New JWT token
#   [Input: user data (optional)]
#   [Output: jwt token]

class jwtgen(Resource):
    hmac_signing_key = "a9ddbcaba8c0ac1a0a812dc0c2f08514b23f2db0a68343cb8199ebb38a6d91e4ebfb378e22ad39c2d01d0b4ec9c34aa91056862ddace3fbbd6852ee60c36acbf"

# This function returns True only if valid and active session exists againt provided userID and sessionID

    def base64url_encode(self,input):
        return base64.urlsafe_b64encode(input).decode('utf-8').replace('=','')

    def base64url_decode(self,input):
        return base64.urlsafe_b64decode(input+'==').decode('utf-8')

# This function inserts new session in epsm.session table.
    def jwt(self,user_input_data='This is default input user_input_data'):
        segments = []
        # 16 byte nonce
        nonce = os.urandom(16).hex()
        req_timestamp = int((datetime.now(timezone.utc) - datetime(1970,1,1, tzinfo=timezone.utc)).total_seconds())
        input_payload = {"data": user_input_data, "date": str(date.today())}

        header = {"typ": "JWT", "alg": "HS512"}
        # a.k.a. claims as per https://datatracker.ietf.org/doc/html/draft-ietf-oauth-json-web-token-19#section-4.1.6
        payload = {"iat": req_timestamp, "jti": nonce, "payload": input_payload}

        base64url_header = self.base64url_encode(json.dumps(header, separators=(",",":")).encode())
        base64url_payload = self.base64url_encode(json.dumps(payload, separators=(",",":")).encode())

        segments.append(base64url_header)
        segments.append(base64url_payload)

        signing_input = ".".join(segments).encode()
        signature = hmac.new(self.hmac_signing_key.encode(), signing_input, hashlib.sha512).digest()
        segments.append(self.base64url_encode(signature))
        jwt_token = ".".join(segments)

        return jwt_token


# POST method to create a new jwt token
    def post(self):
        if request.headers.get('Content-Type') == 'application/json':
            request_body = request.json
            if 'None' == str(request_body['user_data']):
                jwt_token = self.jwt()
            else:
                jwt_token = self.jwt(str(request_body['user_data']))
            out = {'JWT Token': jwt_token}
            return out, 200
        else:
           out = {'status': "invalid content-Type"}
           return out, 202

class jwtverification(Resource):
# Class jwtverification:
# Allowed methods = GET
# GET = Validate JWT token
#   [Input: jwt token, hmac Key]
#   [Output: jwt token data]

    def base64url_encode(self,input):
        return base64.urlsafe_b64encode(input).decode('utf-8').replace('=','')

    def base64url_decode(self,input):
        return base64.urlsafe_b64decode(input+'==').decode('utf-8')

    def get_hmac_signature_for_verification(self,rx_header,rx_payload,rx_key):
        seg=[]
        base64url_header = self.base64url_encode(rx_header.encode())
        base64url_payload = self.base64url_encode(rx_payload.encode())
        seg.append(base64url_header)
        seg.append(base64url_payload)

        signing_input = ".".join(seg).encode()
        signature_calculated = hmac.new(rx_key.encode(), signing_input, hashlib.sha512).digest()
        signature_calculated = self.base64url_encode(signature_calculated)
        return signature_calculated

    def verify_jwt(self,token, input_key):
        # split the given JWT token in to 3 parts namely - header, claims (paylaod) and signature.
        part_list = token.split('.')
        rx_header = part_list[0]
        rx_payload = part_list[1]
        # decode the header as receievd from JWT token
        rx_header_decoded = self.base64url_decode(rx_header)
        # Decode the payload/claim as received from JWT token
        rx_payload_decoded = self.base64url_decode(rx_payload)
        # this returns the signature as calcuated using the header and payload of the incoming GET request using the signing key provided
        sig_calc = self.get_hmac_signature_for_verification(rx_header_decoded, rx_payload_decoded, input_key)
        # match the the calcualted signature with the signature that is present in the JWT token
        if sig_calc.strip() == part_list[2].strip():
            # retrun true if the calculated signature (using the provided the signing key) matches with the provided signature
            return rx_header_decoded, rx_payload_decoded, True
        else:
            return rx_header_decoded, rx_payload_decoded, False


# GET method to validate the JWT token
    def get(self):
        #check for content type
        if request.headers.get('Content-Type') == 'application/json':
            # check if Token exists in request body
            request_body = request.json
            if 'None' == str(request_body['Token']):
                out = {'status': "token can not be empty"}
                return out, 203

            else:
                # check if Signing_key exists in request body
                if 'None' == str(request_body['Signing_key']):
                    out = {'status': "key can not be empty"}
                    return out, 204
                else:
                    # verify the signature using the provided data
                    data = self.verify_jwt(request_body['Token'], request_body['Signing_key'])
                    out = {"Header": json.loads(data[0]), "Claims": json.loads(data[1]), "Signature Verification": data[2]}
                    return out, 200
        else:
           out = {'status': "invalid content-Type"}
           return out, 202


# Add URL endpoints
apiManager.add_resource(jwtgen, '/generateToken')
apiManager.add_resource(jwtverification, '/verifyToken')

if __name__ == '__main__':
    flaskapp.run(threaded=True, debug=False,host='0.0.0.0', port=8000)
