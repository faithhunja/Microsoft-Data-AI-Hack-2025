import { AppBar, Toolbar, Typography, Box } from '@mui/material';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';

export const Navbar = () => {
  return (
    <AppBar position="static" elevation={0} sx={{ bgcolor: '#FF0000' }}>
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          KRA Tax Automation
        </Typography>
        <Box display="flex" alignItems="center">
          <AccountCircleIcon sx={{ mr: 1 }} />
          <Typography>Welcome, User</Typography>
        </Box>
      </Toolbar>
    </AppBar>
  );
};