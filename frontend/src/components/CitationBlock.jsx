import React from 'react';
import { FileText, Quote } from 'lucide-react';

const CitationBlock = ({ citation }) => {
    const { source_file, text_snippet, score } = citation;

    // Format score as percentage
    const confidence = Math.round(score * 100);

    return (
        <div className="bg-slate-800/50 border border-slate-700 rounded p-3 text-xs mt-2">
            <div className="flex items-center justify-between mb-2 text-slate-400">
                <div className="flex items-center gap-1.5">
                    <FileText className="w-3 h-3" />
                    <span className="font-semibold text-slate-300">{source_file}</span>
                </div>
                <span className={`px-1.5 py-0.5 rounded text-[10px] font-mono ${confidence > 80 ? 'bg-green-900/30 text-green-400' :
                        confidence > 60 ? 'bg-yellow-900/30 text-yellow-400' : 'bg-red-900/30 text-red-400'
                    }`}>
                    {confidence}% Match
                </span>
            </div>

            <div className="relative pl-3 border-l-2 border-slate-600">
                <p className="text-slate-300 italic line-clamp-3 leading-relaxed">
                    "{text_snippet}"
                </p>
            </div>
        </div>
    );
};

export default CitationBlock;
