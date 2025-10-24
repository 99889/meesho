import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { productAPI, categoryAPI } from '../services/api';
import ProductCard from '../components/ProductCard';

const CategoryPage = () => {
  const { category } = useParams();
  const [categoryProducts, setCategoryProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (category) {
      fetchCategoryProducts();
    } else {
      fetchAllCategories();
    }
  }, [category]);

  const fetchCategoryProducts = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await productAPI.getByCategory(category);
      setCategoryProducts(data.products || []);
    } catch (error) {
      console.error('Error fetching category products:', error);
      setError('Failed to load products');
    } finally {
      setLoading(false);
    }
  };

  const fetchAllCategories = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await categoryAPI.getAll();
      setCategories(data.categories || []);
    } catch (error) {
      console.error('Error fetching categories:', error);
      setError('Failed to load categories');
      // Fallback to mock categories
      setCategories([
        { name: 'Women Ethnic', image: 'https://images.unsplash.com/photo-1521334884684-d80222895326?w=200&h=200&fit=crop' },
        { name: 'Men Topwear', image: 'https://images.unsplash.com/photo-1602810319586-3a2d0c0b6e4a?w=200&h=200&fit=crop' },
        { name: 'Kids & Toys', image: 'https://images.unsplash.com/photo-1622290291468-a28f7a7dc338?w=200&h=200&fit=crop' },
        { name: 'Beauty & Health', image: 'https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=200&h=200&fit=crop' },
        { name: 'Home & Kitchen', image: 'https://images.pexels.com/photos/279648/pexels-photo-279648.jpeg?w=200&h=200&fit=crop' },
        { name: 'Electronics', image: 'https://images.pexels.com/photos/1599791/pexels-photo-1599791.jpeg?w=200&h=200&fit=crop' }
      ]);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-[#9c1c80] border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  // If no category is specified, show all categories
  if (!category) {
    return (
      <div className="min-h-screen bg-gray-50 py-4 pb-16 md:pb-0">
        <div className="container mx-auto px-4">
          <h1 className="text-xl font-bold mb-4 text-gray-900 px-1">All Categories</h1>
          
          {error && (
            <div className="bg-red-50 border border-red-200 rounded p-3 mb-4">
              <p className="text-red-700 text-sm">{error}</p>
            </div>
          )}
          
          <div className="grid grid-cols-3 gap-3">
            {categories.map((cat, index) => (
              <a 
                key={index} 
                href={`/category/${encodeURIComponent(cat.name)}`}
                className="bg-white rounded-lg overflow-hidden shadow-sm hover:shadow-md transition-shadow"
              >
                <div className="aspect-square overflow-hidden">
                  <img 
                    src={cat.image} 
                    alt={cat.name} 
                    className="w-full h-full object-cover"
                    onError={(e) => {
                      e.target.src = 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=200&h=200&fit=crop';
                    }}
                  />
                </div>
                <div className="p-2">
                  <p className="text-xs font-medium text-gray-900 text-center line-clamp-2">{cat.name}</p>
                </div>
              </a>
            ))}
          </div>
        </div>
      </div>
    );
  }

  // Show products for a specific category
  return (
    <div className="min-h-screen bg-gray-50 py-4 pb-16 md:pb-0">
      <div className="container mx-auto px-4">
        <h1 className="text-xl font-bold mb-2 text-gray-900 px-1">{category}</h1>
        <p className="text-gray-600 text-sm mb-4 px-1">{categoryProducts.length} products</p>
        
        {error && (
          <div className="bg-red-50 border border-red-200 rounded p-3 mb-4">
            <p className="text-red-700 text-sm">{error}</p>
          </div>
        )}
        
        {categoryProducts.length > 0 ? (
          <div className="grid grid-cols-2 gap-3">
            {categoryProducts.map((product) => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>
        ) : (
          <p className="text-center py-16 text-gray-500">No products in this category</p>
        )}
      </div>
    </div>
  );
};

export default CategoryPage;