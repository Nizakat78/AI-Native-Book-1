
  """
  Hugging Face Spaces App for RAG Agent
  """
  import os
  import sys
  import gradio as gr

  # Add the src directory to the path
  sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

  from rag_agent.main import app as fastapi_app
  from rag_agent.agent import RAGAgent
  from rag_agent.config import get_config

  # Initialize the agent
  config = get_config()
  rag_agent = RAGAgent()

  def chat_with_agent(message, history):
      """Chat function for Gradio interface"""
      try:
          # Process the message with the RAG agent
          response_text, sources, conversation_id = rag_agent.process(message)
          return response_text
      except Exception as e:
          return f"Error: {str(e)}"

  # Create Gradio interface
  with gr.Blocks() as demo:
      gr.Markdown("# RAG Agent Chatbot")
      gr.Markdown("Ask questions about the Physical AI and Humanoid Robotics book")

      chatbot = gr.Chatbot()
      msg = gr.Textbox(label="Your Question")
      clear = gr.Button("Clear")

      def respond(message, chat_history):
          bot_message = chat_with_agent(message, chat_history)
          chat_history.append((message, bot_message))
          return "", chat_history

      msg.submit(respond, [msg, chatbot], [msg, chatbot])
      clear.click(lambda: None, None, chatbot, queue=False)

  # For Hugging Face Spaces
  if __name__ == "__main__":
      demo.launch(share=True, server_name="0.0.0.0", server_port=int(os.getenv("PORT", 7860)))