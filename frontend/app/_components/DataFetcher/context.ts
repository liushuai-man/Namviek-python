import { Dispatch, SetStateAction, createContext } from 'react'
import { ExtendedTask } from '@/store/task'

export interface DataFetcherContextType {
  data: ExtendedTask[]
  cursor: string
  totalRecords: number
  restRecords: number
  isLoading: boolean
  hasNextPage: boolean
  deleteRow: (ids: string | string[]) => void
  setData: Dispatch<SetStateAction<ExtendedTask[]>>
  fetchNextPage: () => void
  updateCustomFields: (taskIds: string[], customFields: Record<string, any>) => void
}

export const DataFetcherContext = createContext<DataFetcherContextType>({
  cursor: '',
  data: [],
  totalRecords: 0,
  restRecords: 0,
  isLoading: false,
  hasNextPage: false,
  deleteRow: () => {},
  setData: () => {},
  fetchNextPage: () => {},
  updateCustomFields: () => {}
})
