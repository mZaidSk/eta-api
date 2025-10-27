# Enhanced Chatbot API Guide

## Overview

The ETA API chatbot has been significantly enhanced with the following features:

1. **AI-Powered Financial Assistant** using Google Gemini 2.0 Flash
2. **Function Calling** with 9 specialized financial tools
3. **Conversation History** with persistent storage
4. **Multi-turn Conversations** with context memory
5. **Rich Financial Insights** from real-time data

## API Endpoints

### 1. Send a Message to the Chatbot

**Endpoint:** `POST /api/ai/chat/`

**Authentication:** Required (JWT Token)

**Request Body:**
```json
{
  "message": "What were my expenses this month?",
  "conversation_id": 123  // Optional: to continue an existing conversation
}
```

**Response:**
```json
{
  "success": true,
  "message": "Response generated successfully",
  "data": {
    "reply": "Your total expenses for October 2025 are $1,234.56. Your top spending category is Food with $450.00.",
    "conversation_id": 123
  },
  "errors": null
}
```

**Example Queries:**
- "What are my total expenses this month?"
- "Show me my budget status"
- "What's my biggest expense?"
- "How does my spending compare to last month?"
- "What are my account balances?"
- "Which category am I spending the most on?"

---

### 2. List All Conversations

**Endpoint:** `GET /api/ai/conversations/`

**Authentication:** Required

**Response:**
```json
{
  "success": true,
  "message": "Conversations retrieved successfully",
  "data": [
    {
      "id": 1,
      "title": "What are my expenses this month?",
      "created_at": "2025-10-27T10:00:00Z",
      "updated_at": "2025-10-27T10:05:00Z",
      "message_count": 6,
      "last_message": {
        "role": "assistant",
        "content": "Your total expenses for October are $1,234.56",
        "created_at": "2025-10-27T10:05:00Z"
      }
    }
  ],
  "errors": null
}
```

---

### 3. Get Conversation Details

**Endpoint:** `GET /api/ai/conversations/{conversation_id}/`

**Authentication:** Required

**Response:**
```json
{
  "success": true,
  "message": "Conversation retrieved successfully",
  "data": {
    "id": 1,
    "title": "What are my expenses this month?",
    "created_at": "2025-10-27T10:00:00Z",
    "updated_at": "2025-10-27T10:05:00Z",
    "messages": [
      {
        "id": 1,
        "role": "user",
        "content": "What are my expenses this month?",
        "created_at": "2025-10-27T10:00:00Z"
      },
      {
        "id": 2,
        "role": "assistant",
        "content": "Your total expenses for October are $1,234.56",
        "created_at": "2025-10-27T10:01:00Z"
      }
    ],
    "message_count": 2
  },
  "errors": null
}
```

---

### 4. Create a New Conversation

**Endpoint:** `POST /api/ai/conversations/create/`

**Authentication:** Required

**Request Body:**
```json
{
  "title": "Budget Planning Discussion"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Conversation created successfully",
  "data": {
    "id": 2,
    "title": "Budget Planning Discussion",
    "created_at": "2025-10-27T11:00:00Z",
    "updated_at": "2025-10-27T11:00:00Z",
    "messages": [],
    "message_count": 0
  },
  "errors": null
}
```

---

### 5. Delete a Conversation

**Endpoint:** `DELETE /api/ai/conversations/{conversation_id}/delete/`

**Authentication:** Required

**Response:**
```json
{
  "success": true,
  "message": "Conversation deleted successfully",
  "data": null,
  "errors": null
}
```

---

## AI Assistant Capabilities

The chatbot has access to 9 specialized tools for fetching financial data:

### 1. **Total Expenses** (`expense_tool`)
Get total expenses for the current month.

### 2. **Total Income** (`income_tool`)
Get total income for the current month.

### 3. **Category Breakdown** (`category_breakdown_tool`)
Get expense breakdown by category with transaction counts.

### 4. **Biggest Expense** (`biggest_expense_tool`)
Find the largest single expense for the month.

### 5. **Budget Status** (`budget_status_tool`)
Check all active budgets and see if over/under budget.

### 6. **Recent Transactions** (`recent_transactions_tool`)
Get the 10 most recent transactions.

### 7. **Account Balances** (`account_balances_tool`)
Get current balance of all accounts and total.

### 8. **Spending Trends** (`spending_trends_tool`)
Compare current month spending with last month.

### 9. **Top Spending Category** (`top_spending_category_tool`)
Find which category has the highest spending.

---

## How It Works

1. **User sends a message** via `/api/ai/chat/`
2. **Conversation context** is loaded (last 10 messages)
3. **AI analyzes the query** and determines which tools to use
4. **Tools fetch real-time data** from the database
5. **AI generates a response** based on the data
6. **Response is saved** to conversation history
7. **User receives** the AI's reply

---

## Example Usage Flow

### Starting a New Conversation

```bash
# 1. Send first message (creates new conversation automatically)
curl -X POST http://localhost:8000/api/ai/chat/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "What are my expenses this month?"}'

# Response includes conversation_id: 123
```

### Continuing the Conversation

```bash
# 2. Send follow-up message with conversation_id
curl -X POST http://localhost:8000/api/ai/chat/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Which category am I spending the most on?",
    "conversation_id": 123
  }'

# AI remembers previous context
```

### Viewing Conversation History

```bash
# 3. Get full conversation
curl -X GET http://localhost:8000/api/ai/conversations/123/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

## Technical Architecture

### Models

**Conversation Model:**
- `user`: ForeignKey to User
- `title`: String (auto-generated from first message)
- `created_at`, `updated_at`: Timestamps

**ChatMessage Model:**
- `conversation`: ForeignKey to Conversation
- `role`: 'user' | 'assistant' | 'system'
- `content`: Text
- `created_at`: Timestamp

### LangChain Integration

The chatbot uses LangChain's agent framework:

1. **ChatGoogleGenerativeAI**: Gemini 2.0 Flash model
2. **Tool Calling Agent**: Automatically selects and invokes tools
3. **Agent Executor**: Manages the execution flow
4. **Conversation Memory**: Last 10 messages for context

### Tool Architecture

Each tool:
- Takes `user_id` as parameter
- Fetches data from Django ORM
- Returns formatted string response
- Handles edge cases (no data, empty results)

---

## Configuration

Ensure your `.env` file has:

```env
GEMINI_API_KEY=your-gemini-api-key-here
```

---

## Error Handling

The chatbot includes comprehensive error handling:

- **Empty message**: Returns 400 error
- **Invalid conversation_id**: Returns 404 error
- **AI processing errors**: Returns 500 with user-friendly message
- **Database errors**: Properly caught and logged

---

## Performance Considerations

1. **Conversation history limited to 10 messages** to reduce token usage
2. **Tools use efficient database queries** with `select_related()`
3. **Lazy loading** for conversation lists
4. **Agent max iterations set to 5** to prevent infinite loops

---

## Future Enhancements

Potential improvements:

1. **Streaming responses** for real-time output
2. **Voice input/output** integration
3. **Scheduled financial insights** (weekly summaries)
4. **Proactive budget alerts** via chatbot
5. **Financial goal tracking** and recommendations
6. **Export conversation** to PDF/CSV
7. **Multi-language support**

---

## Testing the Chatbot

You can test the chatbot with various queries:

**Budget Queries:**
- "Am I over budget?"
- "Show me my budget status"
- "How much budget do I have left?"

**Spending Analysis:**
- "What's my biggest expense?"
- "Where am I spending the most?"
- "How does this month compare to last month?"

**Transaction Queries:**
- "Show me my recent transactions"
- "What did I spend on food?"

**Account Information:**
- "What are my account balances?"
- "How much money do I have?"

**Income Queries:**
- "What's my total income this month?"
- "How much did I earn?"

---

## Support

For issues or questions, contact the development team or check the main project documentation.
