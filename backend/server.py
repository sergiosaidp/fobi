from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from models.chatbot import Customization

# Import routes
from routes.chatbots import router as chatbots_router
from routes.conversations import router as conversations_router
from routes.stats import router as stats_router


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'fobi_clone')]

# Create the main app without a prefix
app = FastAPI(
    title="Fobi.io Clone API",
    description="API for creating chatbots from Google Forms",
    version="1.0.0"
)

# Create a router with the /api prefix for general routes
api_router = APIRouter(prefix="/api")

# Health check endpoint
@api_router.get("/")
async def root():
    return {
        "message": "Fobi.io Clone API",
        "status": "healthy",
        "version": "1.0.0"
    }

@api_router.get("/health")
async def health_check():
    return {"status": "healthy", "database": "connected"}

# Include the general router
app.include_router(api_router)

# Mount static files
app.mount("/static", StaticFiles(directory=ROOT_DIR / "static"), name="static")

@app.get("/embed/{chatbot_id}", response_class=HTMLResponse)
async def get_embed_html(chatbot_id: str):
    """
    Serve the standalone chat interface.
    In a real app, this would use a template engine like Jinja2.
    For this clone, we'll return a complete HTML string with embedded React/Vanilla JS logic.
    """
    # Simply return a basic HTML that will load the conversation
    # We will implement a simple vanilla JS chat interface here to avoid complex React builds for the embed
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fobi Chat</title>
    <style>
        body {{ margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background: #fff; }}
        .chat-container {{ display: flex; flex-direction: column; height: 100vh; overflow: hidden; }}
        .header {{ padding: 16px; background: #fff; border-bottom: 1px solid #eee; display: flex; align-items: center; }}
        .avatar {{ width: 32px; height: 32px; border-radius: 50%; background: #eee; margin-right: 12px; display: flex; align-items: center; justify-content: center; font-size: 14px; overflow: hidden; }}
        .messages {{ flex: 1; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 16px; }}
        .message {{ max-width: 80%; padding: 12px 16px; border-radius: 12px; font-size: 15px; line-height: 1.5; animation: fadeIn 0.3s ease; }}
        .message.bot {{ align-self: flex-start; background: #f3f4f6; color: #1f2937; border-bottom-left-radius: 4px; }}
        .message.user {{ align-self: flex-end; background: #2563eb; color: white; border-bottom-right-radius: 4px; }}
        .input-area {{ padding: 16px; border-top: 1px solid #eee; background: #fff; }}
        .input-group {{ display: flex; gap: 8px; }}
        input, select {{ flex: 1; padding: 12px; border: 1px solid #e5e7eb; border-radius: 8px; outline: none; font-size: 15px; }}
        input:focus {{ border-color: #2563eb; }}
        button {{ padding: 12px 24px; background: #2563eb; color: white; border: none; border-radius: 8px; font-weight: 600; cursor: pointer; transition: background 0.2s; }}
        button:hover {{ background: #1d4ed8; }}
        button:disabled {{ opacity: 0.5; cursor: not-allowed; }}
        @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(10px); }} to {{ opacity: 1; transform: translateY(0); }} }}
        .options-grid {{ display: grid; grid-template-columns: 1fr; gap: 8px; margin-top: 8px; }}
        .option-btn {{ text-align: left; background: #fff; border: 1px solid #e5e7eb; color: #374151; padding: 10px 14px; width: 100%; }}
        .option-btn:hover {{ background: #f9fafb; border-color: #d1d5db; }}
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="header" id="header" style="display:none">
            <div class="avatar" id="avatar">🤖</div>
            <div>
                <div style="font-weight: 600" id="botName">Assistant</div>
                <div style="font-size: 12px; color: #6b7280">Online</div>
            </div>
        </div>
        <div class="messages" id="messages">
            <!-- Messages will be injected here -->
        </div>
        <div class="input-area" id="inputArea">
            <div class="input-group" id="inputGroup">
                <!-- Input controls will be injected here -->
            </div>
        </div>
    </div>

    <script>
        const API_URL = '/api';
        const CHATBOT_ID = '{chatbot_id}';
        let conversationId = null;
        let chatbotConfig = null;
        let currentQuestion = null;

        // Init
        async function init() {{
            try {{
                // 1. Get Chatbot Details (for customization)
                const botRes = await fetch(`${{API_URL}}/chatbots/${{CHATBOT_ID}}`);
                const botData = await botRes.json();
                
                if (botData.success) {{
                    chatbotConfig = botData.chatbot.customization;
                    applyCustomization();
                }}

                // 2. Start Conversation
                const convRes = await fetch(`${{API_URL}}/conversations`, {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ chatbot_id: CHATBOT_ID }})
                }});
                const convData = await convRes.json();
                
                if (convData.success) {{
                    conversationId = convData.conversation_id;
                    // Show Welcome Message
                    if (chatbotConfig && chatbotConfig.welcome_message) {{
                        addMessage(chatbotConfig.welcome_message, 'bot');
                    }}
                    
                    // Show First Question
                    if (convData.next_question) {{
                        // Small delay for natural feel
                        setTimeout(() => handleNewQuestion(convData.next_question), 500);
                    }} else {{
                        // No questions?
                        setTimeout(() => addMessage("This form has no questions available.", 'bot'), 500);
                    }}
                }}
            }} catch (err) {{
                console.error(err);
                addMessage("Sorry, I'm having trouble connecting right now.", 'bot');
            }}
        }}

        function applyCustomization() {{
            if (!chatbotConfig) return;
            document.getElementById('header').style.display = 'flex';
            document.getElementById('botName').textContent = chatbotConfig.bot_name;
            const primaryColor = chatbotConfig.primary_color || '#2563eb';
            
            // Inject dynamic style for user messages
            const style = document.createElement('style');
            style.innerHTML = `
                .message.user {{ background: ${{primaryColor}} !important; }}
                button {{ background: ${{primaryColor}} !important; }}
                button:hover {{ opacity: 0.9; }}
                input:focus {{ border-color: ${{primaryColor}} !important; }}
            `;
            document.head.appendChild(style);
        }}

        function addMessage(text, sender) {{
            const div = document.createElement('div');
            div.className = `message ${{sender}}`;
            div.textContent = text;
            document.getElementById('messages').appendChild(div);
            scrollToBottom();
        }}

        function scrollToBottom() {{
            const messages = document.getElementById('messages');
            messages.scrollTop = messages.scrollHeight;
        }}

        function handleNewQuestion(question) {{
            currentQuestion = question;
            // Display question text
            addMessage(question.text, 'bot');
            
            // Validate and render input
            renderInput(question);
        }}

        function renderInput(question) {{
            const container = document.getElementById('inputGroup');
            container.innerHTML = ''; // Clear previous

            if (question.type === 'multiple_choice' || question.type === 'dropdown') {{
                // Render options
                const optionsDiv = document.createElement('div');
                optionsDiv.className = 'options-grid';
                question.options.forEach(opt => {{
                    const btn = document.createElement('button');
                    btn.className = 'option-btn';
                    btn.textContent = opt;
                    btn.onclick = () => submitAnswer(opt);
                    optionsDiv.appendChild(btn);
                }});
                
                // For multiple choice we append options IN the message stream usually, but here 
                // we'll put them in input area for simplicity or stick them to bottom?
                // Let's put them in the input area replacing the text input
                container.appendChild(optionsDiv);
                
            }} else {{
                // Text input
                const input = document.createElement('input');
                input.type = 'text';
                input.placeholder = question.placeholder || 'Type your answer...';
                input.onkeypress = (e) => {{
                    if (e.key === 'Enter') submitAnswer(input.value);
                }};
                
                const btn = document.createElement('button');
                btn.innerHTML = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>';
                btn.onclick = () => submitAnswer(input.value);
                
                container.appendChild(input);
                container.appendChild(btn);
                input.focus();
            }}
        }}

        async function submitAnswer(answer) {{
            if (!answer || !answer.trim()) return;
            
            // UI Update
            addMessage(answer, 'user');
            
            // Clear Input
            document.getElementById('inputGroup').innerHTML = ''; // Disable input while loading
            
            try {{
                // API Call
                const res = await fetch(`${{API_URL}}/conversations/${{conversationId}}`, {{
                    method: 'PUT',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        responses: [{{ 
                            question_id: currentQuestion.id,
                            question: currentQuestion.text,
                            answer: answer 
                        }}]
                    }})
                }});
                const data = await res.json();
                
                if (data.success) {{
                    if (data.next_question) {{
                        setTimeout(() => handleNewQuestion(data.next_question), 400);
                    }} else {{
                        setTimeout(() => {{
                            addMessage("Thank you! Your response has been recorded.", 'bot');
                            // Maybe close or show done state
                            document.getElementById('inputArea').style.display = 'none';
                        }}, 400);
                    }}
                }}
            }} catch (err) {{
                console.error(err);
                addMessage("Failed to send message. Please try again.", 'bot');
                renderInput(currentQuestion); // Re-enable input
            }}
        }}

        // Run
        init();
    </script>
</body>
</html>
    """

# Include feature-specific routers
app.include_router(chatbots_router)
app.include_router(conversations_router)
app.include_router(stats_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()