import React from 'react';import React from 'react';

import { Link, useLocation } from 'react-router-dom';import { Link, useLocation } from 'react-router-dom';

import { Home, ShoppingBag, Store, User2, Search } from 'lucide-react';

export default function BottomNav() {

export default function BottomNav() {  const location = useLocation();

  const location = useLocation();  const isActive = (path) => location.pathname === path;

  const isActive = (path) => location.pathname === path;

  return (

  return (    <nav className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 md:hidden z-50">

    <nav className="fixed bottom-0 left-0 right-0 bg-white shadow-[0_-1px_3px_rgba(0,0,0,0.1)] md:hidden">      <div className="flex justify-around items-center h-[60px] px-2">

      <div className="flex justify-around items-center h-16">        {/* Home */}

        {/* Home */}        <Link to="/" className="flex flex-col items-center justify-center w-1/5">

        <Link           {isActive('/') ? (

          to="/"             <div className="flex flex-col items-center">

          className={`flex flex-col items-center space-y-1 ${isActive('/') ? 'text-[#f43397]' : 'text-gray-500'}`}              <div className="w-6 h-6 rounded-full bg-[#F43397] flex items-center justify-center mb-1">

        >                <span className="text-[#FFD700] text-sm font-bold">M</span>

          <div className={`w-6 h-6 flex items-center justify-center ${isActive('/') ? 'text-[#f43397]' : 'text-gray-500'}`}>              </div>

            {isActive('/') ? (              <span className="text-[10px] text-[#F43397]">Home</span>

              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">            </div>

                <path d="M12 3L4 10v11h16V10L12 3z" fill="#F43397"/>          ) : (

                <text x="12" y="17" textAnchor="middle" fill="#FFD700" fontSize="10" fontWeight="bold">M</text>            <div className="flex flex-col items-center">

              </svg>              <svg viewBox="0 0 24 24" className="w-6 h-6 text-gray-500 mb-1" fill="none" stroke="currentColor">

            ) : (                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />

              <Home size={24} />              </svg>

            )}              <span className="text-[10px] text-gray-500">Home</span>

          </div>            </div>

          <span className="text-xs font-medium">Home</span>          )}

        </Link>        </Link>



        {/* Categories */}        {/* Categories */}

        <Link         <Link to="/categories" className="flex flex-col items-center justify-center w-1/5">

          to="/categories"           {isActive('/categories') ? (

          className={`flex flex-col items-center space-y-1 ${isActive('/categories') ? 'text-[#f43397]' : 'text-gray-500'}`}            <div className="flex flex-col items-center">

        >              <div className="w-6 h-6 flex items-center justify-center mb-1">

          <div className="w-6 h-6 flex items-center justify-center">                <svg viewBox="0 0 24 24" className="w-6 h-6 text-[#F43397]" fill="currentColor">

            {isActive('/categories') ? (                  <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V5h14v14zm-5-7V8c0-.55-.45-1-1-1H8c-.55 0-1 .45-1 1v4c0 .55.45 1 1 1h5c.55 0 1-.45 1-1z"/>

              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">                </svg>

                <rect x="3" y="3" width="18" height="18" rx="2" fill="#F43397"/>              </div>

                <path d="M7 7h10v2H7V7z" fill="white"/>              <span className="text-[10px] text-[#F43397]">Categories</span>

                <path d="M8 11h8v7H8v-7z" fill="white"/>            </div>

                <path d="M12 12l-2 5h4l-2-5z" fill="#F43397"/>          ) : (

              </svg>            <div className="flex flex-col items-center">

            ) : (              <svg viewBox="0 0 24 24" className="w-6 h-6 text-gray-500 mb-1" fill="none" stroke="currentColor">

              <ShoppingBag size={24} />                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 4h2a2 2 0 012 2v14a2 2 0 01-2 2H6a2 2 0 01-2-2V6a2 2 0 012-2h2"/>

            )}                <path strokeLinecap="round" strokeWidth={2} d="M9 10h6m-6 4h6"/>

          </div>              </svg>

          <span className="text-xs font-medium">Categories</span>              <span className="text-[10px] text-gray-500">Categories</span>

        </Link>            </div>

          )}

        {/* Mall */}        </Link>

        <Link 

          to="/mall"         {/* Mall */}

          className={`flex flex-col items-center space-y-1 ${isActive('/mall') ? 'text-[#f43397]' : 'text-gray-500'}`}        <Link to="/mall" className="flex flex-col items-center justify-center w-1/5">

        >          {isActive('/mall') ? (

          <div className="w-6 h-6 flex items-center justify-center">            <div className="flex flex-col items-center">

            {isActive('/mall') ? (              <div className="w-6 h-6 rounded-full bg-[#F43397] flex items-center justify-center mb-1">

              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">                <span className="text-white text-sm font-bold">M</span>

                <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2z" fill="#F43397"/>              </div>

                <text x="12" y="16" textAnchor="middle" fill="white" fontSize="14" fontWeight="bold">M</text>              <span className="text-[10px] text-[#F43397]">Mall</span>

              </svg>            </div>

            ) : (          ) : (

              <Store size={24} />            <div className="flex flex-col items-center">

            )}              <svg viewBox="0 0 24 24" className="w-6 h-6 text-gray-500 mb-1" fill="none" stroke="currentColor">

          </div>                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3h18v18H3z M9 3v18 M15 3v18 M3 9h18 M3 15h18"/>

          <span className="text-xs font-medium">Mall</span>              </svg>

        </Link>              <span className="text-[10px] text-gray-500">Mall</span>

            </div>

        {/* Account */}          )}

        <Link         </Link>

          to="/account" 

          className={`flex flex-col items-center space-y-1 ${isActive('/account') ? 'text-[#f43397]' : 'text-gray-500'}`}        {/* Account */}

        >        <Link to="/account" className="flex flex-col items-center justify-center w-1/5">

          <User2 size={24} />          <div className="flex flex-col items-center">

          <span className="text-xs font-medium">Account</span>            <svg viewBox="0 0 24 24" className={`w-6 h-6 mb-1 ${isActive('/account') ? 'text-[#F43397]' : 'text-gray-500'}`} fill="none" stroke="currentColor">

        </Link>              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />

            </svg>

        {/* Search */}            <span className={`text-[10px] ${isActive('/account') ? 'text-[#F43397]' : 'text-gray-500'}`}>Account</span>

        <Link           </div>

          to="/search"         </Link>

          className={`flex flex-col items-center space-y-1 ${isActive('/search') ? 'text-[#f43397]' : 'text-gray-500'}`}

        >        {/* Search */}

          <Search size={24} />        <Link to="/search" className="flex flex-col items-center justify-center w-1/5">

          <span className="text-xs font-medium">Search</span>          <div className="flex flex-col items-center">

        </Link>            <svg viewBox="0 0 24 24" className={`w-6 h-6 mb-1 ${isActive('/search') ? 'text-[#F43397]' : 'text-gray-500'}`} fill="none" stroke="currentColor">

      </div>              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />

    </nav>            </svg>

  );            <span className={`text-[10px] ${isActive('/search') ? 'text-[#F43397]' : 'text-gray-500'}`}>Search</span>

}          </div>
        </Link>
      </div>
    </nav>
  );
}
