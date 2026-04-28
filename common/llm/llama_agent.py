# from llama_stack_client import LlamaStackClient
# from llama_stack_client.lib.agents.agent import Agent

# class LlamaAgent:
#     def __init__(self):
#         self.client = LlamaStackClient(
#             base_url="http://localhost:8321"
#         )
#         self.agent = self._create_agent()

#     client = Agent(...)
#     client
#     def _create_agent(self):
#         return Agent(
#             client=self.client,
#             model="phi3:mini",   # must match server config

#             input_shields=[
#                 {
#                     "provider_id": "llama-guard",
#                     "provider_shield_id": "content_safety"
#                 }
#             ],
#             output_shields=[
#                 {
#                     "provider_id": "llama-guard",
#                     "provider_shield_id": "content_safety"
#                 }
#             ]
#         )

#     def run(self):
#         session_id = self.agent.create_session("session_1")

#         while True:
#             user_input = input("User: ")

#             response = self.agent.chat(
#                 session_id=session_id,
#                 messages=[{"role": "user", "content": user_input}]
#             )

#             print("Bot:", response)


# if __name__ == "__main__":
#     LlamaAgent().run()

from llama_stack_client import LlamaStackClient
from llama_stack_client.lib.agents.agent import Agent

class LlamaAgent:
    def __init__(self):
        # 1. Connect to your pre-configured Llama Stack server
        self.client = LlamaStackClient(base_url="http://localhost:8321")
        
        # 2. Check which shields are already available on the server
        available_shields = [s.identifier for s in self.client.shields.list()]
        print(f"Server-side shields found: {available_shields}")
        
        # We assume 'llama_guard' or similar is in your server's run.yaml
        self.shield_id = "llama_guard" if "llama_guard" in available_shields else None
        self.agent = self._create_agent()

    def _create_agent(self):
        return Agent(
            client=self.client,
            model="phi3:mini", 
            # 3. Simply pass the ID string of the pre-configured shield
            input_shields=[self.shield_id] if self.shield_id else [],
            output_shields=[self.shield_id] if self.shield_id else []
        )

    def run(self):
        session_id = self.agent.create_session("session_1")
        print("Chat started. Type 'exit' to stop.")

        while True:
            user_input = input("User: ")
            if user_input.lower() in ["exit", "quit"]: break

            # 4. create_turn is the modern way to interact
            response = self.agent.create_turn(
                messages=[{"role": "user", "content": user_input}],
                session_id=session_id,
            )

            # Stream the response
            for chunk in response:
                if hasattr(chunk, 'event') and chunk.event.payload.event_type == "turn_complete":
                    print("Bot:", chunk.event.payload.turn.output_message.content)

if __name__ == "__main__":
    LlamaAgent().run()
