
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from loop_app.hospital_db import HospitalDB
import re

app = FastAPI()
db = HospitalDB()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/query")
async def handle_query(user_query: str = Form(...)):
    user_query_lower = user_query.lower()
    response_text = ""
    number_match = re.search(r'(\d+)\s+hospital', user_query_lower)
    limit = int(number_match.group(1)) if number_match else 3

    # Match everything after "around"
    match = re.search(r'around|in\s+([a-z\s,]+)', user_query_lower)
    if match:
        cities_str = match.group(1)
        # Split by "and" or comma, strip spaces
        cities = [c.strip().title() for c in re.split(r',|and', cities_str)]
        all_results = []

        for city in cities:
            hospitals = db.find_hospitals_by_city(city, limit=limit)
            if hospitals:
                hospital_list = ", ".join([h['Hospital'] for h in hospitals])
                all_results.append(f"{city}: {hospital_list}.\t")
            else:
                all_results.append(f"{city}: Sorry, no hospitals found.")

        response_text = "Here are the hospitals:\n" + "\n".join(all_results)
        return JSONResponse({"response": response_text})

    # Handle "confirm if" queries
#     elif "confirm if" in user_query_lower:
        
# #        # Example: "Can you confirm if Manipal Sarjapur in Bangalore is in my network?"
#         try:
#             parts = user_query_lower.split("if ")[1].split(" in ")
#             hospital_name = parts[0].strip()
#             city_name = parts[1].split(" is")[0].strip()
#             exists = db.check_hospital_in_network(hospital_name, city_name)
#             response_text = f"{hospital_name.title()} is {'in' if exists else 'not in'} your network."
#         except Exception:
#             response_text = "Sorry, I could not understand your confirmation query."
#         return JSONResponse({"response": response_text})

    rag_results = db.rag_search(user_query, top_k=3)
    if rag_results:
        context = "Here are some hospitals I found:\n" + \
                  "\n".join([f"{h['Hospital']} ({h['Address']})  ({h['City']})" for h in rag_results])
        gemini_reply = db.generate_gemini_response(user_query, context)
        response_text += gemini_reply
    else:
        response_text += "I'm sorry, I couldn't find relevant hospitals. Please specify a city or hospital name."

    return JSONResponse({"response": response_text})
