import { Alert, Box, Button, Container } from '@mui/material';
import { ProgressStepper } from '../components/ProgressStepper';

export const SubmitPage = () => {
  return (
    <Container maxWidth="md">
      <ProgressStepper activeStep={2} />
      
      <Box mt={4}>
        <Alert severity="success" sx={{ mb: 3 }}>
          Your tax data has been successfully prepared!
        </Alert>
        
        <Button variant="contained" fullWidth size="large">
          Submit to KRA iTax
        </Button>
      </Box>
    </Container>
  );
};