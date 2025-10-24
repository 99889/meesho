import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Heart, Star } from 'lucide-react';
import { Card, CardContent } from './ui/card';
import { Button } from './ui/button';
import { useCart } from '../context/CartContext';

const ProductCard = ({ product }) => {
  const navigate = useNavigate();
  const { addToWishlist, isInWishlist, removeFromWishlist } = useCart();

  const handleWishlistClick = (e) => {
    e.stopPropagation();
    if (isInWishlist(product.id)) {
      removeFromWishlist(product.id);
    } else {
      addToWishlist(product);
    }
  };

  // Handle both API and mock data structures
  const productName = product.name || product.title || 'Unknown Product';
  const productPrice = product.price || product.currentPrice || 0;
  const productOriginalPrice = product.original_price || product.originalPrice;
  const productDiscount = product.discount || 0;
  const productRating = product.rating || 0;
  const productReviews = product.reviews || product.reviewCount || 0;
  // Use the first image from the images array or fallback to the single image
  const productImage = (product.images && product.images[0]) || product.image || product.imageUrl || 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop';
  const productFreeDelivery = product.free_delivery !== undefined ? product.free_delivery : (product.freeDelivery || false);

  return (
    <Card 
      className="group cursor-pointer hover:shadow-md transition-all duration-300 border border-gray-200 overflow-hidden bg-white rounded-lg"
      onClick={() => navigate(`/product/${encodeURIComponent(productName)}`)}
    >
      <CardContent className="p-0">
        <div className="relative overflow-hidden">
          <img
            src={productImage}
            alt={productName}
            className="w-full h-48 object-cover group-hover:scale-105 transition-transform duration-300"
            onError={(e) => {
              e.target.src = 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop';
            }}
          />
          <Button
            variant="ghost"
            size="icon"
            className={`absolute top-2 right-2 rounded-full w-8 h-8 ${
              isInWishlist(product.id) ? 'bg-pink-100' : 'bg-white/80'
            } hover:bg-pink-100 transition-colors`}
            onClick={handleWishlistClick}
          >
            <Heart 
              className={`w-4 h-4 ${
                isInWishlist(product.id) ? 'fill-[#9c1c80] text-[#9c1c80]' : 'text-gray-600'
              }`}
            />
          </Button>
          {productDiscount > 0 && (
            <div className="absolute top-2 left-2 bg-[#9c1c80] text-white px-2 py-1 rounded text-xs font-semibold">
              {productDiscount}% OFF
            </div>
          )}
        </div>
        
        <div className="p-3">
          <h3 className="font-medium text-sm mb-1 line-clamp-2 text-gray-800">
            {productName}
          </h3>
          
          <div className="flex items-center gap-1 mb-1">
            <span className="text-base font-bold text-gray-900">₹{productPrice}</span>
            {productOriginalPrice && productOriginalPrice > productPrice && (
              <span className="text-xs text-gray-500 line-through">
                ₹{productOriginalPrice}
              </span>
            )}
          </div>
          
          <div className="flex items-center gap-1 mb-2">
            <div className="flex items-center bg-green-600 text-white px-1 py-0.5 rounded text-xs gap-0.5">
              <span>{productRating}</span>
              <Star className="w-2.5 h-2.5 fill-white" />
            </div>
            <span className="text-xs text-gray-500">({productReviews})</span>
          </div>
          
          <div className="flex gap-2 text-xs text-gray-600">
            {productFreeDelivery && (
              <span className="text-green-600 font-medium">Free Delivery</span>
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default ProductCard;