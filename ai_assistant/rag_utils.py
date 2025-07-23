# ai_assistant/rag_utils.py

from vertexai import rag
from vertexai.generative_models import GenerativeModel, Tool
import vertexai
from django.conf import settings
from google.cloud import translate_v2 as translate
import logging
from vertexai import generative_models as genai
import difflib
vertexai.init(project=settings.GCP_PROJECT_ID, location=settings.GCP_REGION)
import json
from vertexai.language_models import ChatModel
from google.api_core.exceptions import GoogleAPIError
import re

DEFAULT_QUIZ_QUESTIONS = [
    {
        "question": "What is the purpose of the Jan Dhan Yojana?",
        "options": ["Education funding", "Financial inclusion", "Pension scheme", "Health insurance"],
        "answer": "Financial inclusion"
    },
    {
        "question": "Which document is essential for opening a bank account in India?",
        "options": ["Aadhar Card", "Pan Card", "Voter ID", "Driving License"],
        "answer": "Aadhar Card"
    },
    {
        "question": "Which is a government-backed savings scheme?",
        "options": ["Mutual Fund", "PPF", "Equity", "Real Estate"],
        "answer": "PPF"
    }
]

def validate_answer_semantically(answer, correct_answer, question=None, lang_code="en"):
    # Example logic for multilingual validation using Gemini
    print("validate_answer_semantically")

    try:
        model = GenerativeModel(model_name=settings.MODEL_NAME)

        prompt = f"""
        Compare the following user answer with the correct answer. 
        Respond with "Yes" if they are semantically similar in {lang_code.upper()}, otherwise "No".

        Question: {question}
        Correct Answer: {correct_answer}
        User Answer: {answer}
        """

        print("validate_answer_semantically")
        print(prompt)
        response = model.generate_content(prompt).text.strip().lower()
        print("response")
        print(response)
        is_correct = any(keyword in response for keyword in ["yes", "similar", "correct", "match"])
        explanation = response
        print("is_correct")
        print(is_correct)
        print("explanation")
        print(explanation)
        return is_correct, explanation

    except Exception as e:
        print(f"Validation failed: {str(e)}")
        return False, f"Validation failed: {str(e)}"


def get_rag_model_safe():
    try:
        return get_rag_model()
    except Exception as e:
        logging.warning(f"RAG model failed: {e}")
        return GenerativeModel(model_name=settings.MODEL_NAME)  # fallback without RAG

def generate_quiz_with_gemini(user_profile, num_questions=3):
    prompt = f"""
    Generate a JSON array of {num_questions} financial inclusion-related multiple choice questions tailored to.
    - Persona: {user_profile.persona}
    - Region: {user_profile.region}
    - Language: {user_profile.language}
    
    Each question should have the following fields:
    - "question": a question string
    - "options": an array of 4 strings
    - "answer": the correct answer string, from the options

    Respond only with the JSON array and no markdown or extra text.
    """

    model = GenerativeModel(model_name=settings.MODEL_NAME)

    try:
        response = model.generate_content(prompt)
        print(response)
        response_text = response.text.strip()
        print("response_text")
        print(response_text)
        quiz_data = extract_json_from_response(response_text)
        print("quiz_data")
        print(quiz_data)
        return quiz_data
    except Exception as e:
        print(f"Falling back to default questions due to: {e}")
        return DEFAULT_QUIZ_QUESTIONS


def extract_json_from_response(response_text):
    """
    Extract the JSON array from Gemini's response text,
    even if it's wrapped in markdown or contains extra text.
    """
    try:
        # Remove markdown code fences if present
        cleaned = re.sub(r"^```json|^```|```$", "", response_text.strip(), flags=re.MULTILINE)
        
        # Try to locate the first valid JSON array
        json_match = re.search(r"(\[\s*{.*}\s*\])", cleaned, flags=re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            json_str = cleaned  # fallback if entire content is JSON

        return json.loads(json_str)
    except Exception as e:
        raise ValueError(f"Failed to extract JSON: {e}")



def is_semantically_similar(user_answer, correct_answer):
    return difflib.SequenceMatcher(None, user_answer.lower(), correct_answer.lower()).ratio() > 0.7


def get_rag_model():
    corpus_resource = f"projects/{settings.GCP_PROJECT_ID}/locations/{settings.GCP_REGION}/ragCorpora/{settings.VERTEX_RAG_CORPUS_ID}"
    rag_retrieval_tool = Tool.from_retrieval(
        retrieval=rag.Retrieval(
            source=rag.VertexRagStore(
                rag_resources=[
                    rag.RagResource(rag_corpus=corpus_resource)
                ],
                rag_retrieval_config=rag.RagRetrievalConfig(
                    top_k=10,
                    filter=rag.utils.resources.Filter(vector_distance_threshold=0.5),
                ),
            )
        )
    )
    return GenerativeModel(
        model_name=settings.MODEL_NAME,
        tools=[rag_retrieval_tool]
    )

def translate_text(text, target_language):
    if target_language == 'en':
        return text
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result['translatedText']

def ask_gemini_with_rag(question, user):
    model = get_rag_model_safe()
    profile = getattr(user, "profile", None)
    if not profile:
        prompt = question  # fallback if no profile
    else:
        prompt = f"""
        You are a financial coach helping the following user:
        👤 Persona Age: {profile.age or "N/A"}
        👤 Persona Type: {profile.persona or "N/A"}
        🌍 Region: {profile.region or "N/A"}
        🏁 Financial Goal: {profile.financial_goal or "Not specified"}
        🌐 Preferred Language: {profile.language or "en"}

        Now respond to this query in a simple, friendly tone, suitable for someone from this background:

        📌 Question: {question}
        """

    print(prompt)
    response = model.generate_content(prompt)
    response_text = response.text
    print("response_text")
    print(response_text)
    if is_unhelpful_response(response_text, lang=getattr(user.profile, 'language', 'en')):
        print("is_unhelpful_response Fallback")
        fallback_model = GenerativeModel(model_name=settings.MODEL_NAME)
        fallback_prompt = build_personalized_prompt(user, question, source="NO_RAG")
        fallback_response = fallback_model.generate_content(fallback_prompt)
        response_text = fallback_response.text.strip()

    translated_response = translate_text(response.text, profile.language)

    return translated_response

def build_personalized_prompt(user, question, source="RAG"):
    context_note = "based on the knowledge from your uploaded documents." if source == "RAG" else "based on general financial knowledge."

    return f"""
    You are a financial assistant.

    User Persona:
    - Age Group: {getattr(user.profile, 'age', 'Unknown')}
    - Region: {getattr(user.profile, 'region', 'Unknown')}
    - Language: {getattr(user.profile, 'language', 'en')}
    - Financial Goal: {getattr(user.profile, 'financial_goal', 'Not specified')}

    Please answer this question {context_note}

    Question: {question}
    """


def is_unhelpful_response(text, lang='en'):
    low_info_phrases = {
        'en': [
            "i couldn't find relevant information",
            "i don't have data",
            "no relevant data",
            "i'm unable to answer that",
            "i don't know",
            "sorry",
            "couldn't find",
            "can't help with that",
            "as an ai"
        ],
        'hi': [
            "मुझे प्रासंगिक जानकारी नहीं मिली",
            "माफ़ कीजिए",
            "मैं इसका उत्तर नहीं दे सकता",
            "मेरे पास यह जानकारी नहीं है",
            "मैं इस पर मदद नहीं कर सकता",
        ],
        'mr': [
            "माफ करा",
            "माझ्याकडे संबंधित माहिती नाही",
            "मी याचे उत्तर देऊ शकत नाही",
            "माहिती उपलब्ध नाही",
            "मी मदत करू शकत नाही"
        ]
    }

    phrases = low_info_phrases.get(lang, low_info_phrases['en'])
    lowered = text.lower()
    print(lowered)
    return any(phrase.lower() in lowered for phrase in phrases)
