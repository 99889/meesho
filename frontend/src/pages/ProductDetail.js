import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Star, Heart, Share2, ShoppingCart, Truck, RotateCcw, StarHalf, ChevronLeft, ChevronRight } from 'lucide-react';
import { productAPI } from '../services/api';
import axios from 'axios';
import { Button } from '../components/ui/button';
import { Card } from '../components/ui/card';
import { useCart } from '../context/CartContext';
import { Badge } from '../components/ui/badge';
import { Progress } from '../components/ui/progress';
import ProductCard from '../components/ProductCard';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const ProductDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [product, setProduct] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [ratingDistribution, setRatingDistribution] = useState({});
  const [loading, setLoading] = useState(true);
  const [recommendedProducts, setRecommendedProducts] = useState([]);
  const [recommendedLoading, setRecommendedLoading] = useState(false);
  const { addToCart, addToWishlist, isInWishlist } = useCart();
  
  const [selectedSize, setSelectedSize] = useState(null);
  const [selectedColor, setSelectedColor] = useState(null);
  const [quantity, setQuantity] = useState(1);
  const [selectedImageIndex, setSelectedImageIndex] = useState(0);
  const [currentImageIndex, setCurrentImageIndex] = useState(0);

  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      await fetchProduct();
      setLoading(false);
    };
    loadData();
  }, [id]);

  // Fetch reviews and recommended products after product is loaded
  useEffect(() => {
    if (product && product.name) {
      fetchReviews();
      fetchRecommendedProducts();
    }
  }, [product]);

  const fetchProduct = async () => {
    try {
      const data = await productAPI.getById(id);
      setProduct(data.product);
    } catch (error) {
      console.error('Error fetching product:', error);
    }
  };

  const fetchReviews = async () => {
    try {
      // Wait for product to be loaded first
      if (!product || !product.name) {
        return;
      }
      
      // Use product name to fetch reviews (reviews are keyed by product name)
      const response = await axios.get(`${API}/reviews/product/${encodeURIComponent(product.name)}`);
      setReviews(response.data.reviews || []);
      setRatingDistribution(response.data.rating_distribution || {});
    } catch (error) {
      console.error('Error fetching reviews:', error);
      setReviews([]);
    }
  };

  const fetchRecommendedProducts = async () => {
    try {
      setRecommendedLoading(true);
      // Fetch products from the same category, excluding the current product
      if (product && product.category) {
        const response = await productAPI.getByCategory(product.category);
        // Filter out the current product and limit to 6 products
        const filteredProducts = (response.products || [])
          .filter(p => p.id !== product.id)
          .slice(0, 6);
        setRecommendedProducts(filteredProducts);
      }
    } catch (error) {
      console.error('Error fetching recommended products:', error);
    } finally {
      setRecommendedLoading(false);
    }
  };

  const nextImage = () => {
    const images = product.images || [product.image];
    setCurrentImageIndex((prevIndex) => (prevIndex + 1) % images.length);
  };

  const prevImage = () => {
    const images = product.images || [product.image];
    setCurrentImageIndex((prevIndex) => (prevIndex - 1 + images.length) % images.length);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-pink-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600">Loading product...</p>
        </div>
      </div>
    );
  }

  if (!product) {
    return (
      <div className="container mx-auto px-4 py-16 text-center">
        <h2 className="text-2xl font-bold mb-4">Product Not Found</h2>
        <Button onClick={() => navigate('/')}>Go Back Home</Button>
      </div>
    );
  }

  const handleAddToCart = () => {
    // Automatically select first available option if not selected
    const sizeToUse = selectedSize || (product.sizes && product.sizes.length > 0 ? product.sizes[0] : null);
    const colorToUse = selectedColor || (product.colors && product.colors.length > 0 ? product.colors[0] : null);
    
    addToCart(product, quantity, sizeToUse, colorToUse);
  };

  const handleShare = () => {
    if (navigator.share) {
      navigator.share({
        title: product.name,
        text: `Check out ${product.name} on Meesho`,
        url: window.location.href,
      });
    }
  };

  const renderStars = (rating) => {
    const stars = [];
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 !== 0;
    
    for (let i = 0; i < fullStars; i++) {
      stars.push(<Star key={i} className="w-4 h-4 fill-yellow-400 text-yellow-400" />);
    }
    if (hasHalfStar) {
      stars.push(<StarHalf key="half" className="w-4 h-4 fill-yellow-400 text-yellow-400" />);
    }
    for (let i = stars.length; i < 5; i++) {
      stars.push(<Star key={i} className="w-4 h-4 text-gray-300" />);
    }
    return stars;
  };

  // Get all images or fallback to single image
  const productImages = product.images && product.images.length > 0 ? product.images : [product.image];
  const currentImage = productImages[currentImageIndex];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Mobile Fixed Bottom Bar */}
      <div className="md:hidden fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 z-50 p-3 shadow-lg">
        <div className="flex gap-2">
          <Button
            variant="outline"
            className="flex-1"
            onClick={() => isInWishlist(product.id) ? null : addToWishlist(product)}
          >
            <Heart className={`w-4 h-4 ${isInWishlist(product.id) ? 'fill-pink-600 text-pink-600' : ''}`} />
          </Button>
          <Button
            className="flex-1 bg-pink-600 hover:bg-pink-700"
            onClick={handleAddToCart}
          >
            <ShoppingCart className="w-4 h-4 mr-2" />
            Add to Cart
          </Button>
          <Button
            className="flex-1 bg-purple-600 hover:bg-purple-700 text-white"
            onClick={() => {
              handleAddToCart();
              navigate('/cart');
            }}
          >
            Buy Now
          </Button>
        </div>
      </div>

      <div className="container mx-auto px-4 md:pb-8 pt-4">
        <div className="grid md:grid-cols-2 gap-6">
          {/* Product Image */}
          <div className="bg-white rounded-lg p-4 md:sticky md:top-24 md:h-fit">
            {/* Main Image with Navigation */}
            <div className="relative">
              <img
                src={currentImage}
                alt={product.name}
                className="w-full h-80 md:h-[500px] object-contain rounded-lg"
              />
              
              {/* Navigation Arrows */}
              {productImages.length > 1 && (
                <>
                  <button
                    onClick={prevImage}
                    className="absolute left-2 top-1/2 -translate-y-1/2 bg-white/70 hover:bg-white rounded-full p-2 shadow-md"
                  >
                    <ChevronLeft className="w-6 h-6" />
                  </button>
                  <button
                    onClick={nextImage}
                    className="absolute right-2 top-1/2 -translate-y-1/2 bg-white/70 hover:bg-white rounded-full p-2 shadow-md"
                  >
                    <ChevronRight className="w-6 h-6" />
                  </button>
                </>
              )}
              
              {/* Image Counter */}
              {productImages.length > 1 && (
                <div className="absolute bottom-4 left-1/2 -translate-x-1/2 bg-black/50 text-white text-sm px-2 py-1 rounded">
                  {currentImageIndex + 1} / {productImages.length}
                </div>
              )}
            </div>
            
            {/* Thumbnail images */}
            {productImages.length > 1 && (
              <div className="flex gap-2 mt-4 overflow-x-auto pb-2">
                {productImages.map((image, index) => (
                  <button
                    key={index}
                    onClick={() => setCurrentImageIndex(index)}
                    className={`flex-shrink-0 w-16 h-16 rounded border-2 ${currentImageIndex === index ? 'border-pink-600' : 'border-gray-200'}`}
                  >
                    <img
                      src={image}
                      alt={`${product.name} ${index + 1}`}
                      className="w-full h-full object-cover rounded"
                    />
                  </button>
                ))}
              </div>
            )}
            
            <div className="hidden md:flex gap-2 mt-4 justify-center">
              <Button
                variant="outline"
                className="flex-1"
                onClick={() => isInWishlist(product.id) ? null : addToWishlist(product)}
              >
                <Heart className={`w-4 h-4 mr-2 ${isInWishlist(product.id) ? 'fill-pink-600 text-pink-600' : ''}`} />
                {isInWishlist(product.id) ? 'In Wishlist' : 'Add to Wishlist'}
              </Button>
              <Button variant="outline" onClick={handleShare}>
                <Share2 className="w-4 h-4 mr-2" />
                Share
              </Button>
            </div>
          </div>

          {/* Product Details */}
          <div className="md:pb-0 pb-20">
            <Card className="p-4 md:p-6 mb-4">
              <h1 className="text-xl md:text-3xl font-bold mb-2 text-gray-900">{product.name}</h1>
              
              <div className="flex items-center gap-3 mb-4">
                <div className="flex items-center bg-green-600 text-white px-2 py-1 rounded gap-1">
                  <span className="font-semibold">{product.rating}</span>
                  <Star className="w-4 h-4 fill-white" />
                </div>
                <span className="text-gray-600">({product.reviews} reviews)</span>
              </div>

              <div className="flex items-center gap-3 mb-4">
                <span className="text-2xl md:text-3xl font-bold text-gray-900">₹{product.price}</span>
                {product.original_price && (
                  <>
                    <span className="text-lg md:text-xl text-gray-500 line-through">₹{product.original_price}</span>
                    <Badge className="bg-pink-600">{product.discount}% OFF</Badge>
                  </>
                )}
              </div>

              <p className="text-gray-600 mb-4 text-sm md:text-base">{product.description}</p>

              {/* Product Details */}
              <div className="border-t border-gray-200 pt-4 mb-4 space-y-2">
                {product.material && (
                  <div className="flex justify-between">
                    <span className="text-gray-600">Material:</span>
                    <span className="font-medium">{product.material}</span>
                  </div>
                )}
                {product.occasion && (
                  <div className="flex justify-between">
                    <span className="text-gray-600">Occasion:</span>
                    <span className="font-medium">{product.occasion}</span>
                  </div>
                )}
                {product.care_instructions && (
                  <div className="flex justify-between">
                    <span className="text-gray-600">Care:</span>
                    <span className="font-medium text-sm">{product.care_instructions}</span>
                  </div>
                )}
              </div>

              <div className="border-t border-gray-200 pt-4 mb-4">
                <div className="flex items-center gap-2 text-green-600 mb-2">
                  <Truck className="w-5 h-5" />
                  <span className="font-medium">Free Delivery</span>
                </div>
                <div className="flex items-center gap-2 text-gray-600 mb-2">
                  <RotateCcw className="w-5 h-5" />
                  <span>{product.return_policy}</span>
                </div>
                <div className="flex items-center gap-2 text-gray-600">
                  {product.cod ? (
                    <span className="text-green-600 font-medium">✓ COD Available</span>
                  ) : (
                    <span className="text-red-600 font-medium">✗ COD Not Available</span>
                  )}
                </div>
              </div>
            </Card>

            {/* Size Selection */}
            {product.sizes && product.sizes.length > 1 && (
              <Card className="p-4 md:p-6 mb-4">
                <h3 className="font-semibold mb-3 text-gray-900">Select Size</h3>
                <div className="flex flex-wrap gap-2">
                  {product.sizes.map((size) => (
                    <Button
                      key={size}
                      variant={selectedSize === size ? 'default' : 'outline'}
                      className={selectedSize === size ? 'bg-pink-600 hover:bg-pink-700' : ''}
                      onClick={() => setSelectedSize(size)}
                    >
                      {size}
                    </Button>
                  ))}
                </div>
              </Card>
            )}

            {/* Color Selection */}
            {product.colors && product.colors.length > 1 && (
              <Card className="p-4 md:p-6 mb-4">
                <h3 className="font-semibold mb-3 text-gray-900">Select Color</h3>
                <div className="flex flex-wrap gap-2">
                  {product.colors.map((color) => (
                    <Button
                      key={color}
                      variant={selectedColor === color ? 'default' : 'outline'}
                      className={selectedColor === color ? 'bg-pink-600 hover:bg-pink-700' : ''}
                      onClick={() => setSelectedColor(color)}
                    >
                      {color}
                    </Button>
                  ))}
                </div>
              </Card>
            )}

            {/* Desktop Quantity & Actions - Hidden on mobile */}
            <div className="hidden md:block">
              <Card className="p-6 mb-4">
                <h3 className="font-semibold mb-3 text-gray-900">Quantity</h3>
                <div className="flex items-center gap-3 mb-4">
                  <Button
                    variant="outline"
                    onClick={() => setQuantity(Math.max(1, quantity - 1))}
                  >
                    -
                  </Button>
                  <span className="text-lg font-semibold w-12 text-center">{quantity}</span>
                  <Button
                    variant="outline"
                    onClick={() => setQuantity(quantity + 1)}
                  >
                    +
                  </Button>
                </div>

                <div className="flex gap-3">
                  <Button
                    className="flex-1 bg-pink-600 hover:bg-pink-700"
                    onClick={handleAddToCart}
                  >
                    <ShoppingCart className="w-4 h-4 mr-2" />
                    Add to Cart
                  </Button>
                  <Button
                    variant="outline"
                    className="flex-1"
                    onClick={() => {
                      handleAddToCart();
                      navigate('/cart');
                    }}
                  >
                    Buy Now
                  </Button>
                </div>
              </Card>
            </div>

            {/* Mobile Quantity Selector - Visible only on mobile */}
            <div className="md:hidden bg-white rounded-lg p-4 mb-4">
              <h3 className="font-semibold mb-3 text-gray-900">Quantity</h3>
              <div className="flex items-center gap-3 mb-4">
                <Button
                  variant="outline"
                  onClick={() => setQuantity(Math.max(1, quantity - 1))}
                  className="w-10 h-10"
                >
                  -
                </Button>
                <span className="text-lg font-semibold w-12 text-center">{quantity}</span>
                <Button
                  variant="outline"
                  onClick={() => setQuantity(quantity + 1)}
                  className="w-10 h-10"
                >
                  +
                </Button>
              </div>
            </div>

            {/* Seller Info */}
            <Card className="p-4 md:p-6 mb-4">
              <h3 className="font-semibold mb-2 text-gray-900">Seller Information</h3>
              <p className="text-gray-600">Sold by: <span className="font-medium">{product.seller || product.seller_name || 'Meesho Seller'}</span></p>
            </Card>
          </div>
        </div>

        {/* Product Details Section */}
        <div className="mt-6">
          <Card className="p-4 md:p-6 mb-6">
            <h2 className="text-xl md:text-2xl font-bold mb-6 text-gray-900">Product Details</h2>
            <div className="grid md:grid-cols-2 gap-6">
              <div className="space-y-3">
                <div className="flex justify-between py-2 border-b">
                  <span className="text-gray-600">Material:</span>
                  <span className="font-medium text-gray-900">{product.material || 'N/A'}</span>
                </div>
                <div className="flex justify-between py-2 border-b">
                  <span className="text-gray-600">Occasion:</span>
                  <span className="font-medium text-gray-900">{product.occasion || 'N/A'}</span>
                </div>
                <div className="flex justify-between py-2 border-b">
                  <span className="text-gray-600">Available Sizes:</span>
                  <span className="font-medium text-gray-900">{product.sizes ? product.sizes.join(', ') : 'N/A'}</span>
                </div>
              </div>
              <div className="space-y-3">
                <div className="flex justify-between py-2 border-b">
                  <span className="text-gray-600">Available Colors:</span>
                  <span className="font-medium text-gray-900">{product.colors ? product.colors.join(', ') : 'N/A'}</span>
                </div>
                <div className="flex justify-between py-2 border-b">
                  <span className="text-gray-600">Return Policy:</span>
                  <span className="font-medium text-gray-900">{product.return_policy || '7 days return'}</span>
                </div>
                <div className="flex justify-between py-2 border-b">
                  <span className="text-gray-600">Stock:</span>
                  <span className="font-medium text-green-600">{product.stock > 50 ? 'In Stock' : product.stock > 0 ? `Only ${product.stock} left` : 'Out of Stock'}</span>
                </div>
                <div className="flex justify-between py-2 border-b">
                  <span className="text-gray-600">Cash on Delivery:</span>
                  <span className={`font-medium ${product.cod ? 'text-green-600' : 'text-red-600'}`}>
                    {product.cod ? 'Available' : 'Not Available'}
                  </span>
                </div>
              </div>
            </div>
            <div className="mt-6 pt-6 border-t">
              <h3 className="font-semibold mb-3 text-gray-900">Care Instructions:</h3>
              <p className="text-gray-600">{product.care_instructions || 'N/A'}</p>
            </div>
          </Card>
        </div>

        {/* Reviews Section */}
        <div className="mt-6">
          <Card className="p-4 md:p-6">
            <h2 className="text-xl md:text-2xl font-bold mb-6 text-gray-900">Customer Reviews</h2>
            
            {/* Rating Overview */}
            <div className="grid md:grid-cols-2 gap-8 mb-8 pb-8 border-b">
              <div className="text-center">
                <div className="text-5xl font-bold text-gray-900 mb-2">{product.rating}</div>
                <div className="flex justify-center mb-2">{renderStars(product.rating)}</div>
                <p className="text-gray-600">{reviews.length} customer reviews</p>
              </div>
              
              <div className="space-y-2">
                {[5, 4, 3, 2, 1].map((star) => {
                  const count = reviews.filter(r => r.rating === star).length;
                  const percentage = reviews.length > 0 ? (count / reviews.length) * 100 : 0;
                  return (
                    <div key={star} className="flex items-center gap-3">
                      <span className="text-sm w-8">{star} ★</span>
                      <Progress value={percentage} className="flex-1 h-2" />
                      <span className="text-sm text-gray-600 w-12">{count}</span>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Reviews List */}
            <div className="space-y-6">
              {reviews.slice(0, 5).map((review) => (
                <div key={review.id} className="border-b pb-6 last:border-b-0">
                  <div className="flex justify-between mb-2">
                    <span className="font-semibold text-gray-900">{review.user_name}</span>
                    <div className="flex items-center gap-1">
                      {renderStars(review.rating)}
                      <span className="text-sm text-gray-600 ml-1">{review.rating}</span>
                    </div>
                  </div>
                  <p className="text-gray-600 mb-2">{review.comment}</p>
                  <div className="flex items-center gap-4 text-sm text-gray-500">
                    <span>{new Date(review.date).toLocaleDateString()}</span>
                    {review.verified && (
                      <span className="bg-green-100 text-green-800 px-2 py-1 rounded">Verified Purchase</span>
                    )}
                  </div>
                </div>
              ))}
              
              {reviews.length === 0 && (
                <p className="text-center text-gray-500 py-8">No reviews yet. Be the first to review this product!</p>
              )}
            </div>
          </Card>
        </div>

        {/* Recommended Products Section */}
        <div className="mt-6">
          <Card className="p-4 md:p-6">
            <h2 className="text-xl md:text-2xl font-bold mb-6 text-gray-900">Recommended Products</h2>
            
            {recommendedLoading ? (
              <div className="flex justify-center py-8">
                <div className="w-8 h-8 border-4 border-pink-600 border-t-transparent rounded-full animate-spin"></div>
              </div>
            ) : recommendedProducts.length > 0 ? (
              <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
                {recommendedProducts.map((product) => (
                  <ProductCard key={product.id} product={product} />
                ))}
              </div>
            ) : (
              <p className="text-center text-gray-500 py-8">No recommended products found.</p>
            )}
          </Card>
        </div>

        {/* PDF Documents Section */}
        {product.pdfDocuments && product.pdfDocuments.length > 0 && (
          <div className="mt-6">
            <Card className="p-4 md:p-6">
              <h2 className="text-xl md:text-2xl font-bold mb-6 text-gray-900">Product Documents</h2>
              <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
                {product.pdfDocuments.map((pdfUrl, index) => (
                  <a 
                    key={index}
                    href={pdfUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="relative group"
                  >
                    <div className="aspect-square rounded-md overflow-hidden border border-gray-200 flex flex-col items-center justify-center bg-gray-50 hover:bg-gray-100 transition-colors">
                      <div className="text-4xl mb-2">📄</div>
                      <p className="text-xs text-center px-2 truncate w-full">Document {index + 1}</p>
                    </div>
                    <div className="absolute inset-0 flex items-center justify-center bg-black bg-opacity-0 group-hover:bg-opacity-20 transition-all">
                      <div className="opacity-0 group-hover:opacity-100 bg-white rounded-full p-2 shadow-lg">
                        <svg className="w-5 h-5 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path>
                        </svg>
                      </div>
                    </div>
                  </a>
                ))}
              </div>
            </Card>
          </div>
        )}
      </div>
    </div>
  );
};

export default ProductDetail;