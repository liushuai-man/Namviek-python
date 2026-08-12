import { Activity, ActivityObjectType, ActivityType } from '@prisma/client'
import { activityCreate } from '@/services/activity'
import { useTaskStore } from '@/store/task'
import { useActivityContext } from './context'
import { Form } from '@ui-components'
import MemberAvatar from '@/components/MemberAvatar'
import { useUser } from '@auth-client'

export default function ActivityCommentEditor() {
  const { taskId, addActivity } = useActivityContext()
  const { user } = useUser()
  const { tasks } = useTaskStore()
  const task = tasks.find(t => t.id === taskId)

  const { createdBy } = task || {}
  if (!createdBy) return null

  const addNewContent = (content: string) => {
    const newComment = {
      uid: createdBy,
      type: ActivityType.TASK_COMMENT_CREATED,
      objectId: taskId,
      objectType: ActivityObjectType.TASK,
      createdAt: new Date(),
      createdBy: createdBy,
      updatedAt: null,
      updatedBy: null,
      data: {
        content
      }
    } as unknown as Omit<Activity, 'id'>

    activityCreate(taskId, newComment)
      .then(res => {
        const {
          data: { data }
        } = res
        addActivity(data)
      })
      .catch(error => console.error('addNewComment error:', error))
  }

  const onEnter = (value: string, target: HTMLTextAreaElement) => {
    addNewContent(value)
    target.value = ''
  }

  return (
    <div className="flex items-start gap-2 mb-3">
      <MemberAvatar uid={user?.id || ''} noName={true} />
      <div className="w-full">
        <Form.Textarea
          placeholder="Write your comments"
          onEnter={onEnter}
          rows={1}
        />
      </div>
    </div>
  )
}
