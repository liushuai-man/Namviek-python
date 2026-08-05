export interface ActivityCommentData {
  content?: string
  edited?: boolean
  interactions?: Array<{
    emoji: string
    updatedBy: string
  }>
}

export interface ActivityAttachData {
  content?: string
  attachedFile?: unknown
}

export interface ActivityLogData {
  content?: string
  changeFrom: string
  changeTo: string
}
