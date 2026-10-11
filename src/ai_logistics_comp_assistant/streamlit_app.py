import html
import re

import streamlit as st

from ai_logistics_comp_assistant.core.agent import stream_response
from ai_logistics_comp_assistant.core.tools import get_product_names


def render_assistant_markdown(content: str) -> None:
	content = html.escape(content)
	content = re.sub(r"&lt;br\s*/?&gt;", "<br>", content, flags=re.IGNORECASE)
	st.markdown(content, unsafe_allow_html=True)


def stream_assistant_markdown(chunks) -> str:
	placeholder = st.empty()
	content = ""
	for chunk in chunks:
		content += chunk
		with placeholder.container():
			render_assistant_markdown(content)
	return content


if "messages" not in st.session_state:
	st.session_state.messages = []

st.title(":ship: GreatGlobe Logistics Assistant")
st.write("Select Product, Source, and Destination to check shipping requirements.")

with st.sidebar.form("shipment_details"):
	st.subheader("Shipment details")
	product_names = get_product_names()
	product_name = st.selectbox(
		"Product name",
		options=product_names,
		index=None,
		placeholder="Type to search products...",
	)
	source = st.text_input("Source country", placeholder="e.g. Canada")
	destination = st.text_input("Destination country", placeholder="e.g. Japan")
	submitted = st.form_submit_button("Check requirements", type="primary")

for message in st.session_state.messages:
	with st.chat_message(message["role"]):
		if message["role"] == "assistant":
			render_assistant_markdown(message["content"])
		else:
			st.markdown(message["content"])

if submitted:
	if not product_name or not source.strip() or not destination.strip():
		st.sidebar.error("Select a product and enter both countries.")
	else:
		query = (
			f"Prepare a shipping compliance manifest for {product_name}, "
			f"shipping from {source.strip()} to {destination.strip()}. "
			"Retrieve the product details, research applicable requirements, and "
			"summarize required documents, customs duties, and payment procedures."
		)
		st.session_state.messages.append({"role": "user", "content": query})

		with st.chat_message("user"):
			st.markdown(query)

		with st.chat_message("assistant"):
			try:
				response = stream_assistant_markdown(
					stream_response(st.session_state.messages)
				)
				st.session_state.messages.append(
					{"role": "assistant", "content": response}
				)
			except Exception as e:
				st.error(
					f"Failed: {str(e)}"
				)

if st.session_state.messages and st.session_state.messages[-1]["role"] == "assistant":
	follow_up = st.chat_input("Ask a follow-up question")
	if follow_up:
		st.session_state.messages.append({"role": "user", "content": follow_up})
		with st.chat_message("user"):
			st.markdown(follow_up)
		with st.chat_message("assistant"):
			try:
				response = stream_assistant_markdown(
					stream_response(st.session_state.messages)
				)
				st.session_state.messages.append(
					{"role": "assistant", "content": response}
				)
			except Exception as e:
				st.error(f"Failed: {str(e)}")
