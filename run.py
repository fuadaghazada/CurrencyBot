from app import config
from app import app

# Running the server
if __name__ == '__main__':
    app.run(host = config['HOST'], port = config['PORT'], debug = True)
