from app import create_app
from app.consumer import start_consuming
import threading

app = create_app()

if __name__ == '__main__':
    consumer_thread = threading.Thread(target=start_consuming)
    consumer_thread.start()
    app.run(host='0.0.0.0', port=5000, debug=True)
