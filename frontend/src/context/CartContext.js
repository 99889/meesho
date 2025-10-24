import React, { createContext, useContext, useState, useEffect } from 'react';
import { toast } from '../hooks/use-toast';

const CartContext = createContext();

export const CartProvider = ({ children }) => {
  const [cart, setCart] = useState([]);
  const [wishlist, setWishlist] = useState([]);

  useEffect(() => {
    // Load cart from localStorage
    const savedCart = localStorage.getItem('cart');
    const savedWishlist = localStorage.getItem('wishlist');
    if (savedCart) setCart(JSON.parse(savedCart));
    if (savedWishlist) setWishlist(JSON.parse(savedWishlist));
  }, []);

  useEffect(() => {
    localStorage.setItem('cart', JSON.stringify(cart));
  }, [cart]);

  useEffect(() => {
    localStorage.setItem('wishlist', JSON.stringify(wishlist));
  }, [wishlist]);

  const addToCart = (product, quantity = 1, selectedSize = null, selectedColor = null) => {
    const existingItem = cart.find(
      item => item.id === product.id && 
              item.selectedSize === selectedSize && 
              item.selectedColor === selectedColor
    );

    if (existingItem) {
      setCart(cart.map(item =>
        item.id === product.id && 
        item.selectedSize === selectedSize && 
        item.selectedColor === selectedColor
          ? { ...item, quantity: item.quantity + quantity }
          : item
      ));
      toast({
        title: 'Updated cart',
        description: `${product.name} quantity updated`
      });
    } else {
      setCart([...cart, { ...product, quantity, selectedSize, selectedColor }]);
      toast({
        title: 'Added to cart',
        description: `${product.name} added to your cart`
      });
    }
  };

  const removeFromCart = (productId, selectedSize, selectedColor) => {
    setCart(cart.filter(item => 
      !(item.id === productId && 
        item.selectedSize === selectedSize && 
        item.selectedColor === selectedColor)
    ));
    toast({
      title: 'Removed from cart',
      description: 'Item removed from your cart'
    });
  };

  const updateQuantity = (productId, quantity, selectedSize, selectedColor) => {
    if (quantity === 0) {
      removeFromCart(productId, selectedSize, selectedColor);
      return;
    }
    setCart(cart.map(item =>
      item.id === productId && 
      item.selectedSize === selectedSize && 
      item.selectedColor === selectedColor
        ? { ...item, quantity }
        : item
    ));
  };

  const clearCart = () => {
    setCart([]);
    toast({
      title: 'Cart cleared',
      description: 'All items removed from cart'
    });
  };

  const addToWishlist = (product) => {
    if (wishlist.find(item => item.id === product.id)) {
      toast({
        title: 'Already in wishlist',
        description: `${product.name} is already in your wishlist`
      });
      return;
    }
    setWishlist([...wishlist, product]);
    toast({
      title: 'Added to wishlist',
      description: `${product.name} added to your wishlist`
    });
  };

  const removeFromWishlist = (productId) => {
    setWishlist(wishlist.filter(item => item.id !== productId));
    toast({
      title: 'Removed from wishlist',
      description: 'Item removed from your wishlist'
    });
  };

  const isInWishlist = (productId) => {
    return wishlist.some(item => item.id === productId);
  };

  const getCartTotal = () => {
    return cart.reduce((total, item) => total + (item.price * item.quantity), 0);
  };

  const getCartCount = () => {
    return cart.reduce((total, item) => total + item.quantity, 0);
  };

  return (
    <CartContext.Provider value={{
      cart,
      wishlist,
      addToCart,
      removeFromCart,
      updateQuantity,
      clearCart,
      addToWishlist,
      removeFromWishlist,
      isInWishlist,
      getCartTotal,
      getCartCount
    }}>
      {children}
    </CartContext.Provider>
  );
};

export const useCart = () => {
  const context = useContext(CartContext);
  if (!context) {
    throw new Error('useCart must be used within CartProvider');
  }
  return context;
};
