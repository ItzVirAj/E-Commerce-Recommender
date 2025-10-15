
E-Commerce LLM-Based Recommender System

This project is an AI-powered E-Commerce Recommender System that combines a FastAPI backend with a React frontend. It uses LLM (Google Gemini) to provide explanations for product recommendations.

Explanation - https://youtu.be/Gprz3R82Z6M

Tech Stack - 

    Backend:
        Python 3.11+

    Frontend:
        React
  
    
LLM Usage - 

    The system uses a Large Language Model (google-generativeai) to generate natural language explanations for why a product is recommended.

    Module: app/llm_explain.py
    Function: generate_explanation(product, recommended_product)
    API: Uses Google’s Generative AI API (requires an API key).
    Output: Textual explanation displayed alongside recommendations in the frontend.



Initilization - 

    Backend Setup (Python)
        
        1. Clone the repository

            git clone <repo-url>
            cd backend
      
        2. Create a virtual environment
            python -m venv .venv
            .venv\Scripts\activate
       
        3. Install dependencies
            pip install -r requirements.txt
        
        4. Configure environment variables

            Create a .env file in root folder with your Google Generative AI API key:
            GENAI_API_KEY=your_google_genai_api_key
        
        5. Initialize the database

            Place sample_data.csv in the backend/ folder.

            The CSV format:
            id,title,description,category,price
            1,Apple iPhone 15,Latest iPhone with AI camera,Electronics,1099
            
            Run the backend initialization: python main.py
        
        6. Run the backend server
            uvicorn app.main:app --reload
            The API will be available at: http://127.0.0.1:8000



    Frontend Setup (React)

        1. Navigate to frontend folder - 
            cd frontend

        2. Install dependencies - 
            npm install

        3. Configure API Base URL - 
            In api.js - export const API_BASE_URL = "http://127.0.0.1:8000";

        4. Run frontend locally - npm run dev
            The app will run at: http://localhost:5173


Notes - 

    1. To refresh the database after updating sample_data.csv, delete the existing database file (database.db) and restart the backend. This will repopulate the database with the new CSV data Or Just rm database.db in powershell, Save the CSV and run backend.

    2. The current frontend UI is functional but basic. Further enhancements can be made to achieve a polished, production-ready look.
