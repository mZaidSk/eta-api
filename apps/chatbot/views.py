from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.conf import settings
from apps.transactions.models import Transaction

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import SystemMessage, HumanMessage


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def chatbot_view(request):
    user_message = request.data.get("message", "").strip()
    if not user_message:
        return Response({"error": "Message cannot be empty"}, status=400)

    # Fetch last 5 transactions for the logged-in user
    transactions = Transaction.objects.filter(user=request.user).order_by("-date")[:5]
    transaction_summary = "\n".join(
        [f"{t.category.name}: ${t.amount}" for t in transactions]
    )

    # Create system prompt
    system_prompt = (
        "You are a financial assistant for an expense tracker app.\n"
        "Here are the user's last 5 transactions:\n"
        f"{transaction_summary}"
    )

    # Initialize LangChain Google Gemini chat model
    chat = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=settings.GEMINI_API_KEY,
    )

    # Generate response
    response = chat(
        [SystemMessage(content=system_prompt), HumanMessage(content=user_message)]
    )

    return Response({"reply": response.content})
