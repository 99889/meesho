import React, { useState } from 'react';
import { ChevronDown, ChevronUp, X } from 'lucide-react';
import { Button } from './ui/button';
import { Card } from './ui/card';

const ProductFilter = ({ onFilterChange, categories = [] }) => {
  const [expandedFilters, setExpandedFilters] = useState({
    price: true,
    rating: true,
    category: true,
    delivery: true
  });

  const [filters, setFilters] = useState({
    priceRange: [0, 10000],
    minRating: 0,
    selectedCategories: [],
    deliveryType: [] // 'free', 'cod'
  });

  const toggleFilter = (filterName) => {
    setExpandedFilters(prev => ({
      ...prev,
      [filterName]: !prev[filterName]
    }));
  };

  const handlePriceChange = (type, value) => {
    const newRange = [...filters.priceRange];
    if (type === 'min') {
      newRange[0] = Math.min(parseInt(value) || 0, newRange[1]);
    } else {
      newRange[1] = Math.max(parseInt(value) || 10000, newRange[0]);
    }
    const updatedFilters = { ...filters, priceRange: newRange };
    setFilters(updatedFilters);
    onFilterChange(updatedFilters);
  };

  const handleRatingChange = (rating) => {
    const updatedFilters = { ...filters, minRating: rating };
    setFilters(updatedFilters);
    onFilterChange(updatedFilters);
  };

  const handleCategoryChange = (category) => {
    const newCategories = filters.selectedCategories.includes(category)
      ? filters.selectedCategories.filter(c => c !== category)
      : [...filters.selectedCategories, category];
    const updatedFilters = { ...filters, selectedCategories: newCategories };
    setFilters(updatedFilters);
    onFilterChange(updatedFilters);
  };

  const handleDeliveryChange = (type) => {
    const newDelivery = filters.deliveryType.includes(type)
      ? filters.deliveryType.filter(d => d !== type)
      : [...filters.deliveryType, type];
    const updatedFilters = { ...filters, deliveryType: newDelivery };
    setFilters(updatedFilters);
    onFilterChange(updatedFilters);
  };

  const clearFilters = () => {
    const clearedFilters = {
      priceRange: [0, 10000],
      minRating: 0,
      selectedCategories: [],
      deliveryType: []
    };
    setFilters(clearedFilters);
    onFilterChange(clearedFilters);
  };

  const hasActiveFilters = 
    filters.selectedCategories.length > 0 ||
    filters.minRating > 0 ||
    filters.deliveryType.length > 0 ||
    filters.priceRange[0] > 0 ||
    filters.priceRange[1] < 10000;

  return (
    <div className="space-y-4">
      {/* Clear Filters Button */}
      {hasActiveFilters && (
        <Button
          onClick={clearFilters}
          variant="outline"
          className="w-full text-[#9c1c80] border-[#9c1c80] hover:bg-pink-50"
        >
          <X className="w-4 h-4 mr-2" />
          Clear All Filters
        </Button>
      )}

      {/* Price Filter */}
      <Card className="p-4">
        <button
          onClick={() => toggleFilter('price')}
          className="w-full flex items-center justify-between font-semibold text-gray-900"
        >
          <span>Price Range</span>
          {expandedFilters.price ? (
            <ChevronUp className="w-5 h-5" />
          ) : (
            <ChevronDown className="w-5 h-5" />
          )}
        </button>
        {expandedFilters.price && (
          <div className="mt-4 space-y-3">
            <div>
              <label className="text-sm text-gray-600">Min Price: ₹{filters.priceRange[0]}</label>
              <input
                type="range"
                min="0"
                max="10000"
                value={filters.priceRange[0]}
                onChange={(e) => handlePriceChange('min', e.target.value)}
                className="w-full"
              />
            </div>
            <div>
              <label className="text-sm text-gray-600">Max Price: ₹{filters.priceRange[1]}</label>
              <input
                type="range"
                min="0"
                max="10000"
                value={filters.priceRange[1]}
                onChange={(e) => handlePriceChange('max', e.target.value)}
                className="w-full"
              />
            </div>
            <div className="flex gap-2">
              <input
                type="number"
                placeholder="Min"
                value={filters.priceRange[0]}
                onChange={(e) => handlePriceChange('min', e.target.value)}
                className="w-1/2 border border-gray-300 rounded px-2 py-1 text-sm"
              />
              <input
                type="number"
                placeholder="Max"
                value={filters.priceRange[1]}
                onChange={(e) => handlePriceChange('max', e.target.value)}
                className="w-1/2 border border-gray-300 rounded px-2 py-1 text-sm"
              />
            </div>
          </div>
        )}
      </Card>

      {/* Rating Filter */}
      <Card className="p-4">
        <button
          onClick={() => toggleFilter('rating')}
          className="w-full flex items-center justify-between font-semibold text-gray-900"
        >
          <span>Rating</span>
          {expandedFilters.rating ? (
            <ChevronUp className="w-5 h-5" />
          ) : (
            <ChevronDown className="w-5 h-5" />
          )}
        </button>
        {expandedFilters.rating && (
          <div className="mt-4 space-y-2">
            {[4, 3, 2, 1].map((rating) => (
              <label key={rating} className="flex items-center gap-2 cursor-pointer">
                <input
                  type="radio"
                  name="rating"
                  checked={filters.minRating === rating}
                  onChange={() => handleRatingChange(rating)}
                  className="w-4 h-4"
                />
                <span className="text-sm text-gray-700">
                  {rating}★ & above ({rating === 4 ? '100+' : rating === 3 ? '500+' : '1000+'} reviews)
                </span>
              </label>
            ))}
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="radio"
                name="rating"
                checked={filters.minRating === 0}
                onChange={() => handleRatingChange(0)}
                className="w-4 h-4"
              />
              <span className="text-sm text-gray-700">All ratings</span>
            </label>
          </div>
        )}
      </Card>

      {/* Category Filter */}
      {categories.length > 0 && (
        <Card className="p-4">
          <button
            onClick={() => toggleFilter('category')}
            className="w-full flex items-center justify-between font-semibold text-gray-900"
          >
            <span>Category</span>
            {expandedFilters.category ? (
              <ChevronUp className="w-5 h-5" />
            ) : (
              <ChevronDown className="w-5 h-5" />
            )}
          </button>
          {expandedFilters.category && (
            <div className="mt-4 space-y-2">
              {categories.map((category) => (
                <label key={category.id} className="flex items-center gap-2 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={filters.selectedCategories.includes(category.name)}
                    onChange={() => handleCategoryChange(category.name)}
                    className="w-4 h-4"
                  />
                  <span className="text-sm text-gray-700">{category.name}</span>
                </label>
              ))}
            </div>
          )}
        </Card>
      )}

      {/* Delivery Type Filter */}
      <Card className="p-4">
        <button
          onClick={() => toggleFilter('delivery')}
          className="w-full flex items-center justify-between font-semibold text-gray-900"
        >
          <span>Delivery</span>
          {expandedFilters.delivery ? (
            <ChevronUp className="w-5 h-5" />
          ) : (
            <ChevronDown className="w-5 h-5" />
          )}
        </button>
        {expandedFilters.delivery && (
          <div className="mt-4 space-y-2">
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                checked={filters.deliveryType.includes('free')}
                onChange={() => handleDeliveryChange('free')}
                className="w-4 h-4"
              />
              <span className="text-sm text-gray-700">Free Delivery</span>
            </label>
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                checked={filters.deliveryType.includes('cod')}
                onChange={() => handleDeliveryChange('cod')}
                className="w-4 h-4"
              />
              <span className="text-sm text-gray-700">Cash on Delivery</span>
            </label>
          </div>
        )}
      </Card>
    </div>
  );
};

export default ProductFilter;
