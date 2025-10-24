import React from "react";
import "./App.css";
import { BrowserRouter, Routes, Route, useLocation } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import { CartProvider } from "./context/CartContext";
import { Toaster } from "./components/ui/toaster";

// Components
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import BottomNav from "./components/BottomNavigation";

// Pages
import Home from "./pages/Home";
import ProductDetail from "./pages/ProductDetail";
import Cart from "./pages/Cart";
import Wishlist from "./pages/Wishlist";
import Login from "./pages/Login";
import SearchPage from "./pages/Search";
import CategoryPage from "./pages/CategoryPage";
import MallPage from "./pages/Mall";
import Checkout from "./pages/Checkout";
import Orders from "./pages/Orders";
import OrderDetail from "./pages/OrderDetail";
import Account from "./pages/Account";
import Help from "./pages/Help";
import AdminDashboard from "./pages/AdminDashboard";
import AdminOrders from "./pages/AdminOrders";

// Conditional Bottom Navigation Component
const ConditionalBottomNav = () => {
  const location = useLocation();
  // Hide bottom nav on product detail page since it has its own action bar
  const hideBottomNav = location.pathname.startsWith('/product/') || 
                        location.pathname.startsWith('/products/');
  
  if (hideBottomNav) {
    return null;
  }
  
  return <BottomNav />;
};

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <CartProvider>
          <div className="App min-h-screen flex flex-col">
            <Navbar />
            <main className="flex-1 pt-16 md:pt-0">
              <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/product/:id" element={<ProductDetail />} />
                <Route path="/products/:id" element={<ProductDetail />} />
                <Route path="/cart" element={<Cart />} />
                <Route path="/wishlist" element={<Wishlist />} />
                <Route path="/login" element={<Login />} />
                <Route path="/search" element={<SearchPage />} />
                <Route path="/category/:category" element={<CategoryPage />} />
                <Route path="/categories" element={<CategoryPage />} />
                <Route path="/mall" element={<MallPage />} />
                <Route path="/checkout" element={<Checkout />} />
                <Route path="/orders" element={<Orders />} />
                <Route path="/orders/:id" element={<OrderDetail />} />
                <Route path="/account" element={<Account />} />
                <Route path="/help" element={<Help />} />
                <Route path="/admin" element={<AdminDashboard />} />
                <Route path="/admin/orders" element={<AdminOrders />} />
              </Routes>
            </main>
            <ConditionalBottomNav />
            <Footer />
            <Toaster />
          </div>
        </CartProvider>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;