import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { Search, ShoppingCart, Heart, User, Menu, X, Home, Grid3X3, ShoppingBag, HelpCircle, UserCircle, Bell, Store, Layers, Package, ShoppingCartIcon, PackageIcon, HeadphonesIcon, User2, Download, UserPlus } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useCart } from '../context/CartContext';
import { Button } from './ui/button';
import { Input } from './ui/input';

const Navbar = () => {
  const { user, logout } = useAuth();
  const { getCartCount, wishlist } = useCart();
  const navigate = useNavigate();
  const location = useLocation();
  const [searchQuery, setSearchQuery] = useState('');
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [userLocation, setUserLocation] = useState(null);
  const [locationError, setLocationError] = useState(null);

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/search?q=${searchQuery}`);
      setSearchQuery('');
    }
  };

  // Handle location request
  const handleLocationRequest = () => {
    if ('geolocation' in navigator) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const { latitude, longitude } = position.coords;
          setUserLocation({ latitude, longitude });
          setLocationError(null);
          // You can show a success message or update UI
          alert(`Location detected! Latitude: ${latitude.toFixed(4)}, Longitude: ${longitude.toFixed(4)}\n\nDiscounts are now available for your location! 🎉`);
        },
        (error) => {
          setLocationError(error.message);
          // If location is denied, show a friendly message
          alert('Please enable location access to see extra discounts in your area.');
        }
      );
    } else {
      alert('Geolocation is not supported by your browser.');
    }
  };

  // Function to check if the current route is active
  const isActive = (path) => {
    if (path === '/') {
      return location.pathname === '/';
    }
    return location.pathname.startsWith(path);
  };

  return (
    <>
      {/* ===== MOBILE NAVBAR ===== */}
      <nav className="md:hidden sticky top-0 z-50 bg-white shadow-sm">
        {/* Top Bar - Hamburger, Logo, Heart, Cart */}
        <div className="flex items-center px-4 py-3 border-b border-gray-100">
          {/* Hamburger Menu */}
          <button onClick={() => setMobileMenuOpen(!mobileMenuOpen)} className="mr-3">
            <Menu className="w-6 h-6 text-gray-700" />
          </button>

          {/* Logo */}
          <Link to="/" className="flex items-center">
            <div className="text-xl font-bold text-[#4a1e41]">meesho</div>
          </Link>

          {/* Spacer */}
          <div className="flex-1"></div>

          {/* Right Icons */}
          <div className="flex items-center gap-4">
            {/* Wishlist/Heart Icon */}
            <Link to="/wishlist" className="relative">
              <Heart className="w-6 h-6 text-red-500 fill-red-500" />
              {wishlist.length > 0 && (
                <span className="absolute -top-1.5 -right-1.5 bg-red-500 text-white text-[10px] rounded-full w-4 h-4 flex items-center justify-center font-semibold">
                  {wishlist.length}
                </span>
              )}
            </Link>

            {/* Cart Icon */}
            <Link to="/cart" className="relative">
              <ShoppingCart className="w-6 h-6 text-[#9c1c80]" />
              {getCartCount() > 0 && (
                <span className="absolute -top-1.5 -right-1.5 bg-[#9c1c80] text-white text-[10px] rounded-full w-4 h-4 flex items-center justify-center font-semibold">
                  {getCartCount()}
                </span>
              )}
            </Link>
          </div>
        </div>

        {/* Search Bar - Full Width */}
        <form onSubmit={handleSearch} className="px-4 py-3 bg-white border-b border-gray-100">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
            <Input
              id="mobile-search-input"
              type="text"
              placeholder="Search for Sarees, Kurtis, Cosmetics, etc."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-sm focus:border-[#9c1c80] focus:outline-none focus:ring-1 focus:ring-[#9c1c80]"
            />
          </div>
        </form>

        {/* Delivery Location Banner */}
        <button
          onClick={handleLocationRequest}
          className="w-full flex items-center gap-2 px-4 py-2.5 bg-blue-50 border-b border-gray-100 hover:bg-blue-100 transition"
        >
          <Bell className="w-4 h-4 text-blue-600 flex-shrink-0" />
          <span className="text-xs text-gray-700 flex-1 text-left">
            {userLocation 
              ? `Location set ✓ - Extra discounts available!`
              : `Add delivery location to check extra discount`
            }
          </span>
          <span className="text-gray-400 text-xs">»»»</span>
        </button>
      </nav>

      {/* ===== DESKTOP NAVBAR ===== */}
      <nav className="hidden md:block sticky top-0 z-50 bg-white shadow-sm">
        <div className="container mx-auto px-4 py-3">
          <div className="flex items-center gap-4">
            {/* Logo - Left aligned */}
            <Link to="/" className="flex items-center">
              <div className="text-2xl font-bold text-[#6e2e61]">Meesho</div>
            </Link>

            {/* Search Bar */}
            <form onSubmit={handleSearch} className="flex-1 max-w-2xl">
              <div className="relative">
                <Input
                  type="text"
                  placeholder="Search for Sarees, Kurtis, Cosmetics, etc."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pr-12 py-3 border border-gray-300 focus:border-[#9c1c80] rounded-lg"
                />
                <Button
                  type="submit"
                  size="sm"
                  className="absolute right-1 top-1/2 -translate-y-1/2 bg-[#9c1c80] hover:bg-[#7a1660] rounded-lg"
                >
                  <Search className="w-4 h-4" />
                </Button>
              </div>
            </form>

            {/* Desktop Menu */}
            <div className="flex items-center gap-4">
              {/* Wishlist */}
              <Link to="/wishlist" className="relative">
                <Button variant="ghost" size="sm" className="flex items-center gap-2">
                  <Heart className="w-5 h-5 text-red-500 fill-red-500" />
                  <span className="hidden lg:inline">Wishlist</span>
                  {wishlist.length > 0 && (
                    <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                      {wishlist.length}
                    </span>
                  )}
                </Button>
              </Link>

              {/* Cart */}
              <Link to="/cart" className="relative">
                <Button variant="ghost" size="sm" className="flex items-center gap-2">
                  <ShoppingCart className="w-5 h-5 text-[#9c1c80]" />
                  <span className="hidden lg:inline">Cart</span>
                  {getCartCount() > 0 && (
                    <span className="absolute -top-1 -right-1 bg-[#9c1c80] text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                      {getCartCount()}
                    </span>
                  )}
                </Button>
              </Link>

              {/* Profile */}
              {user ? (
                <div className="flex items-center gap-2">
                  <User className="w-5 h-5 text-gray-600" />
                  <span className="hidden lg:inline text-sm">{user.name}</span>
                </div>
              ) : (
                <Button
                  onClick={() => navigate('/login')}
                  size="sm"
                  className="bg-[#9c1c80] hover:bg-[#7a1660] text-white"
                >
                  Login
                </Button>
              )}
            </div>
          </div>

          {/* Delivery Location - Desktop */}
          <button 
            onClick={handleLocationRequest}
            className="mt-3 flex items-center gap-2 text-gray-600 hover:text-[#9c1c80] transition"
          >
            <Bell className="w-4 h-4 text-[#9c1c80]" />
            <span className="text-sm">
              {userLocation 
                ? `Location set ✓ - Extra discounts available!`
                : `Add delivery location to check extra discount`
              }
            </span>
          </button>
        </div>
      </nav>

      {/* Mobile Menu */}
      {mobileMenuOpen && (
        <div className="md:hidden bg-white shadow-lg">
          <div className="container mx-auto px-4 py-4">
            <div className="flex flex-col gap-3">
              <Link to="/wishlist" onClick={() => setMobileMenuOpen(false)}>
                <Button variant="ghost" className="w-full justify-start">
                  <Heart className="w-5 h-5 mr-2" />
                  Wishlist ({wishlist.length})
                </Button>
              </Link>
              <Link to="/cart" onClick={() => setMobileMenuOpen(false)}>
                <Button variant="ghost" className="w-full justify-start">
                  <ShoppingCart className="w-5 h-5 mr-2" />
                  Cart ({getCartCount()})
                </Button>
              </Link>
              {user ? (
                <>
                  <Link to="/account" onClick={() => setMobileMenuOpen(false)}>
                    <Button variant="ghost" className="w-full justify-start">
                      <User className="w-5 h-5 mr-2" />
                      My Account
                    </Button>
                  </Link>
                  <Button
                    variant="ghost"
                    className="w-full justify-start text-red-600"
                    onClick={() => {
                      logout();
                      setMobileMenuOpen(false);
                    }}
                  >
                    Logout
                  </Button>
                </>
              ) : (
                <Button
                  onClick={() => {
                    navigate('/login');
                    setMobileMenuOpen(false);
                  }}
                  className="w-full bg-[#9c1c80] hover:bg-[#7a1660] text-white"
                >
                  Login
                </Button>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Bottom Navigation Bar - Mobile Only - EXACT Meesho Match */}
      <div className="md:hidden fixed bottom-0 left-0 right-0 bg-[#f8f8f8] border-t border-gray-200 z-40">
        <div className="grid grid-cols-5">
          {/* Home - Filled house icon when active */}
          <Link 
            to="/" 
            className={`flex flex-col items-center justify-center py-3 gap-1.5 transition-colors ${isActive('/') ? 'text-[#9f2089]' : 'text-gray-500'}`}
          >
            {isActive('/') ? (
              <svg className="w-[28px] h-[28px]" viewBox="0 0 24 24" fill="currentColor">
                <path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/>
              </svg>
            ) : (
              <svg className="w-[28px] h-[28px]" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
                <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
                <polyline points="9 22 9 12 15 12 15 22"/>
              </svg>
            )}
            <span className="text-[10.5px] font-medium">Home</span>
          </Link>
          
          {/* Categories - Four squares grid */}
          <Link 
            to="/categories" 
            className={`flex flex-col items-center justify-center py-3 gap-1.5 transition-colors ${isActive('/categories') ? 'text-[#9f2089]' : 'text-gray-500'}`}
          >
            <svg className="w-[28px] h-[28px]" viewBox="0 0 24 24" fill={isActive('/categories') ? 'currentColor' : 'none'} stroke="currentColor" strokeWidth={1.5}>
              <rect x="3" y="3" width="7.5" height="7.5" rx="1.5"/>
              <rect x="13.5" y="3" width="7.5" height="7.5" rx="1.5"/>
              <rect x="3" y="13.5" width="7.5" height="7.5" rx="1.5"/>
              <rect x="13.5" y="13.5" width="7.5" height="7.5" rx="1.5"/>
            </svg>
            <span className="text-[10.5px] font-medium">Categories</span>
          </Link>
          
          {/* Mall - M shape */}
          <Link 
            to="/mall" 
            className={`flex flex-col items-center justify-center py-3 gap-1.5 transition-colors ${isActive('/mall') ? 'text-[#9f2089]' : 'text-gray-500'}`}
          >
            <svg className="w-[28px] h-[28px]" viewBox="0 0 24 24" fill={isActive('/mall') ? 'currentColor' : 'none'} stroke="currentColor" strokeWidth={1.5}>
              <path d="M4 21V11L7.5 6L12 11L16.5 6L20 11V21"/>
              <line x1="4" y1="21" x2="20" y2="21"/>
            </svg>
            <span className="text-[10.5px] font-medium">Mall</span>
          </Link>
          
          {/* Help - Question mark in circle */}
          <Link 
            to="/help" 
            className={`flex flex-col items-center justify-center py-3 gap-1.5 transition-colors ${isActive('/help') ? 'text-[#9f2089]' : 'text-gray-500'}`}
          >
            <svg className="w-[28px] h-[28px]" viewBox="0 0 24 24" fill={isActive('/help') ? 'currentColor' : 'none'} stroke="currentColor" strokeWidth={1.5}>
              <circle cx="12" cy="12" r="10"/>
              <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/>
              <circle cx="12" cy="17" r="1" fill="currentColor"/>
            </svg>
            <span className="text-[10.5px] font-medium">Help</span>
          </Link>
          
          {/* Account - Smiley face */}
          <Link 
            to="/account" 
            className={`flex flex-col items-center justify-center py-3 gap-1.5 transition-colors ${isActive('/account') ? 'text-[#9f2089]' : 'text-gray-500'}`}
          >
            <svg className="w-[28px] h-[28px]" viewBox="0 0 24 24" fill={isActive('/account') ? 'currentColor' : 'none'} stroke="currentColor" strokeWidth={1.5}>
              <circle cx="12" cy="12" r="10"/>
              <path d="M8 14s1.5 2 4 2 4-2 4-2"/>
              <circle cx="9" cy="9" r="1" fill="currentColor"/>
              <circle cx="15" cy="9" r="1" fill="currentColor"/>
            </svg>
            <span className="text-[10.5px] font-medium">Account</span>
          </Link>
        </div>
      </div>
    </>
  );
};

export default Navbar;