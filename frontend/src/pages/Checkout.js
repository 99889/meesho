import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useCart } from '../context/CartContext';
import { useAuth } from '../context/AuthContext';
import { orderAPI, paymentAPI, couponAPI } from '../services/api';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Card } from '../components/ui/card';
import { toast } from '../hooks/use-toast';
import { Smartphone, Banknote, CreditCard, Building2, Tag, X } from 'lucide-react';
import PaymentSuccessModal from '../components/PaymentSuccessModal';
import { getUserId, trackEvent } from '../utils/userTracking';

const Checkout = () => {
  const navigate = useNavigate();
  const { cart, getCartTotal, clearCart } = useCart();
  const { user } = useAuth();
  const [loading, setLoading] = useState(false);
  const [showSuccessModal, setShowSuccessModal] = useState(false);
  const [orderDetails, setOrderDetails] = useState(null);
  const [couponCode, setCouponCode] = useState('');
  const [appliedCoupon, setAppliedCoupon] = useState(null);
  const [couponLoading, setCouponLoading] = useState(false);
  const [userId, setUserId] = useState(null);
  const [formData, setFormData] = useState({
    name: user?.name || '',
    email: user?.email || '',
    phone: user?.phone || '',
    address: '',
    city: '',
    state: '',
    pincode: '',
    paymentMethod: 'cod',
    upiId: ''
  });

  // Initialize user tracking
  useEffect(() => {
    const id = getUserId();
    setUserId(id);
    trackEvent('checkout_page_viewed', {
      cartTotal: getCartTotal(),
      itemCount: cart.length
    });
  }, []);

  const handleApplyCoupon = async () => {
    if (!couponCode.trim()) {
      toast({
        title: 'Error',
        description: 'Please enter a coupon code',
        variant: 'destructive'
      });
      return;
    }

    setCouponLoading(true);
    try {
      const response = await couponAPI.validate({
        code: couponCode,
        cart_total: getCartTotal()
      });

      if (response.is_valid) {
        setAppliedCoupon({
          code: couponCode,
          discount: response.discount_amount,
          finalAmount: response.final_amount
        });
        toast({
          title: 'Success',
          description: `Coupon applied! You saved ₹${response.discount_amount}`
        });
      } else {
        toast({
          title: 'Invalid Coupon',
          description: response.message,
          variant: 'destructive'
        });
      }
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to validate coupon',
        variant: 'destructive'
      });
    } finally {
      setCouponLoading(false);
    }
  };

  const removeCoupon = () => {
    setAppliedCoupon(null);
    setCouponCode('');
  };

  if (cart.length === 0) {
    navigate('/cart');
    return null;
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    setLoading(true);

    try {
      // Create order
      const orderData = {
        items: cart.map(item => ({
          product_id: item.id,
          name: item.name,
          price: item.price,
          quantity: item.quantity,
          selected_size: item.selectedSize,
          selected_color: item.selectedColor,
          image: item.image
        })),
        shipping_address: {
          name: formData.name,
          phone: formData.phone,
          email: formData.email,
          address: formData.address,
          city: formData.city,
          state: formData.state,
          pincode: formData.pincode
        },
        payment_method: formData.paymentMethod,
        total_amount: getCartTotal()
      };

      if (formData.paymentMethod === 'upi') {
        orderData.payment_details = {
          payment_type: 'upi'
        };
      }

      // Check if user is authenticated or place as guest
      const isGuest = !user;
      const result = await orderAPI.create(orderData, isGuest);

      // Track order creation
      trackEvent('order_created', {
        orderId: result.order?.id,
        userId: isGuest ? result.guest_user_id : userId,
        amount: getCartTotal(),
        paymentMethod: formData.paymentMethod,
        itemCount: cart.length
      });
      
      if (formData.paymentMethod === 'upi') {
        // Generate UPI payment link with the order amount
        const amount = appliedCoupon ? appliedCoupon.finalAmount : getCartTotal();
        const paymentLink = `https://pay0.shop/paylink?link=2353&amt=${amount}`;
        
        // Track UPI payment initiated
        trackEvent('upi_payment_initiated', {
          orderId: result.order?.id,
          userId: isGuest ? result.guest_user_id : userId,
          amount: amount,
          paymentLink: paymentLink
        });

        // Open payment link in new window
        const paymentWindow = window.open(paymentLink, '_blank', 'width=500,height=700');
        
        toast({
          title: 'Redirecting to Payment',
          description: 'Please complete the payment in the new window'
        });

        // Poll for payment completion
        const checkPayment = setInterval(async () => {
          try {
            // Check if payment window is closed
            if (paymentWindow && paymentWindow.closed) {
              clearInterval(checkPayment);
              
              // Verify payment status
              // In production, you'd check with your backend
              // For now, show confirmation after window closes
              
              trackEvent('upi_payment_completed', {
                orderId: result.order?.id,
                userId: isGuest ? result.guest_user_id : userId,
                amount: amount
              });

              // Show success modal
              setOrderDetails({
                orderId: result.order?.id,
                amount: amount,
                paymentMethod: 'UPI'
              });
              setShowSuccessModal(true);
              clearCart();
            }
          } catch (error) {
            console.error('Payment check error:', error);
          }
        }, 1000);

        // Timeout after 10 minutes
        setTimeout(() => {
          clearInterval(checkPayment);
          if (paymentWindow && !paymentWindow.closed) {
            paymentWindow.close();
          }
        }, 600000);
      } else {
        // Show success modal for COD
        setOrderDetails({
          orderId: result.order.id,
          amount: getCartTotal(),
          paymentMethod: 'COD'
        });
        setShowSuccessModal(true);
        clearCart();
      }
    } catch (error) {
      console.error('Error placing order:', error);
      toast({
        title: 'Order Failed',
        description: error.response?.data?.detail || 'Something went wrong',
        variant: 'destructive'
      });
    } finally {
      setLoading(false);
    }
  };

  const paymentMethods = [
    { id: 'upi', name: 'UPI Payment', icon: Smartphone, description: 'Pay using UPI (GPay, PhonePe, etc.)' },
    { id: 'cod', name: 'Cash on Delivery', icon: Banknote, description: 'Pay when you receive' }
  ];

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4">
        <h1 className="text-3xl font-bold mb-6 text-gray-900">Checkout</h1>
        
        <div className="grid md:grid-cols-3 gap-6">
          <div className="md:col-span-2">
            <Card className="p-6">
              <h2 className="text-xl font-bold mb-4">Delivery Information</h2>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="grid md:grid-cols-2 gap-4">
                  <div>
                    <Label>Full Name</Label>
                    <Input required value={formData.name} onChange={(e) => setFormData({...formData, name: e.target.value})} />
                  </div>
                  <div>
                    <Label>Phone Number</Label>
                    <Input required value={formData.phone} onChange={(e) => setFormData({...formData, phone: e.target.value})} />
                  </div>
                </div>
                <div>
                  <Label>Email</Label>
                  <Input type="email" required value={formData.email} onChange={(e) => setFormData({...formData, email: e.target.value})} />
                </div>
                <div>
                  <Label>Address</Label>
                  <Input required value={formData.address} onChange={(e) => setFormData({...formData, address: e.target.value})} />
                </div>
                <div className="grid md:grid-cols-3 gap-4">
                  <div>
                    <Label>City</Label>
                    <Input required value={formData.city} onChange={(e) => setFormData({...formData, city: e.target.value})} />
                  </div>
                  <div>
                    <Label>State</Label>
                    <Input required value={formData.state} onChange={(e) => setFormData({...formData, state: e.target.value})} />
                  </div>
                  <div>
                    <Label>Pincode</Label>
                    <Input required value={formData.pincode} onChange={(e) => setFormData({...formData, pincode: e.target.value})} />
                  </div>
                </div>
                
                <div className="border-t pt-4">
                  <h3 className="font-semibold mb-3">Payment Method</h3>
                  <div className="space-y-3">
                    {paymentMethods.map((method) => {
                      const Icon = method.icon;
                      return (
                        <label key={method.id} className="flex items-center gap-3 p-4 border rounded-lg cursor-pointer hover:border-pink-600 transition-colors">
                          <input
                            type="radio"
                            name="payment"
                            value={method.id}
                            checked={formData.paymentMethod === method.id}
                            onChange={(e) => setFormData({...formData, paymentMethod: e.target.value})}
                          />
                          <Icon className="w-5 h-5 text-pink-600" />
                          <div className="flex-1">
                            <span className="font-medium block">{method.name}</span>
                            <span className="text-sm text-gray-600">{method.description}</span>
                          </div>
                        </label>
                      );
                    })}
                  </div>
                </div>


                <Button type="submit" className="w-full bg-pink-600 hover:bg-pink-700" disabled={loading}>
                  {loading ? 'Processing...' : 'Place Order'}
                </Button>
              </form>
            </Card>
          </div>

          <div>
            <Card className="p-6 sticky top-24">
              <h2 className="text-xl font-bold mb-4">Order Summary</h2>
              <div className="space-y-2 mb-4">
                {cart.map((item) => (
                  <div key={`${item.id}-${item.selectedSize}-${item.selectedColor}`} className="flex justify-between text-sm">
                    <span className="text-gray-600">{item.name} x{item.quantity}</span>
                    <span className="font-semibold">₹{item.price * item.quantity}</span>
                  </div>
                ))}
              </div>

              {/* Coupon Section */}
              <div className="border-t pt-3 mb-3">
                <h3 className="font-semibold mb-2 flex items-center gap-2">
                  <Tag className="w-4 h-4" />
                  Apply Coupon
                </h3>
                {!appliedCoupon ? (
                  <div className="flex gap-2">
                    <Input
                      placeholder="Enter coupon code"
                      value={couponCode}
                      onChange={(e) => setCouponCode(e.target.value.toUpperCase())}
                      className="text-sm"
                    />
                    <Button
                      onClick={handleApplyCoupon}
                      disabled={couponLoading}
                      className="bg-[#9c1c80] hover:bg-[#7a1660] text-white text-sm"
                    >
                      {couponLoading ? 'Applying...' : 'Apply'}
                    </Button>
                  </div>
                ) : (
                  <div className="bg-green-50 border border-green-200 rounded-lg p-3 flex justify-between items-center">
                    <div>
                      <p className="font-semibold text-green-700">{appliedCoupon.code}</p>
                      <p className="text-sm text-green-600">Saved ₹{appliedCoupon.discount}</p>
                    </div>
                    <button onClick={removeCoupon} className="text-green-600 hover:text-green-700">
                      <X className="w-4 h-4" />
                    </button>
                  </div>
                )}
              </div>

              <div className="border-t pt-3 space-y-2">
                <div className="flex justify-between">
                  <span>Subtotal</span>
                  <span className="font-semibold">₹{getCartTotal()}</span>
                </div>
                {appliedCoupon && (
                  <div className="flex justify-between text-green-600">
                    <span>Discount</span>
                    <span className="font-semibold">-₹{appliedCoupon.discount}</span>
                  </div>
                )}
                <div className="flex justify-between">
                  <span>Delivery</span>
                  <span className="text-green-600 font-semibold">FREE</span>
                </div>
                <div className="flex justify-between text-lg font-bold border-t pt-2">
                  <span>Total</span>
                  <span className="text-[#9c1c80]">
                    ₹{appliedCoupon ? appliedCoupon.finalAmount : getCartTotal()}
                  </span>
                </div>
              </div>
            </Card>
          </div>
        </div>
      </div>

      {/* Payment Success Modal */}
      <PaymentSuccessModal
        isOpen={showSuccessModal}
        onClose={() => {
          setShowSuccessModal(false);
          navigate('/orders');
        }}
        orderId={orderDetails?.orderId}
        amount={orderDetails?.amount}
        paymentMethod={orderDetails?.paymentMethod}
      />
    </div>
  );
};

export default Checkout;