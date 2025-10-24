import React from 'react';
import { CheckCircle } from 'lucide-react';
import { Button } from './ui/button';
import { Card } from './ui/card';

const PaymentSuccessModal = ({ isOpen, onClose, orderId, amount, paymentMethod }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <Card className="max-w-md w-full p-8 text-center animate-in fade-in zoom-in duration-300">
        {/* Success Icon */}
        <div className="mb-6">
          <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <CheckCircle className="w-12 h-12 text-green-600" />
          </div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Payment Successful!</h2>
          <p className="text-gray-600">Your order has been placed successfully</p>
        </div>

        {/* Order Details */}
        <div className="bg-gray-50 rounded-lg p-6 mb-6 text-left">
          <div className="flex justify-between mb-3 pb-3 border-b">
            <span className="text-gray-600">Order ID:</span>
            <span className="font-semibold text-gray-900">{orderId}</span>
          </div>
          <div className="flex justify-between mb-3 pb-3 border-b">
            <span className="text-gray-600">Amount Paid:</span>
            <span className="font-semibold text-green-600">₹{amount}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">Payment Method:</span>
            <span className="font-semibold text-gray-900 uppercase">{paymentMethod}</span>
          </div>
        </div>

        {/* Success Message */}
        <div className="mb-6">
          <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-4">
            <p className="text-green-800 text-sm">
              ✓ Payment confirmed<br/>
              ✓ Order confirmation sent to your email<br/>
              ✓ Track your order in "My Orders"
            </p>
          </div>
          <p className="text-sm text-gray-600">
            Your order will be delivered within 5-7 business days
          </p>
        </div>

        {/* Action Buttons */}
        <div className="space-y-3">
          <Button 
            className="w-full bg-pink-600 hover:bg-pink-700"
            onClick={onClose}
          >
            View My Orders
          </Button>
          <Button 
            variant="outline" 
            className="w-full"
            onClick={() => window.location.href = '/'}
          >
            Continue Shopping
          </Button>
        </div>
      </Card>
    </div>
  );
};

export default PaymentSuccessModal;
