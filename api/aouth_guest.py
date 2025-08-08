import requests

def handler(request):
    uid = request.args.get('uid')
    password = request.args.get('password')
    if not uid or not password:
        return {"message": "Missing uid or password"}, 400

    oauth_url = "https://100067.connect.garena.com/oauth/guest/token/grant"
    payload = {
        'uid': uid,
        'password': password,
        'response_type': "token",
        'client_type': "2",
        'client_secret': "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
        'client_id': "100067"
    }
    headers = {
        'User-Agent': "GarenaMSDK/4.0.19P9(SM-M526B ;Android 13;pt;BR;)",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip"
    }

    try:
        oauth_response = requests.post(oauth_url, data=payload, headers=headers, timeout=5)
    except requests.RequestException as e:
        return {"message": str(e)}, 500

    if oauth_response.status_code != 200:
        try:
            return oauth_response.json(), oauth_response.status_code
        except ValueError:
            return {"message": oauth_response.text}, oauth_response.status_code

    try:
        oauth_data = oauth_response.json()
    except ValueError:
        return {"message": "Invalid JSON response from OAuth service"}, 500

    if 'access_token' not in oauth_data or 'open_id' not in oauth_data:
        return {"message": "OAuth response missing access_token or open_id"}, 500

    params = {
        'access_token': oauth_data['access_token'],
        'open_id': oauth_data['open_id'],
        'platform_type': str(oauth_data.get('platform', 4))
    }

    # استدعاء الدالة majorlogin_jwt محليًا
    from .majorlogin_jwt import handler as majorlogin_handler
    class DummyRequest:
        args = params
    return majorlogin_handler(DummyRequest())
