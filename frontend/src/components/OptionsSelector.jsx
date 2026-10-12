import React from 'react';
import { Tag, Sparkles } from 'lucide-react';

export default function OptionsSelector({ selectedCategory, setSelectedCategory, selectedTone, setSelectedTone, disabled }) {
  const categories = [
    { id: 'Nature', label: 'Nature', emoji: '🌿' },
    { id: 'People', label: 'People', emoji: '👥' },
    { id: 'Travel', label: 'Travel', emoji: '✈️' },
    { id: 'Food', label: 'Food', emoji: '🍔' },
    { id: 'Other', label: 'Other', emoji: '✨' },
  ];

  const tones = [
    { id: 'Aesthetic', label: 'Aesthetic', emoji: '🌸' },
    { id: 'Funny', label: 'Funny', emoji: '😂' },
    { id: 'Emotional', label: 'Emotional', emoji: '💖' },
    { id: 'Professional', label: 'Professional', emoji: '💼' },
    { id: 'Romantic', label: 'Romantic', emoji: '💕' },
    { id: 'Attitude', label: 'Attitude', emoji: '⚡' },
    { id: 'Minimalist', label: 'Minimalist', emoji: '🍃' },
  ];

  return (
    <div className="w-full max-w-3xl mx-auto my-8 space-y-6">
      
      {/* Category Pills */}
      <div className="glass-card p-5 sm:p-6 rounded-3xl border border-white/10">
        <div className="flex items-center gap-2 mb-4">
          <Tag className="w-4 h-4 text-purple-400" />
          <h4 className="text-sm font-bold text-white dark:text-white light:text-slate-900 tracking-wide uppercase">
            Image Category (Optional Context)
          </h4>
        </div>
        
        <div className="flex flex-wrap items-center gap-2.5">
          {categories.map((cat) => {
            const isSelected = selectedCategory === cat.id;
            return (
              <button
                key={cat.id}
                type="button"
                disabled={disabled}
                onClick={() => setSelectedCategory(cat.id)}
                className={`flex items-center gap-2 px-4 py-2.5 rounded-2xl text-xs sm:text-sm font-semibold transition-all duration-200 ${
                  isSelected
                    ? 'bg-purple-600 text-white shadow-lg shadow-purple-600/30 ring-2 ring-purple-400 scale-105'
                    : 'bg-slate-900/60 dark:bg-slate-900/60 light:bg-slate-100 text-slate-300 dark:text-slate-300 light:text-slate-700 border border-slate-700 dark:border-slate-700 light:border-slate-300 hover:border-purple-500/50 hover:bg-slate-800'
                }`}
              >
                <span>{cat.emoji}</span>
                <span>{cat.label}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Tone Pills */}
      <div className="glass-card p-5 sm:p-6 rounded-3xl border border-white/10">
        <div className="flex items-center gap-2 mb-4">
          <Sparkles className="w-4 h-4 text-blue-400" />
          <h4 className="text-sm font-bold text-white dark:text-white light:text-slate-900 tracking-wide uppercase">
            Caption Tone & Mood Preference
          </h4>
        </div>

        <div className="flex flex-wrap items-center gap-2.5">
          {tones.map((t) => {
            const isSelected = selectedTone === t.id;
            return (
              <button
                key={t.id}
                type="button"
                disabled={disabled}
                onClick={() => setSelectedTone(t.id)}
                className={`flex items-center gap-2 px-3.5 py-2 rounded-2xl text-xs sm:text-sm font-semibold transition-all duration-200 ${
                  isSelected
                    ? 'bg-blue-600 text-white shadow-lg shadow-blue-600/30 ring-2 ring-blue-400 scale-105'
                    : 'bg-slate-900/60 dark:bg-slate-900/60 light:bg-slate-100 text-slate-300 dark:text-slate-300 light:text-slate-700 border border-slate-700 dark:border-slate-700 light:border-slate-300 hover:border-blue-500/50 hover:bg-slate-800'
                }`}
              >
                <span>{t.emoji}</span>
                <span>{t.label}</span>
              </button>
            );
          })}
        </div>
      </div>

    </div>
  );
}
