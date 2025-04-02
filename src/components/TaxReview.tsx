import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Button, Typography, Box } from '@mui/material';
import DownloadIcon from '@mui/icons-material/Download';

export const DataReview = ({ taxData }: { taxData: any }) => {
  const exportToExcel = () => {
    // Implement Excel export using xlsx
    console.log('Exporting to Excel...', taxData);
  };

  return (
    <Paper elevation={3} sx={{ p: 3 }}>
      <Typography variant="h6" gutterBottom sx={{ mb: 3 }}>
        Review Extracted Tax Data
      </Typography>
      
      <TableContainer component={Paper}>
        <Table>
          <TableHead sx={{ bgcolor: '#f5f5f5' }}>
            <TableRow>
              <TableCell>Field</TableCell>
              <TableCell align="right">Amount (KES)</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {Object.entries(taxData).map(([key, value]) => (
              <TableRow key={key}>
                <TableCell>{key}</TableCell>
                <TableCell align="right">{value as React.ReactNode}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <Box sx={{ mt: 3, display: 'flex', justifyContent: 'flex-end' }}>
        <Button 
          variant="contained" 
          startIcon={<DownloadIcon />}
          onClick={exportToExcel}
          sx={{ mr: 2 }}
        >
          Download Excel
        </Button>
        <Button variant="contained" color="success">
          Submit to KRA
        </Button>
      </Box>
    </Paper>
  );
};