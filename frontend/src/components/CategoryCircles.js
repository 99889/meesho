import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Smartphone, Shirt, User, Baby, Home, Sparkles, ShoppingBag } from 'lucide-react';

const CategoryCircles = () => {
  const navigate = useNavigate();

  const categories = [
    { name: 'Electronics', icon: Smartphone, color: 'bg-blue-100 text-blue-600' },
    { name: 'Women Ethnic', icon: Shirt, color: 'bg-pink-100 text-pink-600' },
    { name: 'Women Western', icon: Shirt, color: 'bg-purple-100 text-purple-600' },
    { name: 'Men', icon: User, color: 'bg-indigo-100 text-indigo-600' },
    { name: 'Kids', icon: Baby, color: 'bg-yellow-100 text-yellow-600' },
    { name: 'Home & Kitchen', icon: Home, color: 'bg-green-100 text-green-600' },
    { name: 'Beauty & Health', icon: Sparkles, color: 'bg-orange-100 text-orange-600' },
    { name: 'Bags & Footwear', icon: ShoppingBag, color: 'bg-red-100 text-red-600' },
  ];

  return (
    <div className="bg-white py-4 px-2 mb-4">
      <div className="flex gap-4 overflow-x-auto pb-2 scrollbar-hide">
        {categories.map((category) => (
          <div
            key={category.name}
            onClick={() => navigate(`/category/${category.name}`)}
            className="flex-shrink-0 flex flex-col items-center cursor-pointer"
          >
            <div className={`w-16 h-16 rounded-full ${category.color} flex items-center justify-center mb-2 transition-transform hover:scale-110`}>
              <category.icon className="w-8 h-8" />
            </div>
            <span className="text-xs text-center w-20 text-gray-700 font-medium">{category.name}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default CategoryCircles;
