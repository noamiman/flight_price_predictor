import http.client

conn = http.client.HTTPSConnection("sky-scrapper.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "3a03b6d91cmsh5a198b6d5afdc72p1f6a2djsn17a93e043e31",
    'x-rapidapi-host': "sky-scrapper.p.rapidapi.com"
}

conn.request("GET", "/api/v1/flights/getFlightDetails?legs=%5B%7B%22destination%22%3A%22LOND%22%2C%22origin%22%3A%22LAXA%22%2C%22date%22%3A%222024-04-11%22%7D%5D&adults=1&currency=USD&locale=en-US&market=en-US&cabinClass=economy&countryCode=US", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))