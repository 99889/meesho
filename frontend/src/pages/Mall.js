import React, { useState, useEffect } from 'react';
import { productAPI } from '../services/api';
import ProductCard from '../components/ProductCard';

const MallPage = () => {
  const [mallProducts, setMallProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchMallProducts();
  }, []);

  const fetchMallProducts = async () => {
    try {
      setLoading(true);
      // Fetch products that are part of the "mall" - these could be premium or featured products
      const data = await productAPI.getAll({ is_featured: true });
      setMallProducts(data.products || data || []);
    } catch (error) {
      console.error('Error fetching mall products:', error);
      setMallProducts([]);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-[#9c1c80] border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600">Loading premium products...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-4 pb-16 md:pb-0">
      <div className="container mx-auto px-4">
        <h1 className="text-xl font-bold mb-2 text-gray-900 px-1">Premium Mall</h1>
        <p className="text-gray-600 text-sm mb-4 px-1">Curated premium products</p>
        
        {mallProducts.length > 0 ? (
          <div className="grid grid-cols-2 gap-3">
            {mallProducts.map((product) => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>
        ) : (
          <p className="text-center py-16 text-gray-500">No premium products available</p>
        )}
      </div>
    </div>
  );
};

export default MallPage;