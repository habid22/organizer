import { useQuery } from 'react-query'
import { getDashboardStats, getRecentActivity, getStorageInfo } from '@/lib/api'
import StatsCard from '@/components/StatsCard'
import ActivityFeed from '@/components/ActivityFeed'
import StorageChart from '@/components/StorageChart'

export default function Dashboard() {
  const { data: stats, isLoading: statsLoading } = useQuery(
    'dashboard-stats',
    getDashboardStats
  )
  
  const { data: activity, isLoading: activityLoading } = useQuery(
    'recent-activity',
    getRecentActivity
  )
  
  const { data: storage, isLoading: storageLoading } = useQuery(
    'storage-info',
    getStorageInfo
  )

  if (statsLoading || activityLoading || storageLoading) {
    return (
      <div className="animate-pulse">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {[...Array(4)].map((_, i) => (
            <div key={i} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
              <div className="h-8 bg-gray-200 rounded w-1/2"></div>
            </div>
          ))}
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-8">
      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatsCard
          title="Total Files"
          value={stats?.total_files || 0}
          icon="📁"
          color="blue"
        />
        <StatsCard
          title="Storage Used"
          value={`${stats?.total_size_mb || 0} MB`}
          icon="💾"
          color="green"
        />
        <StatsCard
          title="Recent Files"
          value={stats?.recent_files || 0}
          icon="🆕"
          color="purple"
        />
        <StatsCard
          title="Duplicates"
          value={stats?.duplicate_count || 0}
          icon="🔄"
          color="red"
        />
      </div>

      {/* Category Breakdown */}
      {stats?.category_stats && stats.category_stats.length > 0 && (
        <div className="card p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Files by Category
          </h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {stats.category_stats.map((category: any) => (
              <div key={category.category} className="text-center">
                <div className="text-2xl font-bold text-primary-600">
                  {category.count}
                </div>
                <div className="text-sm text-gray-600 capitalize">
                  {category.category}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Storage Information */}
      {storage && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <StorageChart storage={storage} />
          <ActivityFeed activity={activity?.recent_activity || []} />
        </div>
      )}
    </div>
  )
}
