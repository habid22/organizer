import { format } from 'date-fns'

interface ActivityItem {
  id: number
  original_name: string
  new_name?: string
  category?: string
  created_at: string
  is_organized: boolean
}

interface ActivityFeedProps {
  activity: ActivityItem[]
}

export default function ActivityFeed({ activity }: ActivityFeedProps) {
  return (
    <div className="card p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">
        Recent Activity
      </h3>
      
      {activity.length === 0 ? (
        <div className="text-center py-8 text-gray-500">
          <div className="text-4xl mb-2">📁</div>
          <p>No recent activity</p>
        </div>
      ) : (
        <div className="space-y-4">
          {activity.slice(0, 5).map((item) => (
            <div key={item.id} className="flex items-start space-x-3">
              <div className="flex-shrink-0">
                <div className={`w-2 h-2 rounded-full ${
                  item.is_organized ? 'bg-green-400' : 'bg-yellow-400'
                }`} />
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm text-gray-900 truncate">
                  {item.is_organized && item.new_name ? item.new_name : item.original_name}
                </p>
                <div className="flex items-center space-x-2 text-xs text-gray-500">
                  <span>{format(new Date(item.created_at), 'MMM d, HH:mm')}</span>
                  {item.category && (
                    <>
                      <span>•</span>
                      <span className="capitalize">{item.category}</span>
                    </>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
