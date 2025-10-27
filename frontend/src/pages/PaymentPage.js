import React, { useEffect, useState, useRef } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { CheckCircle, XCircle, AlertCircle, Clock } from 'lucide-react';

const PaymentPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [paymentStatus, setPaymentStatus] = useState('pending'); // pending, processing, success, failed
  const [orderDetails, setOrderDetails] = useState(null);
  const [qrCodeUrl, setQrCodeUrl] = useState(null);
  const [timeLeft, setTimeLeft] = useState(4 * 60); // 4 minutes in seconds
  const timerRef = useRef(null);

  useEffect(() => {
    // Get order details from location state or message
    if (location.state && location.state.orderDetails) {
      setOrderDetails(location.state.orderDetails);
      if (location.state.qrCodeUrl) {
        setQrCodeUrl(location.state.qrCodeUrl);
      }
    }
    
    // Listen for messages from parent window
    const handleMessage = (event) => {
      if (event.data && event.data.type === 'ORDER_DETAILS') {
        setOrderDetails(event.data.orderDetails);
        if (event.data.qrCodeUrl) {
          setQrCodeUrl(event.data.qrCodeUrl);
        }
      }
      
      // Listen for actual payment status updates from parent
      if (event.data && event.data.type === 'PAYMENT_STATUS_UPDATE') {
        if (event.data.status === 'success') {
          handlePaymentCompletion(true);
        } else if (event.data.status === 'failed') {
          handlePaymentCompletion(false);
        }
      }
    };
    
    window.addEventListener('message', handleMessage);
    
    // Cleanup listener on unmount
    return () => {
      window.removeEventListener('message', handleMessage);
    };
  }, [location]);

  // Timer effect
  useEffect(() => {
    if (paymentStatus === 'pending' && timeLeft > 0) {
      timerRef.current = setInterval(() => {
        setTimeLeft(prev => {
          if (prev <= 1) {
            // Timer expired
            handlePaymentCompletion(false);
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
    } else if (timeLeft === 0 || paymentStatus !== 'pending') {
      clearInterval(timerRef.current);
    }
    
    return () => clearInterval(timerRef.current);
  }, [paymentStatus, timeLeft]);

  const handlePaymentCompletion = (isSuccess) => {
    // Clear timer
    clearInterval(timerRef.current);
    
    // Simulate payment processing
    setPaymentStatus('processing');
    
    // Simulate payment processing time
    setTimeout(() => {
      if (isSuccess) {
        setPaymentStatus('success');
        // Close window after 3 seconds and notify parent of success
        setTimeout(() => {
          if (window.opener) {
            window.opener.postMessage({
              type: 'PAYMENT_SUCCESS',
              orderId: orderDetails?.orderId,
              amount: orderDetails?.amount
            }, '*');
          }
          window.close();
        }, 3000);
      } else {
        setPaymentStatus('failed');
        // Close window after 3 seconds and notify parent of failure
        setTimeout(() => {
          if (window.opener) {
            window.opener.postMessage({
              type: 'PAYMENT_FAILED',
              orderId: orderDetails?.orderId,
              amount: orderDetails?.amount
            }, '*');
          }
          window.close();
        }, 3000);
      }
    }, 2000);
  };

  const handleCancel = () => {
    // Clear timer
    clearInterval(timerRef.current);
    
    // Send message to parent window
    if (window.opener) {
      window.opener.postMessage({
        type: 'PAYMENT_CANCELLED',
        orderId: orderDetails?.orderId
      }, '*');
    }
    window.close();
  };

  // Format time for display (MM:SS)
  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  if (!orderDetails) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
        <div className="text-center">
          <XCircle className="w-16 h-16 text-red-500 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Loading Payment Details</h2>
          <p className="text-gray-600 mb-4">Please wait while we load your order information...</p>
          <Button onClick={() => navigate('/')} className="bg-pink-600 hover:bg-pink-700">
            Go to Home
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <h1 className="text-xl font-bold text-[#6e2e61]">Meesho</h1>
            <Button variant="ghost" onClick={handleCancel}>
              <XCircle className="w-5 h-5" />
            </Button>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-8">
        {paymentStatus === 'pending' && (
          <div className="max-w-md mx-auto">
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-2xl font-bold text-center mb-6">Complete Payment</h2>
              
              {/* Timer */}
              <div className="bg-amber-50 border border-amber-200 rounded-lg p-4 mb-6 text-center">
                <div className="flex items-center justify-center gap-2 mb-2">
                  <Clock className="w-5 h-5 text-amber-600" />
                  <span className="font-semibold text-amber-800">Payment Timer</span>
                </div>
                <div className="text-3xl font-bold text-amber-700 mb-2">
                  {formatTime(timeLeft)}
                </div>
                <p className="text-sm text-amber-700">
                  Please complete payment within 4 minutes
                </p>
              </div>
              
              {/* Order Summary */}
              <div className="bg-gray-50 rounded-lg p-4 mb-6">
                <h3 className="font-semibold text-gray-900 mb-3">Order Summary</h3>
                <div className="flex justify-between mb-2">
                  <span className="text-gray-600">Order ID:</span>
                  <span className="font-medium">#{orderDetails.orderId}</span>
                </div>
                {orderDetails.productName && (
                  <div className="flex justify-between mb-2">
                    <span className="text-gray-600">Product:</span>
                    <span className="font-medium">{orderDetails.productName}</span>
                  </div>
                )}
                {orderDetails.itemCount && orderDetails.itemCount > 1 && (
                  <div className="flex justify-between mb-2">
                    <span className="text-gray-600">Items:</span>
                    <span className="font-medium">{orderDetails.itemCount} items</span>
                  </div>
                )}
                <div className="flex justify-between">
                  <span className="text-gray-600">Amount:</span>
                  <span className="font-bold text-lg text-green-600">₹{orderDetails.amount}</span>
                </div>
              </div>

              {/* QR Code */}
              <div className="bg-gray-100 rounded-lg p-6 text-center mb-6">
                <div className="bg-white p-4 rounded-lg inline-block mb-4">
                  {qrCodeUrl ? (
                    <img 
                      src={qrCodeUrl} 
                      alt="Payment QR Code" 
                      className="w-48 h-48 object-contain"
                    />
                  ) : (
                    <div className="w-48 h-48 bg-gray-200 rounded flex items-center justify-center">
                      <div className="text-center">
                        <div className="w-32 h-32 bg-gray-300 rounded mx-auto mb-2"></div>
                        <p className="text-xs text-gray-600">QR Code Loading...</p>
                      </div>
                    </div>
                  )}
                </div>
                <p className="text-sm text-gray-600 mb-4">
                  Scan this QR code with any UPI app to pay ₹{orderDetails.amount}
                </p>
              </div>

              {/* Payment Instructions */}
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
                <h4 className="font-semibold text-blue-800 mb-2">Payment Instructions</h4>
                <ul className="text-sm text-blue-700 space-y-1">
                  <li>• Open any UPI app on your phone</li>
                  <li>• Scan the QR code above</li>
                  <li>• Confirm the amount: ₹{orderDetails.amount}</li>
                  <li>• Complete the payment within {formatTime(timeLeft)}</li>
                </ul>
                <p className="text-sm text-blue-700 mt-3">
                  <strong>Note:</strong> This window will automatically close and redirect you back to the website once your payment is processed or if time expires.
                </p>
              </div>

              <Button 
                variant="outline" 
                onClick={handleCancel}
                className="w-full"
              >
                Cancel Payment
              </Button>
            </div>
          </div>
        )}

        {paymentStatus === 'processing' && (
          <div className="max-w-md mx-auto">
            <div className="bg-white rounded-lg shadow-md p-8 text-center">
              <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-green-600 mx-auto mb-4"></div>
              <h2 className="text-2xl font-bold text-gray-900 mb-2">Processing Payment</h2>
              <p className="text-gray-600">Please wait while we process your payment...</p>
              <p className="text-sm text-gray-500 mt-4">Amount: ₹{orderDetails.amount}</p>
            </div>
          </div>
        )}

        {paymentStatus === 'success' && (
          <div className="max-w-md mx-auto">
            <div className="bg-white rounded-lg shadow-md p-8 text-center">
              <CheckCircle className="w-16 h-16 text-green-500 mx-auto mb-4" />
              <h2 className="text-2xl font-bold text-gray-900 mb-2">Payment Successful!</h2>
              <p className="text-gray-600 mb-4">
                Your payment of ₹{orderDetails.amount} has been processed successfully.
              </p>
              <div className="bg-green-50 rounded-lg p-4 mb-6">
                <p className="text-green-800 text-sm">
                  ✓ Order confirmed<br/>
                  ✓ Payment verified<br/>
                  ✓ Redirecting to order confirmation...
                </p>
              </div>
              <p className="text-sm text-gray-500">
                Redirecting you back to the website...
              </p>
            </div>
          </div>
        )}

        {paymentStatus === 'failed' && (
          <div className="max-w-md mx-auto">
            <div className="bg-white rounded-lg shadow-md p-8 text-center">
              <AlertCircle className="w-16 h-16 text-red-500 mx-auto mb-4" />
              <h2 className="text-2xl font-bold text-gray-900 mb-2">Payment Failed!</h2>
              <p className="text-gray-600 mb-4">
                {timeLeft === 0 
                  ? `Payment time expired. Please try again.` 
                  : `Your payment of ₹${orderDetails.amount} could not be processed.`}
              </p>
              <div className="bg-red-50 rounded-lg p-4 mb-6">
                <p className="text-red-800 text-sm">
                  ✗ Payment failed<br/>
                  ✗ Order not confirmed<br/>
                  ✗ Redirecting back to checkout...
                </p>
              </div>
              <p className="text-sm text-gray-500">
                Redirecting you back to the website...
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default PaymentPage;