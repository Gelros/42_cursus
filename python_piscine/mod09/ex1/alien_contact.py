from enum import Enum
from pydantic import BaseModel, Field, model_validator
from datetime import datetime
from typing import Optional


class ContactType(Enum):
    radio = "radio"
    visual = "visual"
    physical = "physical"
    telepathic = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: Optional[str] = Field(default=None, max_length=500)
    is_verified: bool = False

    @model_validator(mode="after")
    def validation_rules(self):
        if not self.contact_id.startswith("AC"):
            raise ValueError("Contact ID must start by AC")
        if self.contact_type != ContactType.physical and self.is_verified:
            raise ValueError("Contact must be verified")
        if self.contact_type == ContactType.telepathic \
                and self.witness_count < 3:
            raise ValueError(
                "Telepathic contact requires at least 3 witnesses")
        if self.signal_strength > 7 and not self.message_received:
            raise ValueError(
                "Strong signals (>7.0) should include received messages")
        return self


def main():
    print("Alien Contact Log Validation")
    print("======================================")
    print("Valid contact report:")
    try:
        contact = AlienContact(
            contact_id="AC_2024_001",
            contact_type=ContactType.radio,
            location="Area 51, Nevada",
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=5,
            message_received="Greetings from Zeta Reticuli",
            timestamp=datetime.now(),
        )
        print(f"ID: {contact.contact_id}")
        print(f"Type: {contact.contact_type.value}")
        print(f"Location: {contact.location}")
        print(f"Signal: {contact.signal_strength}/10")
        print(f"Duration: {contact.duration_minutes} minutes")
        print(f"Message: {contact.message_received}")
    except Exception as e:
        print(e)

    print("\n======================================")
    print("Expected validation error:")
    try:
        contact = AlienContact(
            contact_id="AC_2024_001",
            contact_type=ContactType.telepathic,
            location="Area 51, Nevada",
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=2,
            message_received="Greetings from Zeta Reticuli",
            timestamp=datetime.now(),
        )
    except Exception as e:
        print(e.errors()[0]['msg'])


if __name__ == "__main__":
    main()
