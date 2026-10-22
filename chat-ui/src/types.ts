export type Message = {
  content: string;
  sender: "user" | "chat";
  msgID: string;
};

export type MessageToSend = {
    role: "user" | "asisstant";
    content: string;
}