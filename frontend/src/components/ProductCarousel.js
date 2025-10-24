import React from 'react';
import Slider from 'react-slick';
import { useNavigate } from 'react-router-dom';
import { Star } from 'lucide-react';
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';

const ProductCarousel = ({ products, title }) => {
  const navigate = useNavigate();

  const settings = {
    dots: false,
    infinite: products.length > 4,
    speed: 500,
    slidesToShow: 4,
    slidesToScroll: 1,
    autoplay: true,
    autoplaySpeed: 3000,
    responsive: [
      {
        breakpoint: 1024,
        settings: {
          slidesToShow: 3,
          slidesToScroll: 1,
        }
      },
      {
        breakpoint: 768,
        settings: {
          slidesToShow: 2.5,
          slidesToScroll: 1,
        }
      },
      {
        breakpoint: 480,
        settings: {
          slidesToShow: 2.2,
          slidesToScroll: 1,
        }
      }
    ]
  };

  if (!products || products.length === 0) return null;

  return (
    <div className="mb-8">
      {title && (
        <h2 className="text-xl md:text-2xl font-bold mb-4 px-4 text-gray-900">{title}</h2>
      )}
      <div className="product-carousel px-2">
        <Slider {...settings}>
          {products.map((product, index) => (
            <div key={index} className="px-2">
              <div
                onClick={() => navigate(`/product/${encodeURIComponent(product.name)}`)}
                className="cursor-pointer bg-white rounded-lg border border-gray-200 overflow-hidden hover:shadow-md transition-shadow"
              >
                <div className="relative">
                  <img
                    src={product.image}
                    alt={product.name}
                    className="w-full h-40 md:h-48 object-cover"
                  />
                  {product.discount > 0 && (
                    <div className="absolute top-2 left-2 bg-yellow-400 text-xs font-bold px-2 py-1 rounded">
                      {product.discount}% OFF
                    </div>
                  )}
                </div>
                <div className="p-3">
                  <h3 className="text-sm font-medium text-gray-900 line-clamp-2 mb-2 h-10">
                    {product.name}
                  </h3>
                  <div className="flex items-center gap-2 mb-2">
                    <span className="text-lg font-bold text-gray-900">₹{product.price}</span>
                    {product.original_price > product.price && (
                      <span className="text-xs text-gray-500 line-through">
                        ₹{product.original_price}
                      </span>
                    )}
                  </div>
                  <div className="flex items-center gap-1">
                    <div className="flex items-center bg-green-600 text-white px-1.5 py-0.5 rounded text-xs">
                      <span className="font-semibold">{product.rating}</span>
                      <Star className="w-3 h-3 fill-white ml-0.5" />
                    </div>
                    <span className="text-xs text-gray-500">({product.reviews})</span>
                  </div>
                  {product.free_delivery && (
                    <div className="text-xs text-green-600 mt-2 font-medium">Free Delivery</div>
                  )}
                </div>
              </div>
            </div>
          ))}
        </Slider>
      </div>
    </div>
  );
};

export default ProductCarousel;
