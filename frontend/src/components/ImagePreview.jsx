import React from 'react';
import { Button } from './ui/button';

const ImagePreview = ({ 
  file, 
  url, 
  onRemove, 
  isUploading = false,
  uploadError = null
}) => {
  const [imageSrc, setImageSrc] = React.useState(url || null);
  
  React.useEffect(() => {
    if (file && !url) {
      const reader = new FileReader();
      reader.onload = (e) => {
        setImageSrc(e.target.result);
      };
      reader.readAsDataURL(file);
    } else if (url) {
      setImageSrc(url);
    }
  }, [file, url]);

  return (
    <div className="relative group">
      <div className="relative aspect-square rounded-md overflow-hidden border border-gray-200">
        {isUploading ? (
          <div className="w-full h-full flex items-center justify-center bg-gray-100">
            <div className="w-8 h-8 border-4 border-pink-600 border-t-transparent rounded-full animate-spin"></div>
          </div>
        ) : imageSrc ? (
          <img 
            src={imageSrc} 
            alt="Preview" 
            className="w-full h-full object-cover"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center bg-gray-100">
            <svg className="w-8 h-8 text-gray-400" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
              <path fillRule="evenodd" d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z" clipRule="evenodd"></path>
            </svg>
          </div>
        )}
        
        {uploadError && (
          <div className="absolute inset-0 bg-red-500 bg-opacity-70 flex items-center justify-center">
            <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </div>
        )}
      </div>
      
      {onRemove && (
        <Button
          type="button"
          variant="outline"
          size="sm"
          className="absolute -top-2 -right-2 w-6 h-6 p-0 bg-white border border-gray-300 rounded-full shadow-sm hover:bg-red-50"
          onClick={onRemove}
        >
          <svg className="w-3 h-3 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
        </Button>
      )}
      
      {uploadError && (
        <p className="text-xs text-red-600 mt-1 truncate">{uploadError}</p>
      )}
    </div>
  );
};

export default ImagePreview;