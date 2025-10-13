import dotenv from 'dotenv';

// Load environment variables from .env file
dotenv.config();

import { TavilySearchResults } from "@langchain/community/tools/tavily_search";
import { ChatGoogleGenerativeAI } from "@langchain/google-genai";
import { MemorySaver } from "@langchain/langgraph";
import { HumanMessage } from "@langchain/core/messages";
import {createReactAgent} from "@langchain/langgraph/prebuilt"

const agentTools = [new TavilySearchResults({maxResults: 3})]
const agentModel = new ChatGoogleGenerativeAI({temperature: 0, model: "gemini-2.0-flash", maxOutputTokens: 1024});

const agentCheckPonter = new MemorySaver()

const agent = createReactAgent({
    llm: agentModel,
    tools: agentTools,
    checkpointSaver: agentCheckPonter
})

const agentFinalState = await agent.invoke(
    {messages: [new HumanMessage("What is the current weather in sf")]},
    {configurable: {thread_id: "42"}}
)

console.log(
    agentFinalState.messages[agentFinalState.messages.length - 1].content,
)

const agentNextState = await agent.invoke(
    {messages: [new HumanMessage("What about ny")]},
    {configurable: {thread_id: "42"}}
)

console.log(
    agentNextState.messages[agentNextState.messages.length - 1].content,
)

