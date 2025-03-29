import json
import requests
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/jobs.json")
def jobs_api():
    try:
        response = requests.post(
            "https://www.calcareers.ca.gov/CalHrPublic/Search/JobSearchResults",
            headers={"Content-Type": "application/json"},
            json={
                "Keywords": "",
                "Page": 1,
                "PageSize": 10,
                "SortField": "PostingDate",
                "SortDescending": True
            }
        )

        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch jobs", "status": response.status_code})

        data = response.json()
        jobs = []

        for job in data.get("Results", []):
            jobs.append({
                "title": job.get("JobTitle"),
                "department": job.get("DepartmentName"),
                "location": job.get("JobLocation"),
                "salary": job.get("SalaryRange"),
                "url": f"https://www.calcareers.ca.gov/CalHrPublic/Jobs/JobPosting.aspx?JobControlId={job.get('JobControlId')}"
            })

        return jsonify(jobs)

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
