import json
import requests
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/jobs.json")
def jobs_api():
    try:
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

        payload = {
            "Keywords": "",
            "Page": 1,
            "PageSize": 10,
            "SortField": "PostingDate",
            "SortDescending": True
        }

        response = requests.post(
            "https://www.calcareers.ca.gov/CalHrPublic/Search/JobSearchResults",
            headers=headers,
            json=payload
        )

        try:
            data = response.json()
        except Exception as e:
            return jsonify({
                "error": str(e),
                "raw_response": response.text[:1000]
            })

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
