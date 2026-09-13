"""Small, provider-agnostic call assistant used by the Twilio webhook."""

from __future__ import annotations

import html
import re
from dataclasses import dataclass, field
from typing import Dict, Optional

import httpx

from config.config import settings


@dataclass
class CallSession:
    language: str
    recording_consented: bool = False
    caller_name: Optional[str] = None
    caller_email: Optional[str] = None
    appointment_requested: bool = False
    details: Dict[str, str] = field(default_factory=dict)


class PlaceholderCalendarAdapter:
    """Calendar boundary for the prototype; replace with a real provider later."""

    def book(self, session: CallSession) -> str:
        return "Vielen Dank. Unser Team bestätigt den Termin telefonisch oder per E-Mail."


class GeminiResponder:
    def __init__(self, api_key: str, model: str) -> None:
        self.api_key = api_key
        self.model = model

    async def answer(self, text: str, language: str) -> Optional[str]:
        if not self.api_key:
            return None
        prompt = (
            "Du bist die freundliche Telefonassistenz von Dragon & Partner in Deutschland. "
            "Antworte kurz und klar auf Deutsch. Beantworte nur allgemeine FAQs und erfinde "
            "keine Rechtsberatung. " + text
            if language == "de"
            else "You are the friendly phone assistant for Dragon & Partner in Germany. "
            "Answer briefly in English. Only answer general FAQs and do not invent legal advice. "
            + text
        )
        url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self.model}:generateContent"
        )
        try:
            async with httpx.AsyncClient(timeout=8) as client:
                response = await client.post(
                    url,
                    params={"key": self.api_key},
                    json={"contents": [{"parts": [{"text": prompt}]}]},
                )
                response.raise_for_status()
                candidates = response.json().get("candidates", [])
                return candidates[0]["content"]["parts"][0]["text"].strip() if candidates else None
        except (httpx.HTTPError, KeyError, IndexError, TypeError):
            return None


class CallAssistant:
    def __init__(self) -> None:
        self.sessions: Dict[str, CallSession] = {}
        self.calendar = PlaceholderCalendarAdapter()
        self.gemini = GeminiResponder(
            settings.GEMINI_API_KEY or settings.GOOGLE_API_KEY, settings.GEMINI_MODEL
        )

    def session(self, call_sid: str) -> CallSession:
        return self.sessions.setdefault(call_sid, CallSession(language=self.language()))

    @staticmethod
    def language() -> str:
        return "en" if settings.DRAGON_GREETING_LANGUAGE.lower().startswith("en") else "de"

    async def respond(self, call_sid: str, speech: str) -> tuple[str, bool]:
        session = self.session(call_sid)
        normalized = speech.strip().lower()
        if not session.recording_consented and self._is_consent(normalized):
            session.recording_consented = True
            return self._consent_ack(session.language), True
        if not session.recording_consented and self._is_decline(normalized):
            return self._no_recording_ack(session.language), False
        if self._asks_for_appointment(normalized):
            session.appointment_requested = True
            return self._appointment_prompt(session.language), session.recording_consented
        if session.appointment_requested:
            self._collect_details(session, speech)
            if session.caller_name and session.caller_email:
                return self.calendar.book(session), session.recording_consented
        answer = await self.gemini.answer(speech, session.language)
        return answer or self._faq_fallback(session.language), session.recording_consented

    @staticmethod
    def _is_consent(text: str) -> bool:
        return bool(re.search(r"\b(ja|yes|einverstanden|zustimm|okay|ok)\b", text))

    @staticmethod
    def _is_decline(text: str) -> bool:
        return bool(re.search(r"\b(nein|no|nicht|keine|ablehn)\b", text))

    @staticmethod
    def _asks_for_appointment(text: str) -> bool:
        return any(word in text for word in ("termin", "appointment", "beratung", "meeting"))

    @staticmethod
    def _collect_details(session: CallSession, text: str) -> None:
        if not session.caller_name:
            session.caller_name = text.strip()
        elif not session.caller_email and "@" in text:
            session.caller_email = text.strip()

    @staticmethod
    def _consent_ack(language: str) -> str:
        return (
            "Danke, Ihre Zustimmung ist gespeichert. Wie kann ich Ihnen helfen?"
            if language == "de"
            else "Thank you, your consent has been recorded. How may I help you?"
        )

    @staticmethod
    def _no_recording_ack(language: str) -> str:
        return (
            "In Ordnung, wir zeichnen dieses Gespräch nicht auf. Wie kann ich Ihnen helfen?"
            if language == "de"
            else "Understood, we will not record this call. How may I help you?"
        )

    @staticmethod
    def _appointment_prompt(language: str) -> str:
        return (
            "Gerne. Bitte nennen Sie zuerst Ihren Namen und danach Ihre E-Mail-Adresse."
            if language == "de"
            else "Certainly. Please tell me your name, followed by your email address."
        )

    @staticmethod
    def _faq_fallback(language: str) -> str:
        return (
            "Dazu habe ich noch keine verlässliche Antwort. Ich kann Ihre Kontaktdaten aufnehmen "
            "oder einen Beratungstermin vormerken."
            if language == "de"
            else "I do not have a reliable answer for that yet. I can take your contact details "
            "or arrange a consultation request."
        )


def xml_escape(value: str) -> str:
    return html.escape(value, quote=True)


def twiml_say_gather(text: str, action: str, language: str = "de", *, record: bool = False) -> str:
    recording = '<Start><Recording track="both"/></Start>' if record else ""
    voice_language = "en-US" if language == "en" else "de-DE"
    voice = "Polly.Joanna" if language == "en" else "Google.de-DE-Standard-A"
    return (
        '<?xml version="1.0" encoding="UTF-8"?><Response>'
        f"{recording}<Gather input=\"speech\" action=\"{xml_escape(action)}\" "
        'method="POST" speechTimeout="auto">'
        f"<Say language=\"{voice_language}\" voice=\"{voice}\">{xml_escape(text)}</Say>"
        "</Gather></Response>"
    )


def greeting(language: str) -> str:
    return (
        "Willkommen bei Dragon & Partner. Dieses Gespräch kann nur mit Ihrer ausdrücklichen "
        "Zustimmung aufgezeichnet werden. Sagen Sie bitte Ja oder Nein."
        if language == "de"
        else "Welcome to Dragon & Partner. This call may only be recorded with your explicit "
        "consent. Please say yes or no."
    )
