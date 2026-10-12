export function errorHandler(err, req, res, next) {
  console.error('[Backend Error]:', err.message);

  if (err.code === 'LIMIT_FILE_SIZE') {
    return res.status(413).json({
      success: false,
      error: 'File size too large. Maximum permitted size is 10 MB.'
    });
  }

  return res.status(err.status || 500).json({
    success: false,
    error: err.message || 'An unexpected internal server error occurred.'
  });
}
