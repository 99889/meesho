import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const HomeIcon = ({ isActive }) => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M12 3L4 10v11h16V10L12 3z" fill={isActive ? "#800080" : "#9CA3AF"}/>
    <text x="12" y="17" textAnchor="middle" fill={isActive ? "#FFD700" : "#D1D5DB"} fontSize="10" fontWeight="bold">M</text>
  </svg>
);

const CategoryIcon = ({ isActive }) => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    {/* Single square border */}
    <rect x="4" y="4" width="16" height="16" rx="2" stroke={isActive ? "#800080" : "#9CA3AF"} strokeWidth="1.5" fill="white"/>
    {/* Dress icon inside the square - more detailed dress shape */}
    <path d="M12 7 L10 9 L10 12 L8 17 L16 17 L14 12 L14 9 L12 7 Z" fill={isActive ? "#800080" : "#9CA3AF"}/>
    <circle cx="12" cy="9" r="1" fill="white"/>
  </svg>
);

const MallIcon = ({ isActive }) => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <text x="12" y="17" textAnchor="middle" fill={isActive ? "#800080" : "#9CA3AF"} fontSize="18" fontWeight="bold" fontFamily="Arial, sans-serif">M</text>
  </svg>
);

const AccountIcon = ({ isActive }) => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle cx="12" cy="8" r="4" stroke={isActive ? "#800080" : "#9CA3AF"} strokeWidth="2" fill="none"/>
    <path d="M5 20C5 16.134 8.13401 13 12 13C15.866 13 19 16.134 19 20" stroke={isActive ? "#800080" : "#9CA3AF"} strokeWidth="2" fill="none"/>
  </svg>
);

const SearchIcon = ({ isActive }) => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle cx="11" cy="11" r="7" stroke={isActive ? "#800080" : "#9CA3AF"} strokeWidth="2" fill="none"/>
    <path d="M20 20L17 17" stroke={isActive ? "#800080" : "#9CA3AF"} strokeWidth="2" strokeLinecap="round"/>
  </svg>
);

export default function BottomNav() {
  const location = useLocation();
  const isActive = (path) => location.pathname === path;

  return (
    <div className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 md:hidden z-50">
      <div className="flex justify-around items-center h-16">
        <Link to="/" className="flex flex-col items-center justify-center w-1/5">
          <HomeIcon isActive={isActive('/')} />
          <span className={`text-[10px] mt-1 ${isActive('/') ? 'text-[#800080]' : 'text-gray-500'}`}>Home</span>
        </Link>

        <Link to="/categories" className="flex flex-col items-center justify-center w-1/5">
          <CategoryIcon isActive={isActive('/categories')} />
          <span className={`text-[10px] mt-1 ${isActive('/categories') ? 'text-[#800080]' : 'text-gray-500'}`}>Categories</span>
        </Link>

        <Link to="/mall" className="flex flex-col items-center justify-center w-1/5">
          <MallIcon isActive={isActive('/mall')} />
          <span className={`text-[10px] mt-1 ${isActive('/mall') ? 'text-[#800080]' : 'text-gray-500'}`}>Mall</span>
        </Link>

        <Link to="/account" className="flex flex-col items-center justify-center w-1/5">
          <AccountIcon isActive={isActive('/account')} />
          <span className={`text-[10px] mt-1 ${isActive('/account') ? 'text-[#800080]' : 'text-gray-500'}`}>Account</span>
        </Link>

        <Link to="/search" className="flex flex-col items-center justify-center w-1/5">
          <SearchIcon isActive={isActive('/search')} />
          <span className={`text-[10px] mt-1 ${isActive('/search') ? 'text-[#800080]' : 'text-gray-500'}`}>Search</span>
        </Link>
      </div>
    </div>
  );
}