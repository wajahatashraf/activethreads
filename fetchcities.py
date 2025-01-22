from flask import Flask, jsonify
import threading
import time

app = Flask(__name__)

# Define the ThreadChecker class
class ThreadChecker:
    def __init__(self):
        self.threads = []

    def add_thread(self, thread):
        """Add a thread to the list."""
        self.threads.append(thread)

    def check_threads(self):
        """Check if any thread is running (alive)."""
        return any(thread.is_alive() for thread in self.threads)

# Initialize the thread checker object
thread_checker = ThreadChecker()

@app.route('/city_update_analysis_last_15_days', methods=['GET'])
def get_cities_id_list():
    global thread_checker

    try:
        # Define the function for update analysis, which will run in the thread
        def initialize_update_analysis():
            time.sleep(30)  # Simulate processing time (30 sec)

        # Start the update_analysis in a new thread if not already running
        update_analysis_thread = threading.Thread(target=initialize_update_analysis)
        update_analysis_thread.start()

        # Add the thread to the thread_checker
        thread_checker.add_thread(update_analysis_thread)

        # Return a response indicating the update analysis is running
        return jsonify({"message": "update analysis is running"}), 200

    except Exception as e:
        print(f"Error in get_cities_id_list: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/otherthread', methods=['GET'])
def get_other_thread_status():
    global thread_checker
    try:
        # Define the function for update analysis, which will run in the thread
        def initialize_update_analysis1():
            time.sleep(30)  # Simulate processing time (30 sec)

        # Start the update_analysis in a new thread if not already running
        update_analysis_thread = threading.Thread(target=initialize_update_analysis1)
        update_analysis_thread.start()

        # Add the thread to the thread_checker
        thread_checker.add_thread(update_analysis_thread)

        # Return a response indicating the update analysis is running
        return jsonify({"message": "update analysis is running"}), 200

    except Exception as e:
        print(f"Error in get_other_thread_status: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/check_thread', methods=['GET'])
def check_thread():
    """Endpoint to check if any thread is running."""
    # Check if any thread is alive
    if thread_checker.check_threads():
        return "is_thread_running=True", 200
    else:
        return "is_thread_running=False", 200


if __name__ == '__main__':
    app.run(debug=True)
