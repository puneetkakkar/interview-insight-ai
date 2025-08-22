from functools import cache
from typing import TypeAlias

# from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_community.chat_models import ChatOpenAI, FakeListChatModel

from src.app.core.config import settings

from src.app.schemas.language_models import (
    AllModelEnum,
    OpenAIModelName,
    AnthropicModelName,
    FakeModelName,
)


_MODEL_TABLE = (
    {m: m.value for m in AnthropicModelName}
    | {m: m.value for m in OpenAIModelName}
    | {m: m.value for m in FakeModelName}
)


class FakeToolModel(FakeListChatModel):
    def __init__(self, responses: list[str]):
        super().__init__(responses=responses)

    def bind_tools(self, tools):
        return self


ModelT: TypeAlias = ChatAnthropic


@cache
def get_model(model_name: AllModelEnum, /) -> ModelT:
    # NOTE: models with streaming=True will send tokens as they are generated
    # if the /stream endpoint is called with stream_tokens=True (the default)
    api_model_name = _MODEL_TABLE.get(model_name)
    if not api_model_name:
        raise ValueError(f"Unsupported model: {model_name}")

    if model_name in OpenAIModelName:
        return ChatOpenAI(model=api_model_name, temperature=0.5, streaming=True)
    if model_name in AnthropicModelName:
        return ChatAnthropic(
            model=api_model_name,
            temperature=0.5,
            streaming=True,
            api_key=settings.ANTHROPIC_API_KEY,
        )
    if model_name in FakeModelName:
        return FakeToolModel(responses=["This is a test response from the fake model."])

    raise ValueError(f"Unsupported model: {model_name}")
