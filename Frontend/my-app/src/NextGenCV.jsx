import React, { useState } from 'react';

const NextGenCV = () => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [enhancedText, setEnhancedText] = useState('');
  const [error, setError] = useState('');

  // Get API URLs from environment variables with fallbacks
  const getApiUrl = (service, port, path) => {
    // Try environment variables first
    const envUrl = process.env[`REACT_APP_${service.toUpperCase()}_URL`];
    if (envUrl) return `${envUrl}${path}`;
    
    // Fallback to Docker service names or localhost
    const host = process.env.NODE_ENV === 'production' 
      ? service.toLowerCase() 
      : '127.0.0.1';
    
    return `http://${host}:${port}${path}`;
  };

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      alert('Please select a file first.');
      return;
    }

    setLoading(true);
    setError('');
    setEnhancedText('');

    try {
      const formData = new FormData();
      formData.append('file', file);

      // Use dynamic URL based on environment
      const uploadUrl = getApiUrl('UPLOAD', '80', '/upload');
      
      const uploadResponse = await fetch(uploadUrl, {
        method: 'POST',
        body: formData,
      });

      if (!uploadResponse.ok) {
        throw new Error(`Upload service failed with status: ${uploadResponse.status}`);
      }

      const uploadData = await uploadResponse.json();
      const enhanced = uploadData.forward_response?.enhanced_text || uploadData.enhanced_text;

      if (!enhanced) {
        throw new Error('No enhanced text returned from service.');
      }
      
      setEnhancedText(enhanced);

    } catch (err) {
      console.error('Upload error:', err);
      setError(err.message || 'Unexpected error during upload.');
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = async () => {
    if (!enhancedText) {
      alert('No enhanced text available for download.');
      return;
    }

    try {
      setLoading(true);
      
      // Use dynamic URL for PDF service
      const pdfUrl = getApiUrl('PDF', '80', '/pdf');
      
      const response = await fetch(pdfUrl, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Accept': 'application/pdf'
        },
        body: JSON.stringify({
          text: enhancedText,
        }),
      });

      if (!response.ok) {
        throw new Error(`Failed to generate PDF. Status: ${response.status}`);
      }

      const blob = await response.blob();
      const link = document.createElement('a');
      link.href = window.URL.createObjectURL(blob);
      link.download = `enhanced_resume_${new Date().getTime()}.pdf`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(link.href);

      alert('✅ PDF Downloaded Successfully!');
    } catch (err) {
      console.error('Error during PDF download:', err);
      setError(`PDF generation failed: ${err.message}`);
      alert('Failed to download PDF. Please check the console for details.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h1 style={styles.heading}>NextGenCV</h1>
        <p style={styles.subtitle}>Resume Upload and Enhancement</p>
      </div>

      <div style={styles.card}>
        <div style={styles.uploadSection}>
          <div style={styles.fileInputContainer}>
            <input
              type="file"
              accept=".pdf,.docx,.txt"
              onChange={handleFileChange}
              style={styles.fileInput}
            />
            {file && (
              <p style={styles.fileName}>Selected: {file.name}</p>
            )}
          </div>
          <button 
            onClick={handleUpload}
            style={styles.primaryButton}
            disabled={loading || !file}
          >
            {loading ? 'Processing...' : 'Upload and Process'}
          </button>
        </div>

        {enhancedText && (
          <div style={styles.downloadSection}>
            <button 
              onClick={handleDownload} 
              style={styles.secondaryButton}
              disabled={loading}
            >
              📄 Download Enhanced Resume (PDF)
            </button>
          </div>
        )}

        {loading && (
          <div style={styles.loading}>
            <div style={styles.spinner}></div>
            <p>Processing your resume, please wait...</p>
          </div>
        )}

        {error && (
          <div style={styles.error}>
            <strong>Error:</strong> {error}
          </div>
        )}

        {enhancedText && !loading && (
          <div style={styles.resultSection}>
            <h2 style={styles.resultTitle}>Enhanced Resume Preview:</h2>
            <div style={styles.enhancedResult}>
              <pre style={styles.enhancedText}>{enhancedText}</pre>
            </div>
          </div>
        )}
      </div>

      <div style={styles.footer}>
        <p style={styles.footerText}>
          Environment: {process.env.NODE_ENV || 'development'}
        </p>
      </div>
    </div>
  );
};

const styles = {
  container: {
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
    minHeight: '100vh',
    backgroundColor: '#f8fafc',
    padding: '20px',
  },
  header: {
    textAlign: 'center',
    marginBottom: '40px',
  },
  heading: {
    color: '#1e293b',
    fontSize: '2.5rem',
    fontWeight: '700',
    margin: '0',
    marginBottom: '8px',
  },
  subtitle: {
    color: '#64748b',
    fontSize: '1.1rem',
    margin: '0',
  },
  card: {
    maxWidth: '800px',
    margin: '0 auto',
    backgroundColor: 'white',
    borderRadius: '12px',
    boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
    padding: '32px',
  },
  uploadSection: {
    marginBottom: '24px',
  },
  fileInputContainer: {
    marginBottom: '16px',
  },
  fileInput: {
    width: '100%',
    padding: '12px',
    border: '2px dashed #d1d5db',
    borderRadius: '8px',
    backgroundColor: '#f9fafb',
    fontSize: '16px',
    cursor: 'pointer',
  },
  fileName: {
    marginTop: '8px',
    color: '#059669',
    fontSize: '14px',
    fontWeight: '500',
  },
  primaryButton: {
    width: '100%',
    padding: '12px 24px',
    fontSize: '16px',
    fontWeight: '600',
    color: 'white',
    backgroundColor: '#3b82f6',
    border: 'none',
    borderRadius: '8px',
    cursor: 'pointer',
    transition: 'all 0.2s',
    opacity: 1,
  },
  secondaryButton: {
    width: '100%',
    padding: '12px 24px',
    fontSize: '16px',
    fontWeight: '600',
    color: '#374151',
    backgroundColor: '#f3f4f6',
    border: '1px solid #d1d5db',
    borderRadius: '8px',
    cursor: 'pointer',
    transition: 'all 0.2s',
  },
  downloadSection: {
    marginBottom: '24px',
  },
  loading: {
    textAlign: 'center',
    padding: '24px',
    color: '#6b7280',
  },
  spinner: {
    width: '32px',
    height: '32px',
    border: '3px solid #f3f4f6',
    borderTop: '3px solid #3b82f6',
    borderRadius: '50%',
    animation: 'spin 1s linear infinite',
    margin: '0 auto 16px',
  },
  error: {
    backgroundColor: '#fee2e2',
    color: '#dc2626',
    padding: '16px',
    borderRadius: '8px',
    marginBottom: '24px',
    border: '1px solid #fecaca',
  },
  resultSection: {
    marginTop: '32px',
  },
  resultTitle: {
    color: '#1e293b',
    fontSize: '1.5rem',
    fontWeight: '600',
    marginBottom: '16px',
  },
  enhancedResult: {
    backgroundColor: '#f8fafc',
    border: '1px solid #e2e8f0',
    borderRadius: '8px',
    overflow: 'hidden',
  },
  enhancedText: {
    padding: '20px',
    margin: '0',
    whiteSpace: 'pre-wrap',
    fontSize: '14px',
    lineHeight: '1.6',
    color: '#374151',
    fontFamily: 'Monaco, "Cascadia Code", "Roboto Mono", monospace',
    maxHeight: '400px',
    overflow: 'auto',
  },
  footer: {
    textAlign: 'center',
    marginTop: '40px',
  },
  footerText: {
    color: '#9ca3af',
    fontSize: '12px',
  },
};

export default NextGenCV;