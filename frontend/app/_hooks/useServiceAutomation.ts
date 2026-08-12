import {
  automationAdd,
  automationDel,
  automationGet
} from '@/services/automation'
import {
  IAutomateThenProps,
  IAutomateWhenProps,
  IAutomationItem,
  useAutomationStore
} from '@/store/automation'
import { TaskAutomation } from '@prisma/client'
import { messageSuccess, randomId } from '@ui-components'

export const useServiceAutomation = () => {
  const {
    addNewAutomation,
    addAllAutomation,
    updateAutomation,
    deleteAutomation
  } = useAutomationStore()

  const getAutomationByProject = (projectId: string) => {
    automationGet(projectId).then(res => {
      const { data } = res.data
      addAllAutomation(data)
    })
  }

  const delAutomation = (id: string) => {
    deleteAutomation(id)
    automationDel(id).then(res => {
      messageSuccess('Delete automation successfully')
      // deleteAutomation(id)
    })
  }

  const addAutomation = ({
    then,
    when,
    organizationId,
    projectId
  }: {
    then: IAutomateThenProps
    when: IAutomateWhenProps
    organizationId: string
    projectId: string
  }) => {
    const id = 'AUTOMATE_RAND_ID_' + randomId()

    addNewAutomation({
      id,
      then,
      when,
      organizationId,
      projectId
    } as unknown as IAutomationItem)

    automationAdd({
      then: {
        value: then.value || '',
        change: then.change || ''
      },
      when: {
        happens: when.happens || '',
        is: when.is || '',
        valueTo: when.valueTo || null,
        valueFrom: when.valueFrom || null,
        equal: when.equal || null
      },
      organizationId,
      projectId
    } as unknown as Partial<TaskAutomation>)
      .then(res => {
        const { data } = res.data

        updateAutomation(id, data)
      })
      .catch(err => {
        console.error(err)
      })
  }
  return { addAutomation, getAutomationByProject, delAutomation }
}
