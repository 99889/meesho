import React from 'react';
import { Link } from 'react-router-dom';
import { Facebook, Instagram, Twitter, Youtube, Mail, Phone } from 'lucide-react';

const Footer = () => {
  return (
    <footer className="bg-gray-900 text-gray-300 mt-16">
      <div className="container mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {/* About */}
          <div>
            <h3 className="text-white text-lg font-semibold mb-4">Shop Non-Stop on Meesho</h3>
            <p className="text-sm mb-4">
              Trusted by more than 1 Crore Indians. Cash on Delivery | Free Delivery
            </p>
            <div className="flex gap-4 mt-4">
              <a href="#" className="hover:text-pink-500 transition-colors">
                <Facebook className="w-5 h-5" />
              </a>
              <a href="#" className="hover:text-pink-500 transition-colors">
                <Instagram className="w-5 h-5" />
              </a>
              <a href="#" className="hover:text-pink-500 transition-colors">
                <Twitter className="w-5 h-5" />
              </a>
              <a href="#" className="hover:text-pink-500 transition-colors">
                <Youtube className="w-5 h-5" />
              </a>
            </div>
          </div>

          {/* Careers */}
          <div>
            <h3 className="text-white text-lg font-semibold mb-4">Careers</h3>
            <ul className="space-y-2 text-sm">
              <li>
                <Link to="#" className="hover:text-pink-500 transition-colors">
                  Become a Supplier
                </Link>
              </li>
              <li>
                <Link to="#" className="hover:text-pink-500 transition-colors">
                  Hall of Fame
                </Link>
              </li>
              <li>
                <Link to="#" className="hover:text-pink-500 transition-colors">
                  Sitemap
                </Link>
              </li>
            </ul>
          </div>

          {/* Help */}
          <div>
            <h3 className="text-white text-lg font-semibold mb-4">Help</h3>
            <ul className="space-y-2 text-sm">
              <li>
                <Link to="#" className="hover:text-pink-500 transition-colors">
                  FAQ
                </Link>
              </li>
              <li>
                <Link to="#" className="hover:text-pink-500 transition-colors">
                  Shipping
                </Link>
              </li>
              <li>
                <Link to="#" className="hover:text-pink-500 transition-colors">
                  Returns
                </Link>
              </li>
              <li>
                <Link to="#" className="hover:text-pink-500 transition-colors">
                  Track Order
                </Link>
              </li>
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h3 className="text-white text-lg font-semibold mb-4">Contact Us</h3>
            <ul className="space-y-3 text-sm">
              <li className="flex items-center gap-2">
                <Mail className="w-4 h-4" />
                <span>support@meesho.com</span>
              </li>
              <li className="flex items-center gap-2">
                <Phone className="w-4 h-4" />
                <span>1800-890-6999</span>
              </li>
            </ul>
            <div className="mt-4">
              <p className="text-xs">Download the Meesho App</p>
              <div className="flex gap-2 mt-2">
                <div className="h-10 w-28 bg-gray-800 rounded flex items-center justify-center text-xs">
                  Google Play
                </div>
                <div className="h-10 w-28 bg-gray-800 rounded flex items-center justify-center text-xs">
                  App Store
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Bottom */}
        <div className="border-t border-gray-800 mt-8 pt-8">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4 text-sm">
            <p>&copy; 2025 Meesho. All rights reserved.</p>
            <div className="flex gap-6">
              <Link to="#" className="hover:text-pink-500 transition-colors">
                Privacy Policy
              </Link>
              <Link to="#" className="hover:text-pink-500 transition-colors">
                Terms of Service
              </Link>
              <Link to="#" className="hover:text-pink-500 transition-colors">
                Refund Policy
              </Link>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
