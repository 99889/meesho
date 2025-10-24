import React, { useState } from 'react';
import { MessageCircle, Phone, Mail, MapPin, ChevronDown, ChevronUp } from 'lucide-react';
import { Button } from '../components/ui/button';
import { Card } from '../components/ui/card';
import { Input } from '../components/ui/input';

const HelpPage = () => {
  const helpTopics = [
    {
      title: "Order Issues",
      description: "Track orders, returns, cancellations",
      icon: "📦"
    },
    {
      title: "Payment Issues",
      description: "Payment methods, refunds, wallet",
      icon: "💳"
    },
    {
      title: "Account Issues",
      description: "Login, signup, profile",
      icon: "👤"
    },
    {
      title: "Product Issues",
      description: "Quality, specifications, complaints",
      icon: "🛍️"
    }
  ];

  return (
    <div className="min-h-screen bg-gray-50 py-4 pb-16 md:pb-0">
      <div className="container mx-auto px-4">
        <h1 className="text-xl font-bold mb-4 text-gray-900 px-1">Help & Support</h1>
        
        <div className="bg-white rounded-lg shadow-sm p-4 mb-4">
          <h2 className="text-lg font-semibold mb-2">How can we help you?</h2>
          <div className="relative">
            <input
              type="text"
              placeholder="Search for help topics..."
              className="w-full p-3 border border-gray-300 rounded-lg focus:border-[#9c1c80] focus:outline-none"
            />
          </div>
        </div>
        
        <div className="grid grid-cols-2 gap-3">
          {helpTopics.map((topic, index) => (
            <div key={index} className="bg-white rounded-lg shadow-sm p-4 hover:shadow-md transition-shadow">
              <div className="text-2xl mb-2">{topic.icon}</div>
              <h3 className="font-semibold text-sm mb-1">{topic.title}</h3>
              <p className="text-gray-600 text-xs">{topic.description}</p>
            </div>
          ))}
        </div>
        
        <div className="mt-6 bg-white rounded-lg shadow-sm p-4">
          <h2 className="text-lg font-semibold mb-3">Contact Us</h2>
          <div className="space-y-3">
            <div className="flex items-center">
              <span className="text-[#9c1c80] mr-2">📞</span>
              <span className="text-sm">1800-123-4567 (Toll-free)</span>
            </div>
            <div className="flex items-center">
              <span className="text-[#9c1c80] mr-2">✉️</span>
              <span className="text-sm">support@meesho.com</span>
            </div>
            <div className="flex items-center">
              <span className="text-[#9c1c80] mr-2">💬</span>
              <span className="text-sm">Live Chat (9 AM - 9 PM)</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HelpPage;
