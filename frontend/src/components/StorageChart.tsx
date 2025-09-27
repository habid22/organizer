interface StorageInfo {
  total_size_bytes: number
  total_size_mb: number
  total_size_gb: number
  file_count: number
}

interface StorageChartProps {
  storage: StorageInfo
}

export default function StorageChart({ storage }: StorageChartProps) {
  const formatBytes = (bytes: number) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  return (
    <div className="card p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">
        Storage Usage
      </h3>
      
      <div className="space-y-4">
        <div className="flex justify-between items-center">
          <span className="text-sm text-gray-600">Total Size</span>
          <span className="text-lg font-semibold text-gray-900">
            {formatBytes(storage.total_size_bytes)}
          </span>
        </div>
        
        <div className="flex justify-between items-center">
          <span className="text-sm text-gray-600">File Count</span>
          <span className="text-lg font-semibold text-gray-900">
            {storage.file_count.toLocaleString()}
          </span>
        </div>
        
        <div className="pt-4 border-t border-gray-200">
          <div className="grid grid-cols-2 gap-4 text-center">
            <div>
              <div className="text-2xl font-bold text-primary-600">
                {storage.total_size_mb.toFixed(1)}
              </div>
              <div className="text-sm text-gray-600">MB</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-primary-600">
                {storage.total_size_gb.toFixed(2)}
              </div>
              <div className="text-sm text-gray-600">GB</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
