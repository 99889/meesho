import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { Star, Store, Package, TrendingUp, Users, Award } from 'lucide-react';
import { Button } from '../components/ui/button';
import { Card } from '../components/ui/card';
import { Input } from '../components/ui/input';
import { sellerAPI } from '../services/api';

const Seller = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [sellerProfile, setSellerProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({
    shop_name: '',
    shop_description: '',
    shop_logo: '',
    response_time: ''
  });

  useEffect(() => {
    if (!user) {
      navigate('/login');
      return;
    }
    fetchSellerProfile();
  }, [user]);

  const fetchSellerProfile = async () => {
    try {
      setLoading(true);
      const response = await sellerAPI.getMyProfile();
      setSellerProfile(response);
      setFormData({
        shop_name: response.shop_name || '',
        shop_description: response.shop_description || '',
        shop_logo: response.shop_logo || '',
        response_time: response.response_time || ''
      });
    } catch (error) {
      console.error('Error fetching seller profile:', error);
      // Profile doesn't exist yet
    } finally {
      setLoading(false);
    }
  };

  const handleCreateProfile = async (e) => {
    e.preventDefault();
    try {
      const response = await sellerAPI.createProfile(formData);
      setSellerProfile(response);
      setIsEditing(false);
      alert('Seller profile created successfully!');
    } catch (error) {
      console.error('Error creating profile:', error);
      alert('Error creating profile. Please try again.');
    }
  };

  const handleUpdateProfile = async (e) => {
    e.preventDefault();
    try {
      const response = await sellerAPI.updateProfile(sellerProfile.id, formData);
      setSellerProfile(response);
      setIsEditing(false);
      alert('Profile updated successfully!');
    } catch (error) {
      console.error('Error updating profile:', error);
      alert('Error updating profile. Please try again.');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center pt-20">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-[#9c1c80] border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600">Loading seller profile...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 pt-20 pb-16">
      <div className="container mx-auto px-4 py-8">
        {!sellerProfile ? (
          // Create Seller Profile
          <div className="max-w-2xl mx-auto">
            <Card className="p-8">
              <div className="text-center mb-8">
                <Store className="w-16 h-16 text-[#9c1c80] mx-auto mb-4" />
                <h1 className="text-3xl font-bold mb-2">Become a Seller</h1>
                <p className="text-gray-600">
                  Start selling on Meesho and reach millions of customers
                </p>
              </div>

              <form onSubmit={handleCreateProfile} className="space-y-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Shop Name *
                  </label>
                  <Input
                    type="text"
                    placeholder="Enter your shop name"
                    value={formData.shop_name}
                    onChange={(e) =>
                      setFormData({ ...formData, shop_name: e.target.value })
                    }
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Shop Description
                  </label>
                  <textarea
                    placeholder="Describe your shop and products..."
                    value={formData.shop_description}
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        shop_description: e.target.value
                      })
                    }
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:border-[#9c1c80]"
                    rows="4"
                  ></textarea>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Shop Logo URL
                  </label>
                  <Input
                    type="url"
                    placeholder="https://example.com/logo.png"
                    value={formData.shop_logo}
                    onChange={(e) =>
                      setFormData({ ...formData, shop_logo: e.target.value })
                    }
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Response Time
                  </label>
                  <select
                    value={formData.response_time}
                    onChange={(e) =>
                      setFormData({ ...formData, response_time: e.target.value })
                    }
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:border-[#9c1c80]"
                  >
                    <option value="">Select response time</option>
                    <option value="within 1 hour">Within 1 hour</option>
                    <option value="within 4 hours">Within 4 hours</option>
                    <option value="within 24 hours">Within 24 hours</option>
                  </select>
                </div>

                <Button
                  type="submit"
                  className="w-full bg-[#9c1c80] hover:bg-[#7a1660] text-white py-3 font-semibold"
                >
                  Create Seller Profile
                </Button>
              </form>

              <div className="mt-8 pt-8 border-t border-gray-200">
                <h3 className="font-bold mb-4">Benefits of Selling on Meesho:</h3>
                <ul className="space-y-3 text-gray-600">
                  <li className="flex items-center gap-2">
                    <TrendingUp className="w-5 h-5 text-[#9c1c80]" />
                    Reach millions of customers
                  </li>
                  <li className="flex items-center gap-2">
                    <Award className="w-5 h-5 text-[#9c1c80]" />
                    0% commission on first 100 orders
                  </li>
                  <li className="flex items-center gap-2">
                    <Package className="w-5 h-5 text-[#9c1c80]" />
                    Free logistics support
                  </li>
                  <li className="flex items-center gap-2">
                    <Users className="w-5 h-5 text-[#9c1c80]" />
                    Dedicated seller support
                  </li>
                </ul>
              </div>
            </Card>
          </div>
        ) : (
          // Seller Dashboard
          <div>
            {/* Header */}
            <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  {sellerProfile.shop_logo && (
                    <img
                      src={sellerProfile.shop_logo}
                      alt={sellerProfile.shop_name}
                      className="w-16 h-16 rounded-lg object-cover"
                    />
                  )}
                  <div>
                    <h1 className="text-2xl font-bold">{sellerProfile.shop_name}</h1>
                    <div className="flex items-center gap-2 mt-2">
                      <Star className="w-4 h-4 text-yellow-400 fill-yellow-400" />
                      <span className="font-semibold">{sellerProfile.rating.toFixed(1)}</span>
                      <span className="text-gray-600">
                        ({sellerProfile.total_reviews} reviews)
                      </span>
                    </div>
                  </div>
                </div>
                <Button
                  onClick={() => setIsEditing(true)}
                  className="bg-[#9c1c80] hover:bg-[#7a1660] text-white"
                >
                  Edit Profile
                </Button>
              </div>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
              <Card className="p-4">
                <div className="text-center">
                  <Package className="w-8 h-8 text-[#9c1c80] mx-auto mb-2" />
                  <p className="text-2xl font-bold">{sellerProfile.total_products}</p>
                  <p className="text-sm text-gray-600">Products Listed</p>
                </div>
              </Card>
              <Card className="p-4">
                <div className="text-center">
                  <Star className="w-8 h-8 text-yellow-400 mx-auto mb-2" />
                  <p className="text-2xl font-bold">{sellerProfile.rating.toFixed(1)}</p>
                  <p className="text-sm text-gray-600">Rating</p>
                </div>
              </Card>
              <Card className="p-4">
                <div className="text-center">
                  <Users className="w-8 h-8 text-[#9c1c80] mx-auto mb-2" />
                  <p className="text-2xl font-bold">{sellerProfile.total_reviews}</p>
                  <p className="text-sm text-gray-600">Reviews</p>
                </div>
              </Card>
              <Card className="p-4">
                <div className="text-center">
                  <Award className="w-8 h-8 text-[#9c1c80] mx-auto mb-2" />
                  <p className="text-2xl font-bold">
                    {sellerProfile.is_verified ? 'Verified' : 'Pending'}
                  </p>
                  <p className="text-sm text-gray-600">Status</p>
                </div>
              </Card>
            </div>

            {/* Profile Details */}
            <Card className="p-6 mb-6">
              <h2 className="text-xl font-bold mb-4">Shop Information</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Shop Name
                  </label>
                  <p className="text-gray-900">{sellerProfile.shop_name}</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Response Time
                  </label>
                  <p className="text-gray-900">
                    {sellerProfile.response_time || 'Not set'}
                  </p>
                </div>
                <div className="md:col-span-2">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Shop Description
                  </label>
                  <p className="text-gray-900">
                    {sellerProfile.shop_description || 'No description'}
                  </p>
                </div>
              </div>
            </Card>

            {/* Edit Profile Modal */}
            {isEditing && (
              <Card className="p-6 mb-6 bg-blue-50 border-2 border-blue-200">
                <h2 className="text-xl font-bold mb-4">Edit Profile</h2>
                <form onSubmit={handleUpdateProfile} className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Shop Name
                    </label>
                    <Input
                      type="text"
                      value={formData.shop_name}
                      onChange={(e) =>
                        setFormData({ ...formData, shop_name: e.target.value })
                      }
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Shop Description
                    </label>
                    <textarea
                      value={formData.shop_description}
                      onChange={(e) =>
                        setFormData({
                          ...formData,
                          shop_description: e.target.value
                        })
                      }
                      className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:border-[#9c1c80]"
                      rows="4"
                    ></textarea>
                  </div>
                  <div className="flex gap-2">
                    <Button
                      type="submit"
                      className="bg-[#9c1c80] hover:bg-[#7a1660] text-white"
                    >
                      Save Changes
                    </Button>
                    <Button
                      type="button"
                      onClick={() => setIsEditing(false)}
                      variant="outline"
                    >
                      Cancel
                    </Button>
                  </div>
                </form>
              </Card>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default Seller;
