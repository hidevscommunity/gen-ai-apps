"""LLM Config for Socrates AI chatbot."""

import random

from langchain.prompts.prompt import PromptTemplate

from langchain.chains import ConversationChain
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
from copy import copy

OPENAI_MODEL = "gpt-3.5-turbo"
TEMPERATURE = 0.8

class AIPersonality:
    """Socrates AI chatbot."""

    name = "Socrates"
    avatar = "./socrates_v2/resources/socrates.png"
    openai_model = OPENAI_MODEL
    temperature = TEMPERATURE

    GREETINGS = [
        "What truth do you seek today?",
        "With which thought shall we engage this day?"
    ]

    def get_greeting(self) -> str:
        return random.choice(self.GREETINGS)

    character_intro = "You are a wise philosopher."
    conversation_intro = """
    The following is your conversation with one of your pupils.
    You are answering in a friendly manner with the goal of imparting wisdom.
    """
    additional_instructions = [
        "If you do not know the answer to a question, you ask a question in return " +
        "that will help your student reach the answer they seek.",
        "If you can give a decent answer, you do so, and let the student ask " +
        "their own follow-up questions as needed. Don't ask a new question unless " +
        "the student or the conversation is stuck.",
        "If asked something casual or off-topic, steer the conversation back to " +
        "philosophical inquiries with a gentle nudge.",
    ]

    @property
    def prompt_template(self) -> PromptTemplate:
        """Template for the prompt."""
        DEFAULT_TEMPLATE = "\n".join([
            f"You are {self.name}. {self.character_intro}",
            self.conversation_intro,
            "\n".join(self.additional_instructions),
            "",
            "Current conversation:",
            "{history}",
            "Student: {input}",
            f"{self.name}:"
        ])
        return PromptTemplate(
            input_variables=["history", "input"],
            template=DEFAULT_TEMPLATE,
        )

    def create_langchain_chain(self, openai_api_key: str | None) -> ConversationChain:
        memory = ConversationBufferMemory()
        openai_llm = OpenAI(
            # FIXME: should be 'model=' instead of 'model_name=' but
            # calls fail if model name is passed that way.
            model_name=self.openai_model,
            temperature=self.temperature,
            streaming=True,
            openai_api_key=openai_api_key,
        )
        chain = ConversationChain(
            llm=openai_llm,
            memory=memory,
            verbose=True,
            prompt=self.prompt_template,
        )
        return chain


class SocratesAI(AIPersonality):
    """For now, Socrates is already the default personality.
    
    In the future, we can refactor this to use an abstract base class.
    """
    pass


class YodaAI(SocratesAI):
    """Yoda AI chatbot."""

    name = "Yoda"
    character_intro = "You are a wise Jedi Master."
    avatar = "https://upload.wikimedia.org/wikipedia/en/9/9b/Yoda_Empire_Strikes_Back.png"
    GREETINGS = [
        # Wise greetings to a young student, in Yoda's style:
        "A promising Jedi you are. Great wisdom you seek.",
        "Listening am I. Ask questions now, you must.",
    ]

    @property
    def additional_instructions(self) -> list[str]:
        result = copy(super().additional_instructions)
        result.append(
            "Always speak in the distinctive and inverted style Yoda is known for."
        )
        return result


PERSONALITIES = {
    cls.name: cls
    for cls in [SocratesAI, YodaAI]
}

def new_personality(personality_name: str, /) -> AIPersonality:
    """Get the LLM to use."""
    return PERSONALITIES[personality_name]()

__all__ = [
    "AIPersonality",
    "SocratesAI",
    "YodaAI",
    "new_personality",
    "PERSONALITIES",
]
