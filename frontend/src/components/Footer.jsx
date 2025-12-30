import React from 'react';
import { Link } from 'react-router-dom';

const Footer = () => {
  return (
    <footer className="bg-gray-900 text-white py-16">
      <div className="container mx-auto px-6">
        <div className="grid md:grid-cols-3 gap-12 mb-12">
          {/* Logo and Tagline */}
          <div>
            <Link to="/" className="inline-block mb-4">
              <div className="text-3xl font-bold tracking-wider bg-gradient-to-r from-purple-400 via-blue-400 to-indigo-400 bg-clip-text text-transparent">
                FOBI.IO
              </div>
            </Link>
            <p className="text-gray-400 text-sm leading-relaxed">
              Cause no one likes filling out forms on the internet
            </p>
          </div>

          {/* Links */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Link</h3>
            <ul className="space-y-3">
              <li>
                <Link to="/" className="text-gray-400 hover:text-white transition-colors">
                  Home
                </Link>
              </li>
              <li>
                <Link to="/how-it-works" className="text-gray-400 hover:text-white transition-colors">
                  How it works?
                </Link>
              </li>
              <li>
                <Link to="/faqs" className="text-gray-400 hover:text-white transition-colors">
                  FAQs
                </Link>
              </li>
              <li>
                <a href="#" className="text-gray-400 hover:text-white transition-colors">
                  Privacy Policy
                </a>
              </li>
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Contact us</h3>
            <p className="text-gray-400 mb-4">
              Email: <a href="mailto:info@fobi.io" className="text-blue-400 hover:text-blue-300 transition-colors">info@fobi.io</a>
            </p>
            <div className="flex space-x-4">
              <a 
                href="https://chatbotsmagazine.com/meet-the-new-conversational-google-forms-28b12a138a72" 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-gray-400 hover:text-white transition-colors"
              >
                Medium
              </a>
              <a 
                href="https://it.wordpress.org/plugins/fobi-chatbot/" 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-gray-400 hover:text-white transition-colors"
              >
                WordPress
              </a>
            </div>
          </div>
        </div>

        <div className="border-t border-gray-800 pt-8 text-center">
          <p className="text-gray-400 text-sm">
            © {new Date().getFullYear()} Fobi.io - Transform Google Forms into Chatbots
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;