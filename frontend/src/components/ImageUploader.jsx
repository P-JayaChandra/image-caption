import React, { useState, useRef } from 'react';
import { UploadCloud, Image as ImageIcon, Trash2, RefreshCw, AlertCircle, FileCheck, Sparkles } from 'lucide-react';
import { useToast } from '../context/ToastContext';

export default function ImageUploader({
  selectedFile,
  previewUrl,
  onImageSelect,
  onImageRemove,
  onGenerateClick,
  isLoading,
}) {
  const { showToast } = useToast();
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef(null);

  const ALLOWED_TYPES = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp'];
  const MAX_SIZE_BYTES = 50 * 1024 * 1024; // 50MB

  const validateAndHandleFile = (file) => {
    if (!file) return;

    // Validate type
    if (!ALLOWED_TYPES.includes(file.type.toLowerCase())) {
      showToast('Invalid file format. Please upload a JPG, JPEG, PNG, or WEBP image.', 'error');
      return;
    }

    // Validate size
    if (file.size > MAX_SIZE_BYTES) {
      showToast(`File size is too large (${(file.size / (1024 * 1024)).toFixed(1)} MB). Maximum limit is 50 MB.`, 'error');
      return;
    }

    onImageSelect(file);
    showToast('Image uploaded successfully! Ready for AI analysis.', 'success');
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      validateAndHandleFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      validateAndHandleFile(e.target.files[0]);
    }
  };

  return (
    <div className="w-full max-w-3xl mx-auto">
      {/* Hidden File Input */}
      <input
        type="file"
        ref={fileInputRef}
        onChange={handleFileChange}
        accept="image/jpeg,image/png,image/webp,image/jpg"
        className="hidden"
      />

      {!previewUrl ? (
        /* Drag & Drop Upload Dropzone */
        <div
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current?.click()}
          className={`relative border-2 border-dashed rounded-3xl p-8 sm:p-12 text-center cursor-pointer transition-all duration-300 glass-card glass-card-hover ${
            isDragging
              ? 'border-purple-500 bg-purple-500/10 scale-[1.01]'
              : 'border-slate-700 dark:border-slate-700 light:border-slate-300 hover:border-purple-500/60'
          }`}
        >
          <div className="flex flex-col items-center justify-center max-w-md mx-auto">
            {/* Animated Upload Icon */}
            <div className="w-20 h-20 rounded-3xl bg-purple-600/15 border border-purple-500/30 flex items-center justify-center mb-6 shadow-inner group-hover:scale-110 transition-transform duration-300">
              <UploadCloud className="w-10 h-10 text-purple-400 group-hover:animate-bounce" />
            </div>

            <h3 className="text-xl font-bold text-white dark:text-white light:text-slate-900 mb-2">
              Drag & Drop your image here
            </h3>
            <p className="text-sm text-slate-400 dark:text-slate-400 light:text-slate-600 mb-6">
              or browse from your device. AI will analyze details, scenery, mood, and objects.
            </p>

            {/* Choose Image Button */}
            <button
              type="button"
              onClick={(e) => {
                e.stopPropagation();
                fileInputRef.current?.click();
              }}
              className="gradient-btn px-6 py-3 rounded-2xl text-sm font-bold text-white flex items-center gap-2"
            >
              <ImageIcon className="w-4 h-4" />
              <span>Choose Image</span>
            </button>

            {/* Supported Formats Info */}
            <div className="mt-6 flex flex-wrap items-center justify-center gap-2 text-xs text-slate-400">
              <span className="px-2.5 py-1 rounded-full bg-slate-800/80 dark:bg-slate-800/80 light:bg-slate-200 border border-slate-700">
                JPG / JPEG
              </span>
              <span className="px-2.5 py-1 rounded-full bg-slate-800/80 dark:bg-slate-800/80 light:bg-slate-200 border border-slate-700">
                PNG
              </span>
              <span className="px-2.5 py-1 rounded-full bg-slate-800/80 dark:bg-slate-800/80 light:bg-slate-200 border border-slate-700">
                WEBP
              </span>
              <span className="text-slate-400 ml-1">Up to 50 MB</span>
            </div>
          </div>
        </div>
      ) : (
        /* Image Preview State */
        <div className="glass-card rounded-3xl p-6 sm:p-8 animate-fade-in border border-purple-500/20">
          <div className="flex flex-col md:flex-row items-center gap-8">
            
            {/* Left Preview Image Frame with Scan Beam Overlay when loading */}
            <div className="relative w-full md:w-64 h-64 rounded-2xl overflow-hidden bg-slate-900 border border-white/10 shadow-2xl shrink-0 group">
              <img
                src={previewUrl}
                alt="Uploaded preview"
                className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
              />
              
              {/* Neural Vision Scan Animation when loading */}
              {isLoading && (
                <div className="absolute inset-0 bg-purple-950/40 backdrop-blur-[2px] flex flex-col items-center justify-center">
                  <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-purple-500 via-blue-400 to-purple-500 shadow-[0_0_15px_#7C3AED] animate-pulse-scan" />
                  <div className="relative flex flex-col items-center">
                    <div className="w-12 h-12 rounded-full border-2 border-purple-400 border-t-transparent animate-spin mb-3" />
                    <span className="text-xs font-bold text-purple-200 bg-black/60 px-3 py-1 rounded-full border border-purple-500/40">
                      Analyzing pixels...
                    </span>
                  </div>
                </div>
              )}
            </div>

            {/* Right File Info & Action Buttons */}
            <div className="flex-1 w-full flex flex-col justify-between h-full space-y-6">
              <div>
                <div className="flex items-center gap-2 mb-2">
                  <FileCheck className="w-5 h-5 text-emerald-400" />
                  <h4 className="text-lg font-bold text-white dark:text-white light:text-slate-900 truncate">
                    {selectedFile?.name || 'Uploaded Image'}
                  </h4>
                </div>
                <div className="flex flex-wrap items-center gap-3 text-xs text-slate-400 mb-4">
                  <span className="px-3 py-1 rounded-lg bg-slate-800 dark:bg-slate-800 light:bg-slate-200">
                    Size: {selectedFile ? (selectedFile.size / (1024 * 1024)).toFixed(2) : '0'} MB
                  </span>
                  <span className="px-3 py-1 rounded-lg bg-slate-800 dark:bg-slate-800 light:bg-slate-200 uppercase">
                    Format: {selectedFile?.type.split('/')[1] || 'IMAGE'}
                  </span>
                </div>
                <p className="text-xs text-slate-400 leading-relaxed">
                  Image loaded and ready for computer vision analysis. Select your preferred category and tone below, then click Generate Captions.
                </p>
              </div>

              {/* Action Buttons */}
              <div className="flex flex-wrap items-center gap-3 pt-4 border-t border-white/10">
                <button
                  type="button"
                  onClick={() => fileInputRef.current?.click()}
                  disabled={isLoading}
                  className="flex items-center gap-2 px-4 py-2.5 rounded-xl text-xs font-semibold bg-slate-800/80 hover:bg-slate-700 text-slate-300 border border-slate-700 transition-all"
                >
                  <RefreshCw className="w-3.5 h-3.5" />
                  <span>Replace Image</span>
                </button>

                <button
                  type="button"
                  onClick={onImageRemove}
                  disabled={isLoading}
                  className="flex items-center gap-2 px-4 py-2.5 rounded-xl text-xs font-semibold bg-rose-500/10 hover:bg-rose-500/20 text-rose-300 border border-rose-500/30 transition-all"
                >
                  <Trash2 className="w-3.5 h-3.5" />
                  <span>Remove</span>
                </button>
              </div>

            </div>

          </div>
        </div>
      )}
    </div>
  );
}
