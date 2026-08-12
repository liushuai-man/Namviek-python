'use client'

import { useEffect, useState } from 'react'
import {
  EVisionViewMode,
  VisionByDays,
  VisionField,
  VisionProvider
} from './context'
import { visionGetByProject } from '@/services/vision'
import { useParams } from 'next/navigation'
import VisionContainer from './VisionContainer'
import './style.css'
import { Vision } from '@prisma/client'
import { useTaskStore } from '@/store/task'
// import { useProjectStatusStore } from '@/store/status'
import { useStatusFuncs } from '@/hooks/useStatusUtils'

const useVisionByDates = (visions: VisionField[]) => {
  const visionByDays: VisionByDays = {}

  visions.forEach(vision => {
    const d = vision.dueDate
    if (!d) return
    const dateObj = new Date(d)
    const key = `${dateObj.getDate()}-${dateObj.getMonth()}`
    if (!visionByDays[key]) {
      visionByDays[key] = []
    }

    visionByDays[key].push(vision)
  })

  return visionByDays
}

const useVisionProgress = ({ visions }: { visions: VisionField[] }) => {
  const { tasks } = useTaskStore()
  // const { statusDoneId } = useProjectStatusStore()
  const { isDoneStatus } = useStatusFuncs()
  //
  const visionProgress: {
    [key: string]: { total: number; done: number; assigneeIds: string[] }
  } = {}

  let taskTotal = 0
  let taskDone = 0

  visions.forEach(v => {
    visionProgress[v.id] = { total: 0, done: 0, assigneeIds: [] }
  })

  tasks.forEach(task => {
    const { visionId, done, taskStatusId, assigneeIds } = task
    const visionIdStr = visionId as string
    if (!visionIdStr || !visionProgress[visionIdStr]) return

    taskTotal += 1
    visionProgress[visionIdStr].total += 1

    if (assigneeIds.length) {
      assigneeIds.forEach(assigneeId => {
        visionProgress[visionIdStr].assigneeIds.push(assigneeId)
      })
    }

    // if (taskStatusId === statusDoneId) {
    if (isDoneStatus(taskStatusId || '')) {
      visionProgress[visionIdStr].done += 1
      taskDone += 1
    }
  })

  return {
    taskDone,
    taskTotal,
    visionProgress
  }
}

export default function ProjectVision() {
  const [mode, setMode] = useState(EVisionViewMode.CALENDAR)
  const { projectId } = useParams()
  const [loading, setLoading] = useState(true)
  const [selected, setSelected] = useState('')
  const [visions, setVisions] = useState<VisionField[]>([])
  const [filter, setFilter] = useState({
    month: new Date().getMonth() + 1
  })

  const { visionProgress, taskDone, taskTotal } = useVisionProgress({ visions })
  const visionByDays = useVisionByDates(visions)

  const clearLoading = () => {
    setTimeout(() => {
      setLoading(false)
    }, 400)
  }

  useEffect(() => {
    const controller = new AbortController()
    setLoading(true)
    visionGetByProject(projectId, filter, controller.signal)
      .then(res => {
        clearLoading()
        const { data } = res.data
        const visionData = data as Vision[]

        setVisions(
          visionData.map(v => {
            const {
              id,
              name,
              projectId,
              organizationId,
              dueDate,
              startDate,
              progress
            } = v as any
            return {
              id,
              projectId,
              name,
              organizationId,
              progress,
              startDate: startDate ? new Date(startDate) : null,
              dueDate: dueDate ? new Date(dueDate) : null
            } as unknown as VisionField
          })
        )
      })
      .catch(err => {
        clearLoading()
        console.error(err)
      })

    return () => {
      controller.abort()
    }
  }, [projectId, JSON.stringify(filter)])

  return (
    <VisionProvider
      value={{
        mode,
        setMode,
        taskDone,
        taskTotal,
        filter,
        setFilter,
        visions,
        loading,
        visionByDays,
        visionProgress,
        setLoading,
        setVisions,
        selected,
        setSelected
      }}>
      <VisionContainer visible={mode === EVisionViewMode.CALENDAR} />
    </VisionProvider>
  )
}
