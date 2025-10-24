import React from 'react';
import Slider from 'react-slick';
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';

const OffersBanner = () => {
  const settings = {
    dots: true,
    infinite: true,
    speed: 500,
    slidesToShow: 1,
    slidesToScroll: 1,
    autoplay: true,
    autoplaySpeed: 3000,
    arrows: false,
  };

  const banners = [
    {
      id: 1,
      title: "MEGA SALE",
      subtitle: "Up to 70% OFF",
      description: "On All Electronics",
      bgColor: "bg-gradient-to-r from-pink-500 to-purple-600",
      textColor: "text-white"
    },
    {
      id: 2,
      title: "FLASH DEALS",
      subtitle: "Upto 60% OFF",
      description: "Limited Time Offer",
      bgColor: "bg-gradient-to-r from-orange-500 to-red-600",
      textColor: "text-white"
    },
    {
      id: 3,
      title: "SPECIAL OFFERS",
      subtitle: "Extra 10% OFF",
      description: "On Orders Above ₹999",
      bgColor: "bg-gradient-to-r from-green-500 to-teal-600",
      textColor: "text-white"
    },
    {
      id: 4,
      title: "FREE DELIVERY",
      subtitle: "On All Orders",
      description: "No Minimum Purchase",
      bgColor: "bg-gradient-to-r from-blue-500 to-cyan-600",
      textColor: "text-white"
    }
  ];

  return (
    <div className="mb-4">
      <Slider {...settings}>
        {banners.map((banner) => (
          <div key={banner.id}>
            <div className={`${banner.bgColor} ${banner.textColor} rounded-lg mx-2 p-6 md:p-8`}>
              <div className="text-center">
                <h2 className="text-2xl md:text-3xl font-bold mb-2">{banner.title}</h2>
                <p className="text-3xl md:text-4xl font-extrabold mb-2">{banner.subtitle}</p>
                <p className="text-lg md:text-xl">{banner.description}</p>
              </div>
            </div>
          </div>
        ))}
      </Slider>
    </div>
  );
};

export default OffersBanner;
