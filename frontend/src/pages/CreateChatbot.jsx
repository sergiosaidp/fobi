import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Card } from '../components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import { ArrowLeft, Palette, MessageSquare, Monitor, Smartphone, Copy, Check } from 'lucide-react';
import { chatbotAPI } from '../services/api';
import { useToast } from '../hooks/use-toast';

const CreateChatbot = () => {
  const navigate = useNavigate();
  const { toast } = useToast();
  const [loading, setLoading] = useState(false);
  const [showResult, setShowResult] = useState(false);
  const [embedCode, setEmbedCode] = useState(null);
  const [copiedPopup, setCopiedPopup] = useState(false);
  const [copiedIframe, setCopiedIframe] = useState(false);

  const [formData, setFormData] = useState({
    name: '',
    google_form_url: '',
    embed_type: 'popup',
    customization: {
      primary_color: '#7c3aed',
      secondary_color: '#2563eb',
      bot_name: 'Assistant',
      welcome_message: 'Hi! How can I help you today?',
      position: 'bottom-right',
      size: 'medium'
    }
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleCustomizationChange = (key, value) => {
    setFormData(prev => ({
      ...prev,
      customization: {
        ...prev.customization,
        [key]: value
      }
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await chatbotAPI.create(formData);
      
      if (response.data.success) {
        setEmbedCode(response.data.embed_code);
        setShowResult(true);
        toast({
          title: "Success!",
          description: "Your chatbot has been created successfully.",
        });
      }
    } catch (error) {
      toast({
        title: "Error",
        description: error.response?.data?.detail || "Failed to create chatbot. Please try again.",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = (text, type) => {
    navigator.clipboard.writeText(text);
    if (type === 'popup') {
      setCopiedPopup(true);
      setTimeout(() => setCopiedPopup(false), 2000);
    } else {
      setCopiedIframe(true);
      setTimeout(() => setCopiedIframe(false), 2000);
    }
    toast({
      title: "Copied!",
      description: "Embed code copied to clipboard.",
    });
  };

  if (showResult && embedCode) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 via-blue-50 to-indigo-50 pt-24 pb-16">
        <div className="container mx-auto px-6">
          <div className="max-w-4xl mx-auto">
            <div className="text-center mb-8">
              <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-gradient-to-br from-purple-600 to-blue-600 mb-4">
                <Check className="h-10 w-10 text-white" />
              </div>
              <h1 className="text-4xl font-bold text-gray-900 mb-4">Chatbot Created Successfully! 🎉</h1>
              <p className="text-lg text-gray-600">Copy the embed code below and paste it into your website.</p>
            </div>

            <Tabs defaultValue="popup" className="w-full">
              <TabsList className="grid w-full grid-cols-2 mb-8">
                <TabsTrigger value="popup" className="flex items-center gap-2">
                  <MessageSquare className="h-4 w-4" />
                  Chat Popup
                </TabsTrigger>
                <TabsTrigger value="iframe" className="flex items-center gap-2">
                  <Monitor className="h-4 w-4" />
                  IFrame Embed
                </TabsTrigger>
              </TabsList>

              <TabsContent value="popup">
                <Card className="p-6">
                  <div className="mb-4">
                    <h3 className="text-lg font-semibold mb-2">Chat Popup Code</h3>
                    <p className="text-sm text-gray-600 mb-4">
                      This will add a floating chat widget to the bottom corner of your website.
                    </p>
                  </div>
                  <div className="relative">
                    <pre className="bg-gray-900 text-gray-100 p-4 rounded-lg overflow-x-auto text-sm">
                      <code>{embedCode.popup}</code>
                    </pre>
                    <Button
                      onClick={() => copyToClipboard(embedCode.popup, 'popup')}
                      className="absolute top-4 right-4"
                      size="sm"
                    >
                      {copiedPopup ? <Check className="h-4 w-4" /> : <Copy className="h-4 w-4" />}
                      {copiedPopup ? 'Copied!' : 'Copy'}
                    </Button>
                  </div>
                </Card>
              </TabsContent>

              <TabsContent value="iframe">
                <Card className="p-6">
                  <div className="mb-4">
                    <h3 className="text-lg font-semibold mb-2">IFrame Embed Code</h3>
                    <p className="text-sm text-gray-600 mb-4">
                      This will embed the chatbot directly into your page as an inline element.
                    </p>
                  </div>
                  <div className="relative">
                    <pre className="bg-gray-900 text-gray-100 p-4 rounded-lg overflow-x-auto text-sm">
                      <code>{embedCode.iframe}</code>
                    </pre>
                    <Button
                      onClick={() => copyToClipboard(embedCode.iframe, 'iframe')}
                      className="absolute top-4 right-4"
                      size="sm"
                    >
                      {copiedIframe ? <Check className="h-4 w-4" /> : <Copy className="h-4 w-4" />}
                      {copiedIframe ? 'Copied!' : 'Copy'}
                    </Button>
                  </div>
                </Card>
              </TabsContent>
            </Tabs>

            <div className="flex gap-4 mt-8 justify-center">
              <Button
                onClick={() => {
                  setShowResult(false);
                  setFormData({
                    name: '',
                    google_form_url: '',
                    embed_type: 'popup',
                    customization: {
                      primary_color: '#7c3aed',
                      secondary_color: '#2563eb',
                      bot_name: 'Assistant',
                      welcome_message: 'Hi! How can I help you today?',
                      position: 'bottom-right',
                      size: 'medium'
                    }
                  });
                }}
                variant="outline"
              >
                Create Another Chatbot
              </Button>
              <Button onClick={() => navigate('/dashboard')}>
                View Dashboard
              </Button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-white pt-24 pb-16">
      <div className="container mx-auto px-6">
        <div className="max-w-4xl mx-auto">
          {/* Header */}
          <div className="mb-8">
            <Button
              variant="ghost"
              onClick={() => navigate('/')}
              className="mb-4"
            >
              <ArrowLeft className="mr-2 h-4 w-4" /> Back to Home
            </Button>
            <h1 className="text-4xl font-bold mb-4 bg-gradient-to-r from-purple-600 via-blue-600 to-indigo-600 bg-clip-text text-transparent">
              Create Your Chatbot
            </h1>
            <p className="text-lg text-gray-600">
              Transform your Google Form into an engaging chatbot in just a few clicks.
            </p>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-8">
            {/* Basic Information */}
            <Card className="p-6">
              <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
                <MessageSquare className="h-6 w-6 text-purple-600" />
                Basic Information
              </h2>
              
              <div className="space-y-4">
                <div>
                  <Label htmlFor="name">Chatbot Name</Label>
                  <Input
                    id="name"
                    name="name"
                    placeholder="e.g., Contact Form Bot"
                    value={formData.name}
                    onChange={handleInputChange}
                    required
                    className="mt-2"
                  />
                </div>

                <div>
                  <Label htmlFor="google_form_url">Google Form URL</Label>
                  <Input
                    id="google_form_url"
                    name="google_form_url"
                    placeholder="https://docs.google.com/forms/d/e/..."
                    value={formData.google_form_url}
                    onChange={handleInputChange}
                    required
                    className="mt-2"
                  />
                  <p className="text-sm text-gray-500 mt-2">
                    Don't have a form? <a href="https://docs.google.com/forms/u/0/" target="_blank" rel="noopener noreferrer" className="text-purple-600 hover:underline">Create one here</a>
                  </p>
                </div>
              </div>
            </Card>

            {/* Customization */}
            <Card className="p-6">
              <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
                <Palette className="h-6 w-6 text-purple-600" />
                Customize Appearance
              </h2>
              
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <Label htmlFor="primary_color">Primary Color</Label>
                  <div className="flex gap-2 mt-2">
                    <Input
                      id="primary_color"
                      type="color"
                      value={formData.customization.primary_color}
                      onChange={(e) => handleCustomizationChange('primary_color', e.target.value)}
                      className="w-20 h-10"
                    />
                    <Input
                      type="text"
                      value={formData.customization.primary_color}
                      onChange={(e) => handleCustomizationChange('primary_color', e.target.value)}
                      className="flex-1"
                    />
                  </div>
                </div>

                <div>
                  <Label htmlFor="secondary_color">Secondary Color</Label>
                  <div className="flex gap-2 mt-2">
                    <Input
                      id="secondary_color"
                      type="color"
                      value={formData.customization.secondary_color}
                      onChange={(e) => handleCustomizationChange('secondary_color', e.target.value)}
                      className="w-20 h-10"
                    />
                    <Input
                      type="text"
                      value={formData.customization.secondary_color}
                      onChange={(e) => handleCustomizationChange('secondary_color', e.target.value)}
                      className="flex-1"
                    />
                  </div>
                </div>

                <div>
                  <Label htmlFor="bot_name">Bot Name</Label>
                  <Input
                    id="bot_name"
                    value={formData.customization.bot_name}
                    onChange={(e) => handleCustomizationChange('bot_name', e.target.value)}
                    className="mt-2"
                  />
                </div>

                <div>
                  <Label htmlFor="position">Position</Label>
                  <select
                    id="position"
                    value={formData.customization.position}
                    onChange={(e) => handleCustomizationChange('position', e.target.value)}
                    className="mt-2 w-full h-10 px-3 rounded-md border border-gray-300"
                  >
                    <option value="bottom-right">Bottom Right</option>
                    <option value="bottom-left">Bottom Left</option>
                  </select>
                </div>

                <div className="md:col-span-2">
                  <Label htmlFor="welcome_message">Welcome Message</Label>
                  <Input
                    id="welcome_message"
                    value={formData.customization.welcome_message}
                    onChange={(e) => handleCustomizationChange('welcome_message', e.target.value)}
                    className="mt-2"
                  />
                </div>
              </div>
            </Card>

            {/* Embed Type */}
            <Card className="p-6">
              <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
                <Monitor className="h-6 w-6 text-purple-600" />
                Embed Type
              </h2>
              
              <div className="grid md:grid-cols-2 gap-4">
                <button
                  type="button"
                  onClick={() => handleInputChange({ target: { name: 'embed_type', value: 'popup' } })}
                  className={`p-6 rounded-lg border-2 transition-all ${
                    formData.embed_type === 'popup'
                      ? 'border-purple-600 bg-purple-50'
                      : 'border-gray-200 hover:border-purple-300'
                  }`}
                >
                  <MessageSquare className={`h-8 w-8 mb-3 ${
                    formData.embed_type === 'popup' ? 'text-purple-600' : 'text-gray-400'
                  }`} />
                  <h3 className="font-semibold mb-2">Chat Popup</h3>
                  <p className="text-sm text-gray-600">Floating widget in corner</p>
                </button>

                <button
                  type="button"
                  onClick={() => handleInputChange({ target: { name: 'embed_type', value: 'iframe' } })}
                  className={`p-6 rounded-lg border-2 transition-all ${
                    formData.embed_type === 'iframe'
                      ? 'border-purple-600 bg-purple-50'
                      : 'border-gray-200 hover:border-purple-300'
                  }`}
                >
                  <Monitor className={`h-8 w-8 mb-3 ${
                    formData.embed_type === 'iframe' ? 'text-purple-600' : 'text-gray-400'
                  }`} />
                  <h3 className="font-semibold mb-2">IFrame Embed</h3>
                  <p className="text-sm text-gray-600">Inline page element</p>
                </button>
              </div>
            </Card>

            {/* Submit Button */}
            <div className="flex justify-center">
              <Button
                type="submit"
                size="lg"
                disabled={loading}
                className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white px-12 py-6 text-lg"
              >
                {loading ? 'Creating...' : 'Create Chatbot'}
              </Button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default CreateChatbot;