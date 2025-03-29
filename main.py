import asyncio
import json
from flask import Flask, jsonify
from playwright.async_api import async_playwright

app = Flask(__name__)

@app.route("/jobs.json")
def jobs_endpoint():
    return asyncio.run(fetch_jobs())

async def fetch_jobs():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://www.calcareers.ca.gov/CalHrPublic/Jobs/JobPostingList.aspx", wait_until="networkidle")
        await page.wait_for_selector("tr.DataRow")

        jobs = await page.evaluate("""
        () => {
            const rows = Array.from(document.querySelectorAll("tr.DataRow"));
            return rows.map(row => {
                const cells = row.querySelectorAll("td");
                const link = cells[0]?.querySelector("a");
                return {
                    title: link?.innerText.trim(),
                    department: cells[1]?.innerText.trim(),
                    location: cells[2]?.innerText.trim(),
                    salary: cells[3]?.innerText.trim(),
                    url: "https://www.calcareers.ca.gov" + link?.getAttribute("href")
                };
            }).filter(job => job.title);
        }
        """)

        await browser.close()
        return jsonify(jobs)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
