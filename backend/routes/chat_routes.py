from flask import Blueprint, request, jsonify, Response
from services.chat_service import get_chat_response

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("", methods=["POST"])
def send_message():
    """
    Send a message to the League Analytics AI Agent with streaming response.

    Request JSON:
    {
        "message": "string - user's message",
        "puuid": "string (optional) - player's puuid for context",
        "stream": "boolean (optional) - enable streaming (default: true)"
    }

    Response: Server-Sent Events (SSE) stream with chunks of the response
    """
    data = request.json
    message = data.get("message", "").strip()
    puuid = data.get("puuid")
    stream = data.get("stream", True)

    if not message:
        return jsonify({"success": False, "error": "Message is required"}), 400

    try:
        if stream:
            # Return streaming response
            return Response(
                stream_response(message, puuid),
                mimetype="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "X-Accel-Buffering": "no",
                },
            )
        else:
            # Return full response at once
            response = get_chat_response(message, puuid)
            return jsonify({"success": True, "response": response})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


def stream_response(message: str, puuid: str = None):
    """
    Stream the chat response word by word as Server-Sent Events.
    """
    try:
        response_text = get_chat_response(message, puuid)

        # Stream the response word by word
        words = response_text.split()
        for i, word in enumerate(words):
            chunk = word + (" " if i < len(words) - 1 else "")
            yield f"data: {chunk}\n\n"

        # Send completion signal
        yield "data: [DONE]\n\n"
    except Exception as e:
        yield f"data: [ERROR] {str(e)}\n\n"
