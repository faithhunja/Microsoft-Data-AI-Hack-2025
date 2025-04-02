import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { CssBaseline, Box } from '@mui/material';
import { Navbar } from './components/Navbar';
import { HomePage } from './pages/Home';
import { UploadPage } from './pages/Upload';
import { SubmitPage } from './pages/Submission';
import { NotFoundPage } from './pages/NotFound';

function App() {
  return (
    <BrowserRouter>
      <CssBaseline />
      <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
        {/* Navbar appears on all pages */}
        <Navbar />
        
        {/* Main content area with router */}
        <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/upload" element={<UploadPage />} />
            <Route path="/submit" element={<SubmitPage />} />
            <Route path="*" element={<NotFoundPage />} />
          </Routes>
        </Box>

        {/* Footer can be added here */}
      </Box>
    </BrowserRouter>
  );
}

export default App;