import React, { useState } from 'react';
import { Eye, Tag, Sparkles, RefreshCw, CheckCircle, ShieldAlert } from 'lucide-react';
import CaptionCard from './CaptionCard';

export default function AnalysisDashboard({
  analysisData,
  previewUrl,
  selectedCategory,
  selectedTone,
  onRegenerateAll,
  isLoading
}) {
  const [selectedCaptionIndex, setSelectedCaptionIndex] = useState(null);

  if (!analysisData) return null;

  const { analysis, captions, isRealAi, notice } = analysisData;

  return (
    <div className="w-full max-w-5xl mx-auto space-y-8 animate-slide-up">
      
      {/* Top Banner Notice if AI API Key fallback was used */}
      {notice && (
        <div className="flex items-center gap-3 p-4 rounded-2xl bg-amber-950/40 border border-amber-500/30 text-amber-200 text-xs sm:text-sm backdrop-blur-md">
          <ShieldAlert className="w-5 h-5 text-amber-400 shrink-0" />
          <div className="flex-1">
            <span className="font-bold">Notice:</span> {notice}
          </div>
        </div>
      )}

      {/* Main Results Split Card: Image Preview (Left) vs AI Vision Analysis (Right) */}
      <div className="glass-card rounded-3xl p-6 sm:p-8 border border-purple-500/20 shadow-2xl relative overflow-hidden">
        
        {/* Glow Decor Background Blob */}
        <div className="absolute -top-24 -right-24 w-72 h-72 bg-purple-600/10 rounded-full blur-3xl pointer-events-none" />

        <div className="grid grid-cols-1 md:grid-cols-12 gap-8 items-start relative z-10">
          
          {/* Left Side: Uploaded Image Frame (5 Cols) */}
          <div className="md:col-span-5 flex flex-col items-center">
            <div className="relative w-full aspect-square rounded-2xl overflow-hidden bg-slate-900 border border-white/10 shadow-2xl group">
              <img
                src={previewUrl}
                alt="Analyzed subject"
                className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
              />
              
              {/* Vision Lens Indicator Overlay */}
              <div className="absolute top-3 left-3 bg-black/60 backdrop-blur-md px-3 py-1 rounded-full border border-white/10 flex items-center gap-1.5 text-[11px] font-bold text-purple-300">
                <Eye className="w-3.5 h-3.5 text-purple-400" />
                <span>AI Analyzed</span>
              </div>
            </div>
          </div>

          {/* Right Side: What AI Noticed (7 Cols) */}
          <div className="md:col-span-7 flex flex-col justify-between space-y-6">
            
            <div>
              {/* Header Title */}
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-2">
                  <div className="w-8 h-8 rounded-xl bg-purple-600/20 border border-purple-500/30 flex items-center justify-center">
                    <Sparkles className="w-4 h-4 text-purple-400" />
                  </div>
                  <h3 className="text-xl font-bold text-white dark:text-white light:text-slate-900">
                    What AI Noticed
                  </h3>
                </div>

                <button
                  type="button"
                  onClick={onRegenerateAll}
                  disabled={isLoading}
                  className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-semibold bg-purple-600/20 hover:bg-purple-600/30 text-purple-300 border border-purple-500/30 transition-all disabled:opacity-50"
                  title="Regenerate all captions for this image"
                >
                  <RefreshCw className={`w-3.5 h-3.5 ${isLoading ? 'animate-spin' : ''}`} />
                  <span>Regenerate</span>
                </button>
              </div>

              {/* AI Description */}
              <div className="p-4 rounded-2xl bg-slate-900/80 dark:bg-slate-900/80 light:bg-slate-100 border border-slate-800 dark:border-slate-800 light:border-slate-200 mb-5">
                <p className="text-sm sm:text-base text-slate-200 dark:text-slate-200 light:text-slate-700 leading-relaxed font-normal">
                  "{analysis?.description || 'The AI completed analysis of the uploaded visual elements.'}"
                </p>
              </div>

              {/* Recognized Visual Tags */}
              <div>
                <h4 className="text-xs font-bold text-slate-400 dark:text-slate-400 light:text-slate-600 uppercase tracking-wider mb-2.5 flex items-center gap-1.5">
                  <Tag className="w-3.5 h-3.5 text-purple-400" />
                  Detected Scene Elements & Atmosphere
                </h4>
                <div className="flex flex-wrap items-center gap-2">
                  {(analysis?.tags || ['Image Analysis', 'Scene Understanding']).map((tag, idx) => (
                    <span
                      key={idx}
                      className="px-3 py-1.5 rounded-xl text-xs font-semibold bg-purple-500/10 text-purple-300 border border-purple-500/20"
                    >
                      #{tag}
                    </span>
                  ))}
                </div>
              </div>

            </div>

            {/* Bottom Meta Info */}
            <div className="flex items-center gap-4 text-xs text-slate-400 pt-4 border-t border-white/10">
              <span>Category Context: <strong className="text-white">{selectedCategory}</strong></span>
              <span>•</span>
              <span>Tone: <strong className="text-white">{selectedTone}</strong></span>
            </div>

          </div>

        </div>

      </div>

      {/* 3 Unique Instagram Captions Header */}
      <div className="pt-4">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h3 className="text-2xl font-extrabold text-white dark:text-white light:text-slate-900">
              Generated Instagram Captions
            </h3>
            <p className="text-sm text-slate-400">
              Three distinct styles crafted directly from the visual context of your photo.
            </p>
          </div>
        </div>

        {/* 3 Caption Cards Grid */}
        <div className="grid grid-cols-1 gap-6">
          {captions.map((caption, idx) => (
            <CaptionCard
              key={idx}
              caption={caption}
              index={idx}
              isUsed={selectedCaptionIndex === idx}
              onUseCaption={(i) => setSelectedCaptionIndex(i)}
            />
          ))}
        </div>
      </div>

    </div>
  );
}
