import React, { useState } from 'react';
import { Copy, Volume2, VolumeX, Check, Bookmark, Sparkles } from 'lucide-react';
import { speakText, stopSpeech } from '../services/tts';
import { useToast } from '../context/ToastContext';

export default function CaptionCard({
  caption,
  index,
  isUsed,
  onUseCaption,
  onRegenerateSingle
}) {
  const { showToast } = useToast();
  const [copied, setCopied] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);

  const fullTextToCopy = `${caption.text}\n\n${(caption.hashtags || []).join(' ')}`;

  const handleCopy = () => {
    navigator.clipboard.writeText(fullTextToCopy);
    setCopied(true);
    showToast('Caption and hashtags copied to clipboard!', 'success');
    setTimeout(() => setCopied(false), 2500);
  };

  const handleTTS = () => {
    if (isPlaying) {
      stopSpeech();
      setIsPlaying(false);
    } else {
      const speechString = `${caption.text}`;
      speakText(
        speechString,
        () => setIsPlaying(true),
        () => setIsPlaying(false),
        (err) => {
          setIsPlaying(false);
          showToast(`Speech Error: ${err}`, 'error');
        }
      );
    }
  };

  const styleBadgeColors = {
    Aesthetic: 'bg-purple-500/20 text-purple-300 border-purple-500/40',
    Emotional: 'bg-blue-500/20 text-blue-300 border-blue-500/40',
    'Creative / Trending': 'bg-amber-500/20 text-amber-300 border-amber-500/40'
  };

  const badgeClass = styleBadgeColors[caption.style] || 'bg-slate-800 text-slate-300 border-slate-700';

  return (
    <div
      className={`glass-card rounded-3xl p-6 transition-all duration-300 border ${
        isUsed
          ? 'border-purple-500 ring-2 ring-purple-500/30 shadow-2xl bg-purple-950/20'
          : 'border-white/10 hover:border-purple-500/30'
      }`}
    >
      {/* Header Row: Caption # & Style Badge */}
      <div className="flex items-center justify-between gap-3 mb-4">
        <div className="flex items-center gap-3">
          <span className="w-8 h-8 rounded-xl bg-purple-600/30 border border-purple-500/30 text-purple-300 flex items-center justify-center text-xs font-black">
            0{index + 1}
          </span>
          <span className={`text-xs font-bold px-3 py-1 rounded-full border ${badgeClass}`}>
            {caption.style}
          </span>
        </div>

        {isUsed && (
          <span className="flex items-center gap-1 text-[11px] font-bold text-emerald-400 bg-emerald-950/60 px-2.5 py-1 rounded-full border border-emerald-500/30">
            <Check className="w-3 h-3" /> Selected
          </span>
        )}
      </div>

      {/* Main Caption Text */}
      <p className="text-base sm:text-lg text-white dark:text-white light:text-slate-900 font-medium leading-relaxed mb-4 whitespace-pre-line">
        {caption.text}
      </p>

      {/* Hashtags */}
      {caption.hashtags && caption.hashtags.length > 0 && (
        <div className="flex flex-wrap items-center gap-1.5 mb-6">
          {caption.hashtags.map((tag, i) => (
            <span
              key={i}
              className="text-xs font-semibold text-purple-300 dark:text-purple-300 light:text-purple-700 bg-purple-500/10 hover:bg-purple-500/20 px-2.5 py-1 rounded-lg transition-colors cursor-pointer"
              onClick={() => {
                navigator.clipboard.writeText(tag);
                showToast(`Copied ${tag}`, 'info');
              }}
            >
              {tag}
            </span>
          ))}
        </div>
      )}

      {/* Action Toolbar */}
      <div className="flex flex-wrap items-center justify-between gap-3 pt-4 border-t border-white/10">
        <div className="flex items-center gap-2">
          {/* Copy Button */}
          <button
            type="button"
            onClick={handleCopy}
            className={`flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs font-semibold transition-all ${
              copied
                ? 'bg-emerald-600 text-white'
                : 'bg-slate-800/80 hover:bg-slate-700 text-slate-200 border border-slate-700'
            }`}
          >
            {copied ? <Check className="w-3.5 h-3.5" /> : <Copy className="w-3.5 h-3.5 text-purple-400" />}
            <span>{copied ? 'Copied!' : 'Copy Caption'}</span>
          </button>

          {/* Listen Button (TTS) */}
          <button
            type="button"
            onClick={handleTTS}
            className={`flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs font-semibold transition-all ${
              isPlaying
                ? 'bg-blue-600 text-white animate-pulse'
                : 'bg-slate-800/80 hover:bg-slate-700 text-slate-200 border border-slate-700'
            }`}
          >
            {isPlaying ? <VolumeX className="w-3.5 h-3.5" /> : <Volume2 className="w-3.5 h-3.5 text-blue-400" />}
            <span>{isPlaying ? 'Stop' : 'Listen'}</span>
          </button>
        </div>

        <div className="flex items-center gap-2">
          {/* Use This Caption Button */}
          <button
            type="button"
            onClick={() => {
              onUseCaption(index);
              showToast(`Selected Caption #${index + 1} as your choice!`, 'success');
            }}
            className={`flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-semibold transition-all ${
              isUsed
                ? 'bg-purple-600 text-white shadow-lg shadow-purple-600/30'
                : 'bg-purple-500/10 hover:bg-purple-500/20 text-purple-300 border border-purple-500/30'
            }`}
          >
            <Bookmark className="w-3.5 h-3.5" />
            <span>{isUsed ? 'Selected' : 'Use This Caption'}</span>
          </button>
        </div>
      </div>
    </div>
  );
}
