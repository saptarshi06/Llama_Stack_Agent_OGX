


























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