import express from 'express';
import { uploadImage } from '../middleware/uploadMiddleware.js';
import { generateCaptions } from '../controllers/captionController.js';

const router = express.Router();

// POST /api/generate-captions - Generate local offline caption suggestions
router.post('/generate-captions', uploadImage.single('image'), generateCaptions);

// GET /api/health - Health check endpoint
router.get('/health', (req, res) => {
  res.status(200).json({
    status: 'ok',
    service: 'VisionSpeak AI Backend',
    timestamp: new Date().toISOString(),
    mode: 'offline',
    offlineMode: true
  });
});

export default router;
