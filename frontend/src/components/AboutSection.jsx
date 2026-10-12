import React from 'react';
import { Eye, Cpu, ShieldCheck, Zap, Layers, Sparkles, CheckCircle2 } from 'lucide-react';

export default function AboutSection() {
  const steps = [
    {
      title: '1. Multimodal Pixel Analysis',
      desc: 'When you upload an image, VisionSpeak AI passes raw pixel matrices into a vision-language model. The AI scans subjects, backgrounds, lighting, color spectrums, and visible emotions.',
      icon: Eye
    },
    {
      title: '2. Scene Context & Mood Extraction',
      desc: 'Instead of relying on basic file tags, computer vision extracts environmental atmosphere, photography techniques, and spatial relationship between objects.',
      icon: Cpu
    },
    {
      title: '3. 3-Style Instagram Generation',
      desc: 'The model generates 3 distinct Instagram caption styles: Aesthetic (descriptive beauty), Emotional (relatable story), and Creative/Trending (catchy hook & hashtags).',
      icon: Sparkles
    }
  ];

  return (
    <div className="w-full max-w-4xl mx-auto py-6 px-4 animate-fade-in space-y-12">
      
      {/* Title Header */}
      <div className="text-center max-w-2xl mx-auto">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-purple-500/10 border border-purple-500/30 text-purple-300 text-xs font-semibold mb-4">
          <Zap className="w-4 h-4 text-purple-400" />
          <span>About VisionSpeak AI</span>
        </div>
        <h2 className="text-3xl sm:text-4xl font-extrabold text-white dark:text-white light:text-slate-900 mb-4">
          How VisionSpeak AI Works
        </h2>
        <p className="text-sm sm:text-base text-slate-300 dark:text-slate-300 light:text-slate-600 leading-relaxed">
          VisionSpeak AI bridges advanced computer vision and social media storytelling. It analyzes actual image content in real time to generate captions that genuinely reflect your photos.
        </p>
      </div>

      {/* 3 Step Explanation Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {steps.map((step, idx) => {
          const Icon = step.icon;
          return (
            <div key={idx} className="glass-card rounded-3xl p-6 border border-white/10 relative overflow-hidden group hover:border-purple-500/30 transition-all">
              <div className="w-12 h-12 rounded-2xl bg-purple-600/20 border border-purple-500/30 flex items-center justify-center mb-4 text-purple-400 group-hover:scale-110 transition-transform">
                <Icon className="w-6 h-6" />
              </div>
              <h3 className="text-base font-bold text-white mb-2">{step.title}</h3>
              <p className="text-xs text-slate-400 leading-relaxed">{step.desc}</p>
            </div>
          );
        })}
      </div>

      {/* Feature Highlights */}
      <div className="glass-card rounded-3xl p-8 border border-white/10 space-y-6">
        <h3 className="text-xl font-bold text-white flex items-center gap-2">
          <Layers className="w-5 h-5 text-purple-400" />
          <span>Core Capabilities & Standards</span>
        </h3>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div className="flex items-start gap-3 p-4 rounded-2xl bg-slate-900/60 border border-white/5">
            <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0 mt-0.5" />
            <div>
              <h4 className="text-sm font-bold text-white">Genuine Pixel Understanding</h4>
              <p className="text-xs text-slate-400 mt-1">
                Analyzes people, animals, background scenery, lighting, and composition independently per upload.
              </p>
            </div>
          </div>

          <div className="flex items-start gap-3 p-4 rounded-2xl bg-slate-900/60 border border-white/5">
            <ShieldCheck className="w-5 h-5 text-blue-400 shrink-0 mt-0.5" />
            <div>
              <h4 className="text-sm font-bold text-white">Privacy First Memory Storage</h4>
              <p className="text-xs text-slate-400 mt-1">
                Uploaded images are processed directly in memory buffer and never permanently saved to server disk.
              </p>
            </div>
          </div>

          <div className="flex items-start gap-3 p-4 rounded-2xl bg-slate-900/60 border border-white/5">
            <CheckCircle2 className="w-5 h-5 text-purple-400 shrink-0 mt-0.5" />
            <div>
              <h4 className="text-sm font-bold text-white">Interactive Audio TTS & Copying</h4>
              <p className="text-xs text-slate-400 mt-1">
                Preview your captions with text-to-speech audio playback or copy complete text + hashtags in one click.
              </p>
            </div>
          </div>

          <div className="flex items-start gap-3 p-4 rounded-2xl bg-slate-900/60 border border-white/5">
            <CheckCircle2 className="w-5 h-5 text-amber-400 shrink-0 mt-0.5" />
            <div>
              <h4 className="text-sm font-bold text-white">100% Offline Local Architecture</h4>
              <p className="text-xs text-slate-400 mt-1">
                Powered by local Salesforce BLIP neural vision model and deterministic heuristics with zero API keys and zero cloud calls.
              </p>
            </div>
          </div>
        </div>
      </div>

    </div>
  );
}
