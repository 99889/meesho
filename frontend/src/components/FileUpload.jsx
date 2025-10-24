import React, { useState, useRef } from 'react';
import { Button } from './ui/button';

const FileUpload = ({ 
  onFilesSelected, 
  multiple = false, 
  maxFiles = 5,
  accept = "image/*",
  maxSize = 5 * 1024 * 1024 // 5MB default
}) => {
  const [isDragging, setIsDragging] = useState(false);
  const [errors, setErrors] = useState([]);
  const fileInputRef = useRef(null);

  const validateFiles = (files) => {
    const newErrors = [];
    
    // Check file count
    if (!multiple && files.length > 1) {
      newErrors.push("Only one file can be uploaded at a time");
      return newErrors;
    }
    
    if (files.length > maxFiles) {
      newErrors.push(`Maximum ${maxFiles} files allowed`);
      return newErrors;
    }
    
    // Validate each file
    for (let file of files) {
      // Check file size
      if (file.size > maxSize) {
        newErrors.push(`${file.name}: File size exceeds ${maxSize / (1024 * 1024)} MB limit`);
      }
      
      // Check file type
      if (accept === "image/*") {
        if (!file.type.startsWith('image/')) {
          newErrors.push(`${file.name}: Invalid file type. Only images are allowed`);
        }
      } else {
        const acceptedTypes = accept.split(',').map(type => type.trim());
        const isValidType = acceptedTypes.some(type => {
          if (type.endsWith('/*')) {
            const baseType = type.slice(0, -1); // Remove *
            return file.type.startsWith(baseType);
          }
          return file.type === type || file.name.toLowerCase().endsWith(type.toLowerCase());
        });
        
        if (!isValidType) {
          newErrors.push(`${file.name}: Invalid file type`);
        }
      }
    }
    
    return newErrors;
  };

  const handleFiles = (files) => {
    const fileArray = Array.from(files);
    const validationErrors = validateFiles(fileArray);
    
    if (validationErrors.length > 0) {
      setErrors(validationErrors);
      return;
    }
    
    setErrors([]);
    onFilesSelected(fileArray);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    
    const files = e.dataTransfer.files;
    handleFiles(files);
  };

  const handleFileInputChange = (e) => {
    const files = e.target.files;
    handleFiles(files);
  };

  const triggerFileSelect = () => {
    fileInputRef.current?.click();
  };

  return (
    <div className="w-full">
      <div 
        className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
          isDragging 
            ? 'border-pink-500 bg-pink-50' 
            : 'border-gray-300 hover:border-pink-400'
        }`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={triggerFileSelect}
      >
        <input
          type="file"
          ref={fileInputRef}
          className="hidden"
          onChange={handleFileInputChange}
          multiple={multiple}
          accept={accept}
        />
        
        <div className="flex flex-col items-center justify-center">
          <svg 
            className="w-12 h-12 text-gray-400 mb-4" 
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24" 
            xmlns="http://www.w3.org/2000/svg"
          >
            <path 
              strokeLinecap="round" 
              strokeLinejoin="round" 
              strokeWidth="2" 
              d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
            ></path>
          </svg>
          
          <p className="text-gray-600 mb-2">
            <span className="font-medium text-pink-600">Click to upload</span> or drag and drop
          </p>
          <p className="text-sm text-gray-500">
            {multiple 
              ? `Upload up to ${maxFiles} images (Max ${maxSize / (1024 * 1024)} MB each)` 
              : `Upload an image (Max ${maxSize / (1024 * 1024)} MB)`}
          </p>
        </div>
      </div>
      
      {errors.length > 0 && (
        <div className="mt-2">
          {errors.map((error, index) => (
            <p key={index} className="text-sm text-red-600">{error}</p>
          ))}
        </div>
      )}
      
      <div className="mt-3">
        <Button 
          type="button" 
          variant="outline" 
          onClick={triggerFileSelect}
          className="w-full"
        >
          Browse Files
        </Button>
      </div>
    </div>
  );
};

export default FileUpload;