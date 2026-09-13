from fastapi import APIRouter, Form, Request
from fastapi.responses import Response

from app.services.dragon_call import CallAssistant, greeting, twiml_say_gather
from config.config import settings

router = APIRouter()
assistant = CallAssistant()


def _action_url(request: Request) -> str:
    if settings.TWILIO_WEBHOOK_BASE_URL:
        return (
            settings.TWILIO_WEBHOOK_BASE_URL.rstrip("/")
            + settings.API_PREFIX
            + "/v1/dragon/calls/respond"
        )
    return str(request.url_for("handle_call_input"))


@router.post("/incoming")
async def incoming_call(
    request: Request, call_sid: str = Form(default="unknown", alias="CallSid")
) -> Response:
    session = assistant.session(call_sid)
    action = _action_url(request)
    return Response(
        twiml_say_gather(greeting(session.language), action, session.language),
        media_type="application/xml",
    )


@router.post("/respond", name="handle_call_input")
async def handle_call_input(
    request: Request,
    call_sid: str = Form(default="unknown", alias="CallSid"),
    speech_result: str = Form(default="", alias="SpeechResult"),
) -> Response:
    text, record = await assistant.respond(call_sid, speech_result)
    action = _action_url(request)
    return Response(
        twiml_say_gather(text, action, assistant.session(call_sid).language, record=record),
        media_type="application/xml",
    )
