from main import app


@app.route("/ajax/get_next_video", methods=["POST"])
def get_next_video():
    return "video3.mp4"


@app.route("/ajax/get_previous_video", methods=["POST"])
def get_previous_video():
    return "video4.mp4"
