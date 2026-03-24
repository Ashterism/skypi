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
        hourly_breakdown = report["hourly_breakdown"]
    )

if __name__ == "__main__":
    app.run(debug=True)