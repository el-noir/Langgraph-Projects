import "dotenv/config";
import express from 'express';
import { HumanMessage } from '@langchain/core/messages';
import {buildGraph} from './chat/index2.js';

async function startServer(){

    try {
        const PORT = Number(process.env.PORT) || 5000;
        const app = express();
        app.use(express.json());

        const {chatbot, checkpointer} = await buildGraph();

        app.post('/chat', async (req, res) => {
         try {
               const userMessage = req.body.message as string;
               const thread_id = req.body.thread_id ? req.body.thread_id as string : "default";
               if (!userMessage) {
                   return res.status(400).send('Message body parameter is required');
               }

                const response = await chatbot.invoke(
  { messages: [new HumanMessage(userMessage)] },
  { configurable: { thread_id } }
);
                const text = response?.messages?.at(-1)?.content ?? '';

                res.send({reply: text, thread_id});
         } catch (error) {
            console.error('Error processing chat message:', error);
            res.status(500).send('Internal Server Error');
         }
        });

        app.listen(PORT, () => {
            console.log(`Server is running on port ${PORT}`);
        });

    } catch (error) {
        console.error('Error starting server:', error);
    }
}

startServer();
