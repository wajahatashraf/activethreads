from flask import Flask, jsonify
import threading
import time

app = Flask(__name__)

# Initialize the thread checker global variable
thread_checker = None

@app.route('/city_update_analysis_last_15_days', methods=['GET'])
def get_cities_id_list():
    global thread_checker

    try:
        # Define the function for update analysis, which will run in the thread
        def initialize_update_analysis():
            time.sleep(30)  # Simulate processing time (30 sec)

        # Start the update_analysis in a new thread if not already running
        if thread_checker is None or not thread_checker.is_alive():
            update_analysis_thread = threading.Thread(target=initialize_update_analysis)
            update_analysis_thread.start()
            thread_checker = update_analysis_thread

        # Return a response indicating the update analysis is running
        return jsonify({"message": "update analysis is running"}), 200

    except Exception as e:
        thread_checker = None  # Reset on error
        print(f"Error in get_cities_id_list: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/check_thread', methods=['GET'])
def check_thread():
    """Endpoint to check if the update analysis thread is running."""
    # Check if the thread is alive using .is_alive()
    if thread_checker and thread_checker.is_alive():
        return "is_thread_running=True", 200
    else:
        return "is_thread_running=False", 200


if __name__ == '__main__':
    app.run(debug=True)
