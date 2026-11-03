
import type { Message, MessageToSend } from '../types';

const API_URL = import.meta.env.VITE_API_URL
const API_KEY = import.meta.env.VITE_API_KEY

function messageChange({message}: {message: Message}): MessageToSend {
    const role = message.sender === "user" ? "user" : "assistant";
    return(
        {"role": role, "content": message.content}
    )
}

function messageReverse({message}: {message: MessageToSend}): Message {

    const sender = message.role === "user" ? "user" : "chat";
    return(
        {"content": message.content, "sender": sender, "msgID": crypto.randomUUID()}
    )
}

export async function getMessage(id: string): Promise<Message[]> {
    const res = await fetch(`${API_URL}/conversations/${id}/messages`, {
        method: 'GET',
        headers: {
            "X-API-Key": API_KEY,
        }
    })
    if (!res.ok) throw new Error(`API error ${res.status}`)
    const data: MessageToSend[] = await res.json();
    return data.map((element: MessageToSend) => messageReverse({message: element}))
}


export async function createConversation(): Promise<string> {
    const res = await fetch(`${API_URL}/conversations`, {
        method: 'POST',
        headers: {
            "X-API-Key": API_KEY,
        }
    })
    if (!res.ok) throw new Error(`API error ${res.status}`)
    const data = await res.json()
    return data.id
}

export async function sendChat(messages: Message[]): Promise<string> {
    const res = await fetch(`${API_URL}/chat`, {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
            "X-API-Key": API_KEY,
        },
        body: JSON.stringify({ messages: messages.map((message: Message) => (
            messageChange({message})
        ))}),
    });
    if (!res.ok) throw new Error(`API error ${res.status}`);
    const data = await res.json()
    return data.reply
}

export async function streamChat(messages: Message[],
    conversationId: string,
    onToken: (text: string) => void): Promise<void> {
        const res = await fetch(`${API_URL}/chat/stream`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-API-Key": API_KEY
            },
            body: JSON.stringify({ messages: messages.map((message: Message) => (
                messageChange({message}))),
                conversation_id: conversationId,
        }),
        });
        if (!res.ok || !res.body) throw new Error(`API error ${res.status}`);

        const reader = res.body.getReader();
        const decoder = new TextDecoder();
        let buffer = "";

        while(true) {
            const { done, value } = await reader.read();
            if (done) break;
            buffer += decoder.decode(value, { stream: true });
            const events = buffer.split("\n\n");
            buffer = events.pop() ?? "";
            for (const ev of events) {
                if (!ev.startsWith("data: ")) continue;
                const payload = ev.slice(6);
                if (payload === "[DONE]") return;
                onToken(JSON.parse(payload));
            }
        }
    }