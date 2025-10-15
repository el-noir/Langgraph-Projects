import "dotenv/config";
import express from 'express';
import {query} from './chat/index.js';

async function startServer(){
    try {
        const PORT = Number(process.env.PORT) || 5000;
        const app = express();
        app.use(express.json());

        app.post('/chat', async (req, res) => {
            const userMessage = req.body.message as string;
            if (!userMessage) {
                return res.status(400).send('Message body parameter is required');
            }
            const response = await query(userMessage);  
            res.send(response.content);
        });

        app.listen(PORT, () => {
            console.log(`Server is running on port ${PORT}`);
        });

    } catch (error) {
        console.error('Error starting server:', error);
    }
}

startServer();
