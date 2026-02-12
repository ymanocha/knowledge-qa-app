import React, { useEffect, useState } from 'react';
import { useAPI } from '../hooks/useAPI';
import { CheckCircle, XCircle, Activity, ArrowLeft, RefreshCw } from 'lucide-react';
import { Link } from 'react-router-dom';

const StatusPage = () => {
    const { get, loading } = useAPI();
    const [health, setHealth] = useState(null);
    const [lastChecked, setLastChecked] = useState(null);

    const checkHealth = async () => {
        try {
            const data = await get('/health');
            setHealth(data);
            setLastChecked(new Date().toLocaleTimeString());
        } catch (err) {
            setHealth(null); // specific error state handled by UI if health is null
        }
    };

    useEffect(() => {
        checkHealth();
        const interval = setInterval(checkHealth, 30000); // Poll every 30s
        return () => clearInterval(interval);
    }, [get]);

    const StatusRow = ({ label, status }) => (
        <div className="flex items-center justify-between py-3 border-b border-slate-800 last:border-0">
            <span className="text-slate-300 font-medium">{label}</span>
            <div className={`flex items-center gap-2 px-3 py-1 rounded-full text-xs font-bold ${status === 'ok' ? 'bg-green-900/30 text-green-400' : 'bg-red-900/30 text-red-400'
                }`}>
                {status === 'ok' ? (
                    <>
                        <CheckCircle className="w-3 h-3" />
                        <span>OPERATIONAL</span>
                    </>
                ) : (
                    <>
                        <XCircle className="w-3 h-3" />
                        <span>ERROR</span>
                    </>
                )}
            </div>
        </div>
    );

    return (
        <div className="min-h-screen bg-slate-950 flex flex-col items-center justify-center p-4">
            <div className="max-w-md w-full bg-slate-900 border border-slate-800 rounded-xl shadow-2xl p-6">
                <div className="flex items-center justify-between mb-6">
                    <div className="flex items-center gap-3">
                        <Activity className="w-6 h-6 text-blue-500" />
                        <h1 className="text-xl font-bold text-white">System Status</h1>
                    </div>
                    <button
                        onClick={checkHealth}
                        className={`text-slate-500 hover:text-white transition-colors ${loading ? 'animate-spin' : ''}`}
                    >
                        <RefreshCw className="w-5 h-5" />
                    </button>
                </div>

                <div className="bg-slate-950 rounded-lg border border-slate-800 p-4 mb-6">
                    {health ? (
                        <>
                            <StatusRow label="Backend API" status={health.backend} />
                            <StatusRow label="Vector Storage" status={health.storage} />
                            <StatusRow label="Gemini Connection" status={health.gemini} />
                        </>
                    ) : (
                        <div className="text-center py-4 text-red-400">
                            <XCircle className="w-8 h-8 mx-auto mb-2" />
                            <p>Cannot connect to Backend API</p>
                        </div>
                    )}
                </div>

                <div className="flex items-center justify-between text-xs text-slate-500 mt-4">
                    <span>Last checked: {lastChecked || 'Never'}</span>
                    <Link to="/" className="flex items-center gap-1 hover:text-blue-400 transition-colors">
                        <ArrowLeft className="w-3 h-3" />
                        Back to App
                    </Link>
                </div>
            </div>
        </div>
    );
};

export default StatusPage;
