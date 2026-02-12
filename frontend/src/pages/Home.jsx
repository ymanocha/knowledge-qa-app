import React from 'react';
import Sidebar from '../components/Sidebar';
import ChatInterface from '../components/ChatInterface';

const Home = () => {
    return (
        <div className="flex h-screen bg-slate-950 overflow-hidden">
            <Sidebar />
            <main className="flex-1 flex flex-col min-w-0">
                <ChatInterface />
            </main>
        </div>
    );
};

export default Home;
