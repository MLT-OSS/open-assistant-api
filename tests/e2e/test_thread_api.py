
def test_thread_copy(client):
    """
    test copy thread
    """
    thread = client.beta.threads.create()
    contents = ["test1", "test2", "test3"]
    messages = [client.beta.threads.messages.create(thread_id=thread.id, role="user", content=content) for content in contents]
    for index, message in enumerate(messages):
        print(index)
        new_thread = client.beta.threads.create(extra_body={"thread_id": thread.id,
                                                        "end_message_id": message.id})
        new_messages = client.beta.threads.messages.list(thread_id=new_thread.id).data
        assert len(new_messages) == index + 1

        for i in range(index + 1):
            assert new_messages[i].content[0].text.value == contents[i]
        client.beta.threads.delete(thread_id=new_thread.id)
    client.beta.threads.delete(thread_id=thread.id)
