import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { orderAPI } from '../services/api';
import { toast } from '../hooks/use-toast';
import { Button } from '../components/ui/button';
import { Card } from '../components/ui/card';
import { Input } from '../components/ui/input';
import { Select } from '../components/ui/select';
import { useAuth } from '../context/AuthContext';
import { Package, Truck, CheckCircle, Clock } from 'lucide-react';

const AdminOrders = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedOrder, setSelectedOrder] = useState(null);
  const [trackingStatus, setTrackingStatus] = useState('');
  const [trackingLocation, setTrackingLocation] = useState('');
  const [trackingDescription, setTrackingDescription] = useState('');

  useEffect(() => {
    // Check if user is admin
    if (!user || user.role !== 'admin') {
      navigate('/');
      return;
    }
    
    fetchOrders();
  }, [user, navigate]);

  const fetchOrders = async () => {
    try {
      setLoading(true);
      const response = await orderAPI.getAll();
      setOrders(response.orders || []);
    } catch (error) {
      console.error('Error fetching orders:', error);
    } finally {
      setLoading(false);
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'delivered':
        return <CheckCircle className="w-5 h-5 text-green-600" />;
      case 'shipped':
      case 'out_for_delivery':
        return <Truck className="w-5 h-5 text-blue-600" />;
      case 'confirmed':
        return <Package className="w-5 h-5 text-yellow-600" />;
      default:
        return <Clock className="w-5 h-5 text-gray-600" />;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'delivered':
        return 'bg-green-100 text-green-800';
      case 'shipped':
      case 'out_for_delivery':
        return 'bg-blue-100 text-blue-800';
      case 'confirmed':
        return 'bg-yellow-100 text-yellow-800';
      case 'cancelled':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const formatStatus = (status) => {
    return status
      .split('_')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  };

  const handleUpdateTracking = async (orderId) => {
    if (!trackingStatus) {
      toast({
        title: 'Error',
        description: 'Please select a status',
        variant: 'destructive'
      });
      return;
    }

    try {
      const trackingData = {
        status: trackingStatus,
        location: trackingLocation || undefined,
        description: trackingDescription || undefined
      };
      
      await orderAPI.updateTracking(orderId, trackingData);
      
      toast({
        title: 'Success',
        description: `Tracking updated for order ${orderId.substring(0, 8).toUpperCase()}`
      });
      
      // Reset form
      setTrackingStatus('');
      setTrackingLocation('');
      setTrackingDescription('');
      setSelectedOrder(null);
      
      // Refresh orders
      fetchOrders();
    } catch (error) {
      console.error('Error updating tracking:', error);
      toast({
        title: 'Error',
        description: error.response?.data?.detail || 'Error updating tracking information',
        variant: 'destructive'
      });
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-pink-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600">Loading orders...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4">
        <h1 className="text-3xl font-bold mb-6 text-gray-900">Order Management</h1>

        <Card className="p-6 mb-6">
          <h2 className="text-xl font-bold mb-4">Update Order Tracking</h2>
          
          {selectedOrder ? (
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <h3 className="font-medium">Order #{selectedOrder.id.substring(0, 8).toUpperCase()}</h3>
                <Button 
                  variant="outline" 
                  size="sm" 
                  onClick={() => setSelectedOrder(null)}
                >
                  Cancel
                </Button>
              </div>
              
              <div className="grid md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
                  <Select value={trackingStatus} onValueChange={setTrackingStatus}>
                    <Select.Trigger>
                      <Select.Value placeholder="Select Status" />
                    </Select.Trigger>
                    <Select.Content>
                      <Select.Item value="pending">Pending</Select.Item>
                      <Select.Item value="confirmed">Confirmed</Select.Item>
                      <Select.Item value="shipped">Shipped</Select.Item>
                      <Select.Item value="out_for_delivery">Out for Delivery</Select.Item>
                      <Select.Item value="delivered">Delivered</Select.Item>
                      <Select.Item value="cancelled">Cancelled</Select.Item>
                    </Select.Content>
                  </Select>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Location</label>
                  <Input
                    type="text"
                    value={trackingLocation}
                    onChange={(e) => setTrackingLocation(e.target.value)}
                    placeholder="Location (optional)"
                  />
                </div>
                
                <div className="md:col-span-2">
                  <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
                  <Input
                    type="text"
                    value={trackingDescription}
                    onChange={(e) => setTrackingDescription(e.target.value)}
                    placeholder="Description (optional)"
                  />
                </div>
              </div>
              
              <Button 
                onClick={() => handleUpdateTracking(selectedOrder.id)}
                className="bg-pink-600 hover:bg-pink-700"
              >
                Update Tracking
              </Button>
            </div>
          ) : (
            <p className="text-gray-600">Select an order to update tracking information</p>
          )}
        </Card>

        <Card className="p-6">
          <h2 className="text-xl font-bold mb-4">All Orders ({orders.length})</h2>
          
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Order</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Customer</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Amount</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {orders.map((order) => (
                  <tr key={order.id}>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div>
                        <div className="text-sm font-medium text-gray-900">
                          #{order.id.substring(0, 8).toUpperCase()}
                        </div>
                        <div className="text-sm text-gray-500">
                          {order.items.length} item(s)
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">{order.shipping_address.name}</div>
                      <div className="text-sm text-gray-500">{order.shipping_address.email}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {new Date(order.created_at).toLocaleDateString('en-IN')}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-semibold text-gray-900">
                      ₹{order.total_amount}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center gap-2">
                        {getStatusIcon(order.order_status)}
                        <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${getStatusColor(order.order_status)}`}>
                          {formatStatus(order.order_status)}
                        </span>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <Button
                        onClick={() => setSelectedOrder(order)}
                        variant="outline"
                        size="sm"
                        className="mr-2"
                      >
                        Update Tracking
                      </Button>
                      <Button
                        onClick={() => navigate(`/orders/${order.id}`)}
                        variant="outline"
                        size="sm"
                      >
                        View Details
                      </Button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          
          {orders.length === 0 && (
            <div className="text-center py-12">
              <p className="text-gray-500">No orders found</p>
            </div>
          )}
        </Card>
      </div>
    </div>
  );
};

export default AdminOrders;