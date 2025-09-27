import { useState, useEffect } from 'react'
import Head from 'next/head'
import Layout from '@/components/Layout'
import Dashboard from '@/components/Dashboard'
import FileList from '@/components/FileList'
import Settings from '@/components/Settings'
import { useQuery } from 'react-query'
import { getDashboardStats } from '@/lib/api'

export default function Home() {
  const [activeTab, setActiveTab] = useState('dashboard')
  
  const { data: stats, isLoading } = useQuery(
    'dashboard-stats',
    getDashboardStats,
    {
      refetchInterval: 30000, // Refetch every 30 seconds
    }
  )

  const tabs = [
    { id: 'dashboard', name: 'Dashboard', icon: '📊' },
    { id: 'files', name: 'Files', icon: '📁' },
    { id: 'settings', name: 'Settings', icon: '⚙️' },
  ]

  return (
    <>
      <Head>
        <title>Downloads Organizer</title>
        <meta name="description" content="Intelligent file organization system" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <Layout>
        <div className="min-h-screen bg-gray-50">
          {/* Header */}
          <div className="bg-white shadow-sm border-b border-gray-200">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
              <div className="flex justify-between items-center py-4">
                <div className="flex items-center space-x-4">
                  <h1 className="text-2xl font-bold text-gray-900">
                    📁 Downloads Organizer
                  </h1>
                  {stats && (
                    <div className="text-sm text-gray-500">
                      {stats.total_files} files organized
                    </div>
                  )}
                </div>
                
                <div className="flex items-center space-x-2">
                  <div className="flex bg-gray-100 rounded-lg p-1">
                    {tabs.map((tab) => (
                      <button
                        key={tab.id}
                        onClick={() => setActiveTab(tab.id)}
                        className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                          activeTab === tab.id
                            ? 'bg-white text-primary-600 shadow-sm'
                            : 'text-gray-600 hover:text-gray-900'
                        }`}
                      >
                        <span className="mr-2">{tab.icon}</span>
                        {tab.name}
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Main Content */}
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            {activeTab === 'dashboard' && <Dashboard />}
            {activeTab === 'files' && <FileList />}
            {activeTab === 'settings' && <Settings />}
          </div>
        </div>
      </Layout>
    </>
  )
}
