import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Heart, Star, Filter, ChevronDown } from 'lucide-react';
import { productAPI } from '../services/api';
import { useCart } from '../context/CartContext';
import { getUserId, trackEvent } from '../utils/userTracking';

const Home = () => {
  const navigate = useNavigate();
  const { addToWishlist, isInWishlist, removeFromWishlist } = useCart();
  const [products, setProducts] = useState([]);
  const [mobilePhones, setMobilePhones] = useState([]);
  const [budgetPhones, setBudgetPhones] = useState([]);
  const [premiumPhones, setPremiumPhones] = useState([]);
  const [trendingProducts, setTrendingProducts] = useState([]);
  const [bestDeals, setBestDeals] = useState([]);
  const [fashionProducts, setFashionProducts] = useState([]);
  const [homeProducts, setHomeProducts] = useState([]);
  const [electronics, setElectronics] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Filter states
  const [showFilters, setShowFilters] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState('');
  const [selectedGender, setSelectedGender] = useState('');
  const [sortBy, setSortBy] = useState('');
  const [priceRange, setPriceRange] = useState([0, 100000]);
  const [filteredProducts, setFilteredProducts] = useState([]);

  // Category data with real category images - EXACT Meesho order
  const categoryData = [
    {
      name: 'Categories',
      image: 'https://images.unsplash.com/photo-1557821552-17105176677c?w=200&h=200&fit=crop',
      icon: true, // This will be rendered with a special pink gradient
    },
    {
      name: 'Kurti & Dresses',
      image: 'https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=200&h=200&fit=crop',
    },
    {
      name: 'Kids & Toys',
      image: 'https://images.unsplash.com/photo-1515488042361-ee00e0ddd4e4?w=200&h=200&fit=crop',
    },
    {
      name: 'Westernwear',
      image: 'https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=200&h=200&fit=crop',
    },
    {
      name: 'Home',
      image: 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=200&h=200&fit=crop',
    }
  ];

  // Gender options
  const genderOptions = ['Men', 'Women', 'Kids', 'Unisex'];

  // Sort options
  const sortOptions = [
    { value: 'price_low', label: 'Price: Low to High' },
    { value: 'price_high', label: 'Price: High to Low' },
    { value: 'rating', label: 'Top Rated' },
    { value: 'discount', label: 'Best Discount' },
    { value: 'newest', label: 'Newest First' }
  ];

  useEffect(() => {
    // Initialize user tracking
    const userId = getUserId();
    trackEvent('home_page_viewed', { userId });
    
    fetchProducts();
  }, []);

  // Apply filters whenever filter criteria change
  useEffect(() => {
    applyFilters();
  }, [products, selectedCategory, selectedGender, sortBy, priceRange]);

  const fetchProducts = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Try to fetch products
      const response = await productAPI.getAll();
      
      let productsArray = [];
      if (Array.isArray(response)) {
        productsArray = response;
      } else if (response.products && Array.isArray(response.products)) {
        productsArray = response.products;
      } else if (response.data && Array.isArray(response.data)) {
        productsArray = response.data;
      }
      
      const transformedProducts = productsArray.map(product => ({
        ...product,
        id: product.id || product._id,
        original_price: product.original_price || product.price,
        free_delivery: product.free_delivery !== false,
      }));
      
      setProducts(transformedProducts);
      setFilteredProducts(transformedProducts);
      
      // Filter products into different categories
      // Mobile phones
      const phones = transformedProducts.filter(p => 
        p.category && (p.category.includes('Mobile') || p.category.includes('Tablets') ||
        p.name.includes('iPhone') || p.name.includes('Samsung') || 
        p.name.includes('Redmi') || p.name.includes('Realme') ||
        p.name.includes('OnePlus') || p.name.includes('Poco') ||
        p.name.includes('Vivo') || p.name.includes('OPPO') || p.name.includes('Oppo') ||
        p.name.includes('Apple') || p.name.includes('Apple'))
      );
      setMobilePhones(phones);
      
      // Budget phones (< ₹20,000)
      setBudgetPhones(phones.filter(p => p.price < 20000).slice(0, 10));
      
      // Premium phones (> ₹40,000)
      setPremiumPhones(phones.filter(p => p.price > 40000).slice(0, 10));
      
      // Trending (high rating)
      setTrendingProducts(transformedProducts.filter(p => p.rating >= 4.5).slice(0, 10));
      
      // Best deals (high discount)
      setBestDeals(transformedProducts.filter(p => p.discount >= 50).slice(0, 10));
      
      // Fashion products
      setFashionProducts(transformedProducts.filter(p => 
        p.category && (p.category.includes('Women') || p.category.includes('Men') || 
        p.category.includes('Kurti') || p.category.includes('Dress') ||
        p.category.includes('Westernwear') || p.category.includes('Fashion'))
      ).slice(0, 10));
      
      // Home products
      setHomeProducts(transformedProducts.filter(p => 
        p.category && (p.category.includes('Home') || p.category.includes('Kitchen') || 
        p.category.includes('Decor'))
      ).slice(0, 10));
      
      // Electronics (excluding mobile phones)
      setElectronics(transformedProducts.filter(p => 
        p.category && p.category.includes('Electronics') && !(
          p.name.includes('iPhone') || p.name.includes('Samsung') || 
          p.name.includes('Redmi') || p.name.includes('Realme') ||
          p.name.includes('OnePlus') || p.name.includes('Poco') ||
          p.name.includes('Vivo') || p.name.includes('OPPO') || p.name.includes('Oppo') ||
          p.name.includes('Apple') || p.name.includes('Apple'))
      ).slice(0, 10));
      
    } catch (error) {
      console.error('Error fetching products:', error);
      
      // More detailed error handling
      let errorMessage = 'Failed to load products. ';
      
      if (error.code === 'NETWORK_ERROR' || error.message.includes('fetch')) {
        errorMessage += 'Network error - please check your connection and make sure the backend server is running.';
      } else if (error.response) {
        errorMessage += `Server responded with status ${error.response.status}.`;
      } else {
        errorMessage += error.message;
      }
      
      setError(errorMessage);
      setProducts([]);
    } finally {
      setLoading(false);
    }
  };

  const applyFilters = () => {
    let filtered = [...products];
    
    // Apply category filter
    if (selectedCategory) {
      filtered = filtered.filter(product => 
        product.category && product.category.toLowerCase().includes(selectedCategory.toLowerCase())
      );
    }
    
    // Apply gender filter
    if (selectedGender) {
      filtered = filtered.filter(product => 
        (product.category && product.category.toLowerCase().includes(selectedGender.toLowerCase())) ||
        (product.name && product.name.toLowerCase().includes(selectedGender.toLowerCase()))
      );
    }
    
    // Apply price range filter
    filtered = filtered.filter(product => 
      product.price >= priceRange[0] && product.price <= priceRange[1]
    );
    
    // Apply sorting
    switch (sortBy) {
      case 'price_low':
        filtered.sort((a, b) => a.price - b.price);
        break;
      case 'price_high':
        filtered.sort((a, b) => b.price - a.price);
        break;
      case 'rating':
        filtered.sort((a, b) => b.rating - a.rating);
        break;
      case 'discount':
        filtered.sort((a, b) => b.discount - a.discount);
        break;
      case 'newest':
        // Assuming products have a createdAt field, otherwise sort by ID
        filtered.sort((a, b) => (b.id || '').localeCompare(a.id || ''));
        break;
      default:
        // Default sorting (by ID or name)
        break;
    }
    
    setFilteredProducts(filtered);
  };

  const resetFilters = () => {
    setSelectedCategory('');
    setSelectedGender('');
    setSortBy('');
    setPriceRange([0, 100000]);
  };

  const handleWishlistClick = (e, product) => {
    e.stopPropagation();
    if (isInWishlist(product.id)) {
      removeFromWishlist(product.id);
    } else {
      addToWishlist(product);
    }
  };

  const handleDeliveryLocationClick = () => {
    navigate('/account');
  };

  const ProductCard = ({ product }) => {
    const productName = product.name || product.title || 'Unknown Product';
    const productPrice = product.price || 0;
    const productOriginalPrice = product.original_price || product.price;
    const productDiscount = product.discount || 0;
    const productRating = product.rating || 0;
    const productReviews = product.reviews || 0;
    // Use the first image from the images array or fallback to the single image
    const productImage = (product.images && product.images[0]) || product.image || 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop';
    const productFreeDelivery = product.free_delivery !== false;

    return (
      <div
        onClick={() => navigate(`/product/${encodeURIComponent(productName)}`)}
        className="bg-white rounded-md overflow-hidden hover:shadow-lg transition-all cursor-pointer"
      >
        {/* Image Container */}
        <div className="relative bg-gray-50 overflow-hidden group aspect-square">
          <img
            src={productImage}
            alt={productName}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
            onError={(e) => {
              e.target.src = 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop';
            }}
          />
          
          {/* Wishlist Button */}
          <button
            onClick={(e) => handleWishlistClick(e, product)}
            className={`absolute top-1.5 right-1.5 w-7 h-7 rounded-full flex items-center justify-center shadow-sm transition-all ${
              isInWishlist(product.id)
                ? 'bg-white'
                : 'bg-white/90 hover:bg-white'
            }`}
          >
            <Heart
              size={14}
              className={isInWishlist(product.id) ? 'fill-red-500 text-red-500' : 'text-gray-600'}
            />
          </button>

          {/* Discount Badge */}
          {productDiscount > 0 && (
            <div className="absolute top-1.5 left-1.5 bg-red-500 text-white px-1.5 py-0.5 rounded text-[11px] font-semibold shadow-sm">
              {productDiscount}% OFF
            </div>
          )}
        </div>

        {/* Product Info */}
        <div className="p-2.5">
          {/* Product Name */}
          <h3 className="text-[13px] font-medium text-gray-900 line-clamp-2 mb-1.5 leading-tight">
            {productName}
          </h3>

          {/* Price Section */}
          <div className="flex items-center gap-1.5 mb-1">
            <span className="text-[15px] font-bold text-gray-900">₹{productPrice}</span>
            {productOriginalPrice > productPrice && (
              <>
                <span className="text-[12px] text-gray-400 line-through">
                  ₹{productOriginalPrice}
                </span>
                <span className="text-[11px] text-green-600 font-medium">
                  {productDiscount}% off
                </span>
              </>
            )}
          </div>

          {/* Free Delivery Badge */}
          {productFreeDelivery && (
            <p className="text-[11px] text-gray-600 mb-1">Free Delivery</p>
          )}

          {/* Rating */}
          <div className="flex items-center gap-1.5">
            {productRating > 0 && (
              <>
                <div className="flex items-center gap-0.5 bg-green-600 text-white px-1.5 py-0.5 rounded-sm">
                  <Star size={10} fill="white" strokeWidth={0} />
                  <span className="text-[11px] font-semibold">{productRating.toFixed(1)}</span>
                </div>
                <span className="text-[11px] text-gray-500">({productReviews})</span>
              </>
            )}
          </div>
        </div>
      </div>
    );
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-white flex items-center justify-center pb-24">
        <div className="text-center">
          <div className="w-12 h-12 border-4 border-[#9c1c80] border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600 text-sm">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-white pb-24 md:pb-0">
      {/* ===== MOBILE LAYOUT ===== */}
      <div className="md:hidden">
        {/* Navbar is handled by Navbar component - it includes:
            - Free Delivery bar
            - Logo + Search + Menu
            - Delivery Location bar
        */}

        {/* Category Carousel - Circular like Meesho */}
        <div className="bg-white py-3 border-b border-gray-100">
          <div className="flex gap-4 px-4 overflow-x-auto scrollbar-hide">
            {categoryData.map((cat, idx) => (
              <button
                key={idx}
                onClick={() => navigate(cat.name === 'Categories' ? '/categories' : `/category/${cat.name}`)}
                className="flex flex-col items-center gap-2 flex-shrink-0"
              >
                {cat.icon ? (
                  // Special pink gradient icon for "Categories"
                  <div className="w-16 h-16 rounded-full bg-pink-100 flex items-center justify-center shadow-sm border border-pink-200">
                    <svg className="w-8 h-8" viewBox="0 0 24 24" fill="currentColor">
                      <rect x="3" y="3" width="7" height="7" rx="1.5" fill="#f9a8d4"/>
                      <rect x="14" y="3" width="7" height="7" rx="1.5" fill="#be185d"/>
                      <rect x="3" y="14" width="7" height="7" rx="1.5" fill="#be185d"/>
                      <rect x="14" y="14" width="7" height="7" rx="1.5" fill="#f9a8d4"/>
                    </svg>
                  </div>
                ) : (
                  // Regular image for other categories
                  <div className="w-16 h-16 rounded-full overflow-hidden bg-gray-50 shadow-sm">
                    <img
                      src={cat.image}
                      alt={cat.name}
                      className="w-full h-full object-cover"
                      onError={(e) => {
                        e.target.src = 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=200&h=200&fit=crop';
                      }}
                    />
                  </div>
                )}
                <span className="text-xs text-gray-800 text-center max-w-[70px] leading-tight">
                  {cat.name}
                </span>
              </button>
            ))}
          </div>
        </div>

        {/* Banner - Removed "Lowest prices best quality shopping" */}

        {/* Premium Phones */}
        {premiumPhones.length > 0 && (
          <div className="py-4 bg-white">
            <div className="px-4 mb-3 flex justify-between items-center">
              <h2 className="text-base font-bold text-gray-900">📱 Premium Smartphones</h2>
              <button 
                onClick={() => navigate('/search?q=premium')}
                className="text-xs text-[#9c1c80] font-semibold"
              >
                View All
              </button>
            </div>
            <div className="flex overflow-x-auto gap-3 px-4 pb-2 scrollbar-hide">
              {premiumPhones.map((product) => (
                <div key={product.id} className="flex-shrink-0 w-36">
                  <ProductCard product={product} />
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Budget Phones */}
        {budgetPhones.length > 0 && (
          <div className="py-3 border-b border-gray-100">
            <div className="px-3 mb-2 flex justify-between items-center">
              <h2 className="text-sm font-bold text-gray-900">📱 Budget Phones Under ₹20,000</h2>
              <button 
                onClick={() => navigate('/search?q=budget')}
                className="text-xs text-purple-600 font-medium"
              >
                View All
              </button>
            </div>
            <div className="flex overflow-x-auto gap-2 px-3 pb-2">
              {budgetPhones.map((product) => (
                <div key={product.id} className="flex-shrink-0 w-32">
                  <ProductCard product={product} />
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Mobile Phones */}
        {mobilePhones.length > 0 && (
          <div className="py-3 border-b border-gray-100">
            <div className="px-3 mb-2 flex justify-between items-center">
              <h2 className="text-sm font-bold text-gray-900">📱 All Mobile Phones</h2>
              <button 
                onClick={() => navigate('/category/Electronics')}
                className="text-xs text-purple-600 font-medium"
              >
                View All
              </button>
            </div>
            <div className="flex overflow-x-auto gap-2 px-3 pb-2">
              {mobilePhones.slice(0, 8).map((product) => (
                <div key={product.id} className="flex-shrink-0 w-32">
                  <ProductCard product={product} />
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Electronics */}
        {electronics.length > 0 && (
          <div className="py-3 border-b border-gray-100">
            <div className="px-3 mb-2 flex justify-between items-center">
              <h2 className="text-sm font-bold text-gray-900">🎧 Electronics & Gadgets</h2>
              <button 
                onClick={() => navigate('/category/Electronics')}
                className="text-xs text-purple-600 font-medium"
              >
                View All
              </button>
            </div>
            <div className="flex overflow-x-auto gap-2 px-3 pb-2">
              {electronics.map((product) => (
                <div key={product.id} className="flex-shrink-0 w-32">
                  <ProductCard product={product} />
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Best Deals Carousel */}
        {bestDeals.length > 0 && (
          <div className="py-3 border-b border-gray-100">
            <div className="px-3 mb-2 flex justify-between items-center">
              <h2 className="text-sm font-bold text-gray-900">🔥 Best Deals</h2>
              <button 
                onClick={() => navigate('/search?q=discount')}
                className="text-xs text-purple-600 font-medium"
              >
                View All
              </button>
            </div>
            <div className="flex overflow-x-auto gap-2 px-3 pb-2">
              {bestDeals.map((product) => (
                <div key={product.id} className="flex-shrink-0 w-32">
                  <ProductCard product={product} />
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Trending Now */}
        {trendingProducts.length > 0 && (
          <div className="py-3 border-b border-gray-100">
            <div className="px-3 mb-2 flex justify-between items-center">
              <h2 className="text-sm font-bold text-gray-900">⭐ Trending Now</h2>
              <button 
                onClick={() => navigate('/search?q=rating')}
                className="text-xs text-purple-600 font-medium"
              >
                View All
              </button>
            </div>
            <div className="flex overflow-x-auto gap-2 px-3 pb-2">
              {trendingProducts.map((product) => (
                <div key={product.id} className="flex-shrink-0 w-32">
                  <ProductCard product={product} />
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Fashion For You */}
        {fashionProducts.length > 0 && (
          <div className="py-3 border-b border-gray-100">
            <div className="px-3 mb-2 flex justify-between items-center">
              <h2 className="text-sm font-bold text-gray-900">👗 Fashion For You</h2>
              <button 
                onClick={() => navigate('/category/Fashion')}
                className="text-xs text-purple-600 font-medium"
              >
                View All
              </button>
            </div>
            <div className="flex overflow-x-auto gap-2 px-3 pb-2">
              {fashionProducts.map((product) => (
                <div key={product.id} className="flex-shrink-0 w-32">
                  <ProductCard product={product} />
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Home & Kitchen */}
        {homeProducts.length > 0 && (
          <div className="py-3 border-b border-gray-100">
            <div className="px-3 mb-2 flex justify-between items-center">
              <h2 className="text-sm font-bold text-gray-900">🏠 Home & Kitchen</h2>
              <button 
                onClick={() => navigate('/category/Home')}
                className="text-xs text-purple-600 font-medium"
              >
                View All
              </button>
            </div>
            <div className="flex overflow-x-auto gap-2 px-3 pb-2">
              {homeProducts.map((product) => (
                <div key={product.id} className="flex-shrink-0 w-32">
                  <ProductCard product={product} />
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Products For You Section */}
        <div className="px-3 py-3">
          <h3 className="text-sm font-bold text-gray-900 mb-2">Products For You</h3>
          
          {/* Filter Bar */}
          <div className="flex gap-2 mb-3 overflow-x-auto pb-2">
            <button 
              className="text-xs px-2 py-1 border border-gray-300 rounded-full whitespace-nowrap text-gray-700 flex items-center"
              onClick={() => setSortBy(sortBy === 'price_low' ? 'price_high' : 'price_low')}
            >
              <span>↑↓ Sort</span>
            </button>
            <button 
              className="text-xs px-2 py-1 border border-gray-300 rounded-full whitespace-nowrap text-gray-700 flex items-center"
              onClick={() => setShowFilters(!showFilters)}
            >
              <span>Category ▼</span>
            </button>
            <button 
              className="text-xs px-2 py-1 border border-gray-300 rounded-full whitespace-nowrap text-gray-700 flex items-center"
              onClick={() => setShowFilters(!showFilters)}
            >
              <span>Gender ▼</span>
            </button>
            <button 
              className="text-xs px-2 py-1 border border-gray-300 rounded-full whitespace-nowrap text-gray-700 flex items-center"
              onClick={() => setShowFilters(!showFilters)}
            >
              <Filter size={12} className="mr-1" />
              <span>Filters</span>
            </button>
          </div>

          {/* Filter Panel */}
          {showFilters && (
            <div className="bg-white border border-gray-200 rounded-lg p-3 mb-3">
              <div className="flex justify-between items-center mb-2">
                <h4 className="font-medium text-gray-900">Filters</h4>
                <button 
                  onClick={resetFilters}
                  className="text-xs text-purple-600"
                >
                  Reset
                </button>
              </div>
              
              {/* Category Filter */}
              <div className="mb-3">
                <label className="text-xs font-medium text-gray-700 mb-1 block">Category</label>
                <select 
                  value={selectedCategory}
                  onChange={(e) => setSelectedCategory(e.target.value)}
                  className="w-full text-xs border border-gray-300 rounded p-1"
                >
                  <option value="">All Categories</option>
                  <option value="Electronics">Electronics</option>
                  <option value="Fashion">Fashion</option>
                  <option value="Home">Home & Kitchen</option>
                  <option value="Mobile">Mobile Phones</option>
                </select>
              </div>
              
              {/* Gender Filter */}
              <div className="mb-3">
                <label className="text-xs font-medium text-gray-700 mb-1 block">Gender</label>
                <select 
                  value={selectedGender}
                  onChange={(e) => setSelectedGender(e.target.value)}
                  className="w-full text-xs border border-gray-300 rounded p-1"
                >
                  <option value="">All</option>
                  {genderOptions.map(gender => (
                    <option key={gender} value={gender}>{gender}</option>
                  ))}
                </select>
              </div>
              
              {/* Sort By */}
              <div className="mb-3">
                <label className="text-xs font-medium text-gray-700 mb-1 block">Sort By</label>
                <select 
                  value={sortBy}
                  onChange={(e) => setSortBy(e.target.value)}
                  className="w-full text-xs border border-gray-300 rounded p-1"
                >
                  <option value="">Default</option>
                  {sortOptions.map(option => (
                    <option key={option.value} value={option.value}>{option.label}</option>
                  ))}
                </select>
              </div>
              
              <button 
                onClick={() => setShowFilters(false)}
                className="w-full bg-purple-600 text-white text-xs py-1.5 rounded"
              >
                Apply Filters
              </button>
            </div>
          )}

          {/* Error Message */}
          {error && (
            <div className="bg-red-50 border border-red-200 rounded p-2 mb-3">
              <p className="text-red-700 text-xs">Error: {error}</p>
              <button
                onClick={fetchProducts}
                className="mt-2 px-3 py-1 bg-[#9c1c80] text-white rounded text-xs"
              >
                Retry
              </button>
            </div>
          )}

          {/* Products Grid */}
          {filteredProducts.length > 0 ? (
            <div className="grid grid-cols-2 gap-2">
              {filteredProducts.slice(0, 20).map((product) => (
                <ProductCard key={product.id || product._id} product={product} />
              ))}
            </div>
          ) : (
            <div className="text-center py-8">
              <p className="text-gray-500 text-sm">No products available</p>
              <button
                onClick={fetchProducts}
                className="mt-4 px-4 py-2 bg-[#9c1c80] text-white rounded text-sm"
              >
                Retry
              </button>
            </div>
          )}
        </div>
      </div>

      {/* ===== DESKTOP LAYOUT ===== */}
      <div className="hidden md:block container mx-auto px-4 py-8">
        {/* Categories Section */}
        <div className="mb-8">
          <h2 className="text-2xl font-bold mb-4 text-gray-900">Shop by Category</h2>
          <div className="grid grid-cols-5 gap-4">
            {categoryData.map((cat, idx) => (
              <button
                key={idx}
                onClick={() => navigate(`/category/${cat.name}`)}
                className="rounded-lg overflow-hidden hover:shadow-lg transition-shadow group"
              >
                <div className="relative h-48 overflow-hidden bg-gray-200">
                  <img
                    src={cat.image}
                    alt={cat.name}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                    onError={(e) => {
                      e.target.src = 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop';
                    }}
                  />
                </div>
                <div className="p-3 bg-white text-center">
                  <p className="font-semibold text-gray-900 text-sm">{cat.name}</p>
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Premium Phones */}
        {premiumPhones.length > 0 && (
          <div className="py-6">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-bold text-gray-900">📱 Premium Smartphones</h2>
              <button 
                onClick={() => navigate('/search?q=premium')}
                className="text-sm text-purple-600 font-medium"
              >
                View All
              </button>
            </div>
            <div className="grid grid-cols-5 gap-4">
              {premiumPhones.map((product) => (
                <ProductCard key={product.id} product={product} />
              ))}
            </div>
          </div>
        )}

        {/* Budget Phones */}
        {budgetPhones.length > 0 && (
          <div className="py-6">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-bold text-gray-900">📱 Budget Phones Under ₹20,000</h2>
              <button 
                onClick={() => navigate('/search?q=budget')}
                className="text-sm text-purple-600 font-medium"
              >
                View All
              </button>
            </div>
            <div className="grid grid-cols-5 gap-4">
              {budgetPhones.map((product) => (
                <ProductCard key={product.id} product={product} />
              ))}
            </div>
          </div>
        )}

        {/* Mobile Phones */}
        {mobilePhones.length > 0 && (
          <div className="py-6">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-bold text-gray-900">📱 All Mobile Phones</h2>
              <button 
                onClick={() => navigate('/category/Electronics')}
                className="text-sm text-purple-600 font-medium"
              >
                View All
              </button>
            </div>
            <div className="grid grid-cols-5 gap-4">
              {mobilePhones.slice(0, 10).map((product) => (
                <ProductCard key={product.id} product={product} />
              ))}
            </div>
          </div>
        )}

        {/* Electronics */}
        {electronics.length > 0 && (
          <div className="py-6">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-bold text-gray-900">🎧 Electronics & Gadgets</h2>
              <button 
                onClick={() => navigate('/category/Electronics')}
                className="text-sm text-purple-600 font-medium"
              >
                View All
              </button>
            </div>
            <div className="grid grid-cols-5 gap-4">
              {electronics.map((product) => (
                <ProductCard key={product.id} product={product} />
              ))}
            </div>
          </div>
        )}

        {/* Best Deals Carousel */}
        {bestDeals.length > 0 && (
          <div className="py-6">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-bold text-gray-900">🔥 Best Deals</h2>
              <button 
                onClick={() => navigate('/search?q=discount')}
                className="text-sm text-purple-600 font-medium"
              >
                View All
              </button>
            </div>
            <div className="grid grid-cols-5 gap-4">
              {bestDeals.map((product) => (
                <ProductCard key={product.id} product={product} />
              ))}
            </div>
          </div>
        )}

        {/* Trending Now */}
        {trendingProducts.length > 0 && (
          <div className="py-6">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-bold text-gray-900">⭐ Trending Now</h2>
              <button 
                onClick={() => navigate('/search?q=rating')}
                className="text-sm text-purple-600 font-medium"
              >
                View All
              </button>
            </div>
            <div className="grid grid-cols-5 gap-4">
              {trendingProducts.map((product) => (
                <ProductCard key={product.id} product={product} />
              ))}
            </div>
          </div>
        )}

        {/* Fashion For You */}
        {fashionProducts.length > 0 && (
          <div className="py-6">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-bold text-gray-900">👗 Fashion For You</h2>
              <button 
                onClick={() => navigate('/category/Fashion')}
                className="text-sm text-purple-600 font-medium"
              >
                View All
              </button>
            </div>
            <div className="grid grid-cols-5 gap-4">
              {fashionProducts.map((product) => (
                <ProductCard key={product.id} product={product} />
              ))}
            </div>
          </div>
        )}

        {/* Home & Kitchen */}
        {homeProducts.length > 0 && (
          <div className="py-6">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-bold text-gray-900">🏠 Home & Kitchen</h2>
              <button 
                onClick={() => navigate('/category/Home')}
                className="text-sm text-purple-600 font-medium"
              >
                View All
              </button>
            </div>
            <div className="grid grid-cols-5 gap-4">
              {homeProducts.map((product) => (
                <ProductCard key={product.id} product={product} />
              ))}
            </div>
          </div>
        )}

        {/* Products Section with Filters */}
        <div className="mt-8">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-2xl font-bold text-gray-900">Products For You</h2>
            
            {/* Desktop Filters */}
            <div className="flex gap-3">
              <select 
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
                className="border border-gray-300 rounded px-3 py-1 text-sm"
              >
                <option value="">All Categories</option>
                <option value="Electronics">Electronics</option>
                <option value="Fashion">Fashion</option>
                <option value="Home">Home & Kitchen</option>
                <option value="Mobile">Mobile Phones</option>
              </select>
              
              <select 
                value={selectedGender}
                onChange={(e) => setSelectedGender(e.target.value)}
                className="border border-gray-300 rounded px-3 py-1 text-sm"
              >
                <option value="">All Genders</option>
                {genderOptions.map(gender => (
                  <option key={gender} value={gender}>{gender}</option>
                ))}
              </select>
              
              <select 
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                className="border border-gray-300 rounded px-3 py-1 text-sm"
              >
                <option value="">Sort By</option>
                {sortOptions.map(option => (
                  <option key={option.value} value={option.value}>{option.label}</option>
                ))}
              </select>
              
              <button 
                onClick={resetFilters}
                className="border border-gray-300 rounded px-3 py-1 text-sm text-purple-600"
              >
                Reset
              </button>
            </div>
          </div>
          
          {filteredProducts.length > 0 ? (
            <div className="grid grid-cols-4 gap-4">
              {filteredProducts.map((product) => (
                <ProductCard key={product.id || product._id} product={product} />
              ))}
            </div>
          ) : (
            <div className="text-center py-12">
              <p className="text-gray-500">No products available</p>
              <button
                onClick={fetchProducts}
                className="mt-4 px-4 py-2 bg-[#9c1c80] text-white rounded"
              >
                Retry
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Home;