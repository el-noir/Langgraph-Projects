import dotenv from 'dotenv';
import { ChatGoogleGenerativeAI } from '@langchain/google-genai';
import type { BaseMessage } from '@langchain/core/messages';
import { HumanMessage } from '@langchain/core/messages';
import { Annotation, END, messagesStateReducer, START, StateGraph } from '@langchain/langgraph';
import { MemorySaver } from '@langchain/langgraph';


dotenv.config();

const model = new ChatGoogleGenerativeAI({ temperature: 0, model: "gemini-2.0-flash", maxOutputTokens: 1024 });

type ChatState = {
    messages: BaseMessage[];
}

const ChatStateAnnotation = Annotation.Root({
    messages: Annotation<BaseMessage[]>({
        reducer: messagesStateReducer,
        default: () => [],
    })
})

interface ChatNodeState{
    messages: BaseMessage[];
}

interface ChatNodeResponse{
    messages: BaseMessage[];
}

const chatNode = async (state: ChatNodeState): Promise<ChatNodeResponse> =>{
    const messages = state.messages;
    const response = (await model.invoke(messages)) as BaseMessage;
    return { messages: [...messages,response] };
}

async function buildGraph(checkpointer?: any) {
    const checkpointerInstance = checkpointer ?? new MemorySaver();
    const graph = new StateGraph(ChatStateAnnotation as any)
    graph.addNode('chat_node', chatNode);
    graph.addEdge(START as any, 'chat_node' as any);
    graph.addEdge('chat_node' as any, END as any);
    
    const chatbot = graph.compile({ checkpointer: checkpointerInstance });

    // Return compiled chatbot and the checkpointer instance. Do NOT attempt to
    // stream inside buildGraph — streaming should be performed at runtime when
    // invoking the compiled graph (for example from your server handler).
    return { chatbot, checkpointer: checkpointerInstance };
}

// Helper: streamChat
// - chatbot: compiled graph returned from buildGraph()
// - userMessage: string or BaseMessage or array of BaseMessage
// - threadId: optional thread id to persist the conversation
// - onChunk: callback called for each streamed chunk (may be a BaseMessage chunk or metadata)
export async function streamChat(
    chatbot: any,
    userMessage: string | BaseMessage | BaseMessage[],
    threadId?: string,
    onChunk?: (chunk: any) => void
) {
    // Normalize messages array
    let messages: BaseMessage[];
    if (Array.isArray(userMessage)) {
        messages = userMessage as BaseMessage[];
    } else if (typeof userMessage === 'string') {
        messages = [new HumanMessage(userMessage)];
    } else {
        messages = [userMessage as BaseMessage];
    }

    const config = threadId ? { configurable: { thread_id: threadId } } : undefined;

    // chatbot.stream returns an async iterable. Use for-await-of to consume it.
    // The exact shape of each chunk depends on your compiled graph configuration
    // and the stream_mode; many examples yield either BaseMessage fragments or
    // tuples like [chunk, metadata]. We forward whatever the iterator yields to
    // the onChunk callback.
    const iterator = chatbot.stream({ messages }, config, { stream_mode: 'messages' });
    for await (const chunk of iterator) {
        if (onChunk) {
            try {
                onChunk(chunk);
            } catch (err) {
                // swallow user callback errors so streaming continues
                console.error('streamChat onChunk handler error:', err);
            }
        }
    }
}



export { buildGraph };
