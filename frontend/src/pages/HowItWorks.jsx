import React from 'react';
import { CheckCircle, Copy, Code, Palette } from 'lucide-react';
import { Card } from '../components/ui/card';

const HowItWorks = () => {
  return (
    <div className="min-h-screen bg-white pt-24 pb-16">
      <div className="container mx-auto px-6">
        {/* Header */}
        <div className="text-center mb-16">
          <h1 className="text-5xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-purple-600 via-blue-600 to-indigo-600 bg-clip-text text-transparent">
            How It Works?
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Transform your Google Forms into engaging chatbots in just 3 simple steps. No coding required, no registration needed.
          </p>
        </div>

        {/* Steps */}
        <div className="max-w-4xl mx-auto space-y-16">
          {/* Step 1 */}
          <div className="relative">
            <div className="flex flex-col md:flex-row items-start gap-8">
              <div className="flex-shrink-0">
                <div className="w-20 h-20 rounded-full bg-gradient-to-br from-purple-600 to-blue-600 flex items-center justify-center text-white text-3xl font-bold shadow-lg">
                  1
                </div>
              </div>
              <div className="flex-1">
                <div className="bg-gradient-to-br from-purple-50 to-blue-50 rounded-2xl p-8 shadow-lg">
                  <div className="flex items-center gap-3 mb-4">
                    <Copy className="h-8 w-8 text-purple-600" />
                    <h2 className="text-3xl font-bold text-gray-900">Create Your Chatbot</h2>
                  </div>
                  <p className="text-gray-700 text-lg leading-relaxed mb-4">
                    Copy and paste your Google Form link into the input field. Fobi will automatically convert your form questions into conversational chatbot messages.
                  </p>
                  <ul className="space-y-2">
                    <li className="flex items-start gap-2 text-gray-700">
                      <CheckCircle className="h-5 w-5 text-green-600 mt-1 flex-shrink-0" />
                      <span>Paste your Google Form URL</span>
                    </li>
                    <li className="flex items-start gap-2 text-gray-700">
                      <CheckCircle className="h-5 w-5 text-green-600 mt-1 flex-shrink-0" />
                      <span>Edit form questions to suit conversational style</span>
                    </li>
                    <li className="flex items-start gap-2 text-gray-700">
                      <CheckCircle className="h-5 w-5 text-green-600 mt-1 flex-shrink-0" />
                      <span>Preview your chatbot in real-time</span>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>

          {/* Step 2 */}
          <div className="relative">
            <div className="flex flex-col md:flex-row items-start gap-8">
              <div className="flex-shrink-0">
                <div className="w-20 h-20 rounded-full bg-gradient-to-br from-blue-600 to-indigo-600 flex items-center justify-center text-white text-3xl font-bold shadow-lg">
                  2
                </div>
              </div>
              <div className="flex-1">
                <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-2xl p-8 shadow-lg">
                  <div className="flex items-center gap-3 mb-4">
                    <Code className="h-8 w-8 text-blue-600" />
                    <h2 className="text-3xl font-bold text-gray-900">Embed in Your Website</h2>
                  </div>
                  <p className="text-gray-700 text-lg leading-relaxed mb-4">
                    Choose your preferred embedding method. Fobi provides two flexible options to integrate your chatbot seamlessly.
                  </p>
                  <div className="grid md:grid-cols-2 gap-4">
                    <div className="bg-white rounded-lg p-4 border border-blue-200">
                      <h3 className="font-semibold text-gray-900 mb-2">Chat PopUp</h3>
                      <p className="text-sm text-gray-600">Appears as a floating chat widget in the corner of your website</p>
                    </div>
                    <div className="bg-white rounded-lg p-4 border border-blue-200">
                      <h3 className="font-semibold text-gray-900 mb-2">IFrame Embed</h3>
                      <p className="text-sm text-gray-600">Embed directly into your page as an inline element</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Step 3 */}
          <div className="relative">
            <div className="flex flex-col md:flex-row items-start gap-8">
              <div className="flex-shrink-0">
                <div className="w-20 h-20 rounded-full bg-gradient-to-br from-indigo-600 to-purple-600 flex items-center justify-center text-white text-3xl font-bold shadow-lg">
                  3
                </div>
              </div>
              <div className="flex-1">
                <div className="bg-gradient-to-br from-indigo-50 to-purple-50 rounded-2xl p-8 shadow-lg">
                  <div className="flex items-center gap-3 mb-4">
                    <Palette className="h-8 w-8 text-indigo-600" />
                    <h2 className="text-3xl font-bold text-gray-900">Customize & Launch</h2>
                  </div>
                  <p className="text-gray-700 text-lg leading-relaxed mb-4">
                    Make it yours! Adjust colors, size, and text to match your brand. Once you're happy with the design, your chatbot is ready to go live!
                  </p>
                  <ul className="space-y-2">
                    <li className="flex items-start gap-2 text-gray-700">
                      <CheckCircle className="h-5 w-5 text-green-600 mt-1 flex-shrink-0" />
                      <span>Choose your brand colors</span>
                    </li>
                    <li className="flex items-start gap-2 text-gray-700">
                      <CheckCircle className="h-5 w-5 text-green-600 mt-1 flex-shrink-0" />
                      <span>Adjust size and positioning</span>
                    </li>
                    <li className="flex items-start gap-2 text-gray-700">
                      <CheckCircle className="h-5 w-5 text-green-600 mt-1 flex-shrink-0" />
                      <span>Customize greeting and messages</span>
                    </li>
                    <li className="flex items-start gap-2 text-gray-700">
                      <CheckCircle className="h-5 w-5 text-green-600 mt-1 flex-shrink-0" />
                      <span>Launch and start collecting responses!</span>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Bottom CTA */}
        <div className="mt-20 text-center">
          <div className="bg-gradient-to-br from-purple-50 via-blue-50 to-indigo-50 rounded-2xl p-12 shadow-xl">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Ready to Get Started?</h2>
            <p className="text-gray-700 mb-8 max-w-2xl mx-auto">
              It's completely free and takes less than 5 minutes to set up your first chatbot!
            </p>
            <button className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white px-8 py-4 rounded-full font-semibold text-lg shadow-lg hover:shadow-xl transition-all transform hover:scale-105">
              Create Your Chatbot Now
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HowItWorks;