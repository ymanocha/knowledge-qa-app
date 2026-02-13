import axios from 'axios';
import { getSessionId } from '../utils/session';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const client = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add request interceptor for Session ID
client.interceptors.request.use((config) => {
    const sessionId = getSessionId();
    if (sessionId) {
        config.headers['X-Session-ID'] = sessionId;
    }
    return config;
});

export default client;
