from test.unit.webapp import client

def test_landing(client):
  landing=client.get('/')
  html = landing.data.decode()
  

