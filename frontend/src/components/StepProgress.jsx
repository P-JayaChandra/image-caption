import React from 'react';
import { Upload, Scan, MessageSquareQuote, Check } from 'lucide-react';

export default function StepProgress({ currentStep = 1 }) {
  const steps = [
    { number: 1, label: 'Upload', desc: 'Drag or select image', icon: Upload },
    { number: 2, label: 'Analyze', desc: 'AI Vision scene scan', icon: Scan },
    { number: 3, label: 'Get Captions', desc: '3 Unique Instagram styles', icon: MessageSquareQuote },
  ];

  return (
    <div className="w-full max-w-3xl mx-auto mb-10 px-4">
      <div className="relative flex items-center justify-between">
        
        {/* Background Connecting Line */}
        <div className="absolute top-1/2 left-8 right-8 -translate-y-1/2 h-1 bg-slate-800 dark:bg-slate-800 light:bg-slate-200 -z-10 rounded-full overflow-hidden">
          <div 
            className="h-full bg-gradient-to-r from-purple-600 to-blue-500 transition-all duration-500"
            style={{
              width: currentStep === 1 ? '0%' : currentStep === 2 ? '50%' : '100%'
            }}
          />
        </div>

        {/* Step Items */}
        {steps.map((step) => {
          const Icon = step.icon;
          const isCompleted = currentStep > step.number;
          const isActive = currentStep === step.number;

          return (
            <div key={step.number} className="flex flex-col items-center group">
              {/* Step Circle */}
              <div
                className={`w-12 h-12 rounded-2xl flex items-center justify-center font-bold transition-all duration-300 ${
                  isCompleted
                    ? 'bg-emerald-500 text-white shadow-lg shadow-emerald-500/25 scale-105'
                    : isActive
                    ? 'gradient-btn text-white scale-110 ring-4 ring-purple-500/30 shadow-xl shadow-purple-500/30'
                    : 'bg-slate-900 dark:bg-slate-900 light:bg-white text-slate-500 border border-slate-700 dark:border-slate-700 light:border-slate-300'
                }`}
              >
                {isCompleted ? (
                  <Check className="w-6 h-6 stroke-[3]" />
                ) : (
                  <Icon className="w-5 h-5" />
                )}
              </div>

              {/* Labels */}
              <div className="text-center mt-2">
                <span
                  className={`block text-xs font-bold transition-colors ${
                    isActive || isCompleted
                      ? 'text-purple-300 dark:text-purple-300 light:text-purple-700'
                      : 'text-slate-400 dark:text-slate-400 light:text-slate-500'
                  }`}
                >
                  Step {step.number}: {step.label}
                </span>
                <span className="hidden sm:block text-[11px] text-slate-400 dark:text-slate-400 light:text-slate-500 font-medium mt-0.5">
                  {step.desc}
                </span>
              </div>
            </div>
          );
        })}

      </div>
    </div>
  );
}
