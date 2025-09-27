# backend/services/planner.py
from .retriever import load_courses, get_mongo_retriever, get_pinecone_retriever, keyword_search
from langchain.chains import RetrievalQA
from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate
import os


def plan_courses(missing_skills: list):
    """
    Suggest courses for the given missing skills.
    Priority:
    1. Vector DB search (MongoDB or Pinecone)
    2. Keyword fallback (BM25-style inside JSON)
    3. Plain JSON lookup (existing rule-based)
    """

    # ------------------------
    # 1. Check Vector DB (Mongo or Pinecone)
    # ------------------------
    retriever = None
    if os.getenv("MONGO_URI"):
        retriever = get_mongo_retriever(
            uri=os.getenv("MONGO_URI"),
            db_name=os.getenv("MONGO_DB"),
            collection_name=os.getenv("MONGO_COLLECTION"),
        )
    elif os.getenv("PINECONE_API_KEY"):
        retriever = get_pinecone_retriever(
            api_key=os.getenv("PINECONE_API_KEY"),
            index_name=os.getenv("PINECONE_INDEX"),
        )

    if retriever:
        llm = OpenAI(model_name="gpt-3.5-turbo", temperature=0)
        template = """
        You are an expert career coach.
        A student is missing the following skills: {skills}.
        Recommend the best 3 courses from the knowledge base to cover these skills.
        Only return course names as a list.
        """
        prompt = PromptTemplate(
            input_variables=["skills"],
            template=template
        )
        chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever.as_retriever(search_kwargs={"k": 5}),
            chain_type_kwargs={"prompt": prompt}
        )

        response = chain.run({"skills": ", ".join(missing_skills)})
        # Expecting LLM to output course names as text, split into list
        return [c.strip() for c in response.split(",")][:3]

    # ------------------------
    # 2. Fallback: Keyword search (BM25-style)
    # ------------------------
    keyword_results = []
    for skill in missing_skills:
        keyword_results.extend(keyword_search("all", skill))
    if keyword_results:
        return list(dict.fromkeys(keyword_results))[:3]

    # ------------------------
    # 3. Fallback: JSON-based lookup (your old logic)
    # ------------------------
    courses = load_courses()
    recommended = []
    # Get user skills from the calling context (assume global or pass as argument if needed)
    import inspect
    frame = inspect.currentframe().f_back
    user_skills = frame.f_locals.get('user_skills', [])
    user_skills_lower = [s.lower() for s in user_skills]

    for course_name, details in courses.items():
        if isinstance(details, dict):
            course_skills = [s.lower() for s in details.get("skills", [])]
            # Only recommend if at least one course skill is in missing_skills and none are in user_skills
            if any(skill in missing_skills for skill in course_skills):
                # Exclude if all course skills are already in user_skills
                if not any(skill in user_skills_lower for skill in course_skills):
                    recommended.append(course_name)

    recommended = list(dict.fromkeys(recommended))[:3]
    return recommended