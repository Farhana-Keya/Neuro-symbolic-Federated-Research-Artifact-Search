# import sys
#
# sys.path.append("..")
# from fastapi import APIRouter, HTTPException, Depends
# from fastapi.responses import HTMLResponse
# from fastapi.staticfiles import StaticFiles
# from pydantic import BaseModel
# from typing import Literal, Dict, Any
# from app.services.find_keyterm_from_question import Keyterm
# from app.services.service_ranking import Ranking
# from app.routers.routers_unification_of_UI import search_question
# import json
#
# router = APIRouter()
#
# # You can modify this to match your ranking function or replace with actual logic
# def perform_ranking():
#     # Simulate ranking logic, this is where you can plug in the ranking function
#     return {"message": "Ranking process initiated..."}
#
# # Endpoint to serve HTML with the button
# # @router.get("/", response_class=HTMLResponse)
# # async def home():
# #     html_content = """
# #     <!DOCTYPE html>
# #     <html lang="en">
# #     <head>
# #         <meta charset="UTF-8">
# #         <meta name="viewport" content="width=device-width, initial-scale=1.0">
# #         <title>Ranking Button</title>
# #         <script>
# #             function performRanking() {
# #                 fetch('/rank', {
# #                     method: 'POST',
# #                     headers: {
# #                         'Content-Type': 'application/json',
# #                     },
# #                     body: JSON.stringify({query: "example query"})  // Example query
# #                 })
# #                 .then(response => response.json())
# #                 .then(data => {
# #                     alert(data.message);  // Alert the response message
# #                 })
# #                 .catch(error => console.error('Error:', error));
# #             }
# #         </script>
# #     </head>
# #     <body>
# #         <h1>FastAPI Ranking Button</h1>
# #         <button onclick="performRanking()">Ranking</button>
# #     </body>
# #     </html>
# #     """
# #     return HTMLResponse(content=html_content)
#
# # Endpoint to perform ranking
# @router.get("/ranking")
# async def rank(query: dict):
#     try:
#         # Perform ranking logic here
#         search_question
#         ranking_result = perform_ranking()  # Replace with actual ranking logic
#         return ranking_result
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#
#
