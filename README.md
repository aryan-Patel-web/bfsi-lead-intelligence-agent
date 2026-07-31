# AI-Sales-Outreach-Automation

### 👉 Dive into the full article: [**AI Agents + LangGraph: The Winning Formula for Sales Outreach Automation**](https://dev.to/kaymen99/how-ai-automation-can-transform-your-sales-outreach-strategy-aop)  

![outreach-automation](https://github.com/user-attachments/assets/2685ef70-ab9f-4177-9b2a-71086f79726b)

I built an **AI-powered outreach system** designed to integrate with multiple **CRMs**, automate lead research, and enhance the lead generation process. The system analyzes **LinkedIn data**, company websites, recent news, and social media activities to gather comprehensive insights on potential leads. Based on this information, it generates detailed **analysis reports** that highlight lead challenges, gaps, and opportunities for engagement.

The system also creates customized **outreach materials**, including **personalized emails**, **interview preparation scripts**, and **tailored outreach reports** that showcase how our solutions can address the lead's pain points, supported by previous results and case studies.

For this project, I created a sample AI marketing agency, **ElevateAI Marketing Solutions**, which focuses on optimizing and automating content strategies and enhancing digital presence using AI.

While designed for **ElevateAI**, this system can easily be adapted for any agency or freelancer looking to streamline their lead outreach and improve engagement with prospects. With its customizable features, it offers a powerful, automated approach to lead generation.

## Features

### **Multi-CRM Integration**
- Seamlessly connect with popular CRMs like **HubSpot**, **Airtable**, **Google Sheets**, or add your own custom CRM functionality using a standardized schema.

### **Automated Lead Research**
- **LinkedIn Profile Scraping**: Automatically collect essential details about the lead and their company from LinkedIn to create a comprehensive profile.  
- **Company Digital Presence Analysis**: Evaluate the company's website and blog content for insights into their products and services. Additionally, assess their social media activity across platforms like **Facebook**, **Twitter**, **YouTube**, and others.  
- **Recent Company News Analysis**: Keep track of the latest news and announcements related to the company to gain insights into their current initiatives and challenges.  
- **Pain Point Identification**: Identify potential challenges or gaps faced by the company, and provide tailored recommendations on how your agency's offerings and services can address them.  
- **Report Generation**: Generate detailed reports for each analysis, which are saved both locally and in **Google Docs**. A consolidated global research report is created, combining insights from the lead profile, company profile, and digital presence. (You can find examples of the reports in the `/reports` folder.)  

### **Lead Qualification**
Automatically assess and qualify leads based on the gathered data and your predefined criteria, here are some examples of criteria that I used:
- **Digital Presence (Website & Blog)**: Evaluate the quality and relevance of the company’s online presence.
- **Social Media Activity**: Analyze the company’s engagement and activity across various social media platforms.
- **Industry Fit**: Assess how well the company aligns with your target industries and their current or potential use of **AI** and **automation** in marketing.
- **Company Scale and Potential**: Evaluate the company’s size, growth potential, and market expansion indicators such as new hires or funding.

*Note: These criteria can be modified according to specific requirements.*

### **Personalized Outreach**
- **Customized Outreach Report**: Generate a customized outreach report for each lead, highlighting their challenges or gaps, how your services can address them, and referencing previously obtained results and similar case studies (uses RAG to extract them). The report is saved to **Google Docs** for easy sharing.
- **Create Personalized Email**: Craft personalized email templates, including a link to the custom outreach report, to engage qualified leads effectively.
- **Prepare Personalized Interview Script**: Generate a tailored interview script, complete with **SPIN** questions, to help prepare for calls with leads and ensure productive conversations.

### **Efficient Workflow**
- **Seamless Collaboration**: all generated research and outreach reports are saved both locally and in **Google Docs**, ensuring easy access and collaboration across teams.
- **Automated CRM Updates**: Keep your CRM up to date with the latest lead status and links to generated reports, streamlining your outreach efforts.

## System Workflow

The system follows the process to manage lead research and outreach efficiently (check the detailed workflow description [here](https://github.com/kaymen99/sales-outreach-automation-langgraph/tree/main/docs/system-workflow.md) and a visual diagram [here](https://github.com/kaymen99/sales-outreach-automation-langgraph/blob/main/workflow.png)):

1. **Fetch Leads**: Connect to your CRM to fetch new leads.
2. **Research & Insights**:
   - Gather and analyze key information for each lead:
     - Scrape **LinkedIn profiles**.
     - Analyze **company digital presence** (website, blogs, social media, recent news).
   - Generate detailed analysis reports for each lead combining insights from all previous research. (You can find examples of the reports in the `/reports` folder.)  
3. **Lead Qualification**: Evaluate each lead based on specific criteria such as **digital presence**, **social media activity**, **industry fit**, or **company scale**.
4. **Outreach Preparation**: For qualified leads, generate personalized outreach materials:
     - A **customized outreach report** detailing identified challenges faced by the company and how our services can address them, the system will use RAG to fetch similar case studies (from our internal knowledge base) to be referenced in the report.
     - A **personalized email** tailored to the lead with a link to the outreach report.
     - A **customized interview script** to prepare for calls with leads.
5. **Update CRM**: All generated research and outreach materials are saved locally and to **Google Docs**, and the CRM is updated with the latest lead status and links to the reports.


### Advantages of This automation

- **Automated Lead Research & Qualification**: The system streamlines lead research by gathering insights from LinkedIn, company websites, social media, and more. It ensures every lead is thoroughly evaluated based on criteria tailored to your agency’s needs.

- **Increased Outreach Reply Rates & Conversions**: Instead of sending a simple standalone email, the system generates a detailed audit report for each lead, attached to the email. These reports demonstrate that you’ve thoroughly researched their business, identified key challenges, and can provide tailored solutions, supported by relevant case studies. This approach increases the likelihood of positive responses, boosting your outreach reply rates and conversions.

- **Time-Saving & Optimized Team Efficiency**: By automating lead research and generating reports with valuable insights, challenges, and recommendations, the system saves time and enhances teamwork. It provides a prepared interview script to help your team engage clients effectively during calls, and the comprehensive reports enable them to quickly craft and present tailored solutions to potential clients.


## Integration with APIs

- **Airtable CRM**: To integrate with your Airtable contacts CRM, you must [sign up](https://www.airtable.com/) for an Airtable account and create your own contacts database with the relevant fields.
- **HubSpot CRM**: To integrate with your HubSpot contacts CRM, sign up for a [HubSpot account](https://www.hubspot.com/), then create a private app and obtain your API key. [Follow this tutorial](https://www.youtube.com/watch?v=hSipSbiwc2s) for guidance.
- **LinkedIn Data**: Scrape profile information using the **RapidAPI LinkedIn Profile Data API**. [Get your API key here](https://rapidapi.com/freshdata-freshdata-default/api/fresh-linkedin-profile-data).
- **Google APIs**: Used to access **Google Docs**, **Google Sheets** (needed only when used as CRM source), and **Gmail**. Follow [this guide](https://developers.google.com/gmail/api/quickstart/python) and ensure all required APIs are enabled.
- **Google Searches**: Perform web searches using the **Serper API**. [Get your API key here](https://serper.dev).
- **LLM**: Leverages **Google Gemini LLM models** (Flash and Pro) and their Embedding model. [Get your API key here](https://ai.google.dev/gemini-api/docs/api-key).

## Tech Stack

- **[Langchain](https://python.langchain.com/docs/introduction/)**: Framework for interacting with multiple LLMs like GPT-4, Gemini, LLAMA3 and building AI agents and RAG applications.
- **[Langgraph](https://langchain-ai.github.io/langgraph/)**: Framework for building AI agents and automation workflows.

## How to Run

### Prerequisites

- Python 3.9+
- Google Gemini API key (or choose other LLM providers like OpenAI or Groq).
- Google APIs credentials.
- API keys for integrated tools (RapidAPI, Serper API).
- API keys and configurations for your chosen CRM (check `.env.example` for more information).
- Necessary Python libraries (listed in `requirements.txt`).

### Setup

1. **Clone the repository:**

   ```sh
   git clone https://github.com/kaymen99/sales-outreach-automation-langgraph.git
   cd sales-outreach-automation-langgraph
   ```

2. **Create and activate a virtual environment:**

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**

   ```sh
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**

   Create a copy of the `.env.example` file:

   ```bash
   cp .env.example .env
   ```

   After running this command, open the new `.env` file and add your API keys as needed.

---

### Start the Application

Run the main script to begin automation:

```sh
python main.py
```

The system will connect with your CRM to fetch new leads, perform automated research, qualify leads, and generate personalized outreach materials (You can see examples of reports generated, including the personalized email in the `/reports` folder).

---

### Customizing the Automation

For developers who wish to integrate their own CRM or customize the behavior of the automation, please refer to the [Customization Guide](./docs/customization.md). The guide covers:

- **Add your own service/product data**: The `/data` folder includes agency details and past case studies used in reports, emails, and interviews generation. You should update these files to reflect your own service/product details and your past case studies.
- **Integrating Custom CRMs**: Instructions for adding your CRM to the system by extending the base class.
- **Customizing Lead Statuses**: Learn how to modify the statuses used to filter and fetch leads.
- **Updating CRM Fields**: Tailor the functions in the `OutReachAutomationNodes` class to handle different CRM field names or additional fields.
- **Customizing Prompts**: Update the prompts used for qualifying leads, generating reports, personalizing emails, and preparing interview questions.

---

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or features you’d like to see.

## Contact

For questions or suggestions, contact me at `patel914078@gmail.com`.