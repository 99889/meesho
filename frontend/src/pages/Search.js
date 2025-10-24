import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { Search } from 'lucide-react';
import { productAPI } from '../services/api';
import ProductCard from '../components/ProductCard';

const SearchPage = () => {
  const [searchParams] = useSearchParams();
  const query = searchParams.get('q') || '';
  const [searchResults, setSearchResults] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (query) {
      fetchSearchResults();
    } else {
      setSearchResults([]);
    }
  }, [query]);

  const fetchSearchResults = async () => {
    try {
      setLoading(true);
      let data;
      
      // Handle special queries for discounts and ratings
      if (query === 'discount') {
        // Get products with high discounts (50% or more)
        data = await productAPI.getAll({ discount: 50 });
      } else if (query === 'rating') {
        // Get products with high ratings (4.5 or more)
        data = await productAPI.getAll({ rating: 4.5 });
      } else if (query === 'budget') {
        // Get budget phones under ₹20,000
        data = await productAPI.getAll({ category: 'Electronics', max_price: 20000 });
      } else if (query === 'premium') {
        // Get premium phones over ₹40,000
        data = await productAPI.getAll({ category: 'Electronics', min_price: 40000 });
      } else {
        // Regular search
        data = await productAPI.search(query);
      }
      
      setSearchResults(data.products || []);
    } catch (error) {
      console.error('Error searching products:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-pink-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600">Searching...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4">
        <h1 className="text-2xl font-bold mb-2 text-gray-900">
          Search Results for "{query}"
        </h1>
        <p className="text-gray-600 mb-6">{searchResults.length} products found</p>

        {searchResults.length > 0 ? (
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
            {searchResults.map((product) => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>
        ) : (
          <div className="text-center py-16">
            <Search className="w-24 h-24 mx-auto text-gray-300 mb-4" />
            <p className="text-gray-600">No products found matching your search</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default SearchPage;
