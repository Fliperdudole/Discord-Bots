


def variable_set(message) -> str:
    p_message = message.content.lower()

    if p_message == "!setchannel": # This response allows the user to set the channel they want the notifications in
        return str(message.channel.id) 
    
    return None