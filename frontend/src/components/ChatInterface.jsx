import React, { useState, useRef, useEffect } from 'react';
import { useAPI } from '../hooks/useAPI';
import CitationBlock from './CitationBlock';
import { Send, Bot, User, Sparkles } from 'lucide-react';
import ReactMarkdown from 'react-markdown';

const ChatInterface = () => {
    const [messages, setMessages] = useState([
        { role: 'system', content: 'Hello! I am your private knowledge assistant. Upload some documents and ask me anything about them.' }
    ]);
    const [input, setInput] = useState('');
    const { post, loading } = useAPI();
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSend = async (e) => {
        e.preventDefault();
        if (!input.trim() || loading) return;

        const userMsg = { role: 'user', content: input };
        setMessages(prev => [...prev, userMsg]);
        setInput('');

        try {
            // Optimistic UI handled by loading state in UI
            const response = await post('/query', { question: userMsg.content, k: 3 });

            const botMsg = {
                role: 'assistant',
                content: response.answer,
                citations: response.citations
            };
            setMessages(prev => [...prev, botMsg]);

        } catch (err) {
            setMessages(prev => [...prev, { role: 'error', content: "Sorry, I encountered an error answering that query." }]);
        }
    };

    return (
        <div className="flex flex-col h-full bg-slate-950">
            {/* Messages Area */}
            <div className="flex-1 overflow-y-auto p-4 space-y-6">
                {messages.map((msg, idx) => (
                    <div key={idx} className={`flex gap-4 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                        {msg.role !== 'user' && (
                            <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${msg.role === 'error' ? 'bg-red-500/20 text-red-500' : 'bg-blue-600/20 text-blue-400'
                                }`}>
                                <Bot className="w-5 h-5" />
                            </div>
                        )}

                        <div className={`max-w-[80%] rounded-2xl p-4 ${msg.role === 'user'
                                ? 'bg-blue-600 text-white rounded-br-none'
                                : msg.role === 'error'
                                    ? 'bg-red-900/20 border border-red-800 text-red-200'
                                    : 'bg-slate-800/50 border border-slate-800 text-slate-100 rounded-bl-none'
                            }`}>
                            <div className="prose prose-invert prose-sm">
                                {msg.role === 'assistant' || msg.role === 'system' ? (
                                    <ReactMarkdown>{msg.content}</ReactMarkdown>
                                ) : (
                                    <p>{msg.content}</p>
                                )}
                            </div>

                            {/* Citations */}
                            {msg.citations && msg.citations.length > 0 && (
                                <div className="mt-4 pt-4 border-t border-slate-700/50">
                                    <p className="text-xs font-semibold text-slate-400 mb-2 flex items-center gap-1">
                                        <Sparkles className="w-3 h-3 text-yellow-500" />
                                        Sources Used
                                    </p>
                                    <div className="space-y-2">
                                        {msg.citations.map((cit, cIdx) => (
                                            <CitationBlock key={cIdx} citation={cit} />
                                        ))}
                                    </div>
                                </div>
                            )}
                        </div>

                        {msg.role === 'user' && (
                            <div className="w-8 h-8 rounded-full bg-slate-700 flex items-center justify-center shrink-0">
                                <User className="w-5 h-5 text-slate-300" />
                            </div>
                        )}
                    </div>
                ))}

                {loading && (
                    <div className="flex gap-4">
                        <div className="w-8 h-8 rounded-full bg-blue-600/20 text-blue-400 flex items-center justify-center shrink-0">
                            <Bot className="w-5 h-5" />
                        </div>
                        <div className="bg-slate-800/50 border border-slate-800 rounded-2xl rounded-bl-none p-4 flex items-center gap-2">
                            <span className="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '0s' }}></span>
                            <span className="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></span>
                            <span className="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></span>
                        </div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>

            {/* Input Area */}
            <div className="p-4 bg-slate-900 border-t border-slate-800">
                <form onSubmit={handleSend} className="relative max-w-4xl mx-auto">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Ask a question about your documents..."
                        className="w-full bg-slate-800 text-white pl-4 pr-12 py-3 rounded-xl border border-slate-700 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 placeholder-slate-500"
                        disabled={loading}
                    />
                    <button
                        type="submit"
                        disabled={!input.trim() || loading}
                        className="absolute right-2 top-2 p-1.5 bg-blue-600/20 text-blue-400 rounded-lg hover:bg-blue-600 hover:text-white transition-colors disabled:opacity-50 disabled:hover:bg-blue-600/20 disabled:hover:text-blue-400"
                    >
                        <Send className="w-5 h-5" />
                    </button>
                </form>
            </div>
        </div>
    );
};

export default ChatInterface;
