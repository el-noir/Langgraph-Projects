import "dotenv/config";
import express from 'express';
import { buildGraph } from './chat/index3.js';
import { streamChat } from './chat/index3.js';

async function startServer(){

    try {
        const PORT = Number(process.env.PORT) || 5000;
        const app = express();
        app.use(express.json());

        const { chatbot, checkpointer } = await buildGraph();

        // Simple per-thread lock to serialize invocations for the same thread_id
        const locks = new Map<string, Promise<any>>();
        const withThreadLock = async <T>(threadId: string, fn: () => Promise<T>): Promise<T> => {
            const previous = locks.get(threadId) ?? Promise.resolve();
            const next = previous.then(() => fn()).finally(() => {
                // remove lock only if it's still the same promise
                if (locks.get(threadId) === next) locks.delete(threadId);
            });
            locks.set(threadId, next);
            return next;
        };

        // SSE helper
        function sseSend(res: express.Response, name: string | null, data: any) {
            if (name) res.write(`event: ${name}\n`);
            const payload = typeof data === 'string' ? data : JSON.stringify(data);
            res.write(`data: ${payload}\n\n`);
        }

    
        app.post('/chat/stream', async (req, res) => {
            try {
                const userMessage = (req.body?.message ?? req.query?.message) as string;
                if (!userMessage) return res.status(400).send('message is required');

                const threadId = (req.body?.thread_id ?? req.query?.thread_id) as string ?? Math.random().toString(36).slice(2,10);

                // SSE headers
                res.setHeader('Content-Type', 'text/event-stream; charset=utf-8');
                res.setHeader('Cache-Control', 'no-cache, no-transform');
                res.setHeader('Connection', 'keep-alive');
                res.flushHeaders?.();

                // send open event with thread id
                sseSend(res, 'open', { thread_id: threadId });

                // Serialize per-thread executions to avoid races
                await withThreadLock(threadId, async () => {
                    await streamChat(chatbot, userMessage, threadId, (chunk) => {
                        // forward chunk to client; chunk may be array [c, meta] or plain
                        if (Array.isArray(chunk) && chunk.length === 2) {
                            const [c, meta] = chunk;
                            sseSend(res, 'chunk', { chunk: c, meta });
                        } else {
                            sseSend(res, 'chunk', chunk);
                        }
                    });
                });

                sseSend(res, 'end', { ok: true });
                res.end();
            } catch (err) {
                console.error('Stream error', err);
                try { sseSend(res, 'error', { message: (err as any)?.message ?? String(err) }); res.end(); } catch {};
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
