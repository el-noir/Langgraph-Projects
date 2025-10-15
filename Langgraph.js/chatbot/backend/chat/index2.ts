import dotenv from 'dotenv';
import { ChatGoogleGenerativeAI } from '@langchain/google-genai';
import type { BaseMessage } from '@langchain/core/messages';
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
    
    const chatbot = graph.compile({checkpointer: checkpointerInstance});

    return {chatbot, checkpointer: checkpointerInstance};
}

export { buildGraph };
