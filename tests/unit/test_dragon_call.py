import asyncio

from app.services.dragon_call import CallAssistant, greeting, twiml_say_gather


def test_greeting_is_german_by_default(monkeypatch):
    monkeypatch.setattr("config.config.settings.DRAGON_GREETING_LANGUAGE", "de")
    assert "Willkommen" in greeting(CallAssistant.language())


def test_declining_consent_never_starts_recording(monkeypatch):
    monkeypatch.setattr("config.config.settings.DRAGON_GREETING_LANGUAGE", "de")
    assistant = CallAssistant()
    text, record = asyncio.run(assistant.respond("CA-no-recording", "Nein, ich möchte das nicht"))
    assert "nicht auf" in text
    assert record is False


def test_consent_enables_recording_only_after_yes(monkeypatch):
    monkeypatch.setattr("config.config.settings.DRAGON_GREETING_LANGUAGE", "de")
    assistant = CallAssistant()
    response = asyncio.run(assistant.respond("CA-consent", "Ja"))
    assert response[1] is True
    assert '<Start><Recording track="both"/></Start>' in twiml_say_gather(
        response[0], "/respond", "de", record=response[1]
    )
