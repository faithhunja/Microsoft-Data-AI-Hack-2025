import { Button, Container, Typography, Stack } from '@mui/material';
import { useNavigate } from 'react-router-dom';

export const HomePage = () => {
  const navigate = useNavigate();

  return (
    <Container maxWidth="md">
      <Stack spacing={4} alignItems="center" textAlign="center" py={8}>
        <Typography variant="h3" gutterBottom>
          KRA Tax Automation Portal
        </Typography>
        <Typography color="text.secondary" paragraph>
          Upload your P9 form and we'll automatically prepare your KRA tax return
        </Typography>
        <Button 
          variant="contained" 
          size="large"
          onClick={() => navigate('/upload')}
        >
          Start Now
        </Button>
      </Stack>
    </Container>
  );
};