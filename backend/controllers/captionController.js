import { analyzeImageAndGenerateCaptions } from '../services/aiVisionService.js';

/**
 * Controller to handle POST /api/generate-captions
 */
export async function generateCaptions(req, res, next) {
  try {
    // 1. Validate file presence
    if (!req.file) {
      return res.status(400).json({
        success: false,
        error: 'No image file uploaded. Please upload a valid JPG, JPEG, PNG, or WEBP image.'
      });
    }

    // 2. Extract options from request body and headers
    const category = req.body.category || 'Other';
    const tone = req.body.tone || 'Aesthetic';

    console.log(`[Caption Controller] Processing image: ${req.file.originalname} (${req.file.size} bytes), Category: ${category}, Tone: ${tone}`);

    // 3. Analyze image using AI Vision Service
    const result = await analyzeImageAndGenerateCaptions(
      req.file.buffer,
      req.file.mimetype,
      { category, tone, originalname: req.file.originalname }
    );

    // 4. Return success response
    return res.status(200).json({
      success: true,
      filename: req.file.originalname,
      fileSize: req.file.size,
      mimeType: req.file.mimetype,
      category,
      tone,
      analysis: result.analysis,
      captions: result.captions,
      isRealAi: result.isRealAi,
      notice: result.notice || null
    });

  } catch (error) {
    console.error('[Caption Controller Error]:', error);
    return next(error);
  }
}
