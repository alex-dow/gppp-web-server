from gppp import create_gppp_app
from flask_socketio import SocketIO

if __name__ == '__main__':
  app = create_gppp_app()
  socketio = SocketIO(app)
  socketio.run(app, debug=True, host='0.0.0.0', port=5000)
