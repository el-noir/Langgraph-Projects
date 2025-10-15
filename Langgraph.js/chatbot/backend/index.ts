import { TavilySearchResults } from "@langchain/community/tools/tavily_search";
import { ChatGoogleGenerativeAI } from "@langchain/google-genai";
import { HumanMessage, AIMessage } from "@langchain/core/messages";
import { ToolNode } from "@langchain/langgraph/prebuilt";
import { StateGraph, MessagesAnnotation } from "@langchain/langgraph";
import dotenv from 'dotenv';

dotenv.config();

const tools = [new TavilySearchResults({maxResults: 3})]
const toolNode = new ToolNode(tools)

const model = new ChatGoogleGenerativeAI({temperature: 0, model: "gemini-2.0-flash", maxOutputTokens: 1024}).bindTools(tools);

function shouldContinue({messages}: typeof MessagesAnnotation.State){
    const lastMessage = messages[messages.length - 1] as AIMessage;

    if(lastMessage.tool_calls?.length){
        return "tools";
    }
    return "__end__";
}

async function callModel(state:typeof MessagesAnnotation.State) {
    const response = await model.invoke(state.messages)
    
    return {messages: [response]}
}

const workflow = new StateGraph(MessagesAnnotation)
    .addNode("agent", callModel)
    .addEdge("__start__", "agent")
    .addNode("tools", toolNode)
    .addEdge("tools", "agent")
    .addConditionalEdges("agent", shouldContinue);

const app = workflow.compile();

const finalState = await app.invoke({
    messages: [new HumanMessage("what is the weather in sf")],
});

console.log(finalState.messages[finalState.messages.length - 1]?.content);

const nextState = await app.invoke({
  messages: [...finalState.messages, new HumanMessage("What about ny")]  
})

console.log(nextState.messages[nextState.messages.length -1]?.content)



