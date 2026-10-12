import React from 'react';
import { Eye, Sparkles, Instagram, Flame } from 'lucide-react';

export default function HeroSection() {
  const featureBadges = [
    { label: 'AI Image Analysis', icon: Eye, color: 'text-purple-400 border-purple-500/30 bg-purple-500/10' },
    { label: 'Smart Captions', icon: Sparkles, color: 'text-blue-400 border-blue-500/30 bg-blue-500/10' },
    { label: 'Instagram Ready', icon: Instagram, color: 'text-pink-400 border-pink-500/30 bg-pink-500/10' },
  ];

  return (
    <section className="relative text-center py-10 md:py-14 max-w-4xl mx-auto px-4">
      {/* Top Trending Badge */}
      <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-purple-950/60 dark:bg-purple-950/60 light:bg-purple-50 border border-purple-500/30 text-purple-300 dark:text-purple-300 light:text-purple-700 text-xs font-semibold mb-6 shadow-lg shadow-purple-500/10 animate-fade-in">
        <Flame className="w-4 h-4 text-purple-400 animate-bounce" />
        <span>Powered by Multimodal AI Vision Technology</span>
      </div>

      {/* Main Title */}
      <h1 className="text-3xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight text-white dark:text-white light:text-slate-900 leading-[1.15] mb-6">
        Turn Your Photos into{' '}
        <span className="gradient-text">Perfect Instagram Captions</span>
      </h1>

      {/* Subtitle */}
      <p className="text-base sm:text-lg md:text-xl text-slate-300 dark:text-slate-300 light:text-slate-600 max-w-2xl mx-auto leading-relaxed mb-8">
        Upload your image and let AI understand the scene, capture the mood, and create captions that tell your story.
      </p>

      {/* Feature Badges */}
      <div className="flex flex-wrap items-center justify-center gap-3 max-w-xl mx-auto">
        {featureBadges.map((badge, idx) => {
          const Icon = badge.icon;
          return (
            <div
              key={idx}
              className={`flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs sm:text-sm font-semibold border backdrop-blur-md transition-all duration-300 hover:scale-105 ${badge.color}`}
            >
              <Icon className="w-4 h-4" />
              <span>{badge.label}</span>
            </div>
          );
        })}
      </div>
    </section>
  );
}
