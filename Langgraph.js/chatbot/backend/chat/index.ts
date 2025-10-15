import dotenv from 'dotenv';
import { ChatGoogleGenerativeAI } from '@langchain/google-genai';

dotenv.config();

const model = new ChatGoogleGenerativeAI({ temperature: 0, model: "gemini-2.0-flash", maxOutputTokens: 1024 });

async function query(userMessage: string) {
    const response = await model.invoke(
        userMessage
    );
    return response;
}

export { query };


