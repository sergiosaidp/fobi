import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { Card } from '../components/ui/card';
import { Plus, Edit, Trash2, BarChart3, Copy, ExternalLink } from 'lucide-react';
import { chatbotAPI } from '../services/api';
import { useToast } from '../hooks/use-toast';

const Dashboard = () => {
  const navigate = useNavigate();
  const { toast } = useToast();
  const [chatbots, setChatbots] = useState([]);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({});

  useEffect(() => {
    fetchChatbots();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const fetchChatbots = async () => {
    try {
      const response = await chatbotAPI.getAll();
      if (response.data.success) {
        setChatbots(response.data.chatbots);
        
        // Fetch stats for each chatbot
        const statsPromises = response.data.chatbots.map(bot => 
          chatbotAPI.getStats(bot.chatbot_id)
        );
        const statsResponses = await Promise.all(statsPromises);
        
        const statsMap = {};
        statsResponses.forEach((res, index) => {
          if (res.data.success) {
            statsMap[response.data.chatbots[index].chatbot_id] = res.data.stats;
          }
        });
        setStats(statsMap);
      }
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to load chatbots",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (chatbotId) => {
    if (!window.confirm('Are you sure you want to delete this chatbot?')) {
      return;
    }

    try {
      await chatbotAPI.delete(chatbotId);
      toast({
        title: "Success",
        description: "Chatbot deleted successfully",
      });
      fetchChatbots();
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to delete chatbot",
        variant: "destructive",
      });
    }
  };

  const viewEmbedCode = async (chatbotId) => {
    try {
      const response = await chatbotAPI.getById(chatbotId);
      if (response.data.success) {
        const embedCode = response.data.embed_code.popup;
        navigator.clipboard.writeText(embedCode);
        toast({
          title: "Copied!",
          description: "Embed code copied to clipboard",
        });
      }
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to get embed code",
        variant: "destructive",
      });
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 pt-24 pb-16">
        <div className="container mx-auto px-6">
          <div className="text-center">
            <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-purple-600 border-r-transparent"></div>
            <p className="mt-4 text-gray-600">Loading your chatbots...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 pt-24 pb-16">
      <div className="container mx-auto px-6">
        <div className="max-w-6xl mx-auto">
          {/* Header */}
          <div className="flex items-center justify-between mb-8">
            <div>
              <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-purple-600 via-blue-600 to-indigo-600 bg-clip-text text-transparent">
                My Chatbots
              </h1>
              <p className="text-gray-600">Manage and monitor your chatbots</p>
            </div>
            <Button
              onClick={() => navigate('/create')}
              className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700"
            >
              <Plus className="mr-2 h-4 w-4" />
              Create New
            </Button>
          </div>

          {/* Empty State */}
          {chatbots.length === 0 && (
            <Card className="p-12 text-center">
              <div className="max-w-md mx-auto">
                <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-purple-100 mb-4">
                  <Plus className="h-8 w-8 text-purple-600" />
                </div>
                <h2 className="text-2xl font-bold mb-2">No chatbots yet</h2>
                <p className="text-gray-600 mb-6">
                  Create your first chatbot to get started transforming your Google Forms into engaging conversations.
                </p>
                <Button
                  onClick={() => navigate('/create')}
                  className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700"
                >
                  <Plus className="mr-2 h-4 w-4" />
                  Create Your First Chatbot
                </Button>
              </div>
            </Card>
          )}

          {/* Chatbots Grid */}
          {chatbots.length > 0 && (
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {chatbots.map((chatbot) => {
                const botStats = stats[chatbot.chatbot_id] || {};
                return (
                  <Card key={chatbot.chatbot_id} className="p-6 hover:shadow-lg transition-shadow">
                    {/* Status Badge */}
                    <div className="flex items-start justify-between mb-4">
                      <div className="flex-1">
                        <h3 className="text-xl font-bold mb-1">{chatbot.name}</h3>
                        <p className="text-sm text-gray-500">ID: {chatbot.chatbot_id}</p>
                      </div>
                      <span className={`px-2 py-1 rounded-full text-xs font-semibold ${
                        chatbot.is_active
                          ? 'bg-green-100 text-green-700'
                          : 'bg-gray-100 text-gray-700'
                      }`}>
                        {chatbot.is_active ? 'Active' : 'Inactive'}
                      </span>
                    </div>

                    {/* Stats */}
                    <div className="grid grid-cols-2 gap-4 mb-6">
                      <div className="bg-purple-50 rounded-lg p-3">
                        <p className="text-xs text-gray-600 mb-1">Conversations</p>
                        <p className="text-2xl font-bold text-purple-600">{botStats.total_conversations || 0}</p>
                      </div>
                      <div className="bg-blue-50 rounded-lg p-3">
                        <p className="text-xs text-gray-600 mb-1">Views</p>
                        <p className="text-2xl font-bold text-blue-600">{botStats.total_views || 0}</p>
                      </div>
                    </div>

                    {/* Customization Preview */}
                    <div className="mb-6">
                      <p className="text-xs text-gray-600 mb-2">Colors</p>
                      <div className="flex gap-2">
                        <div
                          className="w-8 h-8 rounded-full border-2 border-gray-200"
                          style={{ backgroundColor: chatbot.customization?.primary_color }}
                        ></div>
                        <div
                          className="w-8 h-8 rounded-full border-2 border-gray-200"
                          style={{ backgroundColor: chatbot.customization?.secondary_color }}
                        ></div>
                      </div>
                    </div>

                    {/* Actions */}
                    <div className="flex gap-2">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => viewEmbedCode(chatbot.chatbot_id)}
                        className="flex-1"
                      >
                        <Copy className="mr-1 h-4 w-4" />
                        Copy Code
                      </Button>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => handleDelete(chatbot.chatbot_id)}
                        className="text-red-600 hover:text-red-700 hover:bg-red-50"
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </Card>
                );
              })}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;