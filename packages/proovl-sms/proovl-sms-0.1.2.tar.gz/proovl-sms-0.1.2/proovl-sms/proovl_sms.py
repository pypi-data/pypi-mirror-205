import requests

class Proovl:
    def __init__(self, user, token, from_num):
        self.user = user
        self.token = token
        self.from_num = from_num
        self.base_url = 'https://www.proovl.com/api/send.php'

    def send_sms(self, destination, message):
        params = {
            'user': self.user,
            'token': self.token,
            'from': self.from_num,
            'to': destination,
            'text': message
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        response = requests.get(self.base_url, params=params, headers=headers)
        return response.text

    def send_bulk_sms(self, destinations, message):
        numbers = destinations.split(';')
        results = []
        for number in numbers:
            params = {
                'user': self.user,
                'token': self.token,
                'from': self.from_num,
                'to': number,
                'text': message
            }
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'en-US,en;q=0.9',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
            response = requests.get(self.base_url, params=params, headers=headers)
            result = {'number': number, 'response': response.text}
            results.append(result)
        return results
		