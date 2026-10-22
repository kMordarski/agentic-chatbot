
import type { Message, MessageToSend } from '../src/types';


function messageChange({message}: {message: Message}): MessageToSend {
    const role = message.sender === "user" ? "user" : "assistant";
    return(
        {"role": role, "content": message.content}
    )
}

export function sendChat(messages: Message[]) {
    return(
            messages.map((message: Message) => (
                messageChange({message})
            ))
    )
}