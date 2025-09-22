import requests
from Constants import Constants


class TestValidationWalletNetwork:
    def test_validation_wallet_network(self):

        url = Constants.API_URL + "/validate/wallet-network"
        payload = {
                  "wallet": "bc1qp6lzy3t2hv90f8tcmesca5hk4c5fde20a79t8h",
                  "network": "btc"
                }

        response = requests.post(url, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 1

    def test_validation_invalid_wallet(self):

        url = Constants.API_URL + "/validate/wallet-network"
        payload = {
                  "wallet": "0x1234567890abcdefприветандрей1234567890abcdef12345678",
                  "network": "ether"
                }

        response = requests.post(url, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 0
        assert data["error"] == "INVALID_ADDRESS"

    def test_validation_invalid_network(self):

        url = Constants.API_URL + "/validate/wallet-network"
        payload = {
                  "wallet": "0x1234567890abcdef1234567890abcdef12345678",
                  "network": "бсц"
                }

        response = requests.post(url, json=payload)
        print("RESPONSE TEXT:", response.text)

        data = response.json()
        assert data["ok"] == 0
        assert data["error"] == "INVALID_NETWORK"

