# utils.py
import re
import fitz  # PyMuPDF (corrige l'erreur 'fitz' is not defined)
from django.conf import settings
from django.utils import timezone
import google.generativeai as genai
import time
from langdetect import detect
import logging
import json





# Configure Gemini API
genai.configure(api_key=settings.GEMINI_API_KEY)
MODEL = genai.GenerativeModel('gemini-1.5-flash-latest')

# Configuration du logger pour capturer les erreurs
logger = logging.getLogger(__name__)



def validate_password(password):
    """
    Verifies the strength of the password.
    Passwords must contain:
        - At least 8 characters
        - A mix of uppercase and lowercase letters
        - A digit
        - A special character
    """
    if len(password) < 8:
        return "Password must be at least 8 characters long."
    if not re.search(r'(?=.*[A-Z])(?=.*[a-z])', password):
        return "Password must contain at least one uppercase and one lowercase letter."
    if not re.search(r'\d', password):
        return "Password must contain at least one number."
    if not re.search(r'[^a-zA-Z0-9]', password):
        return "Password must contain at least one special character."
    return None

def extract_text_from_pdf(file):
    """Extract raw text from a PDF using PyMuPDF."""
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text("text") or ""
    doc.close()
    return text

def detect_job_language(job_description):
    try:
        lang = detect(job_description)
        lang_map = {
            'fr': 'French',
            'en': 'English',
            'es': 'Spanish',
            'de': 'German',
            'it': 'Italian'
        }
        return lang_map.get(lang, 'English')
    except:
        return 'English'
def calculate_match_score(resume_text, job_offer_text, plan):
    """Calculate a match score using Gemini."""
    lang = detect_job_language(resume_text)
    prompt = f"""
    Compare the following resume and job offer to determine their match.
    Provide a match score from 0 to 100 based on skills, experience, and relevance.
    Resume: {resume_text[:4000]}
    Job Offer: {job_offer_text[:4000]}
    Plan: {plan} (for Premium, give more weight to technical skills and relevant experience).
    Respond with an integer score only (e.g., 75).
    Language: {lang}
    """
    response = MODEL.generate_content(prompt)
    score = int(response.text.strip())
    return min(max(score, 0), 100)

def generate_suggestions(resume_text, job_offer_text, plan):
    """Generate structured suggestions to improve the resume in English without formatting characters."""
    suggestion_count = 3 if plan == "Free" else 10
    detail_level = "short and precise (max 20 words per suggestion)" if plan == "Free" else "detailed with explanations (1-2 sentences per suggestion)"

    prompt = f"""
    Analyze the following resume and job offer.
    Provide exactly {suggestion_count} specific suggestions to improve the resume to better match the job offer.
    Resume: {resume_text[:4000]}
    Job Offer: {job_offer_text[:4000]}
    Plan: {plan}
    - Format as a bullet list using '- ' for each suggestion.
    - Each suggestion must be {detail_level}.
    - Ensure suggestions are actionable, relevant, and avoid vague phrases like 'improve your resume'.
    - All suggestions must be in English, regardless of the input language.
    - Do not include special characters like stars (★), bold markers (**), or other formatting symbols in the suggestion text.
    - Example for Free: '- Add Python skills to match job requirements.'
    - Example for Premium: '- Add Python skills to technical section because the job requires advanced programming expertise.'
    Respond with the suggestion list only.
    """
    response = MODEL.generate_content(prompt)
    suggestions = response.text.strip()

    # Post-process to remove any ** characters in case the model still includes them
    suggestions = suggestions.replace('**', '')

    # Validation du format et du nombre
    suggestion_lines = [line for line in suggestions.split('\n') if line.strip().startswith('- ')]
    if len(suggestion_lines) != suggestion_count or not suggestions.startswith('- '):
        suggestions = f"- Error: Expected {suggestion_count} suggestions, got {len(suggestion_lines)}. Please try again."

    return suggestions


def generate_optimized_resume(resume_text, job_offer_text, version):
    """
    Generate an optimized resume with a clean, structured format.
    Args:
        resume_text (str): Extracted text from the original resume.
        job_offer_text (str): Text from the job offer.
        version (int): 1 for skills-focused, 2 for experience-focused.
    Returns:
        str: Optimized resume text or original text if optimization fails.
    """
    try:
        lang = detect(resume_text) if resume_text.strip() else "fr"  # Français par défaut
        lang = "fr" if lang.startswith("fr") else "en"
        
        version_instructions = {
            1: "Focus on aligning skills: add, rephrase, or emphasize key skills from the job offer. List skills concisely without repetition.",
            2: "Focus on tailoring experience: reorder, detail, or emphasize relevant experiences. Avoid duplicating entries."
        }
        
        prompt = f"""
        You are an expert resume optimizer. Create an optimized resume based on the provided resume and job offer. Use a simple, professional structure with the following sections: Profil, Formation Académique, Compétences, Expérience (if applicable).

        **Resume**:
        {resume_text[:6000]}

        **Job Offer**:
        {job_offer_text[:6000]}

        **Instructions**:
        - {version_instructions[version]}
        - Structure the resume with these sections in order: Profil, Formation Académique, Compétences, Expérience.
        - Keep each section concise and relevant to the job offer.
        - Correct spelling/grammar errors (e.g., 'Écócialité' to 'Spécialité', 'logicie' to 'logiciel').
        - Avoid repeating entries (e.g., do not repeat 'Spécialité: Génie logiciel').
        - Separate sections with double newlines (\\n\\n).
        - Use a professional, concise tone matching the original resume.
        - Output in {lang} language.
        - Return only the optimized resume text, without comments.

        **Output Format**:
        Profil\n\n[Short professional summary]\n\nFormation Académique\n\n[Education details]\n\nCompétences\n\n[Key skills]\n\nExpérience\n\n[Relevant experience, if any]
        """
        
        response = MODEL.generate_content(prompt)
        optimized_text = response.text.strip() if hasattr(response, 'text') else response
        
        if not optimized_text or len(optimized_text) < 50:
            logger.warning(f"Invalid response from MODEL for version {version}")
            return resume_text
        
        # Supprimer les répétitions
        lines = optimized_text.split("\n")
        unique_lines = []
        for line in lines:
            if line.strip() and line not in unique_lines:
                unique_lines.append(line)
        optimized_text = "\n".join(unique_lines)
        
        return optimized_text
    
    except Exception as e:
        logger.error(f"Error in generate_optimized_resume (version {version}): {str(e)}")
        return resume_text

def check_subscription_expiration(user):
    """Check and update subscription expiration status."""
    from .models import UserSubscription  # Importé ici pour éviter circular imports
    subscription = UserSubscription.objects.filter(user=user).first()
    if subscription and subscription.plan == "Premium" and subscription.expiration_date and subscription.expiration_date < timezone.now():
        subscription.plan = "Free"
        subscription.expiration_date = None
        subscription.save()

def analyze_cv_structure(cv_content):
    # Robust regex patterns for personal info
    email = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', cv_content, re.IGNORECASE)
    phone = re.search(r'(\+?\d{1,3}[-.\s]?)?(\d{2,4}[-.\s]?){2,3}\d{2,4}', cv_content)
    github = re.search(r'(?:github\.com/)[A-Za-z0-9_-]+', cv_content, re.IGNORECASE)
    linkedin = re.search(r'(?:linkedin\.com/in/)[A-Za-z0-9_-]+', cv_content, re.IGNORECASE)

    personal_info = {
        "email": email.group(0) if email else None,
        "phone": phone.group(0) if phone else None,
        "github": github.group(0) if github else None,
        "linkedin": linkedin.group(0) if linkedin else None
    }

    return {
        "has_contact_info": bool(email or phone or github or linkedin),
        "has_education": any(keyword in cv_content.lower() for keyword in ["education", "formation", "diplôme"]),
        "has_experience": any(keyword in cv_content.lower() for keyword in ["expérience", "emploi", "stage"]),
        "has_skills": any(keyword in cv_content.lower() for keyword in ["compétence", "skill", "expertise"]),
        "languages": set(re.findall(r'(français|anglais|espagnol|allemand|italien)', cv_content.lower())),
        "potential_skills": set(re.findall(r'(java|python|c\+\+|javascript|sql|aws|docker|git|agile)', cv_content.lower())),
        "personal_info": personal_info
    }

def extract_job_keywords(job_description):
    prompt = f"""
    Analyse cette offre d’emploi et extrais en JSON :
    {{
        "technical_skills": [],
        "soft_skills": [],
        "education": [],
        "experience": [],
        "industry": []
    }}
    Offre d’emploi : {job_description}
    """
    try:
        response = MODEL.generate_content(prompt)
        json_match = re.search(r'```json\s*(.*?)\s*```', response.text, re.DOTALL)
        json_str = json_match.group(1) if json_match else response.text
        return json.loads(json_str)
    except Exception as e:
        return {"technical_skills": [], "soft_skills": [], "education": [], "experience": [], "industry": []}
    
def optimize_cv(cv_content, job_description, cv_analysis):
    job_language = detect_job_language(job_description)
    section_titles = {
        'English': {
            'contact': 'CONTACT',
            'profile': 'PROFILE',
            'education': 'EDUCATION',
            'skills': 'SKILLS',
            'experience': 'EXPERIENCE',
            'languages': 'LANGUAGES',
            'certifications': 'CERTIFICATIONS'
        },
        'French': {
            'contact': 'CONTACT',
            'profile': 'PROFIL',
            'education': 'FORMATION',
            'skills': 'COMPÉTENCES',
            'experience': 'EXPÉRIENCE',
            'languages': 'LANGUES',
            'certifications': 'CERTIFICATIONS'
        }
    }
    titles = section_titles.get(job_language, section_titles['English'])

    # Prepare personal info for prompt
    personal_info = cv_analysis["personal_info"]
    personal_info_str = ""
    if personal_info["email"]:
        personal_info_str += f"Email: {personal_info['email']}\n"
    if personal_info["phone"]:
        personal_info_str += f"Phone: {personal_info['phone']}\n"
    if personal_info["github"]:
        personal_info_str += f"GitHub: {personal_info['github']}\n"
    if personal_info["linkedin"]:
        personal_info_str += f"LinkedIn: {personal_info['linkedin']}\n"

    structure_info = ""
    if cv_analysis:
        missing = [s for s, v in cv_analysis.items() if not v and s in ["has_contact_info", "has_education", "has_experience", "has_skills"]]
        if missing:
            structure_info = f"Le CV manque : {', '.join(missing)}."
        if cv_analysis["languages"]:
            structure_info += f"\nLangues : {', '.join(cv_analysis['languages'])}."
        if cv_analysis["potential_skills"]:
            structure_info += f"\nCompétences : {', '.join(cv_analysis['potential_skills'])}."
        if personal_info_str:
            structure_info += f"\nInformations personnelles :\n{personal_info_str}"

    job_keywords = extract_job_keywords(job_description)
    keywords_info = f"""
    Offre d’emploi :
    - Compétences techniques : {', '.join(job_keywords['technical_skills'])}
    - Soft skills : {', '.join(job_keywords['soft_skills'])}
    - Formation : {', '.join(job_keywords['education'])}
    - Expérience : {', '.join(job_keywords['experience'])}
    - Secteur : {', '.join(job_keywords['industry'])}
    """

    prompt = f"""
    Optimise ce CV pour l’offre d’emploi suivante en respectant ces directives et en écrivant entièrement en {job_language} :
    - CV actuel : {cv_content}
    - Offre : {job_description}
    - Analyse CV : {structure_info}
    - Mots-clés : {keywords_info}

    **Directives** :
    1. Structure : NOM, Titre, {titles['contact']}, {titles['profile']} (3-4 lignes), {titles['education']}, {titles['skills']}, {titles['experience']}, {titles['languages']}, {titles['certifications']}.
    2. Section {titles['contact']} : Inclure les informations personnelles suivantes, mot pour mot, une par ligne, dans cet ordre (omettre si non disponible) :
       - Email: {personal_info['email'] or 'N/A'}
       - Phone: {personal_info['phone'] or 'N/A'}
       - GitHub: {personal_info['github'] or 'N/A'}
       - LinkedIn: {personal_info['linkedin'] or 'N/A'}
    3. Expériences : Chaque entrée doit suivre ce format exact sur une ligne : **Poste** | **Entreprise** | Dates | Lieu, suivi de 3-4 réalisations (puces avec •, verbes d’action, chiffres). Poste et Entreprise doivent être en gras.
    4. Optimisation : Mots-clés exacts, réalisations quantifiées, concis (2 pages max).
    5. Format : Titres en MAJUSCULES, professionnel, cohérent. Utiliser • pour les puces. Séparateurs dans l’expérience doivent être des pipes (|).
    6. Langue : Générer le CV entièrement en {job_language}, avec une terminologie appropriée.

    Retourne uniquement le contenu du CV optimisé, formaté en texte brut avec les titres en MAJUSCULES.
    """
    try:
        response = MODEL.generate_content(prompt)
        optimized_cv = response.text
        return optimized_cv
    except Exception as e:
        return "Erreur lors de la génération du CV."
