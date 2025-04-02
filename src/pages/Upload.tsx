import { useState } from 'react';
import { Container, Box } from '@mui/material';
import { Navbar } from '../components/Navbar';
import { ProgressStepper } from '../components/ProgressStepper';
import { FileUpload } from '../components/FileUpload';
import { DataReview } from '../components/TaxReview';

export const UploadPage = () => {
  const [taxData, setTaxData] = useState<any>(null);
  const [activeStep, setActiveStep] = useState(0);

  const handleFileProcessed = (data: any) => {
    setTaxData(data);
    setActiveStep(1);
  };

  return (
    <>
      <Navbar />
      <Container maxWidth="md" sx={{ mt: 4, mb: 6 }}>
        <ProgressStepper activeStep={taxData ? 1 : 0} />
        
        {!taxData ? (
          <FileUpload onFileProcessed={handleFileProcessed} />
        ) : (
          <DataReview taxData={taxData} />
        )}
      </Container>
    </>
  );
};