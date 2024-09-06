import json

from openai import AssistantEventHandler


def test_sub_stream_with_submit_tool_outputs_stream(client):

    def get_current_weather(location):
        return f"{location}今天是雨天。 "

    assistant = client.beta.assistants.create(
        name="Assistant Demo",
        instructions="You are a helpful assistant. When asked a question, use tools wherever possible.",
        model="gpt-4o",
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "get_current_weather",
                    "description": "当你想查询指定城市的天气时非常有用。",
                    "parameters": {"type": "object", "properties": {"location": {"type": "string", "description": "城市或县区，比如北京市、杭州市、余杭区等。"}}, "required": ["location"]},  # 查询天气时需要提供位置，因此参数设置为location
                },
            }
        ],
    )
    print("=====> : %s\n", assistant)

    thread = client.beta.threads.create()
    print("=====> : %s\n", thread)

    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="北京天气如何？",
    )
    print("=====> : %s\n", message)

    funcs = [get_current_weather]

    class EventHandler(AssistantEventHandler):

        def on_event(self, event):
            print(event.event)
            if event.event == "thread.run.requires_action":
                print(event)
                run_id = event.data.id  # Retrieve the run ID from the event data
                self.handle_requires_action(event.data, run_id)

        def handle_requires_action(self, data, run_id):
            tool_outputs = []

            for tool in data.required_action.submit_tool_outputs.tool_calls:
                func = next(iter([func for func in funcs if func.__name__ == tool.function.name]))
                try:
                    output = func(**eval(tool.function.arguments))
                except Exception as e:
                    output = "Error: " + str(e)

                tool_outputs.append({"tool_call_id": tool.id, "output": json.dumps(output)})

            print(tool_outputs)

            # Submit all tool_outputs at the same time
            self.submit_tool_outputs(tool_outputs, run_id)

        def submit_tool_outputs(self, tool_outputs, run_id):
            # Use the submit_tool_outputs_stream helper
            with client.beta.threads.runs.submit_tool_outputs_stream(
                thread_id=self.current_run.thread_id,
                run_id=self.current_run.id,
                tool_outputs=tool_outputs,
                event_handler=EventHandler(),
            ) as stream:
                # for text in stream.text_deltas:
                #     print(text, end="", flush=True)
                #     print()
                stream.until_done()

        def on_text_delta(self, delta, snapshot) -> None:
            print("=====> text delta")
            print("delta   : %s", delta)

    with client.beta.threads.runs.stream(
        thread_id=thread.id,
        assistant_id=assistant.id,
        event_handler=EventHandler(),
    ) as stream:
        stream.until_done()
