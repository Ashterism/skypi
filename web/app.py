from flask import Flask, render_template
from skypi.services.daily_report import get_daily_report

"""
python -m web.app
"""

app = Flask(__name__)

@app.route("/")
def tonight():
    report = get_daily_report()

    return render_template(
        "index.html", 
        go_no_go = report["go_no_go"],
        at_a_glance = report["at_a_glance"],
        # next_three_days = report["next_three_days"],
        next_good_night = report["next_good_night"],
        astro_session_data = report["astro_session_data"],
    )

if __name__ == "__main__":
    app.run(debug=True, port=5001)