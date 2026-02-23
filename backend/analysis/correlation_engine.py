import sys
import os
from datetime import datetime, timezone

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from storage.activity_db import fetch_all_logs, fetch_all_emotions
from analysis.content_classifier import categorize_url


TIME_WINDOW_MINUTES = 30
MIN_SESSION_THRESHOLD = 2
MIN_DURATION_THRESHOLD = 20  # minutes


def parse_time(ts):
    dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    return dt.astimezone(timezone.utc).replace(tzinfo=None)


def analyze_correlation():
    activities = fetch_all_logs()
    emotions = fetch_all_emotions()

    category_data = {}

    # -------- Time-based Matching --------
    for activity in activities:
        _, url, duration, activity_ts = activity
        activity_time = parse_time(activity_ts)

        for emotion_row in emotions:
            _, emotion_label, score, emotion_ts = emotion_row
            emotion_time = parse_time(emotion_ts)

            time_diff = abs((emotion_time - activity_time).total_seconds()) / 60

            if time_diff <= TIME_WINDOW_MINUTES:
                category = categorize_url(url)

                if category not in category_data:
                    category_data[category] = {
                        "scores": [],
                        "total_duration": 0,
                        "sessions": 0
                    }

                category_data[category]["scores"].append(score)
                category_data[category]["total_duration"] += duration
                category_data[category]["sessions"] += 1

    print("\n==============================")
    print("🧠 EMOTRACE DIGITAL WELLBEING REPORT")
    print("==============================\n")

    if not category_data:
        print("No sufficient activity-emotion matches found.")
        return

    overall_scores = []
    primary_category = None
    strongest_impact = 0

    # -------- Category Analysis --------
    for category, data in category_data.items():
        avg_score = sum(data["scores"]) / len(data["scores"])
        overall_scores.append(avg_score)

        if abs(avg_score) > abs(strongest_impact):
            strongest_impact = avg_score
            primary_category = category

        print(f"Category: {category.capitalize()}")
        print(f"  Sessions: {data['sessions']}")
        print(f"  Total Duration: {data['total_duration']} minutes")
        print(f"  Average Emotional Score: {round(avg_score, 3)}\n")

    overall_trend = sum(overall_scores) / len(overall_scores)

    # -------- Confidence Check --------
    total_sessions = sum(data["sessions"] for data in category_data.values())
    total_duration = sum(data["total_duration"] for data in category_data.values())

    if total_sessions < MIN_SESSION_THRESHOLD and total_duration < MIN_DURATION_THRESHOLD:
        risk_level = "Low Confidence (Insufficient Behavioral Data)"
    else:
        if overall_trend < -0.4:
            risk_level = "High Emotional Strain"
        elif overall_trend < -0.2:
            risk_level = "Moderate Emotional Impact"
        elif overall_trend > 0.4:
            risk_level = "Positive Engagement"
        else:
            risk_level = "Neutral / Balanced"

    # -------- Report Summary --------
    print("Overall Emotional Trend:", round(overall_trend, 3))
    print("Primary Impact Category:", primary_category.capitalize())
    print("Behavioral Risk Level:", risk_level)

    print("\nObservations:")

    if risk_level.startswith("Low Confidence"):
        print("- Limited behavioral data available.")
        print("- More sessions are required for accurate assessment.")

    elif overall_trend < -0.3:
        print("- Repeated negative emotional correlation detected.")
        print("- Behavioral adjustments may improve digital wellbeing.")

    elif overall_trend > 0.3:
        print("- Digital activities show positive emotional alignment.")

    else:
        print("- No strong emotional pattern identified.")

    print("\nRecommendations:")

    if risk_level.startswith("Low Confidence"):
        print("- Continue tracking behavior to build stronger insight patterns.")

    elif strongest_impact < -0.4:
        print(f"- Consider reducing prolonged exposure to {primary_category} content.")
        print("- Avoid extended or late-night sessions.")

    elif strongest_impact > 0.4:
        print(f"- Continue structured engagement with {primary_category} content.")
        print("- Maintain balanced digital consumption habits.")

    else:
        print("- Maintain current usage and monitor emotional responses.")

    print("\n==============================\n")


if __name__ == "__main__":
    analyze_correlation()
