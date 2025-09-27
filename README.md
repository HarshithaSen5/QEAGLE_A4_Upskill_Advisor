# 🚀 Upskill Advisor AI  
**Your Personal Career Growth Assistant**

---

## ✨ Features  
- **RAG-based Hybrid Retrieval**: Combines MongoDB vector search with BM25-style keyword retrieval.  
- **LLM-Powered Advisor**: Uses Ollama Phi-3 and MiniLM embeddings for context-aware recommendations.  
- **Personalized Learning Plans**: Gap analysis against target job roles.  
- **Course Timelines**: Structured roadmap with prerequisites, outcomes, and estimated duration.  
- **Motivation Messages**: Encouragement included at the end of every learning plan.  
- **PDF Export**: Downloadable personalized career roadmap.  
- **Frontend Dashboard**: Clean React interface for role/skills input and path visualization.  

---

## 🛠 Tech Stack  
- **Frontend**: React.js + TailwindCSS  
- **Backend**: FastAPI (Python)  
- **Database**: MongoDB (Atlas/local) with Vector Search  
- **AI Models**: Ollama Phi-3 LLM, MiniLM (HuggingFace) embeddings  
- **Other**: RAG pipeline for course + JD retrieval  

---

## 📂 Project Structure  
upskill_advisor/ 
│── backend/
│ ├── data/ # Course & JD seed data 
│ ├── models/ # MongoDB schemas 
│ ├── services/ # Retrieval & advisor services 
│ ├── main.py # FastAPI entrypoint 
│ ├── seed_courses.py # Script to seed courses 
│ ├── seed_jds.py # Script to seed job descriptions 
│ │── project/ # Frontend root 
│ ├── src/ # React components 
│ ├── index.html 
│ ├── package.json 
│ ├── tailwind.config.js 
│ │── .gitignore 
│── README.md


---

## ⚙️ Setup Instructions  

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/QEAGLE_A4_Upskill_Advisor.git
cd QEAGLE_A4_Upskill_Advisor

2. Backend Setup
cd backend
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt

3. Environment Variables

Create .env inside backend/:

MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/upskill
MONGODB_DB=upskill
MONGODB_COURSES_COLL=courses
MONGODB_JDS_COLL=jds

EMBED_MODEL=sentence-transformers/all-MiniLM-L6-v2
LLM_MODEL=phi3

4. Seed Database
python seed_courses.py
python seed_jds.py

5. Run Backend
uvicorn main:app --reload --port 8000


Backend: http://localhost:8000

API Docs: http://localhost:8000/docs

6. Run Frontend
cd project
npm install
npm run dev


Frontend: http://localhost:5173

📊 Evaluation

Skill Coverage % (JD vs Recommended Skills)

Path Diversity (unique vs redundant courses)

Latency (retrieval & response time)

🏗 Architecture
<img width="3600" height="842" alt="upskill_architecture_minimal_timeline_hd" src="https://github.com/user-attachments/assets/a779ee43-8cbc-4501-a5ff-33382c88aad1" />
flowchart LR
    User[👤 User Input: Role & Skills] -->|Frontend| ReactUI
    ReactUI --> FastAPI
    FastAPI -->|Query| RAGPipeline
    RAGPipeline -->|Vector Search| MongoDB
    RAGPipeline -->|Embeddings| MiniLM
    RAGPipeline -->|LLM Reasoning| OllamaPhi3
    RAGPipeline --> Recommendations[📚 Personalized Learning Path]
    Recommendations --> ReactUI
    ReactUI -->|PDF Export| Download

🔮 Future Improvements

Role-specific fine-tuned recommendations

Authentication & user profiles

Multi-language support

Advanced analytics dashboard

📸 Screenshots
📝 User Input
<img width="1889" height="946" alt="Screenshot 2025-09-27 103553" src="https://github.com/user-attachments/assets/cff15fb7-128a-42bb-aa24-b066ac6c70a3" />
🎯 Learning Path Output
<img width="1890" height="945" alt="Screenshot 2025-09-27 110208" src="https://github.com/user-attachments/assets/807cbc6d-725d-4876-ba71-00643056db1f" /> <img width="1894" height="956" alt="Screenshot 2025-09-27 110159" src="https://github.com/user-attachments/assets/341f2692-6edd-400e-967c-1d8f581558c2" /> ![Last img](https://github.com/user-attachments/assets/4e9d8911-1096-4006-ad5d-ae62d655e1af) ```
