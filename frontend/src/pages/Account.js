import React from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

const AccountPage = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  // Base account options
  const baseAccountOptions = [
    {
      title: "My Orders",
      description: "View your order history",
      icon: "📦",
      action: () => navigate('/orders')
    },
    {
      title: "My Wishlist",
      description: "Your saved items",
      icon: "❤️",
      action: () => navigate('/wishlist')
    },
    {
      title: "Address Book",
      description: "Manage delivery addresses",
      icon: "📍",
      action: () => console.log('Address book')
    },
    {
      title: "Payment Methods",
      description: "Saved payment options",
      icon: "💳",
      action: () => console.log('Payment methods')
    }
  ];

  // Add admin option if user is admin
  const accountOptions = user && (user.role === 'admin' || user.role === 'seller') 
    ? [
        ...baseAccountOptions,
        {
          title: "Admin Dashboard",
          description: "Manage products and orders",
          icon: "👑",
          action: () => navigate('/admin')
        }
      ]
    : baseAccountOptions;

  return (
    <div className="min-h-screen bg-gray-50 py-4 pb-16 md:pb-0">
      <div className="container mx-auto px-4">
        <h1 className="text-xl font-bold mb-4 text-gray-900 px-1">My Account</h1>
        
        {user ? (
          <>
            <div className="bg-white rounded-lg shadow-sm p-4 mb-4">
              <div className="flex items-center">
                <div className="w-12 h-12 rounded-full bg-[#9c1c80] flex items-center justify-center text-white font-bold text-lg mr-3">
                  {user.name?.charAt(0) || 'U'}
                </div>
                <div>
                  <h2 className="font-semibold">{user.name || 'User'}</h2>
                  <p className="text-gray-600 text-sm">{user.email || 'user@example.com'}</p>
                  {user.role && (user.role === 'admin' || user.role === 'seller') && (
                    <span className="inline-block mt-1 px-2 py-1 bg-purple-100 text-purple-800 text-xs rounded-full">
                      {user.role === 'admin' ? 'Administrator' : 'Seller'}
                    </span>
                  )}
                </div>
              </div>
            </div>
            
            <div className="grid grid-cols-2 gap-3">
              {accountOptions.map((option, index) => (
                <div 
                  key={index} 
                  className="bg-white rounded-lg shadow-sm p-4 hover:shadow-md transition-shadow cursor-pointer"
                  onClick={option.action}
                >
                  <div className="text-2xl mb-2">{option.icon}</div>
                  <h3 className="font-semibold text-sm mb-1">{option.title}</h3>
                  <p className="text-gray-600 text-xs">{option.description}</p>
                </div>
              ))}
            </div>
            
            <div className="mt-6 bg-white rounded-lg shadow-sm p-4">
              <button 
                onClick={logout}
                className="w-full py-3 bg-red-500 text-white rounded-lg font-medium hover:bg-red-600 transition-colors"
              >
                Logout
              </button>
            </div>
          </>
        ) : (
          <div className="bg-white rounded-lg shadow-sm p-8 text-center">
            <p className="text-gray-600 mb-4">You need to login to access your account</p>
            <button 
              onClick={() => navigate('/login')}
              className="px-6 py-3 bg-[#9c1c80] text-white rounded-lg font-medium hover:bg-[#7a1660] transition-colors"
            >
              Login
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default AccountPage;