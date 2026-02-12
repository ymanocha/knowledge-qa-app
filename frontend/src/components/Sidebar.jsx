import React, { useEffect, useState } from 'react';
import { useAPI } from '../hooks/useAPI';
import UploadDropzone from './UploadDropzone';
import { FileText, Database, RefreshCw, Trash2 } from 'lucide-react';
import { Link } from 'react-router-dom';

const Sidebar = () => {
    const { get, remove, loading } = useAPI();
    const [documents, setDocuments] = useState([]);
    const [deletingId, setDeletingId] = useState(null);

    const fetchDocuments = async () => {
        try {
            const docs = await get('/documents');
            setDocuments(docs || []);
        } catch (err) {
            console.error("Failed to fetch documents", err);
        }
    };

    const handleDelete = async (id) => {
        if (!window.confirm("Are you sure you want to remove this document? This will also remove the associated data from the knowledge base.")) {
            return;
        }

        setDeletingId(id);
        try {
            await remove(`/documents/${id}`);
            await fetchDocuments();
        } catch (err) {
            console.error("Delete failed", err);
            alert("Failed to delete document: " + (err.response?.data?.detail || err.message));
        } finally {
            setDeletingId(null);
        }
    };

    useEffect(() => {
        fetchDocuments();
    }, [get]); // get is stable from useAPI

    return (
        <div className="w-80 bg-slate-900 border-r border-slate-800 flex flex-col h-full">
            <div className="p-4 border-b border-slate-800">
                <h1 className="text-xl font-bold text-white flex items-center gap-2">
                    <Database className="w-6 h-6 text-blue-500" />
                    Knowledge Base
                </h1>
                <p className="text-xs text-slate-400 mt-1">Private RAG System</p>
            </div>

            <div className="p-4">
                <UploadDropzone onUploadSuccess={fetchDocuments} />
            </div>

            <div className="flex-1 overflow-y-auto p-4">
                <div className="flex items-center justify-between mb-2">
                    <h2 className="text-sm font-semibold text-slate-300">Uploaded Documents</h2>
                    <button onClick={fetchDocuments} className="text-slate-500 hover:text-white transition-colors">
                        <RefreshCw className={`w-3 h-3 ${loading && !deletingId ? 'animate-spin' : ''}`} />
                    </button>
                </div>

                {documents.length === 0 ? (
                    <div className="text-center py-8 text-slate-500 text-sm">
                        No documents yet.
                    </div>
                ) : (
                    <div className="space-y-2">
                        {documents.map((doc) => (
                            <div key={doc.id} className="group bg-slate-800/50 p-3 rounded border border-slate-800 hover:border-slate-700 transition-all">
                                <div className="flex items-start gap-2">
                                    <FileText className="w-4 h-4 text-blue-400 mt-0.5" />
                                    <div className="flex-1 min-w-0">
                                        <p className="text-sm text-slate-200 truncate font-medium">{doc.filename}</p>
                                        <p className="text-xs text-slate-500 mt-0.5">
                                            {doc.chunk_count} chunks • {doc.upload_date.split(' ')[0]}
                                        </p>
                                    </div>
                                    <button
                                        onClick={() => handleDelete(doc.id)}
                                        disabled={deletingId === doc.id}
                                        className="text-slate-600 hover:text-red-400 transition-colors p-1 opacity-0 group-hover:opacity-100 disabled:opacity-50"
                                        title="Delete document"
                                    >
                                        {deletingId === doc.id ? (
                                            <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                                        ) : (
                                            <Trash2 className="w-3.5 h-3.5" />
                                        )}
                                    </button>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>

            <div className="p-4 border-t border-slate-800">
                <Link to="/status" className="text-xs text-slate-500 hover:text-blue-400 transition-colors flex items-center justify-center gap-1">
                    System Status
                </Link>
            </div>
        </div>
    );
};

export default Sidebar;
