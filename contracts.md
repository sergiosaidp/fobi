# Fobi.io Clone - Backend Contracts

## Overview
Backend API para crear, gestionar y embedir chatbots desde Google Forms.

## Database Models

### 1. Chatbot Model
```python
{
  "_id": ObjectId,
  "chatbot_id": str (unique),
  "google_form_url": str,
  "name": str,
  "created_at": datetime,
  "updated_at": datetime,
  "customization": {
    "primary_color": str,
    "secondary_color": str,
    "bot_name": str,
    "welcome_message": str,
    "position": str (bottom-right, bottom-left),
    "size": str (small, medium, large)
  },
  "stats": {
    "total_conversations": int,
    "total_views": int,
    "completion_rate": float
  },
  "embed_type": str (popup, iframe),
  "is_active": bool
}
```

### 2. Conversation Model
```python
{
  "_id": ObjectId,
  "conversation_id": str,
  "chatbot_id": str,
  "started_at": datetime,
  "completed_at": datetime (nullable),
  "responses": list,
  "user_data": dict,
  "status": str (started, completed, abandoned)
}
```

### 3. Global Stats Model (for homepage stats)
```python
{
  "_id": ObjectId,
  "total_chatbots": int,
  "total_conversations": int,
  "total_websites": int,
  "avg_engagement_rate": float,
  "last_updated": datetime
}
```

## API Endpoints

### Chatbot Management

#### POST /api/chatbots
Create a new chatbot from Google Form
```json
Request:
{
  "google_form_url": "https://docs.google.com/forms/...",
  "name": "Contact Form Chatbot",
  "customization": {
    "primary_color": "#7c3aed",
    "secondary_color": "#2563eb",
    "bot_name": "Assistant",
    "welcome_message": "Hi! How can I help you?",
    "position": "bottom-right",
    "size": "medium"
  },
  "embed_type": "popup"
}

Response:
{
  "success": true,
  "chatbot_id": "abc123xyz",
  "message": "Chatbot created successfully",
  "embed_code": {
    "popup": "<script>...</script>",
    "iframe": "<iframe>...</iframe>"
  }
}
```

#### GET /api/chatbots
Get all chatbots (with pagination)
```json
Response:
{
  "success": true,
  "chatbots": [...],
  "total": 25,
  "page": 1,
  "per_page": 10
}
```

#### GET /api/chatbots/{chatbot_id}
Get specific chatbot details
```json
Response:
{
  "success": true,
  "chatbot": {...}
}
```

#### PUT /api/chatbots/{chatbot_id}
Update chatbot customization
```json
Request:
{
  "customization": {
    "primary_color": "#8b5cf6"
  }
}

Response:
{
  "success": true,
  "message": "Chatbot updated successfully"
}
```

#### DELETE /api/chatbots/{chatbot_id}
Delete a chatbot
```json
Response:
{
  "success": true,
  "message": "Chatbot deleted successfully"
}
```

### Statistics

#### GET /api/stats
Get global statistics for homepage
```json
Response:
{
  "success": true,
  "stats": {
    "total_websites": 50234,
    "total_conversations": 5123456,
    "avg_engagement_rate": 90.5,
    "total_chatbots": 52000
  }
}
```

#### GET /api/chatbots/{chatbot_id}/stats
Get specific chatbot statistics
```json
Response:
{
  "success": true,
  "stats": {
    "total_conversations": 1234,
    "total_views": 5678,
    "completion_rate": 87.5,
    "daily_conversations": [...]
  }
}
```

### Conversations

#### POST /api/conversations
Create/start a new conversation
```json
Request:
{
  "chatbot_id": "abc123xyz",
  "user_data": {
    "user_agent": "...",
    "referrer": "..."
  }
}

Response:
{
  "success": true,
  "conversation_id": "conv_123"
}
```

#### PUT /api/conversations/{conversation_id}
Update conversation (add responses, mark completed)
```json
Request:
{
  "status": "completed",
  "responses": [...]
}

Response:
{
  "success": true,
  "message": "Conversation updated"
}
```

### Embed Code Generation

#### GET /api/embed/{chatbot_id}
Get embed code for specific chatbot
```json
Response:
{
  "success": true,
  "embed_code": {
    "popup": "<script src='...' data-chatbot-id='abc123xyz'></script>",
    "iframe": "<iframe src='...' width='100%' height='600px'></iframe>"
  }
}
```

## Frontend Integration Plan

### Mock Data to Replace (in frontend)

Currently mocked data:
- Hero section: "50K+ websites, 90% engagement, 5M+ conversations" → Replace with GET /api/stats
- All CTA buttons → Connect to chatbot creation flow
- Navigation and footer links → Keep as is (static pages)

### New Frontend Components to Create

1. **Chatbot Builder Page** (`/create`)
   - Form to input Google Form URL
   - Customization panel (colors, text, position)
   - Live preview of chatbot
   - Generate embed code

2. **Dashboard Page** (`/dashboard`)
   - List all created chatbots
   - View statistics per chatbot
   - Edit/Delete chatbots
   - Copy embed code

3. **Embed Preview Page** (`/preview/{chatbot_id}`)
   - Show how chatbot looks in both popup and iframe modes

### API Integration Points

1. **Home Page (`/`)**
   - On mount: Fetch `/api/stats` to display real statistics

2. **Create Chatbot Flow**
   - User clicks "Get Started" → Redirect to `/create`
   - Submit form → POST `/api/chatbots`
   - Show embed code in modal/page

3. **Dashboard**
   - List chatbots → GET `/api/chatbots`
   - View stats → GET `/api/chatbots/{id}/stats`
   - Update → PUT `/api/chatbots/{id}`
   - Delete → DELETE `/api/chatbots/{id}`

## Implementation Steps

### Backend:
1. ✅ Create MongoDB models
2. ✅ Implement chatbot CRUD endpoints
3. ✅ Implement statistics endpoints
4. ✅ Implement conversation tracking endpoints
5. ✅ Add validation for Google Form URLs
6. ✅ Generate embed code templates
7. ✅ Add error handling

### Frontend:
1. ✅ Connect Home page to stats API
2. ✅ Create Chatbot Builder page
3. ✅ Create Dashboard page
4. ✅ Add API integration layer (axios)
5. ✅ Replace mock data with real API calls
6. ✅ Add loading states and error handling

## Notes
- No authentication required (as per original Fobi.io concept)
- Embed code will be simple script/iframe tags
- Statistics will be tracked server-side
- Google Form URL validation: basic URL format check (no API integration with Google)
