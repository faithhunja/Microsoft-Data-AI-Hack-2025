import { useDropzone } from 'react-dropzone';
import { Paper, Button, Typography, Box, CircularProgress } from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import { useState } from 'react';

// Define or import processP9
const processP9 = async (file: File) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({ message: "P9 form processed successfully!" });
    }, 2000);
  });
};

export const FileUpload = ({ onFileProcessed }: { onFileProcessed: (data: any) => void }) => {
  const [isProcessing, setIsProcessing] = useState(false);

  const onDrop = async (acceptedFiles: File[]) => {
    setIsProcessing(true);
    try {
      const extractedData = await processP9(acceptedFiles[0]); // Ensure processP9 is defined
      onFileProcessed(extractedData);
    } finally {
      setIsProcessing(false);
    }
  };

  const { getRootProps, getInputProps } = useDropzone({
    onDrop,
    accept: { 'application/pdf': ['.pdf'], 'image/*': ['.jpg', '.jpeg', '.png'] },
    maxFiles: 1
  });

  return (
    <Paper elevation={3} sx={{ p: 4, textAlign: 'center', cursor: 'pointer' }} {...getRootProps()}>
      <input {...getInputProps()} />
      {isProcessing ? (
        <Box>
          <CircularProgress size={60} />
          <Typography mt={2}>Processing your P9 form...</Typography>
        </Box>
      ) : (
        <>
          <CloudUploadIcon sx={{ fontSize: 60, color: '#1976d2' }} />
          <Typography variant="h6" gutterBottom>
            Drag & drop your P9 form here
          </Typography>
          <Typography color="text.secondary" sx={{ mb: 2 }}>
            Supported formats: PDF, JPG, PNG
          </Typography>
          <Button variant="contained" size="large">
            Browse Files
          </Button>
        </>
      )}
    </Paper>
  );
};
