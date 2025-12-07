import { Card, Title, Text } from "@tremor/react";
import { Activity, TrendingUp, AlertCircle, BarChart3 } from "lucide-react";

export default function Home() {
  return (
    <div className="min-h-screen bg-slate-950">
      {/* Header */}
      <header className="border-b border-slate-800 bg-slate-900/50 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Activity className="h-8 w-8 text-blue-500" />
              <div>
                <h1 className="text-2xl font-bold text-white">CAEZAM</h1>
                <p className="text-xs text-slate-400">Quantum Ledger Protocol v1.0</p>
              </div>
            </div>
            <div className="flex items-center space-x-2">
              <span className="text-sm text-slate-400">Status:</span>
              <span className="flex items-center space-x-1 text-green-400">
                <div className="h-2 w-2 rounded-full bg-green-400 animate-pulse"></div>
                <span className="text-sm font-medium">LIVE</span>
              </span>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {/* Dashboard Title */}
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-white mb-2">Trading Dashboard</h2>
          <p className="text-slate-400">
            Statistical arbitrage engine for lottery optimization
          </p>
        </div>

        {/* KPI Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card className="bg-slate-900 border-slate-800">
            <div className="flex items-center justify-between">
              <div>
                <Text className="text-slate-400">Bankroll</Text>
                <Title className="text-white mt-1">$10,000</Title>
                <Text className="text-green-400 text-sm mt-1">+12.5%</Text>
              </div>
              <TrendingUp className="h-8 w-8 text-green-400" />
            </div>
          </Card>

          <Card className="bg-slate-900 border-slate-800">
            <div className="flex items-center justify-between">
              <div>
                <Text className="text-slate-400">ROI</Text>
                <Title className="text-white mt-1">8.3%</Title>
                <Text className="text-green-400 text-sm mt-1">+2.1%</Text>
              </div>
              <BarChart3 className="h-8 w-8 text-blue-400" />
            </div>
          </Card>

          <Card className="bg-slate-900 border-slate-800">
            <div className="flex items-center justify-between">
              <div>
                <Text className="text-slate-400">Win Rate</Text>
                <Title className="text-white mt-1">42%</Title>
                <Text className="text-slate-400 text-sm mt-1">Last 30 days</Text>
              </div>
              <Activity className="h-8 w-8 text-purple-400" />
            </div>
          </Card>

          <Card className="bg-slate-900 border-slate-800">
            <div className="flex items-center justify-between">
              <div>
                <Text className="text-slate-400">Max Drawdown</Text>
                <Title className="text-white mt-1">-3.2%</Title>
                <Text className="text-yellow-400 text-sm mt-1">Within limits</Text>
              </div>
              <AlertCircle className="h-8 w-8 text-yellow-400" />
            </div>
          </Card>
        </div>

        {/* War Room Section */}
        <div className="mb-8">
          <h3 className="text-2xl font-bold text-white mb-4">⚡ War Room - Active Signals</h3>
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Signal Card 1 */}
            <Card className="bg-gradient-to-br from-slate-900 to-slate-800 border-slate-700">
              <div className="mb-4">
                <div className="flex items-center justify-between mb-2">
                  <Text className="text-slate-300 font-medium">Powerball</Text>
                  <span className="px-2 py-1 rounded text-xs font-bold bg-green-500/20 text-green-400">
                    RANK #1
                  </span>
                </div>
                <Title className="text-white text-2xl font-mono">
                  07 - 14 - 28 - 45 - 63
                </Title>
              </div>
              <div className="space-y-2 mb-4">
                <div className="flex justify-between">
                  <Text className="text-slate-400">Confidence</Text>
                  <Text className="text-white font-bold">87.3%</Text>
                </div>
                <div className="w-full bg-slate-700 rounded-full h-2">
                  <div className="bg-green-400 h-2 rounded-full" style={{ width: "87.3%" }}></div>
                </div>
                <div className="flex justify-between pt-2">
                  <Text className="text-slate-400">Kelly Fraction</Text>
                  <Text className="text-blue-400 font-mono">2.5%</Text>
                </div>
                <div className="flex justify-between">
                  <Text className="text-slate-400">Suggested Bet</Text>
                  <Text className="text-white font-bold">$250</Text>
                </div>
              </div>
              <button className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded transition">
                View Details
              </button>
            </Card>

            {/* Signal Card 2 */}
            <Card className="bg-gradient-to-br from-slate-900 to-slate-800 border-slate-700">
              <div className="mb-4">
                <div className="flex items-center justify-between mb-2">
                  <Text className="text-slate-300 font-medium">Powerball</Text>
                  <span className="px-2 py-1 rounded text-xs font-bold bg-blue-500/20 text-blue-400">
                    RANK #2
                  </span>
                </div>
                <Title className="text-white text-2xl font-mono">
                  12 - 23 - 34 - 51 - 69
                </Title>
              </div>
              <div className="space-y-2 mb-4">
                <div className="flex justify-between">
                  <Text className="text-slate-400">Confidence</Text>
                  <Text className="text-white font-bold">82.1%</Text>
                </div>
                <div className="w-full bg-slate-700 rounded-full h-2">
                  <div className="bg-blue-400 h-2 rounded-full" style={{ width: "82.1%" }}></div>
                </div>
                <div className="flex justify-between pt-2">
                  <Text className="text-slate-400">Kelly Fraction</Text>
                  <Text className="text-blue-400 font-mono">2.1%</Text>
                </div>
                <div className="flex justify-between">
                  <Text className="text-slate-400">Suggested Bet</Text>
                  <Text className="text-white font-bold">$210</Text>
                </div>
              </div>
              <button className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded transition">
                View Details
              </button>
            </Card>

            {/* Signal Card 3 */}
            <Card className="bg-gradient-to-br from-slate-900 to-slate-800 border-slate-700">
              <div className="mb-4">
                <div className="flex items-center justify-between mb-2">
                  <Text className="text-slate-300 font-medium">Lonabol</Text>
                  <span className="px-2 py-1 rounded text-xs font-bold bg-purple-500/20 text-purple-400">
                    RANK #1
                  </span>
                </div>
                <Title className="text-white text-2xl font-mono">
                  05 - 18 - 29 - 42 - 56
                </Title>
              </div>
              <div className="space-y-2 mb-4">
                <div className="flex justify-between">
                  <Text className="text-slate-400">Confidence</Text>
                  <Text className="text-white font-bold">79.8%</Text>
                </div>
                <div className="w-full bg-slate-700 rounded-full h-2">
                  <div className="bg-purple-400 h-2 rounded-full" style={{ width: "79.8%" }}></div>
                </div>
                <div className="flex justify-between pt-2">
                  <Text className="text-slate-400">Kelly Fraction</Text>
                  <Text className="text-blue-400 font-mono">1.8%</Text>
                </div>
                <div className="flex justify-between">
                  <Text className="text-slate-400">Suggested Bet</Text>
                  <Text className="text-white font-bold">$180</Text>
                </div>
              </div>
              <button className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded transition">
                View Details
              </button>
            </Card>
          </div>
        </div>

        {/* Info Section */}
        <Card className="bg-slate-900/50 border-slate-800">
          <Title className="text-white mb-4">System Information</Title>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
            <div>
              <Text className="text-slate-400 mb-1">Last Update</Text>
              <Text className="text-white font-mono">03:00 AM BOT</Text>
            </div>
            <div>
              <Text className="text-slate-400 mb-1">Next Analysis</Text>
              <Text className="text-white font-mono">Tomorrow 03:00 AM</Text>
            </div>
            <div>
              <Text className="text-slate-400 mb-1">Active Lotteries</Text>
              <Text className="text-white font-mono">2 (Powerball, Lonabol)</Text>
            </div>
          </div>
        </Card>
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-800 mt-12">
        <div className="container mx-auto px-4 py-6">
          <Text className="text-center text-slate-400 text-sm">
            Caezam Protocol v1.0 - &quot;We don&apos;t play, we operate.&quot; 🎯
          </Text>
        </div>
      </footer>
    </div>
  );
}
