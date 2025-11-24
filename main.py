from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
import uvicorn
import sys
import os
sys.path.insert(0, 'src')

from clients.ai_clients.client_factory import AIClientFactory
from clients.faiss.faiss_client import FAISSClient
from clients.mcp.mcp_client import MCPClient
from config.settings import MONGODB_URI, DATABASE_NAME
from sentence_transformers import SentenceTransformer

app = FastAPI(title="MOBO Chat Interface")

@app.get("/", response_class=HTMLResponse)
async def chat_interface():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>MOBO Chat</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .chat { border: 1px solid #ccc; padding: 10px; height: 300px; overflow-y: scroll; margin-bottom: 10px; }
            .message { margin: 5px 0; }
            .user { color: blue; }
            .bot { color: green; }
            form { margin-bottom: 10px; }
        </style>
    </head>
    <body>
        <h1>MOBO Chat Interface</h1>
        
        <div>
            <label>RAG Role:
                <select id="rag_role">
                    <option value="">Disabled</option>
                    <option value="ADMIN">ADMIN</option>
                    <option value="DEV">DEV</option>
                    <option value="HR">HR</option>
                    <option value="ALL">ALL</option>
                </select>
            </label>
            <label>MCP: <input type="checkbox" id="use_mcp"></label>
            <button onclick="openMongoExpress()">View Database</button>
        </div>
        
        <div class="chat" id="chat"></div>
        
        <form onsubmit="sendMessage(event)">
            <input type="text" id="message" placeholder="Type your message..." required style="width: 300px;">
            <button type="submit">Send</button>
        </form>
        
        <script>
            async function sendMessage(event) {
                event.preventDefault();
                const message = document.getElementById('message').value;
                const ragRole = document.getElementById('rag_role').value;
                const useMcp = document.getElementById('use_mcp').checked;
                
                addMessage('user', message);
                document.getElementById('message').value = '';
                
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message, rag_role: ragRole, use_mcp: useMcp })
                });
                const data = await response.json();
                addMessage('bot', data.response);
            }
            
            function addMessage(sender, text) {
                const chat = document.getElementById('chat');
                const div = document.createElement('div');
                div.className = 'message ' + sender;
                div.textContent = (sender === 'user' ? 'You: ' : 'Bot: ') + text;
                chat.appendChild(div);
                chat.scrollTop = chat.scrollHeight;
            }
            
            function openMongoExpress() {
                window.open('http://admin:express123@localhost:8081', '_blank');
            }
        </script>
    </body>
    </html>
    """
    return html

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    message = data.get('message', '')
    rag_role = data.get('rag_role', '')
    use_mcp = data.get('use_mcp', False)
    
    # Get AI response
    client = AIClientFactory.create_client("openrouter")  # Default to openrouter
    
    prompt = message
    
    # Add RAG context if enabled
    if rag_role:
        try:
            model = SentenceTransformer('all-MiniLM-L6-v2')
            query_vector = model.encode(message).tolist()
            faiss_client = FAISSClient(base_url="http://faiss:8001")
            results = faiss_client.search_similar(query_vector, k=3)
            context = "\\n".join([f"Doc {i+1}: {res['id']} (score: {res['score']:.3f})" for i, res in enumerate(results)])
            prompt = f"Context from {rag_role} docs:\\n{context}\\n\\nUser: {message}"
        except Exception as e:
            prompt += f"\\n(RAG error: {str(e)})"
    
    # Add MCP data if enabled
    if use_mcp:
        mcp_client = MCPClient()
        try:
            usd_data = await mcp_client.get_usd_price()
            prompt += f"\\n\\nCurrent USD rates: {usd_data}"
        except Exception as e:
            prompt += f"\\n(MCP error: {str(e)})"
    
    try:
        response = client.generate_text(prompt)
    except Exception as e:
        response = f"Error: {str(e)}"
    
    return {"response": response}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)
