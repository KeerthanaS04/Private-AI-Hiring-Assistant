import requests

NGROK_URL = "https://0d42b057cdda.ngrok-free.app/infer"  # use your current URL

def run_inference(resume_text, jd_text, task="match", query=None):
    payload = {
        "resume": resume_text,
        "jd": jd_text,
        "task": task
    }
    if task == "chat" and query:
        payload["query"] = query

    try:
        response = requests.post(NGROK_URL, json=payload)
        response.raise_for_status()
        return response.json()["result"]
    except Exception as e:
        print("API error:", e)
        return "Error contacting the remote model API."

