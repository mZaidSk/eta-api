from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.shortcuts import get_object_or_404

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from .models import Conversation, ChatMessage
from .serializers import ConversationSerializer, ConversationListSerializer, ChatMessageSerializer
from .agents import tools
from eta_api.utils.responses import success_response, error_response


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def chatbot_view(request):
    """
    Send a message to the AI chatbot
    Request body:
    {
        "message": "What were my expenses this month?",
        "conversation_id": 123  // optional, for continuing a conversation
    }
    """
    user_message = request.data.get("message", "").strip()
    conversation_id = request.data.get("conversation_id")

    if not user_message:
        return error_response(
            message="Message cannot be empty",
            status=400
        )

    # Get or create conversation
    if conversation_id:
        conversation = get_object_or_404(
            Conversation,
            id=conversation_id,
            user=request.user
        )
    else:
        # Create new conversation with title from first message
        conversation = Conversation.objects.create(
            user=request.user,
            title=user_message[:100]  # Use first 100 chars as title
        )

    # Save user message
    ChatMessage.objects.create(
        conversation=conversation,
        role='user',
        content=user_message
    )

    # Get conversation history (last 10 messages for context)
    history_messages = conversation.messages.all()[:10]
    messages_for_llm = []

    for msg in history_messages:
        if msg.role == 'user':
            messages_for_llm.append(HumanMessage(content=msg.content))
        elif msg.role == 'assistant':
            messages_for_llm.append(AIMessage(content=msg.content))

    # Initialize Gemini chat model
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-exp",
        google_api_key=settings.GEMINI_API_KEY,
        temperature=0.7,
    )

    # Create system prompt with user context
    system_prompt = f"""You are an intelligent financial assistant for an expense tracking application.
You help users understand their spending patterns, budgets, income, and provide financial insights.

Current user ID: {request.user.id}

You have access to several tools that can fetch real-time financial data:
- Total expenses and income for the current month
- Category breakdown of spending
- Budget status and alerts
- Account balances
- Spending trends
- Recent transactions
- Top spending categories

Always use the appropriate tool to fetch accurate, up-to-date information.
Be friendly, helpful, and provide actionable insights.
When showing monetary values, always include the currency symbol ($).
Keep responses concise but informative."""

    # Create the prompt template for the agent
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    # Create tool-calling agent
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=5,
    )

    try:
        # Invoke the agent with user message and conversation history
        result = agent_executor.invoke({
            "input": user_message,
            "chat_history": messages_for_llm[:-1] if len(messages_for_llm) > 0 else [],
        })

        assistant_response = result.get("output", "I'm sorry, I couldn't process that request.")

        # Save assistant response
        ChatMessage.objects.create(
            conversation=conversation,
            role='assistant',
            content=assistant_response
        )

        return success_response(
            message="Response generated successfully",
            data={
                "reply": assistant_response,
                "conversation_id": conversation.id
            }
        )

    except Exception as e:
        # Log the error and return user-friendly message
        print(f"Chatbot error: {str(e)}")
        return error_response(
            message="An error occurred while processing your request. Please try again.",
            errors={"detail": str(e)},
            status=500
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def conversation_list_view(request):
    """Get all conversations for the authenticated user"""
    conversations = Conversation.objects.filter(user=request.user)
    serializer = ConversationListSerializer(conversations, many=True)
    return success_response(
        message="Conversations retrieved successfully",
        data=serializer.data
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def conversation_detail_view(request, conversation_id):
    """Get a specific conversation with all messages"""
    conversation = get_object_or_404(
        Conversation,
        id=conversation_id,
        user=request.user
    )
    serializer = ConversationSerializer(conversation)
    return success_response(
        message="Conversation retrieved successfully",
        data=serializer.data
    )


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def conversation_delete_view(request, conversation_id):
    """Delete a conversation"""
    conversation = get_object_or_404(
        Conversation,
        id=conversation_id,
        user=request.user
    )
    conversation.delete()
    return success_response(
        message="Conversation deleted successfully"
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def conversation_create_view(request):
    """Create a new conversation"""
    title = request.data.get("title", "New Conversation")
    conversation = Conversation.objects.create(
        user=request.user,
        title=title
    )
    serializer = ConversationSerializer(conversation)
    return success_response(
        message="Conversation created successfully",
        data=serializer.data,
        status=201
    )
