import React, { useState } from 'react';
import { useAPI } from '../hooks/useAPI';
import { Upload, X, FileText, CheckCircle, AlertCircle } from 'lucide-react';

const UploadDropzone = ({ onUploadSuccess }) => {
    const [file, setFile] = useState(null);
    const [uploadStatus, setUploadStatus] = useState('idle'); // idle, uploading, success, error
    const { post, error } = useAPI();

    const handleFileChange = (e) => {
        const selected = e.target.files[0];
        if (selected) {
            // Client-side validation
            if (!selected.name.endsWith('.txt')) {
                setUploadStatus('error');
                return;
            }
            if (selected.size > 10 * 1024 * 1024) { // 10MB
                setUploadStatus('error');
                return;
            }
            setFile(selected);
            setUploadStatus('idle');
        }
    };

    const handleUpload = async () => {
        if (!file) return;
        setUploadStatus('uploading');

        const formData = new FormData();
        formData.append('file', file);

        try {
            await post('/api/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            setUploadStatus('success');
            setFile(null);
            if (onUploadSuccess) onUploadSuccess();

            // Reset status after 3s
            setTimeout(() => setUploadStatus('idle'), 3000);
        } catch (err) {
            setUploadStatus('error');
            console.error("Upload error details:", err);
        }
    };

    return (
        <div className="p-4 border-2 border-dashed border-slate-700/50 rounded-lg bg-slate-800/50">
            <div className="flex flex-col items-center gap-3">
                {uploadStatus === 'success' ? (
                    <div className="text-green-400 flex flex-col items-center">
                        <CheckCircle className="w-8 h-8 mb-2" />
                        <span className="text-sm font-medium">Upload Complete</span>
                    </div>
                ) : (
                    <>
                        <input
                            type="file"
                            accept=".txt"
                            onChange={handleFileChange}
                            className="hidden"
                            id="file-upload"
                        />

                        {!file ? (
                            <label
                                htmlFor="file-upload"
                                className="cursor-pointer flex flex-col items-center text-slate-400 hover:text-white transition-colors"
                            >
                                <Upload className="w-8 h-8 mb-2" />
                                <span className="text-sm">Click to upload .txt</span>
                                <span className="text-xs text-slate-500 mt-1">Max 10MB</span>
                            </label>
                        ) : (
                            <div className="w-full">
                                <div className="flex items-center justify-between bg-slate-700 p-2 rounded mb-3">
                                    <div className="flex items-center gap-2 truncate">
                                        <FileText className="w-4 h-4 text-blue-400" />
                                        <span className="text-sm text-slate-200 truncate">{file.name}</span>
                                    </div>
                                    <button onClick={() => setFile(null)} className="text-slate-400 hover:text-red-400">
                                        <X className="w-4 h-4" />
                                    </button>
                                </div>

                                <button
                                    onClick={handleUpload}
                                    disabled={uploadStatus === 'uploading'}
                                    className="w-full py-2 bg-blue-600 hover:bg-blue-500 disabled:opacity-50 text-white rounded text-sm font-medium transition-colors"
                                >
                                    {uploadStatus === 'uploading' ? 'Uploading...' : 'Upload File'}
                                </button>
                            </div>
                        )}

                        {uploadStatus === 'error' && (
                            <div className="flex items-center gap-2 text-red-400 text-xs mt-2">
                                <AlertCircle className="w-3 h-3" />
                                <span>{error || "Invalid file"}</span>
                            </div>
                        )}
                    </>
                )}
            </div>
        </div>
    );
};

export default UploadDropzone;
