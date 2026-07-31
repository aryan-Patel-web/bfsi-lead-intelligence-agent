from src.utils import invoke_llm
from .base.linkedin_tools import scrape_linkedin

CREATE_COMPANY_PROFILE = """
### Role  
You are an Expert Company profile generator with a particular expertise for generating a company profile from their scraped LinkedIn & website pages. 

### Objective  
Your goal is to look through the scraped LinkedIn company profile & website and create a 300-word company profile summarizing its operations, value proposition, target audience, products/services, location, company size, year founded and any other relevant information that might be useful to use when meeting the inbound lead that works for this company .

### Context  
This profile provides context for engaging with a prospect who works at the company.  

### Instructions  
- If no data is available from LinkedIn *and* the website, output only: *"No company info available."*  
- Use the available data from one or both sources; do not assume or invent information.  
- Always include:  
  - Company description  
  - Value proposition  
  - Target audience  
  - Products/services  
  - Location, size, and year founded  
- Keep the tone neutral and factual; avoid hype or subjective language.  
- Limit the profile to 300 words.  
"""

def research_lead_company(linkedin_url):
    # Scrape company LinkedIn profile
    company_page_content = scrape_linkedin(linkedin_url, True)
    if "data" not in company_page_content:
        return "LinkedIn profile not found"
    
    # Structure collected information about company
    company_profile = company_page_content["data"]
    return {
        "company_name": company_profile.get('company_name', ''),
        "description": company_profile.get('description', ''),
        "year_founded": company_profile.get('year_founded', ''),
        "industries": company_profile.get('industries', []),
        "specialties": company_profile.get('specialties', ''),
        "employee_count": company_profile.get('employee_count', ''),
        "social_metrics": {
            "follower_count": company_profile.get('follower_count', 0)
        },
        "locations": company_profile.get('locations', [])
    }

def generate_company_profile(company_linkedin_info, scraped_website):
    # Get company profile summary
    inputs = (
        f"# Scraped Website:\n {scraped_website}\n\n"
        f"# Company LinkedIn Information:\n{company_linkedin_info}"
    )
    profile_summary = invoke_llm(
        system_prompt=CREATE_COMPANY_PROFILE, 
        user_message=inputs,
        model="gemini-1.5-flash"
    )
    return profile_summary