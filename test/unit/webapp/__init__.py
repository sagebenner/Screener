import pytest
from main import app

"""Initialize the testing environment

Creates an app for testing that has the configuration flag ``TESTING`` set to
``True``.

"""

@pytest.fixture
def client():
  """Configures the app for testing

  Sets app config variable ``TESTING`` to ``True``

  :return: App for testing
  """
  #app.config['TESTING'] = True
  client = app.test_client()

  yield client