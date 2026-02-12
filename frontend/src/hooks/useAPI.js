import { useState, useCallback } from 'react';
import client from '../api/client';

export const useAPI = () => {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const request = useCallback(async (method, url, data = null, config = {}) => {
        setLoading(true);
        setError(null);
        try {
            const response = await client({
                method,
                url,
                data,
                ...config,
            });
            return response.data;
        } catch (err) {
            const message = err.response?.data?.detail || err.message || 'An unexpected error occurred';
            setError(message);
            throw err;
        } finally {
            setLoading(false);
        }
    }, []);

    const get = useCallback((url, config) => request('GET', url, null, config), [request]);
    const post = useCallback((url, data, config) => request('POST', url, data, config), [request]);
    const remove = useCallback((url, config) => request('DELETE', url, null, config), [request]);

    return { loading, error, get, post, remove };
};
