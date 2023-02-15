import requests

def BlackListed(address):
    url = "https://api.tatum.io/v3/security/address/" + address

    headers = {"x-api-key": "a841c932-46fb-429d-a95d-b42a0ffdefc3"}

    response = requests.get(url, headers=headers)

    data = response.json()
    return(data)

address = "bc1qwukmzzjqn5hwsp4uaswc4c53gc0xz5asrv0prx"
isBlackListed = BlackListed(address)
print(isBlackListed)