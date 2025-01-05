import { useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Loader2, AlertCircle, TrendingUp, Eye, MessageSquare, Share2, Lightbulb } from 'lucide-react';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Badge } from '@/components/ui/badge';
import axios from 'axios';
import { BACKEND_URL } from '@/lib/config';

interface MetricData {
  post_type: string;
  avg_likes: number;
  avg_views: number;
  avg_comments: number;
  avg_shares: number;
}

const SocialAnalyticsDashboard = () => {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<MetricData[]>([]);
  const [insights, setInsights] = useState('');
  const [error, setError] = useState('');

  const fetchData = async () => {
    setLoading(true);
    setError('');
    
    try {
      // Initialize data
      await axios.post(`${BACKEND_URL}/api/initialize`);
      
      // Get analytics
      const response = await axios.get(`${BACKEND_URL}/api/analytics`);
      const { metrics, insights } = response.data;
      
      if (!metrics || metrics.length === 0) {
        throw new Error('No analytics data available');
      }
      
      setData(metrics);
      setInsights(insights);
    } catch (error) {
      console.error('Error fetching data:', error);
      setError('Failed to fetch analytics data. Please try again.');
      setData([]);
      setInsights('');
    } finally {
      setLoading(false);
    }
  };

  const getInsightColor = (index: number) => {
    const colors = ['bg-blue-100', 'bg-green-100', 'bg-yellow-100', 'bg-purple-100', 'bg-pink-100'];
    return colors[index % colors.length];
  };

  const getInsightIcon = (index: number) => {
    const icons = [TrendingUp, Eye, MessageSquare, Share2, Lightbulb];
    const Icon = icons[index % icons.length];
    return <Icon className="h-6 w-6" />;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 p-8">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-5xl font-extrabold text-gray-900 mb-4 tracking-tight">Social Media Analytics Dashboard</h1>
          <p className="text-xl text-gray-600 mb-8">Gain valuable insights into your social media performance</p>
          <Button 
            onClick={fetchData} 
            className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-6 rounded-full shadow-lg transition duration-300 ease-in-out transform hover:scale-105"
            disabled={loading}
          >
            {loading ? (
              <>
                <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                Analyzing Data...
              </>
            ) : (
              <>
                <TrendingUp className="mr-2 h-5 w-5" />
                Analyze Engagement
              </>
            )}
          </Button>
        </div>

        {error && (
          <Alert variant="destructive" className="mb-8 max-w-2xl mx-auto">
            <AlertCircle className="h-5 w-5" />
            <AlertDescription className="ml-2">{error}</AlertDescription>
          </Alert>
        )}

        {data.length > 0 && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <Card className="col-span-full shadow-xl">
              <CardHeader>
                <CardTitle className="text-2xl font-bold">Engagement Metrics Comparison</CardTitle>
              </CardHeader>
              <CardContent className="h-[400px]">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={data}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
                    <XAxis dataKey="post_type" stroke="#718096" />
                    <YAxis stroke="#718096" />
                    <Tooltip contentStyle={{ backgroundColor: '#f7fafc', border: 'none', borderRadius: '8px', boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)' }} />
                    <Legend wrapperStyle={{ paddingTop: '20px' }} />
                    <Bar dataKey="avg_likes" fill="#8884d8" name="Avg. Likes" radius={[4, 4, 0, 0]} />
                    <Bar dataKey="avg_comments" fill="#82ca9d" name="Avg. Comments" radius={[4, 4, 0, 0]} />
                    <Bar dataKey="avg_shares" fill="#ffc658" name="Avg. Shares" radius={[4, 4, 0, 0]} />
                    <Bar dataKey="avg_views" fill="#ff8042" name="Avg. Views" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            {data.map((item) => (
              <Card key={item.post_type} className="shadow-lg hover:shadow-xl transition-shadow duration-300">
                <CardHeader>
                  <CardTitle className="text-xl font-bold capitalize">{item.post_type} Posts</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <span className="text-gray-600 flex items-center"><TrendingUp className="mr-2 h-4 w-4" /> Avg. Likes:</span>
                      <span className="font-semibold text-lg">{item.avg_likes.toFixed(2)}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-gray-600 flex items-center"><Eye className="mr-2 h-4 w-4" /> Avg. Views:</span>
                      <span className="font-semibold text-lg">{item.avg_views.toFixed(2)}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-gray-600 flex items-center"><MessageSquare className="mr-2 h-4 w-4" /> Avg. Comments:</span>
                      <span className="font-semibold text-lg">{item.avg_comments.toFixed(2)}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-gray-600 flex items-center"><Share2 className="mr-2 h-4 w-4" /> Avg. Shares:</span>
                      <span className="font-semibold text-lg">{item.avg_shares.toFixed(2)}</span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}

            <Card className="col-span-full shadow-xl">
              <CardHeader>
                <CardTitle className="text-2xl font-bold">Key Insights</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {insights.split('\n').map((insight, index) => (
                    <div key={index} className={`p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300 ${getInsightColor(index)}`}>
                      <div className="flex items-start space-x-4">
                        <div className="flex-shrink-0">
                          <div className="p-3 bg-white rounded-full shadow-inner">
                            {getInsightIcon(index)}
                          </div>
                        </div>
                        <div className="flex-1">
                          <h3 className="text-lg font-semibold mb-2">Insight {index + 1}</h3>
                          <p className="text-gray-800 leading-relaxed">{insight}</p>
                          <div className="mt-4">
                            <Badge variant="secondary" className="text-xs font-medium">
                              {['Trend', 'Performance', 'Engagement', 'Growth', 'Strategy'][index % 5]}
                            </Badge>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        )}
      </div>
    </div>
  );
};

export default SocialAnalyticsDashboard;

