import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { productAPI, uploadAPI } from '../services/api';
import { Button } from '../components/ui/button';
import { Card } from '../components/ui/card';
import { Input } from '../components/ui/input';
import { Textarea } from '../components/ui/textarea';
import { useAuth } from '../context/AuthContext';
import FileUpload from '../components/FileUpload';
import ImagePreview from '../components/ImagePreview';

const AdminDashboard = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showAddForm, setShowAddForm] = useState(false);
  const [editingProduct, setEditingProduct] = useState(null);
  
  // Form state
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    price: '',
    original_price: '',
    discount: '',
    category: '',
    images: [''], // Changed from single image to array for main images
    additionalImages: [''], // Additional images
    pdfDocuments: [], // PDF documents
    sizes: [''],
    colors: [''],
    stock: '',
    seller_name: '',
    return_policy: '7 days return',
    free_delivery: true,
    cod: true
  });
  
  // File upload state
  const [mainImageFiles, setMainImageFiles] = useState([]); // Changed to array for multiple main images
  const [additionalImageFiles, setAdditionalImageFiles] = useState([]);
  const [pdfFiles, setPdfFiles] = useState([]); // PDF files
  const [isUploading, setIsUploading] = useState(false);
  const [uploadErrors, setUploadErrors] = useState([]);

  useEffect(() => {
    // Check if user is admin/seller
    if (!user || (user.role !== 'seller' && user.role !== 'admin')) {
      navigate('/');
      return;
    }
    
    fetchProducts();
  }, [user, navigate]);

  const fetchProducts = async () => {
    try {
      setLoading(true);
      const response = await productAPI.getAll();
      let productsArray = [];
      if (Array.isArray(response)) {
        productsArray = response;
      } else if (response.products && Array.isArray(response.products)) {
        productsArray = response.products;
      } else if (response.data && Array.isArray(response.data)) {
        productsArray = response.data;
      }
      setProducts(productsArray);
    } catch (error) {
      console.error('Error fetching products:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleArrayInputChange = (index, value, field) => {
    const newArray = [...formData[field]];
    newArray[index] = value;
    setFormData(prev => ({
      ...prev,
      [field]: newArray
    }));
  };

  const addArrayField = (field) => {
    setFormData(prev => ({
      ...prev,
      [field]: [...prev[field], '']
    }));
  };

  const removeArrayField = (index, field) => {
    const newArray = [...formData[field]];
    newArray.splice(index, 1);
    setFormData(prev => ({
      ...prev,
      [field]: newArray
    }));
  };

  const handleMainImagesUpload = (files) => {
    // Limit to 6 main images
    const limitedFiles = files.slice(0, 6);
    setMainImageFiles(limitedFiles);
    // Initialize image URLs array with empty strings for each file
    setFormData(prev => ({
      ...prev,
      images: Array(limitedFiles.length).fill('')
    }));
  };

  const handleAdditionalImagesUpload = (files) => {
    setAdditionalImageFiles(files);
    // Initialize image URLs array with empty strings for each file
    setFormData(prev => ({
      ...prev,
      additionalImages: Array(files.length).fill('')
    }));
  };

  const handlePdfUpload = (files) => {
    // Filter only PDF files
    const pdfFiles = files.filter(file => file.type === 'application/pdf' || file.name.toLowerCase().endsWith('.pdf'));
    setPdfFiles(pdfFiles);
    // Initialize PDF URLs array
    setFormData(prev => ({
      ...prev,
      pdfDocuments: Array(pdfFiles.length).fill('')
    }));
  };

  const uploadFiles = async () => {
    setIsUploading(true);
    setUploadErrors([]);
    
    try {
      // Upload main images if files are selected
      let mainImageUrls = [...formData.images];
      if (mainImageFiles.length > 0) {
        const uploadResponse = await uploadAPI.uploadMultipleImages(mainImageFiles);
        mainImageUrls = uploadResponse.files.map(file => file.url);
      }
      
      // Upload additional images if files are selected
      let additionalImageUrls = [...formData.additionalImages];
      if (additionalImageFiles.length > 0) {
        const uploadResponse = await uploadAPI.uploadMultipleImages(additionalImageFiles);
        additionalImageUrls = uploadResponse.files.map(file => file.url);
      }
      
      // Upload PDF documents if files are selected
      let pdfUrls = [...formData.pdfDocuments];
      if (pdfFiles.length > 0) {
        // PDF files can be uploaded using the same method as images since the backend supports both
        const uploadResponse = await uploadAPI.uploadMultipleImages(pdfFiles);
        pdfUrls = uploadResponse.files.map(file => file.url);
      }
      
      return {
        mainImages: mainImageUrls,
        additionalImages: additionalImageUrls,
        pdfDocuments: pdfUrls
      };
    } catch (error) {
      console.error('Error uploading files:', error);
      const errorMessage = error.response?.data?.detail || error.response?.data?.message || error.message || 'Failed to upload files';
      setUploadErrors([errorMessage]);
      throw new Error(`Upload failed: ${errorMessage}`);
    } finally {
      setIsUploading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      // Upload files first
      const { mainImages, additionalImages, pdfDocuments } = await uploadFiles();
      
      const productData = {
        ...formData,
        images: mainImages, // Now using mainImages array
        additionalImages: additionalImages,
        pdfDocuments: pdfDocuments,
        price: parseFloat(formData.price),
        original_price: parseFloat(formData.original_price) || null,
        discount: parseFloat(formData.discount) || 0,
        stock: parseInt(formData.stock) || 100
      };
      
      if (editingProduct) {
        // Update existing product
        console.log('Updating product with ID:', editingProduct.id);
        console.log('Product data:', productData);
        const response = await productAPI.update(editingProduct.id, productData);
        console.log('Update response:', response);
      } else {
        // Create new product
        console.log('Creating new product with data:', productData);
        const response = await productAPI.create(productData);
        console.log('Create response:', response);
      }
      
      // Reset form and refresh products
      setFormData({
        name: '',
        description: '',
        price: '',
        original_price: '',
        discount: '',
        category: '',
        images: [''],
        additionalImages: [''],
        pdfDocuments: [],
        sizes: [''],
        colors: [''],
        stock: '',
        seller_name: '',
        return_policy: '7 days return',
        free_delivery: true,
        cod: true
      });
      setMainImageFiles([]);
      setAdditionalImageFiles([]);
      setPdfFiles([]);
      setShowAddForm(false);
      setEditingProduct(null);
      fetchProducts();
    } catch (error) {
      console.error('Error saving product:', error);
      console.error('Error response:', error.response);
      const errorMessage = error.response?.data?.detail || error.response?.data?.message || error.message || 'Unknown error';
      alert('Error saving product: ' + errorMessage);
    }
  };

  const handleEdit = (product) => {
    console.log('Editing product:', product);
    setEditingProduct(product);
    setFormData({
      name: product.name || '',
      description: product.description || '',
      price: product.price || '',
      original_price: product.original_price || '',
      discount: product.discount || '',
      category: product.category || '',
      images: product.images || [''], // Main images
      additionalImages: product.additionalImages || [''], // Additional images
      pdfDocuments: product.pdfDocuments || [], // PDF documents
      sizes: product.sizes || [''],
      colors: product.colors || [''],
      stock: product.stock || '',
      seller_name: product.seller_name || '',
      return_policy: product.return_policy || '7 days return',
      free_delivery: product.free_delivery !== undefined ? product.free_delivery : true,
      cod: product.cod !== undefined ? product.cod : true
    });
    setMainImageFiles([]);
    setAdditionalImageFiles([]);
    setPdfFiles([]);
    setShowAddForm(true);
  };

  const handleDelete = async (productId) => {
    if (window.confirm('Are you sure you want to delete this product?')) {
      try {
        console.log('Attempting to delete product with ID:', productId);
        const response = await productAPI.delete(productId);
        console.log('Delete response:', response);
        fetchProducts();
      } catch (error) {
        console.error('Error deleting product:', error);
        console.error('Error response:', error.response);
        alert('Error deleting product: ' + (error.response?.data?.detail || error.message || 'Unknown error'));
      }
    }
  };

  const cancelEdit = () => {
    setEditingProduct(null);
    setShowAddForm(false);
    setFormData({
      name: '',
      description: '',
      price: '',
      original_price: '',
      discount: '',
      category: '',
      images: [''],
      additionalImages: [''],
      pdfDocuments: [],
      sizes: [''],
      colors: [''],
      stock: '',
      seller_name: '',
      return_policy: '7 days return',
      free_delivery: true,
      cod: true
    });
    setMainImageFiles([]);
    setAdditionalImageFiles([]);
    setPdfFiles([]);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-pink-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Admin Dashboard</h1>
          <div className="flex gap-2">
            <Button onClick={() => navigate('/admin/orders')} variant="outline">
              Manage Orders
            </Button>
            <Button onClick={() => setShowAddForm(!showAddForm)}>
              {showAddForm ? 'Cancel' : 'Add New Product'}
            </Button>
          </div>
        </div>

        {showAddForm && (
          <Card className="p-6 mb-8">
            <h2 className="text-2xl font-bold mb-6 text-gray-900">
              {editingProduct ? 'Edit Product' : 'Add New Product'}
            </h2>
            
            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Product Name</label>
                  <Input
                    type="text"
                    name="name"
                    value={formData.name}
                    onChange={handleInputChange}
                    required
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Category</label>
                  <Input
                    type="text"
                    name="category"
                    value={formData.category}
                    onChange={handleInputChange}
                    required
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Price (₹)</label>
                  <Input
                    type="number"
                    name="price"
                    value={formData.price}
                    onChange={handleInputChange}
                    required
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Original Price (₹)</label>
                  <Input
                    type="number"
                    name="original_price"
                    value={formData.original_price}
                    onChange={handleInputChange}
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Discount (%)</label>
                  <Input
                    type="number"
                    name="discount"
                    value={formData.discount}
                    onChange={handleInputChange}
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Stock</label>
                  <Input
                    type="number"
                    name="stock"
                    value={formData.stock}
                    onChange={handleInputChange}
                  />
                </div>
                
                {/* Main Images (5-6 images for slideshow) */}
                <div className="md:col-span-2">
                  <label className="block text-sm font-medium text-gray-700 mb-1">Main Images (5-6 images for slideshow)</label>
                  {mainImageFiles.length > 0 || formData.images.some(img => img) ? (
                    <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-4 mb-4">
                      {mainImageFiles.map((file, index) => (
                        <ImagePreview 
                          key={index}
                          file={file}
                          onRemove={() => {
                            const newFiles = [...mainImageFiles];
                            newFiles.splice(index, 1);
                            setMainImageFiles(newFiles);
                          }}
                        />
                      ))}
                      {formData.images.map((imageUrl, index) => {
                        // Only show existing URLs that don't have corresponding files
                        if (index < mainImageFiles.length) return null;
                        return (
                          <ImagePreview 
                            key={index}
                            url={imageUrl}
                            onRemove={() => {
                              const newImages = [...formData.images];
                              newImages.splice(index, 1);
                              setFormData(prev => ({ ...prev, images: newImages }));
                            }}
                          />
                        );
                      })}
                    </div>
                  ) : null}
                  <FileUpload 
                    onFilesSelected={handleMainImagesUpload}
                    multiple={true}
                    maxFiles={6}
                    accept="image/*"
                    maxSize={5 * 1024 * 1024}
                  />
                  <p className="text-xs text-gray-500 mt-1">Upload 5-6 images for product slideshow</p>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Seller Name</label>
                  <Input
                    type="text"
                    name="seller_name"
                    value={formData.seller_name}
                    onChange={handleInputChange}
                  />
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
                <Textarea
                  name="description"
                  value={formData.description}
                  onChange={handleInputChange}
                  rows={3}
                />
              </div>
              
              {/* Additional Images */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Additional Images</label>
                {additionalImageFiles.length > 0 || formData.additionalImages.some(img => img) ? (
                  <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4 mb-4">
                    {additionalImageFiles.map((file, index) => (
                      <ImagePreview 
                        key={index}
                        file={file}
                        onRemove={() => {
                          const newFiles = [...additionalImageFiles];
                          newFiles.splice(index, 1);
                          setAdditionalImageFiles(newFiles);
                        }}
                      />
                    ))}
                    {formData.additionalImages.map((imageUrl, index) => {
                      // Only show existing URLs that don't have corresponding files
                      if (index < additionalImageFiles.length) return null;
                      return (
                        <ImagePreview 
                          key={index}
                          url={imageUrl}
                          onRemove={() => {
                            const newImages = [...formData.additionalImages];
                            newImages.splice(index, 1);
                            setFormData(prev => ({ ...prev, additionalImages: newImages }));
                          }}
                        />
                      );
                    })}
                  </div>
                ) : null}
                <FileUpload 
                  onFilesSelected={handleAdditionalImagesUpload}
                  multiple={true}
                  maxFiles={6}
                  accept="image/*"
                  maxSize={5 * 1024 * 1024}
                />
                <p className="text-xs text-gray-500 mt-1">Upload up to 6 additional images</p>
              </div>
              
              {/* PDF Documents */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Product Documents (PDF)</label>
                {pdfFiles.length > 0 || formData.pdfDocuments.some(doc => doc) ? (
                  <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4 mb-4">
                    {pdfFiles.map((file, index) => (
                      <div key={index} className="relative group">
                        <div className="aspect-square rounded-md overflow-hidden border border-gray-200 flex flex-col items-center justify-center bg-gray-50">
                          <div className="text-4xl mb-2">📄</div>
                          <p className="text-xs text-center px-2 truncate w-full">{file.name}</p>
                        </div>
                        <Button
                          type="button"
                          variant="outline"
                          size="sm"
                          className="absolute -top-2 -right-2 w-6 h-6 p-0 bg-white border border-gray-300 rounded-full shadow-sm hover:bg-red-50"
                          onClick={() => {
                            const newFiles = [...pdfFiles];
                            newFiles.splice(index, 1);
                            setPdfFiles(newFiles);
                          }}
                        >
                          <svg className="w-3 h-3 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path>
                          </svg>
                        </Button>
                      </div>
                    ))}
                    {formData.pdfDocuments.map((docUrl, index) => {
                      // Only show existing URLs that don't have corresponding files
                      if (index < pdfFiles.length) return null;
                      return (
                        <div key={index} className="relative group">
                          <div className="aspect-square rounded-md overflow-hidden border border-gray-200 flex flex-col items-center justify-center bg-gray-50">
                            <div className="text-4xl mb-2">📄</div>
                            <p className="text-xs text-center px-2 truncate w-full">Document {index + 1}</p>
                          </div>
                          <Button
                            type="button"
                            variant="outline"
                            size="sm"
                            className="absolute -top-2 -right-2 w-6 h-6 p-0 bg-white border border-gray-300 rounded-full shadow-sm hover:bg-red-50"
                            onClick={() => {
                              const newDocs = [...formData.pdfDocuments];
                              newDocs.splice(index, 1);
                              setFormData(prev => ({ ...prev, pdfDocuments: newDocs }));
                            }}
                          >
                            <svg className="w-3 h-3 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path>
                            </svg>
                          </Button>
                        </div>
                      );
                    })}
                  </div>
                ) : null}
                <FileUpload 
                  onFilesSelected={handlePdfUpload}
                  multiple={true}
                  maxFiles={5}
                  accept=".pdf,application/pdf"
                  maxSize={10 * 1024 * 1024} // 10MB for PDFs
                />
                <p className="text-xs text-gray-500 mt-1">Upload up to 5 PDF documents (max 10MB each)</p>
              </div>
              
              {/* Sizes Array */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Sizes</label>
                {formData.sizes.map((size, index) => (
                  <div key={index} className="flex gap-2 mb-2">
                    <Input
                      type="text"
                      value={size}
                      onChange={(e) => handleArrayInputChange(index, e.target.value, 'sizes')}
                      placeholder="Size"
                    />
                    {formData.sizes.length > 1 && (
                      <Button
                        type="button"
                        variant="outline"
                        onClick={() => removeArrayField(index, 'sizes')}
                      >
                        Remove
                      </Button>
                    )}
                  </div>
                ))}
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => addArrayField('sizes')}
                  className="mt-2"
                >
                  Add Size
                </Button>
              </div>
              
              {/* Colors Array */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Colors</label>
                {formData.colors.map((color, index) => (
                  <div key={index} className="flex gap-2 mb-2">
                    <Input
                      type="text"
                      value={color}
                      onChange={(e) => handleArrayInputChange(index, e.target.value, 'colors')}
                      placeholder="Color"
                    />
                    {formData.colors.length > 1 && (
                      <Button
                        type="button"
                        variant="outline"
                        onClick={() => removeArrayField(index, 'colors')}
                      >
                        Remove
                      </Button>
                    )}
                  </div>
                ))}
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => addArrayField('colors')}
                  className="mt-2"
                >
                  Add Color
                </Button>
              </div>
              
              <div className="flex items-center gap-4">
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    name="free_delivery"
                    checked={formData.free_delivery}
                    onChange={handleInputChange}
                    className="mr-2"
                  />
                  Free Delivery
                </label>
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    name="cod"
                    checked={formData.cod}
                    onChange={handleInputChange}
                    className="mr-2"
                  />
                  Cash on Delivery
                </label>
              </div>
              
              {uploadErrors.length > 0 && (
                <div className="bg-red-50 border border-red-200 rounded-md p-4">
                  <h3 className="text-red-800 font-medium">Upload Errors</h3>
                  {uploadErrors.map((error, index) => (
                    <p key={index} className="text-red-600 text-sm">{error}</p>
                  ))}
                </div>
              )}
              
              <div className="flex gap-3">
                <Button 
                  type="submit" 
                  className="bg-pink-600 hover:bg-pink-700"
                  disabled={isUploading}
                >
                  {isUploading ? (
                    <>
                      <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
                      Uploading...
                    </>
                  ) : (
                    editingProduct ? 'Update Product' : 'Add Product'
                  )}
                </Button>
                <Button type="button" variant="outline" onClick={cancelEdit}>
                  Cancel
                </Button>
              </div>
            </form>
          </Card>
        )}

        <Card className="p-6">
          <h2 className="text-2xl font-bold mb-6 text-gray-900">Products ({products.length})</h2>
          
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Product</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Category</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Price</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Stock</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {products.map((product) => (
                  <tr key={product.id}>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <div className="flex-shrink-0 h-10 w-10">
                          <img className="h-10 w-10 rounded-md object-cover" src={product.image} alt={product.name} />
                        </div>
                        <div className="ml-4">
                          <div className="text-sm font-medium text-gray-900">{product.name}</div>
                          <div className="text-sm text-gray-500">{product.seller_name || 'Unknown Seller'}</div>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {product.category}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      ₹{product.price}
                      {product.original_price && product.original_price > product.price && (
                        <div className="text-xs text-gray-400 line-through">₹{product.original_price}</div>
                      )}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {product.stock > 0 ? (
                        <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                          {product.stock} in stock
                        </span>
                      ) : (
                        <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-red-100 text-red-800">
                          Out of stock
                        </span>
                      )}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <Button
                        onClick={() => handleEdit(product)}
                        variant="outline"
                        size="sm"
                        className="mr-2"
                      >
                        Edit
                      </Button>
                      <Button
                        onClick={() => handleDelete(product.id)}
                        variant="outline"
                        size="sm"
                        className="text-red-600 border-red-600 hover:bg-red-50"
                      >
                        Delete
                      </Button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          
          {products.length === 0 && (
            <div className="text-center py-12">
              <p className="text-gray-500">No products found</p>
            </div>
          )}
        </Card>
      </div>
    </div>
  );
};

export default AdminDashboard;