from src.utils import invoke_llm
from .base.search_tools import google_search
from .base.linkedin_tools import extract_linkedin_url, scrape_linkedin


SUMMARIZE_LINKEDIN_PROFILE = """
# Role  
You are an Expert Lead profile creator with a particular expertise for generating a lead profile from a from a scraped linkedin.  

# Objective  
Generate a 300-word summary of the lead's key information, focusing on their job title, expertise, and current focus, without assumptions or exaggeration. 
Your goal is to look at the provided data about the lead and generate a 300-word lead profile that clearly summarizes the lead's key information, focusing on their job title, expertise, and current focus, without assumptions or exaggeration.  

# Context  
The lead profile you are generating help sales teams understand inbound leads for meetings or calls.

# Instructions  
- Use only the provided data; no assumptions.  
- Highlight the lead's job title, expertise, and relevant context for sales interactions.  
- Keep the profile neutral and factual; avoid words like "impressive" or "seasoned."  
- Limit the profile to 300 words.   
"""

def extract_company_name(email):
    """
    Extracts the company name from a professional email address.
    """
    try:
        # Split the email to get the domain part
        company_name = email.split('@')[1]
        return company_name
    except IndexError:
        return "Company not found"

def research_lead_on_linkedin(lead_name, lead_email):
    """
    Searches for the lead's LinkedIn profile based on the lead name and company name.
    
    @param lead_name: The name of the lead to search for.
    @return: A dictionary containing the lead profile data or an error message if not found.
    """
    # extract company name from pro email
    company_name = extract_company_name(lead_email)
        
    # Find lead LinkedIn URL by searching on Google 'LinkedIn {{lead name}} {{company name}}'
    query = f"LinkedIn {lead_name} {company_name}"
    search_results = google_search(query)
    lead_linkedin_url = extract_linkedin_url(search_results)
    if not lead_linkedin_url:
        return "Lead LinkedIn URL not found."

    # Scrape lead LinkedIn profile
    linkedin_data = scrape_linkedin(lead_linkedin_url)
    if "data" not in linkedin_data:
        return "LinkedIn profile not found"
    
    # Summarize collected information about lead
    profile_data = linkedin_data["data"]
    lead_profile_content = {
        "about": profile_data.get('about', ''),
        "full_name": profile_data.get('full_name', ''),
        "location": profile_data.get('location', ''),
        "city": profile_data.get('city', ''),
        "country": profile_data.get('country', ''),
        "skills": profile_data.get('skills', []),
        "current_company": {
            "name": profile_data.get('company', ''),
            "industry": profile_data.get('company_industry', ''),
            "join_month": profile_data.get('current_company_join_month', ''),
            "join_year": profile_data.get('current_company_join_year', '')
        },
        "educations": [
            {
                "school": edu.get('school', ''),
                "field_of_study": edu.get('field_of_study', ''),
                "degree": edu.get('degree', ''),
                "date_range": edu.get('date_range', ''),
                "activities_and_societies": edu.get('activities_and_societies', '')
            } for edu in profile_data.get('educations', [])
        ],
        "experiences": [
            {
                "company": exp.get('company', ''),
                "title": exp.get('title', ''),
                "date_range": exp.get('date_range', ''),
                "is_current": exp.get('is_current', False),
                "location": exp.get('location', ''),
                "description": exp.get('description', '')
            } for exp in profile_data.get('experiences', [])
        ],
        "certifications": [
            {
                "name": cert.get('name', ''),
                "issuer": cert.get('issuer', ''),
                "date": cert.get('date', '')
            } for cert in profile_data.get('certifications', [])
        ],
        "organizations": [
            {
                "name": org.get('name', ''),
                "role": org.get('role', ''),
                "date_range": org.get('date_range', '')
            } for org in profile_data.get('organizations', [])
        ],
        "volunteer_experience": [
            {
                "organization": vol.get('organization', ''),
                "role": vol.get('role', ''),
                "date_range": vol.get('date_range', ''),
                "description": vol.get('description', '')
            } for vol in profile_data.get('volunteers', [])
        ],
        "awards": [
            {
                "name": award.get('name', ''),
                "issuer": award.get('issuer', ''),
                "date": award.get('date', ''),
                "description": award.get('description', '')
            } for award in profile_data.get('honors_and_awards', [])
        ]
    }
    
    # Extract the exact company name and LinkedIn & website url for later research
    company_name = profile_data.get('company', '')
    company_website = profile_data.get('company_website', '')
    company_linkedin_url = profile_data.get('company_linkedin_url', '')
    
    # Get Lead Linkedin profile summary
    inputs = (
        f"# Lead Name: {lead_name}\n\n"
        f"# LinkedIn Scraped Information:\n{lead_profile_content}"
    )
    profile_summary = invoke_llm(
        system_prompt=SUMMARIZE_LINKEDIN_PROFILE, 
        user_message=inputs,
        model="gemini-1.5-flash"
    )
    
    return (
        profile_summary, 
        company_name, 
        company_website,
        company_linkedin_url
    )