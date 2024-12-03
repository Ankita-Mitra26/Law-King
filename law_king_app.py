import os
import google.generativeai as genai
import streamlit as st
#backend
# Ensure the API key is set correctly
os.environ["GEMINI_API_KEY"] = "AIzaSyC8ny8wMxx8wNXtbEg1TPmF7d_geRPIfW0"
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Define generation settings
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
}

# Create the model instance
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Define legal keywords
LEGAL_KEYWORDS = [
    # Add your list of legal keywords here
    "Law", "Justice", "Judiciary", "Constitution", "Statute", "Legislation", 
    "Bill", "Ordinance", "Act", "Amendment", "Case Law", "Precedent",
     # General Consumer Protection Terms
    "consumer law", "consumer protection", "consumer rights", "unfair trade practices", 
    "consumer complaint", "consumer advocacy", "consumer fraud", "consumer safety", 
    "false advertising", "product liability", "consumer credit", "warranty law", 
    "consumer guarantees", "consumer dispute resolution",
    
    # Regulations and Authorities
    "consumer protection agency", "Federal Trade Commission (FTC)", "Consumer Financial Protection Bureau (CFPB)", 
    "Bureau of Consumer Protection", "consumer law enforcement agency", "consumer watchdog", 
    "consumer protection regulations", "trade regulation", "consumer legislation", 
    "mandatory disclosure", "consumer standards", "fair trading laws",
    
    # Consumer Rights and Protections
    "right to refund", "right to replacement", "right to repair", "right to cancel", 
    "misleading representations", "defective products", "consumer guarantees act", 
    "contract terms", "cooling-off period", "unfair contract terms", "truth in advertising", 
    "right to be informed", "right to fair treatment", "class action lawsuits",
    
    # E-Commerce and Digital Consumer Law
    "online consumer protection", "e-commerce regulations", "digital consumer rights", 
    "online fraud", "privacy policy", "data protection laws", "cookie consent", 
    "digital contracts", "terms of service violations", "cybersecurity for consumers", 
    "identity theft protection", "electronic signatures law", "consumer rights in online purchases",
    
    # Financial Consumer Protection
    "consumer credit regulation", "predatory lending", "debt collection law", 
    "fair credit reporting", "truth in lending", "consumer loan protection", 
    "financial product mis-selling", "credit card fraud", "mortgage fraud", 
    "loan agreements", "overdraft protection", "billing disputes",
    
    # Consumer Dispute Resolution & Remedies
    "small claims court", "mediation in consumer disputes", "consumer arbitration", 
    "settlement offers", "consumer ombudsman", "consumer restitution", 
    "compensation for consumers", "consumer legal aid", "consumer redress", 
    "consumer litigation"
    
    # General Legal Terms
    "Law",
    "Justice",
    "Judiciary",
    "Constitution",
    "Statute",
    "Legislation",
    "Bill",
    "Ordinance",
    "Act",
    "Amendment",
    "Case Law",
    "Precedent",
    "Jurisdiction",
    "Code",
    "Rule",
    "Regulation",
    "Bylaw",
    "Litigation",
    "Prosecution",
    "Defense",
    "Plaintiff",
    "Defendant",
    "Complainant",
    "Witness",
    "Evidence",
    "Affidavit",
    "Contract",
    "Tort",
    "Liability",
    "Penalty",
    "Punishment",
    "Appeal",
    "Petition",
    "Writ",
    "Summons",
    "Decree",
    "Judgment",
    "Order",
    "Hearing",
    "Trial",
    "Bail",
    "Arrest",
    "Conviction",
    "Acquittal",
    "Sentence",
    "Penalty",
    "Fine",
    "Arbitration",
    "Mediation",
    "Conciliation",
    "Adjudication",

    # Branches of Law
    "Criminal Law",
    "Civil Law",
    "Constitutional Law",
    "Corporate Law",
    "Commercial Law",
    "Contract Law",
    "Family Law",
    "Property Law",
    "Labor Law",
    "Employment Law",
    "Intellectual Property Law",
    "Consumer Law",
    "Environmental Law",
    "Cyber Law",
    "Human Rights Law",
    "Tax Law",
    "International Law",
    "Maritime Law",
    "Insurance Law",
    "Banking Law",
    "Administrative Law",
    "Public Law",
    "Private Law",
    # Judicial Terms
    "Supreme Court",
    "High Court",
    "District Court",
    "Sessions Court",
    "Tribunal",
    "Family Court",
    "Consumer Court",
    "Arbitration Panel",
    "Bench",
    "Judges",
    "Chief Justice",
    "Magistrate",
    "Advocate",
    "Lawyer",
    "Solicitor",
    "Prosecutor",
    "Public Prosecutor",
    "Attorney General",
    "Legal Counsel",
    # Constitutional Law
    "Fundamental Rights",
    "Directive Principles",
    "Right to Equality",
    "Right to Freedom",
    "Right to Education",
    "Right to Constitutional Remedies",
    "Right to Life",
    "Separation of Powers",
    "Federalism",
    "Parliament",
    "Legislature",
    "Executive",
    "Judiciary",
    "Amendment",
    "Article",
    "Preamble",
    # Civil Law keywords
    "Contract Breach",
    "Negligence",
    "Defamation",
    "Compensation",
    "Inheritance",
    "Succession",
    "Partition",
    "Specific Performance",
    "Injunction",
    "Damages",
    "Legal Notice",
    "Will",
    "Probate",
    "Mortgage",
    "Lease",
    "Tenancy",
    # Consumer Law Keywords
    "Consumer Protection Act",
    "Consumer Rights",
    "Unfair Trade Practices",
    "Deficiency in Service",
    "Misleading Advertisement",
    "Product Liability",
    "E-Commerce",
    "Refund Policy",
    "Warranty",
    "Consumer Dispute",
    "Redressal Forum",
    "Consumer Complaint",
# Cyber Law Keywords
    "Data Protection",
    "Cybersecurity",
    "Cyber Crime",
    "Phishing",
    "Hacking",
    "Identity Theft",
    "Digital Evidence",
    "Online Fraud",
    "IT Act",
    "Electronic Signature",
    "Data Breach",
    "Cyber Defamation",
# Family Law Keywords
    "Marriage",
    "Divorce",
    "Maintenance",
    "Child Custody",
    "Adoption",
    "Domestic Violence",
    "Dowry Prohibition",
    "Guardianship",
    "Inheritance",
    "Succession",
    "Alimony",
#Property Law Keywords
    "Property Dispute",
    "Title Deed",
    "Mortgage",
    "Lease Agreement",
    "Ownership",
    "Possession",
    "Easement",
    "Partition",
    "Transfer of Property",
    "Tenancy",
#International Law Keywords
    "Treaty",
    "United Nations",
    "International Criminal Court",
    "Humanitarian Law",
    "Extradition",
    "Diplomatic Immunity",
    "Law of the Sea",
    "International Arbitration",
    "Refugee Law",
    "Human Rights"
 
    # Add more keywords as needed...
]

def is_law_related(query):
    """
    Check if the user query is related to law by matching keywords.
    """
    query_lower = query.lower()
    return any(keyword.lower() in query_lower for keyword in LEGAL_KEYWORDS)

def chat_with_model(history, user_message):
    """
    Continue a chat session with the generative AI model.
    """
    chat_session = model.start_chat(history=history)
    response = chat_session.send_message(user_message)
    return response.text

# Streamlit app setup
st.set_page_config(page_title="Law-King Chatbot", layout="wide")

# Title
st.title("Law-King: Your Legal Chat Assistant")

# Sidebar for Chat History
st.sidebar.header("Chat History")

# Initialize session state for conversation
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = [
        {"role": "user", "parts": ["Hello"]},
        {"role": "model", "parts": ["Hello! 👋 What can I do for you today? 😊"]},
    ]

if "messages" not in st.session_state:
    st.session_state.messages = [
        "Law-King: Hello! 👋 What can I do for you today? 😊"
    ]

if "last_input" not in st.session_state:
    st.session_state.last_input = None  # Track the last input to avoid multiple generations
#frontend
st.markdown("""
    <style>
        .chat-container {
            display: flex;
            flex-direction: column;
            justify-content: flex-end;
            height: 85vh;  /* Adjust height to leave space for the title and other elements */
            overflow-y: auto;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        .fixed-input {
            position: fixed;
            bottom: 0;
            width: 100%;
            padding: 10px;
            background-color: #fff;
            border-top: 1px solid #fff;
        }
    </style>
""", unsafe_allow_html=True)


# Display chat in the sidebar
for message in st.session_state.messages:
    st.write(message)
# Input area for user queries
user_input = st.text_input("Ask me your problem", "", key="fixed_input", placeholder="Type your query here...")
# Handle user input
if user_input and user_input != st.session_state.last_input:
    # Mark the current input as processed
    st.session_state.last_input = user_input

    # Check if the query is law-related
    if is_law_related(user_input):
        # Add user message to conversation history
        st.session_state.conversation_history.append({"role": "user", "parts": [user_input]})
        
        # Generate response from the model
        response = chat_with_model(st.session_state.conversation_history, user_input)
        
        # Update conversation history and display messages
        st.session_state.conversation_history.append({"role": "model", "parts": [response]})
        st.session_state.messages.append(f"User: {user_input}")
        st.session_state.messages.append(f"Law-King: {response}")
    else:
        # Inform the user about non-legal queries
        response = "I only handle law-related queries. Please ask something about legal topics."
        st.session_state.messages.append(f"User: {user_input}")
        st.session_state.messages.append(f"Law-King: {response}")
    
    # Refresh the UI to display the new messages
    st.experimental_rerun()

# Display conversation history on the main page
# st.sidebar.write("### Chat")
# for message in st.session_state.messages:
#     st.sidebar.write(message)
