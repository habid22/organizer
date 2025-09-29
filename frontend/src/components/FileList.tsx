import { useState } from 'react'
import { useQuery } from 'react-query'
import { getFiles, organizeFiles, scanFiles } from '@/lib/api'
import toast from 'react-hot-toast'

export default function FileList() {
  const [category, setCategory] = useState<string>('')
  const [search, setSearch] = useState('')

  const { data, isLoading, refetch } = useQuery(
    ['files', category],
    () => getFiles({ category: category || undefined })
  )

  const handleOrganizeFiles = async (dryRun = true) => {
    try {
      const result = await organizeFiles(dryRun)
      if (dryRun) {
        toast.success(`Dry run: Would organize ${result.organized_count} files`)
      } else {
        toast.success(`Organized ${result.organized_count} files successfully!`)
        refetch()
      }
    } catch (error) {
      toast.error('Failed to organize files')
    }
  }

  const handleScanFiles = async () => {
    try {
      const result = await scanFiles()
      toast.success(`Found ${result.files_found} files`)
      refetch()
    } catch (error) {
      toast.error('Failed to scan files')
    }
  }

  if (isLoading) {
    return (
      <div className="animate-pulse">
        <div className="card p-6">
          <div className="h-4 bg-gray-200 rounded w-1/4 mb-4"></div>
          <div className="space-y-3">
            {[...Array(5)].map((_, i) => (
              <div key={i} className="h-16 bg-gray-200 rounded"></div>
            ))}
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Controls */}
      <div className="card p-6">
        <div className="flex flex-col sm:flex-row gap-4 items-start sm:items-center justify-between">
          <div className="flex flex-col sm:flex-row gap-4">
            <div>
              <label className="label">Category</label>
              <select
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                className="input"
              >
                <option value="">All Categories</option>
                <option value="images">Images</option>
                <option value="documents">Documents</option>
                <option value="software">Software</option>
                <option value="archives">Archives</option>
              </select>
            </div>
            
            <div>
              <label className="label">Search</label>
              <input
                type="text"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Search files..."
                className="input"
              />
            </div>
          </div>
          
          <div className="flex gap-2">
            <button
              onClick={handleScanFiles}
              className="btn btn-secondary"
            >
              🔍 Scan Files
            </button>
            <button
              onClick={() => handleOrganizeFiles(true)}
              className="btn btn-secondary"
            >
              👁️ Preview Organize
            </button>
            <button
              onClick={() => handleOrganizeFiles(false)}
              className="btn btn-primary"
            >
              🗂️ Organize Files
            </button>
          </div>
        </div>
      </div>

      {/* File List */}
      <div className="card">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900">
            Files ({data?.total || 0})
          </h3>
        </div>
        
        <div className="divide-y divide-gray-200">
          {data?.files?.length === 0 ? (
            <div className="text-center py-12">
              <div className="text-4xl mb-4">📁</div>
              <p className="text-gray-500">No files found</p>
            </div>
          ) : (
            data?.files?.map((file: any) => (
              <div key={file.path} className="px-6 py-4 hover:bg-gray-50">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-4">
                    <div className="text-2xl">
                      {file.category === 'Images' && '🖼️'}
                      {file.category === 'Documents' && '📄'}
                      {file.category === 'Software' && '💿'}
                      {file.category === 'Archives' && '📦'}
                      {file.category === 'Videos' && '🎥'}
                      {file.category === 'Audio' && '🎵'}
                      {file.category === 'Other' && '📁'}
                    </div>
                    <div>
                      <p className="text-sm font-medium text-gray-900">
                        {file.name}
                      </p>
                      <p className="text-xs text-gray-500">
                        {file.path}
                      </p>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-4">
                    <span className="text-xs text-gray-500">
                      {file.category && file.category.charAt(0).toUpperCase() + file.category.slice(1)}
                    </span>
                    <span className="text-xs text-gray-500">
                      {new Date(file.created).toLocaleDateString()}
                    </span>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  )
}
