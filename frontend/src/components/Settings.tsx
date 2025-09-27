import { useState } from 'react'
import { useQuery } from 'react-query'
import { getSettings, getOrganizationRules } from '@/lib/api'
import toast from 'react-hot-toast'

export default function Settings() {
  const [activeTab, setActiveTab] = useState('general')
  
  const { data: settings } = useQuery('settings', getSettings)
  const { data: rules } = useQuery('organization-rules', getOrganizationRules)

  const tabs = [
    { id: 'general', name: 'General', icon: '⚙️' },
    { id: 'rules', name: 'Organization Rules', icon: '📋' },
    { id: 'cleanup', name: 'Cleanup', icon: '🧹' },
  ]

  return (
    <div className="space-y-6">
      {/* Tab Navigation */}
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === tab.id
                  ? 'border-primary-500 text-primary-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <span className="mr-2">{tab.icon}</span>
              {tab.name}
            </button>
          ))}
        </nav>
      </div>

      {/* General Settings */}
      {activeTab === 'general' && (
        <div className="card p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-6">
            General Settings
          </h3>
          
          <div className="space-y-6">
            <div>
              <label className="label">Downloads Folder Path</label>
              <input
                type="text"
                value={settings?.downloads_path || ''}
                className="input"
                readOnly
              />
              <p className="text-xs text-gray-500 mt-1">
                Path to your downloads folder
              </p>
            </div>
            
            <div>
              <label className="label">Maximum File Size (MB)</label>
              <input
                type="number"
                value={settings?.max_file_size_mb || 100}
                className="input"
              />
              <p className="text-xs text-gray-500 mt-1">
                Files larger than this will be skipped
              </p>
            </div>
            
            <div>
              <label className="label">Supported File Extensions</label>
              <div className="mt-2 flex flex-wrap gap-2">
                {settings?.supported_extensions?.map((ext: string) => (
                  <span
                    key={ext}
                    className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary-100 text-primary-800"
                  >
                    {ext}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Organization Rules */}
      {activeTab === 'rules' && (
        <div className="space-y-6">
          <div className="flex justify-between items-center">
            <h3 className="text-lg font-semibold text-gray-900">
              Organization Rules
            </h3>
            <button className="btn btn-primary">
              ➕ Add Rule
            </button>
          </div>
          
          <div className="card">
            <div className="px-6 py-4 border-b border-gray-200">
              <h4 className="font-medium text-gray-900">Default Categories</h4>
            </div>
            <div className="divide-y divide-gray-200">
              {settings?.default_categories && Object.entries(settings.default_categories).map(([category, extensions]) => (
                <div key={category} className="px-6 py-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <h5 className="font-medium text-gray-900 capitalize">
                        {category}
                      </h5>
                      <p className="text-sm text-gray-500">
                        {extensions.join(', ')}
                      </p>
                    </div>
                    <div className="flex items-center space-x-2">
                      <span className="text-sm text-gray-500">
                        {extensions.length} extensions
                      </span>
                      <button className="text-sm text-primary-600 hover:text-primary-800">
                        Edit
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Cleanup Settings */}
      {activeTab === 'cleanup' && (
        <div className="card p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-6">
            Cleanup Settings
          </h3>
          
          <div className="space-y-6">
            <div>
              <label className="label">Clean Temporary Files After (Days)</label>
              <input
                type="number"
                value={settings?.cleanup_temp_files_days || 7}
                className="input"
              />
              <p className="text-xs text-gray-500 mt-1">
                Automatically delete temporary files after this many days
              </p>
            </div>
            
            <div>
              <label className="label">Archive Old Files After (Days)</label>
              <input
                type="number"
                value={settings?.cleanup_old_files_days || 30}
                className="input"
              />
              <p className="text-xs text-gray-500 mt-1">
                Move old files to archive folder after this many days
              </p>
            </div>
            
            <div className="pt-4 border-t border-gray-200">
              <button className="btn btn-danger">
                🧹 Run Cleanup Now
              </button>
              <p className="text-xs text-gray-500 mt-2">
                This will clean up files based on your current settings
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
