from flask import Flask, jsonify, request
import threading
import time
import requests

app = Flask(__name__)

# Variable to track if the thread is running
is_thread_running = False

@app.route('/city_update_analysis_last_15_days', methods=['GET'])
def get_cities_id_list():
    global is_thread_running
    """
    It fetches the list of city IDs that were updated between the 1st and 15th of the current month if the current date is the 16th.
    If the current date is the 1st, it fetches the list of IDs that were updated between the 16th of the previous month and the end of the previous month.
    After that, it sends this list of IDs to the `city_update_analysis` endpoint, which provides an email report of the updated city analysis based on the provided city IDs.
    """
    global is_thread_running
    if is_thread_running:
        return jsonify({"message": "Another analysis is already running"}), 429

    try:
        is_thread_running = True
        host_url = request.host_url

        def initialize_update_analysis():
            global is_thread_running
            time.sleep(60)  # Sleep for 2 minutes

            # Assuming the processing is done, reset the flag
            is_thread_running = False

        # Start the update_analysis in a new thread
        update_analysis_thread = threading.Thread(target=initialize_update_analysis)
        update_analysis_thread.start()

        # Return a response indicating the update_analysis is running
        return jsonify({"message": "update analysis is running"}), 200

    except Exception as e:
        is_thread_running = False
        print(f"Error in get_cities_id_list: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/check_thread', methods=['GET'])
def check_thread():
    """Endpoint to check if the update analysis thread is running."""
    return jsonify({"is_thread_running": is_thread_running}), 200


if __name__ == '__main__':
    app.run(debug=True)