// services/ocrService.ts
export const extractP9Data = async (file: File) => {
    // In production: Replace with Azure Document Intelligence API
    return {
      grossSalary: 1200000,
      paye: 240000,
      nhif: 12000,
      nssf: 1080,
      // ...other fields
    };
  };