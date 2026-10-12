import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import rateLimit from 'express-rate-limit';
import captionRoutes from './routes/captionRoutes.js';
import { errorHandler } from './middleware/errorHandler.js';

// Load environment variables
dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;

// CORS setup
const allowedOrigins = process.env.CORS_ORIGIN 
  ? process.env.CORS_ORIGIN.split(',') 
  : ['http://localhost:5173', 'http://localhost:3000', 'http://127.0.0.1:5173'];

app.use(cors({
  origin: function (origin, callback) {
    // Allow requests with no origin (like mobile apps or curl)
    if (!origin) return callback(null, true);
    if (allowedOrigins.indexOf(origin) !== -1 || process.env.NODE_ENV !== 'production') {
      return callback(null, true);
    }
    return callback(new Error('CORS policy error: Origin not allowed.'));
  },
  credentials: true
}));

// Body parser
app.use(express.json({ limit: '60mb' }));
app.use(express.urlencoded({ extended: true, limit: '60mb' }));

// Basic rate limiting (100 requests per 15 minutes)
const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100,
  message: {
    success: false,
    error: 'Too many requests from this IP. Please try again after 15 minutes.'
  },
  standardHeaders: true,
  legacyHeaders: false,
});

app.use('/api/', apiLimiter);

// Register routes
app.use('/api', captionRoutes);

// Root route
app.get('/', (req, res) => {
  res.json({
    message: 'Welcome to VisionSpeak AI Backend API',
    endpoints: {
      health: 'GET /api/health',
      generateCaptions: 'POST /api/generate-captions'
    }
  });
});

// Register central error handler
app.use(errorHandler);

// Start server
app.listen(PORT, () => {
  console.log(`=================================================`);
  console.log(`🚀 VisionSpeak AI Backend running on port ${PORT}`);
  console.log(`🌐 API Endpoint: http://localhost:${PORT}/api/generate-captions`);
  console.log('🔒 Offline caption mode: no API key required.');
  console.log(`=================================================`);
});
