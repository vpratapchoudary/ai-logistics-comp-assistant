import logging

from langchain.agents import create_agent
from langchain_core.messages import AIMessageChunk

from ai_logistics_comp_assistant.core.prompt import SYSTEM_PROMPT
from ai_logistics_comp_assistant.core.tools import get_product_details, search_shipping_requirements


def assistant():
    logging.info("Initializing assistant workflow...")
    tools = [get_product_details, search_shipping_requirements]
    return create_agent(
        model="groq:openai/gpt-oss-120b",
        tools=tools,
        system_prompt=SYSTEM_PROMPT,
    )


def stream_response(messages: list[dict[str, str]]):
	agent = assistant()
	for message, _metadata in agent.stream(
		{"messages": messages},
		stream_mode="messages",
	):
		if not isinstance(message, AIMessageChunk):
			continue

		if isinstance(message.content, str):
			yield message.content
		else:
			for item in message.content:
				if isinstance(item, dict) and item.get("type") == "text":
					yield item.get("text", "")