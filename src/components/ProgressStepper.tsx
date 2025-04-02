import { Stepper, Step, StepLabel, Box } from '@mui/material';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';

const steps = ['Upload P9', 'Review Data', 'Submit to KRA'];

export const ProgressStepper = ({ activeStep }: { activeStep: number }) => {
  return (
    <Box sx={{ width: '100%', mb: 4 }}>
      <Stepper activeStep={activeStep} alternativeLabel>
        {steps.map((label, index) => (
          <Step key={label}>
            <StepLabel
              icon={index < activeStep ? <CheckCircleIcon color="primary" /> : undefined} // ✅ Use `icon` prop instead
            >
              {label}
            </StepLabel>
          </Step>
        ))}
      </Stepper>
    </Box>
  );
};
