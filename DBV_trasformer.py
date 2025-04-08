import streamlit as st
import json
import plotly.graph_objects as go
# Import your OpenAI client libraries, etc.
from openai import OpenAI

api_key = st.text_input("Enter your OpenAI API key:", type="password")

if not api_key:
    st.warning("Please enter your OpenAI API key to continue.")
    st.stop()

client = OpenAI(api_key=api_key)

# Define your domains (same as in your Agent 1 code)
DOMAINS = [
    "Seamless Mobility: Focused on integrating technology, infrastructure, and services to provide efficient, safe, and convenient transport experiences, including autonomous driving and shared mobility solutions.",
    "Holistic Wellbeing: Centers on comprehensive approaches to health, combining digital health innovations, alternative medicine, preventive healthcare, elderly care, health literacy, and healing architecture to improve overall quality of life.",
    "Rest and Relaxation: Targets stress reduction and rejuvenation through wellness offerings such as spa treatments, fitness programs, and immersive travel experiences.",
    "New Work: Emphasizes flexible, digitally enabled work environments, fostering collaboration, gig economy platforms, remote and hybrid working models, and transformative HR practices.",
    "Personal Wealth and Legal: Deals with managing personal finances, investments, real estate, and legal affairs through innovative digital tools, open banking, decentralized finance, and professional services.",
    "Customized and Fast Demand Fulfillment: Optimizes consumer access to products and services, leveraging innovative retail solutions, e-commerce, everyday outsourcing, and the sharing economy to quickly satisfy consumer needs.",
    "Belief and Mindfulness: Encourages mental and emotional well-being through spiritual, religious, and mindfulness practices, including meditation, yoga, coaching, and esoteric approaches.",
    "Relationships: Fosters interpersonal and professional connections through social networks, digital communication, matchmaking, dating services, and networking events.",
    "Adaptive Development: Supports continuous personal and professional growth via structured education systems, lifelong learning opportunities, and scientific research initiatives.",
    "Personalized Pleasure: Offers customized entertainment experiences, including digital media streaming, gaming, arts, and sports events, tailored to individual preferences.",
    "Smart Environment: Integrates digital technologies into homes and cities to enhance living conditions, safety, sustainability, and efficiency through smart homes, DIY improvements, and smart city initiatives.",
    "Security: Provides comprehensive protection through robust defense, law enforcement, identity management, cybersecurity, justice systems, and privacy protection services.",
    "Infrastructure: Builds foundational digital and physical systems necessary for modern society, including smart energy grids, logistics, telecommunications, e-government, financial transactions, and intelligent building construction.",
    "B2B-Services: Enables business success through specialized services like accounting, B2B banking and insurance, business administration, consulting, and legal support.",
    "Industrie 4.0: Transforms manufacturing and production through digital technologies such as IoT, AI, robotics, predictive maintenance, and 3D printing, allowing greater efficiency and customization."
]

# =========================
# Agent 1: Company Analysis
# =========================

def get_company_analysis(api_key, company_name):
    """
    Get company analysis using OpenAI API.
    Returns a JSON with scores and detailed explanations.
    """
    if not api_key or not company_name:
        return None
    
    # Replace with your actual OpenAI API client code
    # Here is a sample prompt building logic:
    prompt = f"""You are a business analyst expert. Please analyze {company_name} across these business domains and provide a JSON response.
    
    For each of these domains, provide a score (0-10) and detailed explanation:
    {', '.join([domain.split(':')[0] for domain in DOMAINS])}
    
    IMPORTANT: Your response must be a valid JSON object with this exact structure (no additional text):
    {{
        "Seamless Mobility": {{"score": 0, "explanation": "detailed explanation"}},
        "Holistic Wellbeing": {{"score": 0, "explanation": "detailed explanation"}},
        "Rest and Relaxation": {{"score": 0, "explanation": "detailed explanation"}},
        "New Work": {{"score": 0, "explanation": "detailed explanation"}},
        "Personal Wealth and Legal": {{"score": 0, "explanation": "detailed explanation"}},
        "Customized and Fast Demand Fulfillment": {{"score": 0, "explanation": "detailed explanation"}},
        "Belief and Mindfulness": {{"score": 0, "explanation": "detailed explanation"}},
        "Relationships": {{"score": 0, "explanation": "detailed explanation"}},
        "Adaptive Development": {{"score": 0, "explanation": "detailed explanation"}},
        "Personalized Pleasure": {{"score": 0, "explanation": "detailed explanation"}},
        "Smart Environment": {{"score": 0, "explanation": "detailed explanation"}},
        "Security": {{"score": 0, "explanation": "detailed explanation"}},
        "Infrastructure": {{"score": 0, "explanation": "detailed explanation"}},
        "B2B-Services": {{"score": 0, "explanation": "detailed explanation"}},
        "Industrie 4.0": {{"score": 0, "explanation": "detailed explanation"}}
    }}
    
    Note: Each score must be an integer between 0 and 10, and each explanation should be a detailed paragraph.
    """
    
    try:
        # Make the actual API call
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a business analyst expert that provides detailed domain analysis in JSON format. You must return a valid JSON object with scores and explanations for each domain."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            response_format={ "type": "json_object" }
        )
        
        # Extract the response content
        response_text = response.choices[0].message.content
        print(f"Raw response: {response_text}")  # Debug print
        parsed_response = json.loads(response_text)
        return parsed_response
    except json.JSONDecodeError as e:
        st.error(f"Error parsing JSON response: {str(e)}")
        st.error(f"Raw response was: {response_text}")
        return None
    except Exception as e:
        st.error(f"Error in Agent 1 API call: {str(e)}")
        return None

def create_radar_chart(data, company_name):
    """Create a radar chart using Plotly."""
    fig = go.Figure()
    domain_names = [domain.split(':')[0] for domain in DOMAINS]
    scores = [data[domain.strip()]["score"] for domain in domain_names]
    
    fig.add_trace(go.Scatterpolar(
        r=scores + [scores[0]],
        theta=domain_names + [domain_names[0]],
        fill='toself',
        name=company_name
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10]
            )
        ),
        showlegend=True
    )
    
    return fig

# =========================
# Agent 2: Domain-Based Vision Ideation
# =========================

def get_domain_based_vision(api_key, company_name, original_vision, analysis_results):
    """
    Use OpenAI API to create a domain-based vision statement.
    This should blend the original vision with insights from the domain analysis.
    """
    prompt = f"""You are an innovative business strategist. Given the company {company_name} and its original vision:
    
    "{original_vision}"
    
    and the following domain analysis insights: {json.dumps(analysis_results, indent=2)}
    
    Please ideate and produce a refined, domain-based vision statement that integrates human-centric needs across various industries.
    
    IMPORTANT: Your response must be a single, well-structured paragraph that:
    1. Starts with the company name
    2. Incorporates insights from the domain analysis
    3. Maintains the core essence of the original vision
    4. Is forward-looking and inspirational
    5. Is between 100-150 words
    
    Do not include any additional text or formatting in your response.
    """
    
    try:
        # Make the actual API call
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an innovative business strategist that creates refined vision statements. You must return a single, well-structured paragraph."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        # Extract the response content
        response_text = response.choices[0].message.content
        print(f"Raw response: {response_text}")  # Debug print
        return response_text.strip()
    except Exception as e:
        st.error(f"Error in Agent 2 API call: {str(e)}")
        return None

# =========================
# Agent 3: Inspirational Company Search
# =========================

def find_inspirational_companies(api_key, refined_vision):
    """
    Use OpenAI API to list companies in other industries with similar visions.
    Return a list of companies along with reasons for their inspirational value.
    """
    prompt = f"""You are an expert market researcher. Given the refined vision statement:
    
    "{refined_vision}"
    
    Please provide a list of companies from various industries that embody a similar vision. For each company, provide a brief explanation why they can serve as inspiration.
    
    IMPORTANT: Your response must be a valid JSON object with a single key "companies" containing an array of exactly 3 objects. Each object must have exactly two keys: "company" and "explanation".
    
    Example format:
    {{
        "companies": [
            {{
                "company": "Company Name 1",
                "explanation": "Brief explanation of why this company is inspirational"
            }},
            {{
                "company": "Company Name 2",
                "explanation": "Brief explanation of why this company is inspirational"
            }},
            {{
                "company": "Company Name 3",
                "explanation": "Brief explanation of why this company is inspirational"
            }}
        ]
    }}
    """
    
    try:
        # Make the actual API call
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert market researcher that provides lists of inspirational companies in JSON format. You must return exactly 3 companies in a valid JSON object with a 'companies' array."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            response_format={ "type": "json_object" }
        )
        
        # Extract the response content
        response_text = response.choices[0].message.content
        print(f"Raw response: {response_text}")  # Debug print
        parsed_response = json.loads(response_text)
        
        # Verify the response structure
        if "companies" not in parsed_response:
            st.error("Response missing 'companies' key")
            return None
            
        companies = parsed_response["companies"]
        if not isinstance(companies, list):
            st.error("'companies' is not a list")
            return None
            
        if len(companies) != 3:
            st.error(f"Expected 3 companies, got {len(companies)}")
            return None
            
        for company in companies:
            if not isinstance(company, dict):
                st.error("Company entry is not a dictionary")
                return None
            if "company" not in company or "explanation" not in company:
                st.error("Company entry missing required keys")
                return None
                
        return companies
    except json.JSONDecodeError as e:
        st.error(f"Error parsing JSON response: {str(e)}")
        st.error(f"Raw response was: {response_text}")
        return None
    except Exception as e:
        st.error(f"Error in Agent 3 API call: {str(e)}")
        return None

# =========================
# Agent 4: Business Model Ideation
# =========================

def suggest_business_models(api_key, inspirational_companies, refined_vision):
    """
    Use OpenAI API to ideate specific business models.
    Leverage the inspirational companies and refined vision to propose models that the focal company could adopt.
    """
    prompt = f"""You are a creative business model strategist. Based on the refined vision:
    
    "{refined_vision}"
    
    and taking inspiration from these companies: {json.dumps(inspirational_companies, indent=2)},
    
    please suggest several innovative business models that the company could introduce to optimize its vision.
    
    IMPORTANT: Your response must be a valid JSON object containing exactly 3 business models. Each model should have a descriptive title as the key and a brief explanation as the value.
    
    Example format:
    {{
        "Subscription-based Service Model": "Description of how this model would work and its benefits",
        "Platform-as-a-Service Model": "Description of how this model would work and its benefits",
        "Freemium Model": "Description of how this model would work and its benefits"
    }}
    """
    
    try:
        # Make the actual API call
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a creative business model strategist that provides business model suggestions in JSON format. You must return exactly 3 business models in a valid JSON object."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            response_format={ "type": "json_object" }
        )
        
        # Extract the response content
        response_text = response.choices[0].message.content
        print(f"Raw response: {response_text}")  # Debug print
        parsed_response = json.loads(response_text)
        return parsed_response
    except json.JSONDecodeError as e:
        st.error(f"Error parsing JSON response: {str(e)}")
        st.error(f"Raw response was: {response_text}")
        return None
    except Exception as e:
        st.error(f"Error in Agent 4 API call: {str(e)}")
        return None

# =========================
# Main Streamlit Application
# =========================

def main():
    st.title("Company Vision and Domain Strategy Analyzer")
    
    # User inputs for API key, company name, and original vision statement
    company_name = st.text_input("Enter the company name:")
    original_vision = st.text_area("Enter the company's original vision statement:")
    
    analyze_button = st.button("Analyze Company")
    
    if analyze_button:
        if not company_name:
            st.error("Please enter a company name.")
            return
        
        # ----- Agent 1: Company Analysis -----
        with st.spinner("Analyzing company domains..."):
            analysis_results = get_company_analysis(api_key, company_name)
        if analysis_results:
            st.subheader("Domain Performance Overview")
            fig = create_radar_chart(analysis_results, company_name)
            st.plotly_chart(fig, use_container_width=True)
            
            st.subheader("Detailed Analysis")
            cols = st.columns(2)
            for idx, domain in enumerate(DOMAINS):
                col = cols[idx % 2]
                with col:
                    domain_name = domain.split(':')[0].strip()
                    score = analysis_results[domain_name]["score"]
                    explanation = analysis_results[domain_name]["explanation"]
                    st.markdown(f"""
                    **{domain}**  
                    **Score:** {score}/10  
                    {explanation}
                    """)
        else:
            st.error("Failed to obtain domain analysis from Agent 1.")
        
        # ----- Agent 2: Domain-Based Vision Ideation -----
        if original_vision:
            with st.spinner("Refining vision statement..."):
                refined_vision = get_domain_based_vision(api_key, company_name, original_vision, analysis_results)
            if refined_vision:
                st.subheader("Refined Domain-Based Vision Statement")
                st.write(refined_vision)
            else:
                st.error("Agent 2 could not generate a refined vision statement.")
        else:
            st.error("Please provide the company's original vision statement for further ideation.")
        
        # ----- Agent 3: Inspirational Company Search -----
        if refined_vision:
            with st.spinner("Searching for inspirational companies..."):
                inspirational_companies = find_inspirational_companies(api_key, refined_vision)
            if inspirational_companies:
                st.subheader("Inspirational Companies")
                for comp in inspirational_companies:
                    st.markdown(f"**{comp['company']}**: {comp['explanation']}")
            else:
                st.error("Agent 3 could not find inspirational companies.")
        
        # ----- Agent 4: Business Model Ideation -----
        if inspirational_companies and refined_vision:
            with st.spinner("Generating business model ideas..."):
                business_models = suggest_business_models(api_key, inspirational_companies, refined_vision)
            if business_models:
                st.subheader("Proposed Business Models")
                for model, explanation in business_models.items():
                    st.markdown(f"**{model}**: {explanation}")
            else:
                st.error("Agent 4 could not generate business model ideas.")

if __name__ == "__main__":
    main()
