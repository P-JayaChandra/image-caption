const HISTORY_KEY = 'visionspeak_history';

/**
 * Get all history items from localStorage
 */
export function getHistory() {
  try {
    const data = localStorage.getItem(HISTORY_KEY);
    return data ? JSON.parse(data) : [];
  } catch (e) {
    console.error('Failed to load history:', e);
    return [];
  }
}

/**
 * Save a new generation result to history
 * @param {Object} item - { id, timestamp, filename, category, tone, analysis, captions, imagePreview }
 */
export function saveToHistory(item) {
  try {
    const history = getHistory();
    // Prepare item, optionally saving lightweight thumbnail or metadata
    const newItem = {
      id: item.id || Date.now().toString(),
      timestamp: new Date().toISOString(),
      filename: item.filename || 'uploaded-image.jpg',
      category: item.category || 'Other',
      tone: item.tone || 'Aesthetic',
      analysis: item.analysis,
      captions: item.captions,
      // Store preview if under reasonable length (to avoid quota overflow)
      imagePreview: item.imagePreview && item.imagePreview.length < 300000 ? item.imagePreview : null
    };

    const updated = [newItem, ...history].slice(0, 30); // Keep last 30 entries
    localStorage.setItem(HISTORY_KEY, JSON.stringify(updated));
    return updated;
  } catch (e) {
    console.error('Failed to save to history:', e);
    return getHistory();
  }
}

/**
 * Clear all history
 */
export function clearHistory() {
  try {
    localStorage.removeItem(HISTORY_KEY);
    return [];
  } catch (e) {
    console.error('Failed to clear history:', e);
    return [];
  }
}

/**
 * Delete a specific history item
 */
export function deleteHistoryItem(id) {
  try {
    const history = getHistory();
    const updated = history.filter(item => item.id !== id);
    localStorage.setItem(HISTORY_KEY, JSON.stringify(updated));
    return updated;
  } catch (e) {
    console.error('Failed to delete history item:', e);
    return getHistory();
  }
}

