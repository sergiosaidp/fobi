import React, { useEffect, useState } from 'react';
import { ArrowRight, CheckCircle, Users, TrendingUp, Zap } from 'lucide-react';
import { Button } from '../components/ui/button';
import { Card } from '../components/ui/card';

const Home = () => {
  return (
    <div className="min-h-screen bg-white">
      {/* Hero Section */}
      <section className="relative bg-gradient-to-br from-purple-50 via-blue-50 to-indigo-50 pt-32 pb-20 overflow-hidden">
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-20 left-10 w-72 h-72 bg-purple-400 rounded-full mix-blend-multiply filter blur-xl animate-pulse"></div>
          <div className="absolute bottom-20 right-10 w-72 h-72 bg-blue-400 rounded-full mix-blend-multiply filter blur-xl animate-pulse" style={{ animationDelay: '1s' }}></div>
        </div>
        
        <div className="container mx-auto px-6 relative z-10">
          <div className="max-w-4xl mx-auto text-center">
            <h1 className="text-6xl md:text-7xl font-bold mb-6 bg-gradient-to-r from-purple-600 via-blue-600 to-indigo-600 bg-clip-text text-transparent leading-tight">
              Create Awesome Chatbots using Google Forms
            </h1>
            <p className="text-xl md:text-2xl text-gray-700 mb-8 font-light">
              <span className="font-semibold text-purple-600">Expand</span> your pipeline, 
              <span className="font-semibold text-blue-600"> improve</span> customer experience and 
              <span className="font-semibold text-indigo-600"> grow</span> your business.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-12">
              <a 
                href="https://docs.google.com/forms/u/0/" 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-purple-600 hover:text-purple-700 font-medium underline transition-colors"
              >
                Don't have a Google Form?
              </a>
              <Button 
                size="lg" 
                className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white px-8 py-6 text-lg rounded-full shadow-lg hover:shadow-xl transition-all transform hover:scale-105"
              >
                Get Started <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
            </div>
            
            <div className="mt-16">
              <img 
                src="https://images.unsplash.com/photo-1762330470070-249e7c23c8c0?w=800&q=80" 
                alt="Chatbot Interface" 
                className="rounded-2xl shadow-2xl mx-auto max-w-2xl w-full transform hover:scale-105 transition-transform duration-300"
              />
            </div>
          </div>
        </div>
      </section>

      {/* Yes, it's free! Section */}
      <section className="py-20 bg-white">
        <div className="container mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="text-5xl font-bold text-gray-900 mb-4">Yes, it's free!</h2>
            <p className="text-xl text-gray-600">But why else do I need a chatbot for?</p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-12 max-w-6xl mx-auto">
            {/* Card 1 */}
            <div className="text-center group">
              <div className="relative mb-6 overflow-hidden rounded-2xl">
                <img 
                  src="https://images.unsplash.com/photo-1626863905121-3b0c0ed7b94c?w=400&q=80" 
                  alt="Make customers happy" 
                  className="w-full h-64 object-cover transform group-hover:scale-110 transition-transform duration-500"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-purple-900/50 to-transparent"></div>
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-3">Make customers happy</h3>
              <p className="text-gray-600 leading-relaxed">
                Fobi helps you communicate with your customers better. Welcome new visitors, reduce response time and offer help.
              </p>
            </div>
            
            {/* Card 2 */}
            <div className="text-center group">
              <div className="relative mb-6 overflow-hidden rounded-2xl">
                <img 
                  src="https://images.unsplash.com/photo-1730382624709-81e52dd294d4?w=400&q=80" 
                  alt="Generate more leads" 
                  className="w-full h-64 object-cover transform group-hover:scale-110 transition-transform duration-500"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-blue-900/50 to-transparent"></div>
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-3">Generate more leads</h3>
              <p className="text-gray-600 leading-relaxed">
                Fobi supports your marketing and sales by generating new leads, gathering information about your users, and improving your reach.
              </p>
            </div>
            
            {/* Card 3 */}
            <div className="text-center group">
              <div className="relative mb-6 overflow-hidden rounded-2xl">
                <img 
                  src="https://images.unsplash.com/photo-1648539356777-6a6d9ba6bcd0?w=400&q=80" 
                  alt="Quick and Easy" 
                  className="w-full h-64 object-cover transform group-hover:scale-110 transition-transform duration-500"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-indigo-900/50 to-transparent"></div>
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-3">Quick and Easy</h3>
              <p className="text-gray-600 leading-relaxed">
                Fobi is not only free, but it is also super easy to setup. It requires no pre registration, only 3 simple steps and you're done.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Statistics Section */}
      <section className="py-20 bg-gradient-to-br from-purple-600 via-blue-600 to-indigo-600 relative overflow-hidden">
        <div className="absolute inset-0 opacity-10" style={{ backgroundImage: `url('https://images.unsplash.com/photo-1723631537826-c40cd320d72f?w=1200&q=80')`, backgroundSize: 'cover', backgroundPosition: 'center' }}></div>
        
        <div className="container mx-auto px-6 relative z-10">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-4">Join</h2>
            <p className="text-xl text-white/90">
              Over 50,000 websites around the world are using Fobi to scale their business!
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-12 max-w-5xl mx-auto">
            <div className="text-center">
              <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20 hover:bg-white/20 transition-all transform hover:scale-105">
                <div className="text-6xl font-bold text-white mb-2">50K+</div>
                <div className="text-white/90 text-lg">Websites using Fobi</div>
              </div>
            </div>
            
            <div className="text-center">
              <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20 hover:bg-white/20 transition-all transform hover:scale-105">
                <div className="text-6xl font-bold text-white mb-2">90%</div>
                <div className="text-white/90 text-lg">Increase in customer engagement rate</div>
              </div>
            </div>
            
            <div className="text-center">
              <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20 hover:bg-white/20 transition-all transform hover:scale-105">
                <div className="text-6xl font-bold text-white mb-2">5M+</div>
                <div className="text-white/90 text-lg">Conversations created using Fobi</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* How it works - 3 Steps */}
      <section className="py-20 bg-gray-50">
        <div className="container mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="text-5xl font-bold text-gray-900 mb-4">Only 3 easy steps</h2>
          </div>
          
          <div className="max-w-6xl mx-auto space-y-20">
            {/* Step 1 */}
            <div className="flex flex-col md:flex-row items-center gap-12">
              <div className="md:w-1/2 order-2 md:order-1">
                <div className="bg-gradient-to-br from-purple-100 to-blue-100 rounded-2xl p-8 shadow-xl">
                  <img 
                    src="https://images.unsplash.com/photo-1648539356777-6a6d9ba6bcd0?w=600&q=80" 
                    alt="Create step" 
                    className="rounded-xl w-full"
                  />
                </div>
              </div>
              <div className="md:w-1/2 order-1 md:order-2">
                <div className="flex items-center gap-4 mb-4">
                  <div className="w-16 h-16 rounded-full bg-gradient-to-br from-purple-600 to-blue-600 flex items-center justify-center text-white text-2xl font-bold shadow-lg">1</div>
                  <h3 className="text-3xl font-bold text-gray-900">Create</h3>
                </div>
                <p className="text-lg text-gray-700 leading-relaxed">
                  Copy and paste your Google form link in the upper section. Then edit your form to suit the conversational character of a chatbot.
                </p>
              </div>
            </div>
            
            {/* Step 2 */}
            <div className="flex flex-col md:flex-row items-center gap-12">
              <div className="md:w-1/2">
                <div className="flex items-center gap-4 mb-4">
                  <div className="w-16 h-16 rounded-full bg-gradient-to-br from-blue-600 to-indigo-600 flex items-center justify-center text-white text-2xl font-bold shadow-lg">2</div>
                  <h3 className="text-3xl font-bold text-gray-900">Embed</h3>
                </div>
                <p className="text-lg text-gray-700 leading-relaxed">
                  Choose how you want to embed the chatbot in your website. There are two ways: A Chat PopUp and an IFrame.
                </p>
              </div>
              <div className="md:w-1/2">
                <div className="bg-gradient-to-br from-blue-100 to-indigo-100 rounded-2xl p-8 shadow-xl">
                  <img 
                    src="https://images.unsplash.com/photo-1762330470070-249e7c23c8c0?w=600&q=80" 
                    alt="Embed step" 
                    className="rounded-xl w-full"
                  />
                </div>
              </div>
            </div>
            
            {/* Step 3 */}
            <div className="flex flex-col md:flex-row items-center gap-12">
              <div className="md:w-1/2 order-2 md:order-1">
                <div className="bg-gradient-to-br from-indigo-100 to-purple-100 rounded-2xl p-8 shadow-xl">
                  <img 
                    src="https://images.unsplash.com/photo-1626863905121-3b0c0ed7b94c?w=600&q=80" 
                    alt="Customize step" 
                    className="rounded-xl w-full"
                  />
                </div>
              </div>
              <div className="md:w-1/2 order-1 md:order-2">
                <div className="flex items-center gap-4 mb-4">
                  <div className="w-16 h-16 rounded-full bg-gradient-to-br from-indigo-600 to-purple-600 flex items-center justify-center text-white text-2xl font-bold shadow-lg">3</div>
                  <h3 className="text-3xl font-bold text-gray-900">Customize</h3>
                </div>
                <p className="text-lg text-gray-700 leading-relaxed">
                  Design the bot to your taste. Adjust the colors, size and texts, and... that's it! Your bot is ready to use!
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Final CTA */}
      <section className="py-20 bg-gradient-to-br from-purple-50 via-blue-50 to-indigo-50">
        <div className="container mx-auto px-6 text-center">
          <h2 className="text-5xl font-bold text-gray-900 mb-8">Start Using Fobi and Scale Your Business</h2>
          <Button 
            size="lg" 
            className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white px-12 py-6 text-xl rounded-full shadow-lg hover:shadow-xl transition-all transform hover:scale-105"
          >
            Get Started Now <ArrowRight className="ml-2 h-6 w-6" />
          </Button>
        </div>
      </section>
    </div>
  );
};

export default Home;