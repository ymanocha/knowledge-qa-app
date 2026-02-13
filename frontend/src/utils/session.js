import { v4 as uuidv4 } from 'uuid';

const SESSION_KEY = 'knowledge_qa_session_id';

export const getSessionId = () => {
    let sessionId = localStorage.getItem(SESSION_KEY);
    if (!sessionId) {
        sessionId = uuidv4();
        localStorage.setItem(SESSION_KEY, sessionId);
    }
    return sessionId;
};
