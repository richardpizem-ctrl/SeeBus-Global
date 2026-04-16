# status_controller.py
# Controller pre základný status endpoint

def get_status_info():
    return {
        "status": "OK",
        "service": "SeeBus-Global API",
        "version": "1.0",
        "controller": "status_controller"
    }
