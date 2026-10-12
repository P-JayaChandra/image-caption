import crypto from 'crypto';

/**
 * Offline caption engine.
 * This module does not call an external AI provider and never needs an API key.
 * It uses the uploaded file's fingerprint plus the user's category/tone choices
 * to produce repeatable, locally generated caption suggestions.
 *
 * Note: without a local vision model, this does not identify objects in pixels.
 */
export async function analyzeImageAndGenerateCaptions(imageBuffer, mimeType, options = {}) {
  const { category = 'Other', tone = 'Aesthetic', originalname = 'image.jpg' } = options;
  const safeCategory = categoryNames[category] ? category : 'Other';
  const safeTone = tonePhrases[tone] ? tone : 'Aesthetic';
  const hash = crypto.createHash('sha256').update(imageBuffer).digest('hex');
  const fileLabel = String(originalname).replace(/\.[^/.]+$/, '').replace(/[-_]+/g, ' ').trim() || 'this moment';
  const categoryData = categoryNames[safeCategory];
  const phrases = tonePhrases[safeTone];
  const offset = parseInt(hash.slice(0, 8), 16) % phrases.length;
  const tags = [...categoryData.tags, `Frame${hash.slice(0, 4)}`, 'VisionSpeak'];
  const captionStyles = ['Aesthetic', 'Emotional', 'Creative / Trending'];

  const captions = captionStyles.map((style, index) => {
    const phrase = phrases[(offset + index) % phrases.length];
    const cleanTag = fileLabel.replace(/[^a-zA-Z0-9]/g, '').slice(0, 18);
    return {
      id: index + 1,
      style,
      text: `${phrase}${index === 0 ? ' ✨📸' : index === 1 ? ' 🤍🌿' : ' ⚡💫'}`,
      hashtags: [
        `#${categoryData.hashtag}`,
        `#${safeTone.replace(/[^a-zA-Z0-9]/g, '')}`,
        cleanTag ? `#${cleanTag}` : '#PhotoMoment',
        '#VisionSpeak',
        '#CapturedMoments'
      ]
    };
  });

  return {
    success: true,
    isRealAi: false,
    mode: 'offline',
    notice: 'Offline mode: captions are generated locally from your selected category, tone, and file fingerprint. No API key or external AI service is used.',
    analysis: {
      description: `Local caption suggestions for "${fileLabel}". Category: ${safeCategory}. Tone: ${safeTone}. The offline engine does not claim to recognize objects or scenes in the image.`,
      tags: [...new Set(tags)]
    },
    captions,
    metadata: {
      mimeType: String(mimeType || 'application/octet-stream'),
      imageSizeBytes: imageBuffer.length,
      fingerprint: hash.slice(0, 16)
    }
  };
}

const categoryNames = {
  Nature: { hashtag: 'Nature', tags: ['Nature', 'Outdoors', 'NaturalLight', 'ScenicMoments'] },
  People: { hashtag: 'People', tags: ['Portrait', 'People', 'EverydayMoments', 'Expressions'] },
  Travel: { hashtag: 'Travel', tags: ['TravelDiary', 'Wanderlust', 'ExploreMore', 'TravelMoments'] },
  Food: { hashtag: 'Food', tags: ['Foodie', 'FoodPhotography', 'TasteAndTell', 'FoodMoments'] },
  Other: { hashtag: 'Photography', tags: ['Photography', 'VisualStory', 'DailyMoments', 'CreativeFrame'] }
};

const tonePhrases = {
  Aesthetic: [
    'Finding beauty in the little details',
    'A quiet frame, a lasting feeling',
    'Collecting moments in their own colors',
    'A little pause in a busy world'
  ],
  Funny: [
    'Proof that my camera roll has a personality',
    'Posted before I could overthink it',
    'The moment understood the assignment',
    'Casually adding this to the highlight reel'
  ],
  Emotional: [
    'Some moments stay with us long after they pass',
    'A little memory to keep close',
    'The simplest moments often mean the most',
    'Keeping this feeling for another day'
  ],
  Professional: [
    'A considered frame with a clear point of view',
    'Thoughtful details, intentional storytelling',
    'A study in perspective and composition',
    'Simple visuals, meaningful impact'
  ],
  Romantic: [
    'Soft moments and a little bit of magic',
    'A memory wrapped in warmth',
    'The kind of moment that makes you pause',
    'A little sweetness in the everyday'
  ],
  Attitude: [
    'Showing up in my own way',
    'No extra noise, just my energy',
    'On my own wavelength',
    'Making this moment count'
  ],
  Minimalist: [
    'Less noise, more meaning',
    'Keeping it simple',
    'Just this moment',
    'Nothing extra needed'
  ]
};
